"""
This script will walk through DVR_V2 and update the 'path' field in the file table with the new path to the file.
"""

import os
import psycopg2.extras
from datetime import datetime
from dotenv.main import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)

execution_log = open(os.environ.get('UPDATE_FILE_EXECUTION_LOG'), 'w')
error_log = open(os.environ.get('UPDATE_FILE_ERROR_LOG'), 'w')

CONN = psycopg2.connect(
    database="vital_records_printing",
    user="vital_records_printing_db",
    host="127.0.0.1",
    port="5432")
CUR = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

for subdir, dirs, files in os.walk('/mnt/dvr_v2'):
    for file in files:
        filepath = subdir + os.sep + file
        split_filepath = filepath.split('/')
        filename = split_filepath[-1]
        filename = filename.replace('.pdf', '')
        sql = "UPDATE file SET path='{}' WHERE name='{}';".format(filepath, filename)
        print(datetime.utcnow())
        try:
            CUR.execute(sql)
            CUR.execute('COMMIT;')
        except Exception:
            execution_log.write('Something went wrong when trying to execute:\n')
            print('Something went wrong when trying to execute:')
            error_log.write(sql + '\n')
            error_log.close()
            error_log = open(os.environ.get('UPDATE_FILE_ERROR_LOG'), 'a')
        execution_log.write(sql + '\n\n')
        execution_log.close()
        execution_log = open(os.environ.get('UPDATE_FILE_EXECUTION_LOG'), 'a')
        print(sql + '\n')



