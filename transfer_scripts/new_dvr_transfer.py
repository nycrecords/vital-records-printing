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

execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'w')
non_pdf_log = open(os.environ.get('NON_PDF_LOG_FILE_PATH'), 'w')
bad_format_log = open(os.environ.get('BAD_FORMAT_LOG_FILE_PATH'), 'w')
stats_log = open(os.environ.get('STATS_LOG_FILE_PATH'), 'w')
copy_failed_log = open(os.environ.get('COPY_FAILED_LOG_FILE_PATH'), 'w')

start_time = datetime.utcnow()
stats_log.write('Program started at ' + str(start_time) + '\n')
stats_log.close()
stats_log = open(os.environ.get('STATS_LOG_FILE_PATH'), 'a')
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
    if not os.path.exists(new_dvr_structure_path):
        os.system('sudo mkdir ' + new_dvr_structure_path)
    else:
        execution_log.write('Directory: ' + new_dvr_structure_path + " already exists" + '\n')
        execution_log.close()
        execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')

    for county in counties:
        new_dvr_structure_path = os.path.join(new_dvr_structure_path, county)
        if not os.path.exists(new_dvr_structure_path):
            os.system('sudo mkdir' + new_dvr_structure_path)
        else:
            execution_log.write('Directory: ' + new_dvr_structure_path + " already exists" + '\n')
            execution_log.close()
            execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')
        remove_county = os.path.split(new_dvr_structure_path)
        new_dvr_structure_path = remove_county[0]
    new_dvr_structure_path = os.environ.get('NEW_DVR_BASE_DIR')
execution_log.write('New Default DVR structure created' + '\n\n')
execution_log.close()
execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')

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
                execution_log.write('BAD FILENAME DETECTED' + '\n' + filepath + '\n\n')
                execution_log.close()
                execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')
                bad_format_log.write(filepath + '\n')
                bad_format_log.close()
                bad_format_log = open(os.environ.get('BAD_FORMAT_LOG_FILE_PATH'), 'a')
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

                # make the directory for year if it doesn't already exist
                if not os.path.exists(new_path):
                    os.system('sudo mkdir ' + new_path)

                original_dvr_path = filepath.replace(' ', '\ ')
                # execution_log.write('Original: ' + original_dvr_path + '\n')
                # execution_log.write('New: ' + new_path + '\n')
                copy_command = 'sudo cp ' + original_dvr_path + ' ' + new_path
                new_completed_path = new_path + filename
                execution_log.write(copy_command + '\n\n')
                execution_log.close()
                execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')
                print('Original: ' + original_dvr_path)
                print('New: ' + new_path)
                print(copy_command)
                print(new_completed_path)
                print(datetime.utcnow())
                print()

                if not os.path.exists(new_completed_path):
                    os.system(copy_command)
                    if not os.path.exists(new_completed_path):
                        print('COPY FAILED' + '\n')
                        copy_failed_log.write(original_dvr_path + '\n')
                        copy_failed_log.close()
                        copy_failed_log = open(os.environ.get('COPY_FAILED_LOG_FILE_PATH'), 'a')
                        execution_log.write('COPY FAILED' + '\n')
                    else:
                        files_copied_counter += 1
                else:
                    execution_log.write('FILE ALREADY ON SERVER' + '\n\n')
                    print('FILE ALREADY ON SERVER' + '\n')

                execution_log.close()
                execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')

                new_path = os.environ.get('NEW_DVR_BASE_DIR') + os.sep
        else:
            # write the paths of all non pdf files to a file for later processing
            execution_log.write("NON PDF DETECTED" + '\n' + filepath + '\n\n')
            execution_log.close()
            execution_log = open(os.environ.get('EXECUTION_LOG_FILE_PATH'), 'a')
            non_pdf_log.write(filepath + '\n')
            non_pdf_log.close()
            non_pdf_log = open(os.environ.get('NON_PDF_LOG_FILE_PATH'), 'a')
            non_pdf_counter += 1
end_time = datetime.utcnow()
stats_log.write('Program ended at ' + str(end_time) + '\n')
elapsed_time = end_time - start_time
stats_log.write('Program took ' + str(elapsed_time) + " to run\n")
stats_log.write('Files in directory: ' + str(files_counter) + '\n')
stats_log.write('Files copied: ' + str(files_copied_counter) + '\n')
stats_log.write('Bad format: ' + str(bad_format_counter) + '\n')
stats_log.write('Non PDF:' + str(non_pdf_counter) + '\n')

execution_log.close()
non_pdf_log.close()
bad_format_log.close()
stats_log.close()
