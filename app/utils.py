import os
import subprocess
from flask import current_app


def certificate_pdf_to_png(pdf_path):
    """
    Saves a PNG version of the supplied certificate PDF in to the PNG directory.
    
    Example:
        
        Given "certificate_name.pdf" with 3 pages, creates 3 PNG files and stores them like so:
        
        pngs_directory/
            certificate_name/
                0.png
                1.png
                2.png
                
    """
    pdf_path_extensionless, _ = os.path.splitext(pdf_path)
    png_path = os.path.join(
        current_app.config['PNGS_DIRECTORY'],
        os.path.basename(pdf_path_extensionless)
    )
    if not os.path.exists(png_path):
        os.mkdir(png_path)
    subprocess.call([
        "convert",
        pdf_path,
        # TODO: set appropriate DPI (?)
        os.path.join(png_path, ''.join(("%d", os.extsep, "png")))
    ])