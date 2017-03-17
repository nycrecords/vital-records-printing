import subprocess
import os


def pdf_to_png(input_file_path, output_file_path):
    """
    Util function used to convert a pdf file to png and create its own folder for them
    :param input_file_path:
    :param output_file_path:
    """
    new_file_name = os.path.basename(input_file_path)
    new_file_name = os.path.splitext(new_file_name)[0]
    new_directory_path = output_file_path + new_file_name
    subprocess.call(['mkdir {}'.format(new_directory_path)], shell=True)
    subprocess.call(['convert {} {}/{}.png'.format(input_file_path, new_directory_path, new_file_name)], shell=True)