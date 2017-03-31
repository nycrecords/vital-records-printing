"""
Migrate data from vital records access database tables (that have been
previously converted) to Vital Records Printing, and store file data.

Usage:
    PYTHONPATH=/.../vital_records_printing python transfer_scripts/access_to_db.py
    
"""
import os
import math
import subprocess
import psycopg2.extras
from time import time
from functools import wraps
from multiprocessing import Pool
from app.constants import counties, months, certificate_types

DVR_MOUNT_POINT = "/mnt/smb"  # CHANGE THIS TO MATCH YOUR ENVIRONMENT!
NUM_DVR_DIRS = 15

CHUNKSIZE = 500  # Bump it up if you got the RAM

SHOW_PROGRESSBAR = True
try:
    import progressbar

    MOCK_PROGRESSBAR = False
except ImportError:
    MOCK_PROGRESSBAR = True

CONN = psycopg2.connect(
    database="vital_records_printing",
    user="vital_records_printing_db",
    host="10.0.0.2",
    port="5432")
CUR_ = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
CUR = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)


class MockProgressBar(object):
    """
    Mock progressbar.ProgressBar
    (Used if progressbar2 is not installed.)
    """

    def __init__(self, max_value):
        self.max_value = max_value

    def update(self, num):
        print('{:.0f}% ({} of {})'.format(
            (num / self.max_value) * 100, num, self.max_value))
        print("\x1b[1A\x1b[2K", end='')

    def finish(self):
        print('100% ({0} of {0})'.format(self.max_value))


def transfer(tablename):
    def decorator(transfer_func):
        """
        Run args.transfer_func for every row fetched by args.query,
        committing every 500 rows.
        """

        @wraps(transfer_func)
        def wrapped(*args):
            CUR_.execute("SELECT * from {}".format(tablename))
            bar = progressbar.ProgressBar if not MOCK_PROGRESSBAR else MockProgressBar
            bar = bar(max_value=CUR_.rowcount)
            print("{} -> {}".format(tablename, "certificate"))
            max_init = bar.max_value
            for chunk in range(math.ceil(CUR_.rowcount / CHUNKSIZE)):
                for i, row in enumerate(CUR_.fetchmany(CHUNKSIZE)):
                    max_value_shift = transfer_func(*args, row)
                    if max_value_shift:
                        bar.max_value += max_value_shift
                    if SHOW_PROGRESSBAR:
                        bar.update(i + 1 + (chunk * CHUNKSIZE) - (max_init - bar.max_value))
                CONN.commit()
            if SHOW_PROGRESSBAR:
                bar.finish()

        return wrapped

    return decorator


@transfer("NYC_Births_1901_190")
def transfer_births(birth):
    _transfer_record(birth, certificate_types.BIRTH)


@transfer("Grooms_1866_1900")
def transfer_grooms(groom):
    _transfer_record(groom, certificate_types.MARRIAGE)


@transfer("Brides_1866_1900")
def transfer_brides(bride):
    _transfer_record(bride, certificate_types.MARRIAGE)


@transfer("_1868_1890_Deaths_Ma")
def transfer_deaths(death):
    _transfer_record(death, certificate_types.DEATH, has_age=True)

@transfer("Jrs")
def transfer_deaths_jrs(death):
    _transfer_record(death, certificate_types.DEATH, has_age=True)


def _transfer_record(record, certificate_type, has_age=False):
    if record.surname is not None and record.county is not None:
        number, month, county, year = _normalize_data(
            record.certnbr, record.month, record.county, record.year
        )
        _add_certificate(
            certificate_type,
            county,
            month,
            record.day,
            year,
            number,
            record.givenname,
            record.surname,
            record.soundex,
            record.age if has_age else None
        )


def _normalize_data(certificate_number, month, county, year):
    # certificate number
    if certificate_number is not None:
        certificate_number = certificate_number.replace(' ', '')
    # month
    if month is not None:
        month = month.lower().replace(' ', '')
        if month not in months.ALL:
            month = months.TO_VALID.get(month)
    # county
    county = county.lower().replace(' ', '')
    if county not in counties.ALL:
        if county == "brinx":
            county = counties.BRONX
        else:
            # prompt to fix invalid county
            print(" Invalid county value: '{}'".format(county))
            for i, county in enumerate(counties.ALL):
                print("{}. {}".format(i, county))
            counties_list = list(counties.ALL)  # to preserve order
            while True:
                try:
                    choice = int(input("Choose appropriate county: "))
                    if choice >= 0 and choice <= len(counties_list):
                        county = counties_list[choice]
                        print(county)
                        break
                except Exception:
                    pass
                print("Invalid option.")
    # year
    if year is not None:
        year = int(year)
    return certificate_number, month, county, year


