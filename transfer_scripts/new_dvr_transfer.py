import os
from dotenv.main import load_dotenv
from datetime import datetime

not_pdf_file = open('not_pdf.txt', 'w')
bad_format_file = open('bad_format.txt', 'w')
stats_file = open('stats.txt', 'w')

start_time = datetime.utcnow()
stats_file.write("Program started at " + str(start_time) + '\n')

files_counter = 0
files_copied_counter = 0
not_pdf_counter = 0
bad_format_counter = 0

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)

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
                new_dvr_path = os.environ.get('NEW_DVR_TARGET_DIR') + new_path
                print('New: ' + new_dvr_path)
                copy_command = 'cp ' + original_dvr_path + ' ' + new_dvr_path
                print(copy_command + '\n')

                try:
                    os.system(copy_command)
                except Exception:
                    print('Something went wrong!')

                new_path = os.environ.get('NEW_DVR_BASE_DIR') + os.sep
        else:
            # write the paths of all non pdf files to a file for later processing
            print("NOT A PDF DETECTED")
            print(filepath + '\n')
            not_pdf_file.write(filepath)
            not_pdf_file.close()
            not_pdf_file = open('not_pdf.txt', 'w')
            not_pdf_counter += 1
end_time = datetime.utcnow()
stats_file.write('Program ended at ' + str(end_time) + '\n')
elapsed_time = end_time - start_time
stats_file.write('Program took ' + str(elapsed_time) + " to run\n")
stats_file.write('Files in directory: ' + files_counter + '\n')
stats_file.write('Files copied: '+ files_copied_counter + '\n')
stats_file.write('Bad format: ' + bad_format_counter + '\n')
stats_file.write('Not PDF:' + not_pdf_counter + '\n')

not_pdf_file.close()
bad_format_file.close()
stats_file.close()
