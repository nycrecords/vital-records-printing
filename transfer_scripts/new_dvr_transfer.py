"""
This script will create a new DVR directory in your desired path with the format DVR_V2 > TYPE > COUNTY > YEAR > FILE.
The script will then walk through the current DVR and copy each file in to its respective directory.
All files that are not PDF or are not in the proper name format will be written to log files for later processing.
"""

import os
from dotenv.main import load_dotenv
from datetime import datetime

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)

non_pdf_log = open(os.environ.get('NON_PDF_LOG_FILE_PATH'), 'w')
bad_format_log = open(os.environ.get('BAD_FORMAT_LOG_FILE_PATH'), 'w')
stats_log = open(os.environ.get('STATS_LOG_FILE_PATH'), 'w')

start_time = datetime.utcnow()
stats_log.write("Program started at " + str(start_time) + '\n')
files_counter = 0
files_copied_counter = 0
non_pdf_counter = 0
bad_format_counter = 0

cert_types = ['Births', 'Deaths', 'Marriages']
counties = ['Kings', 'Queens', 'Bronx', 'Manhattan', 'Richmond']

# create the new default DVR structure
new_dvr_structure_path = os.environ.get('NEW_DVR_BASE_DIR')
for cert_type in cert_types:
    new_dvr_structure_path = os.path.join(new_dvr_structure_path, cert_type)
    for county in counties:
        new_dvr_structure_path = os.path.join(new_dvr_structure_path, county)
        try:
            os.makedirs(new_dvr_structure_path)
        except FileExistsError:
            print('Directory: ' + new_dvr_structure_path + " already exists")
        remove_county = os.path.split(new_dvr_structure_path)
        new_dvr_structure_path = remove_county[0]
    new_dvr_structure_path = os.environ.get('NEW_DVR_BASE_DIR')
print('New Default DVR structure created' + '\n')

new_path = os.environ.get('NEW_DVR_BASE_DIR') + os.sep

for subdir, dirs, files in os.walk(os.environ.get('CUR_DVR_BASE_DIR')):
    for file in files:
        files_counter += 1
        filepath = subdir + os.sep + file

        if filepath.endswith(".pdf"):
            split_filepath = filepath.split('/')
            filename = split_filepath[-1]

            split_filename = filename.split('-')
            # to ensure all files have the format 'TYPE-COUNTY-YEAR-NUMBER.pdf'
            # if it is not in the proper format, write it to a file for later processing
            if len(split_filename) != 4:
                print('BAD FILENAME DETECTED')
                print(filepath + '\n')
                bad_format_file.write(filepath + '\n')
                bad_format_file.close()
                bad_format_file = open('bad_format.txt', 'w')
                bad_format_counter += 1
            else:
                cert_type = split_filename[0]
                county = split_filename[1]
                year = split_filename[2]
                cert_num = split_filename[3]

                if cert_type is 'B':
                    new_path = os.path.join(new_path, 'Births') + os.sep
                if cert_type is 'D':
                    new_path = os.path.join(new_path, 'Deaths') + os.sep
                if cert_type is 'M':
                    new_path = os.path.join(new_path, 'Marriages') + os.sep

                if county is 'K':
                    new_path = os.path.join(new_path, 'Kings') + os.sep
                if county is 'Q':
                    new_path = os.path.join(new_path, 'Queens') + os.sep
                if county is 'B':
                    new_path = os.path.join(new_path, 'Bronx') + os.sep
                if county is 'X':
                    new_path = os.path.join(new_path, 'Bronx') + os.sep
                if county is 'M':
                    new_path = os.path.join(new_path, 'Manhattan') + os.sep
                if county is 'R':
                    new_path = os.path.join(new_path, 'Richmond') + os.sep
                if county is 'S':
                    new_path = os.path.join(new_path, 'Richmond') + os.sep

                new_path = os.path.join(new_path, year) + os.sep

                try:
                    os.makedirs(new_path)
                    print('Directory: ' + new_path + " created \n")
                except FileExistsError:
                    # print("Directory: " + new_path + " already exists")
                    pass

                original_dvr_path = filepath.replace(' ', '\ ')
                print('Original: ' + original_dvr_path)
                print('New: ' + new_path)
                copy_command = 'cp ' + original_dvr_path + ' ' + new_path
                print(copy_command + '\n')

                try:
                    os.system(copy_command)
                    files_copied_counter += 1
                except Exception:
                    print('Something went wrong!')

                new_path = os.environ.get('NEW_DVR_BASE_DIR') + os.sep
        else:
            # write the paths of all non pdf files to a file for later processing
            print("NON PDF DETECTED")
            print(filepath + '\n')
            non_pdf_log.write(filepath)
            non_pdf_log.close()
            non_pdf_log = open('not_pdf.txt', 'w')
            non_pdf_counter += 1
end_time = datetime.utcnow()
stats_log.write('Program ended at ' + str(end_time) + '\n')
elapsed_time = end_time - start_time
stats_log.write('Program took ' + str(elapsed_time) + " to run\n")
stats_log.write('Files in directory: ' + str(files_counter) + '\n')
stats_log.write('Files copied: ' + str(files_copied_counter) + '\n')
stats_log.write('Bad format: ' + str(bad_format_counter) + '\n')
stats_log.write('Non PDF:' + str(non_pdf_counter) + '\n')

non_pdf_log.close()
bad_format_log.close()
stats_log.close()
