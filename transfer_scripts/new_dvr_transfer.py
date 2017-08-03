import os
from dotenv.main import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)

not_pdf_file = open('not_pdf.txt', 'w')
bad_format_file = open('bad_format.txt', 'w')

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
print('New Default DVR structure created')


new_path = os.environ.get('NEW_DVR_BASE_DIR')

for subdir, dirs, files in os.walk('/mnt/dvr/'):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".pdf"):
            split_filepath = filepath.split('/')
            filename = split_filepath[-1]

            split_filename = filename.split('-')
            if len(split_filename) != 4:
                print('BAD FILENAME DETECTED')
                print(filepath + '\n')
                bad_format_file.write(filepath + '\n')
                bad_format_file.close()
                bad_format_file = open('bad_format.txt', 'w')
            else:
                cert_type = split_filename[0]
                county = split_filename[1]
                year = split_filename[2]
                cert_num = split_filename[3]

                # add os.path.join
                if cert_type is 'B':
                    new_path += 'Births/'
                if cert_type is 'D':
                    new_path += 'Deaths/'
                if cert_type is 'M':
                    new_path += 'Marriages/'

                if county is 'K':
                    new_path += 'Kings/'
                if county is 'Q':
                    new_path += 'Queens/'
                if county is 'B':
                    new_path += 'Bronx/'
                if county is 'X':
                    new_path += 'Bronx/'
                if county is 'M':
                    new_path += 'Manhattan/'
                if county is 'R':
                    new_path += 'Richmond/'
                if county is 'S':
                    new_path += 'Richmond/'

                new_path += year + "/"

                try:
                    os.makedirs(new_path)
                    print(new_path + " created")
                except FileExistsError:
                    # print("Directory: " + new_path + " already exists")
                    pass

                original_dvr_path = filepath.replace(' ', '\ ')
                print('Original: ' + original_dvr_path)
                new_dvr_path = '/vagrant/transfer_scripts/' + new_path
                print('New: ' + new_dvr_path)
                copy_command = 'cp ' + original_dvr_path + ' ' + new_dvr_path
                print(copy_command + '\n')

                # try:
                #     os.system(copy_command)
                # except Exception:
                #     print('Something went wrong!')

                new_path = 'DVR/'
        else:
            print("NOT A PDF DETECTED")
            print(filepath + '\n')
            not_pdf_file.write(filepath)
            not_pdf_file.close()
            not_pdf_file = open('not_pdf.txt', 'w')

not_pdf_file.close()
bad_format_file.close()