def _add_certificate(type_,
                     county,
                     month,
                     day,
                     year,
                     number,
                     first_name,
                     last_name,
                     soundex,
                     age):
    query = ("INSERT INTO certificate ("
             "type, "
             "county, "
             "month, "
             "day, "
             "year, "
             "number, "
             "first_name, "
             "last_name, "
             "age, "
             "soundex)"
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    CUR.execute(
        query,
        (
            type_,
            county,
            month,
            day,
            year,
            number,
            first_name,
            last_name,
            age,
            soundex
        )
    )


def create_files(error_log_file=None):
    """
    Walks through the certificate files directory, searches for a corresponding 
    certificate record, creates a File record, and links it to the certificate record.
    
    Assumes `certificate` has already been populated and 'DVR' has been mounted.
    To mount: `sudo mount -t cifs -o username=<USERNAME>,password=<PASSWORD> //10.132.41.31/DVR /mnt/smb`
    
    """
    def write_to_log(msg, path):
        if error_log_file is not None:
            error_log_file.write("{path}{n}{msg}{n}{n}".format(path=path, msg=msg, n=os.linesep))

    counter = 0
    for root, dirs, files in os.walk(DVR_MOUNT_POINT):
        # certificate files are assumed to be in "Delivery*" directories
        if "Delivery" in root:
            for file_ in files:
                path = os.path.join(root, file_)
                name, ext = os.path.splitext(file_)
                # certificate files are assumed to be PDFs
                if ext == ".pdf":
                    parts = name.split('-')
                    try:
                        # parse file name
                        type_ = certificate_types.FROM_FILE_IDENTIFIER[parts[0]]
                        county = counties.FROM_FILE_IDENTIFIER[parts[1]]
                        year = int(parts[2])
                        number = parts[3].lstrip('0')
                        fields = (type_, county, year, number)
                    except Exception:
                        msg = "Could not parse file name: '{}'".format(name)
                        write_to_log(msg, path)
                        print(msg)
                    else:
                        try:
                            # SELECT certificate record, INSERT file record, UPDATE certificate record

                            CUR.execute(
                                "SELECT * FROM certificate "
                                "WHERE type = %s "
                                "AND county = %s "
                                "AND year = %s "
                                "AND number = %s",
                                fields
                            )
                            certificate = CUR.fetchone()

                            # certificate not found, boo
                            if certificate is None:
                                msg = "No certificate found for '{}' {}".format(name, fields)
                                write_to_log(msg, path)
                                print(msg)
                            # CERTIFICATE FOUND! YAY!
                            else:
                                print(certificate)

                                # create file record
                                CUR.execute(
                                    "INSERT INTO file (name, path, converted) VALUES (%s, %s, %s)",
                                    (name, path, False)
                                )

                                # link to certificate record
                                CUR.execute("SELECT LASTVAL()")
                                file_id = CUR.fetchone().lastval
                                CUR.execute(
                                    "UPDATE certificate "
                                    "SET file_id = %s "
                                    "WHERE type = %s "
                                    "AND county = %s "
                                    "AND year = %s "
                                    "AND number = %s",
                                    tuple([file_id] + list(fields))
                                )

                                # increment counter
                                counter += 1
                                if counter == CHUNKSIZE:
                                    # commit and reset counter
                                    CONN.commit()
                                    counter = 0

                        except Exception as e:
                            msg = "Failure while accessing database: {}".format(e)
                            write_to_log(msg, path)
                            print(msg)
                            CONN.rollback()

        CONN.commit()


def create_sql_to_create_files():
    # TODO: create index before running this
    with open("add_files.sql", "w") as sql:
        for root, dirs, files in os.walk(DVR_MOUNT_POINT):
            # certificate files are assumed to be in "Delivery*" directories
            if "Delivery" in root:
                for file_ in files:
                    path = os.path.join(root, file_)
                    name, ext = os.path.splitext(file_)
                    # certificate files are assumed to be PDFs
                    if ext == ".pdf":
                        parts = name.split('-')
                        try:
                            # parse file name
                            type_ = certificate_types.FROM_FILE_IDENTIFIER[parts[0]]
                            county = counties.FROM_FILE_IDENTIFIER[parts[1]]
                            year = int(parts[2])
                            number = parts[3].lstrip('0')
                        except Exception:
                            msg = "Could not parse file name: '{}'".format(name)
                            print(msg)
                        else:
                            if len(number) <= 10:
                                sql.write(
                                    "INSERT INTO file (name, path, converted) "
                                    "VALUES ('{name}', '{path}', false);{newline}"
                                    "UPDATE certificate SET file_id = CAST((SELECT LASTVAL()) as int) "
                                    "WHERE type = '{type}' "
                                    "AND county = '{county}' "
                                    "AND year = {year} "
                                    "AND number = '{number}';{newline}"
                                        .format(name=name,
                                                path=path,
                                                type=type_,
                                                county=county,
                                                year=year,
                                                number=number,
                                                newline=os.linesep))
                            else:
                                print("Skipping: {}".format(name))


def transfer_all():
    transfer_births()
    transfer_brides()
    transfer_grooms()
    transfer_deaths()
    transfer_deaths_jrs()


def search_for_file(dvr_num, type, county, year, number):
    start = time()
    regex = ".*/{t}\-{c}\-{y}\-0*{n}\.pdf".format(t=type, c=county, y=year, n=number)
    options = [
        os.path.join(DVR_MOUNT_POINT, "DVR_{}".format(dvr_num)),  # /mnt/smb/DVR_1
        "-name", "*RECYCLE.BIN*", "-prune", "-o",  # ignore files in RECYCLE.BIN
        "-regex", "{}".format(regex),  # -regex '.*/...'
        "-print"
    ]
    cmd = ["find"] + options
    print(' '.join(cmd))
    subprocess.call(cmd)
    print("{}: {} seconds".format(dvr_num, time() - start))


if __name__ == "__main__":
    create_sql_to_create_files()

    # search_for_file(1, 'D', 'K', 1911, 65)
    # start = time()
    # with Pool(processes=NUM_DVR_DIRS) as pool:
    #     pool.starmap(search_for_file, [(i, 'D', 'K', 1911, 65) for i in range(1, NUM_DVR_DIRS + 1)])
    # print("Total: {} seconds".format(time() - start))

    # with open("create_files_error_log.txt", "w") as flog:
    #     create_files(flog)
