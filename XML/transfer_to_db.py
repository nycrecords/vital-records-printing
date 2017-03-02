import xml.etree.ElementTree as ET
import psycopg2.extras

CONN = psycopg2.connect(database="vital_records_printing",
                           user="vital_records_printing_db",
                           host="10.0.0.2",
                           port="5432")
CUR = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

# Parse 'Brides 1866-1900.xml'
# counter = 0
# for bride in ET.iterparse('Brides 1866-1900.xml'):
#     for ID in bride[1].findall('ID'):
#         id = ID.text
#     for Surname in bride[1].findall('Surname'):
#         print(Surname.text)
#     for GivenName in bride[1].findall('GivenName'):
#         print(GivenName.text)
#     for Month in bride[1].findall('Month'):
#         print(Month.text)
#     for Day in bride[1].findall('Day'):
#         print(Day.text)
#     for Year in bride[1].findall('Year'):
#         print(Year.text)
#     for CertNbr in bride[1].findall('CertNbr'):
#         print(CertNbr.text)
#     for County in bride[1].findall('County'):
#         print(County.text)
#     for Soundex in bride[1].findall('Soundex'):
#         print(Soundex.text)


# Parse 'Grooms 1866-1900.xml'
counter = 0
for groom in ET.iterparse('Grooms 1866-1900.xml'):

    for ID in groom[1].findall('ID'):
        id = ID.text
        counter += 1
        # print(counter)
        # print(id)
    for Surname in groom[1].findall('Surname'):
        surname = Surname.text.strip()
        counter += 1
    for GivenName in groom[1].findall('GivenName'):
        givenname = GivenName.text.strip()
        counter += 1
    for Month in groom[1].findall('Month'):
        month = Month.text.strip()
        counter += 1
    for Day in groom[1].findall('Day'):
        day = Day.text.strip()
        counter += 1
    for Year in groom[1].findall('Year'):
        year = Year.text.strip()
        counter += 1
    for CertNbr in groom[1].findall('CertNbr'):
        certnbr = CertNbr.text.strip()
        counter += 1
    for County in groom[1].findall('County'):
        county = County.text.strip()
        counter += 1
    for Soundex in groom[1].findall('Soundex'):
        soundex = Soundex.text.strip()
        counter += 1

    if counter > 8:
        print(id, surname, givenname, month, day, year, certnbr, county, soundex)
        counter = 0

        query = ("INSERT INTO certificate ("
                 "type, "
                 "last_name, "
                 "first_name, "
                 # "Month, "
                 # "Day, "
                 "year, "
                 "number, "
                 "county, "
                  "soundex) "
                 "VALUES ('Marriage', %s, %s, %s, %s, %s, %s)")

        CUR.execute(query, (
            surname,
            givenname,
            # month,
            # day,
            year,
            certnbr,
            county,
            soundex
        ))

        CONN.commit()


# Parse 'NYC Births 1901-1907.xml'
# for birth in ET.iterparse('NYC Births 1901-1907.xml'):
#     for ID in birth[1].findall('ID'):
#         print(ID.text)
#     for Surname in birth[1].findall('Surname'):
#         print(Surname.text)
#     for GivenName in birth[1].findall('GivenName'):
#         print(GivenName.text)
#     for Month in birth[1].findall('Month'):
#         print(Month.text)
#     for Day in birth[1].findall('Day'):
#         print(Day.text)
#     for Year in birth[1].findall('Year'):
#         print(Year.text)
#     for CertNbr in birth[1].findall('CertNbr'):
#         print(CertNbr.text)
#     for County in birth[1].findall('County'):
#         print(County.text)
#     for Soundex in birth[1].findall('Soundex'):
#         print(Soundex.text)

# Parse '1868-1890 Deaths Manhattan.xml'
# for death in ET.iterparse('1868-1890 Deaths Manhattan.xml'):
#     for Age in death[1].findall('Age'):
#         print(Age.text)
#     for Surname in death[1].findall('Surname'):
#         print(Surname.text)
#     for GivenName in death[1].findall('GivenName'):
#         print(GivenName.text)
#     for Month in death[1].findall('Month'):
#         print(Month.text)
#     for Day in death[1].findall('Day'):
#         print(Day.text)
#     for Year in death[1].findall('Year'):
#         print(Year.text)
#     for CertNbr in death[1].findall('CertNbr'):
#         print(CertNbr.text)
#     for County in death[1].findall('County'):
#         print(County.text)
#     for Soundex in death[1].findall('Soundex'):
#         print(Soundex.text)
