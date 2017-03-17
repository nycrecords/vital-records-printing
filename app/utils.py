from flask import current_app
import subprocess
import os


def pdf_to_png(input_file_path):
    """
    Util function used to convert a pdf file to png and create its own folder for them
    :param input_file_path: the path of where the pdf is stored
    """
    new_file_name = os.path.basename(input_file_path)
    new_file_name = os.path.splitext(new_file_name)[0]
    new_directory_path = os.path.join(current_app.config['OUTPUT_FILE_PATH'], new_file_name)
    try:
        os.mkdir(new_directory_path)
    except:
        print("{} already exists".format(new_directory_path))
    subprocess.call([
        "convert",
        input_file_path,
        os.path.join(new_directory_path, ''.join((new_file_name, ".png")))
    ])