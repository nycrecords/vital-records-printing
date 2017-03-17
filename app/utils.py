import subprocess


def pdf_to_png():
    subprocess.call(['convert app/static/pdf/bitcoin.pdf app/static/img/bitcoin.png'], shell=True)