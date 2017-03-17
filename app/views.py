from app import app
from app.forms import SearchForm
from app.models import Cert
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from app.utils import pdf_to_png

@app.route('/', methods=['GET', 'POST'])
def main():
    """
    Stuff
    """
    pdf_to_png(input_file_path="app/static/pdf/bitcoin.pdf", output_file_path="app/png/")
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Return login page
    """
    return render_template('login.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Return search page
    """
    form = SearchForm()
    if request.method == "POST":
        # form = SearchForm(request.form)
        # if form.validate()
        if form.validate_on_submit():
            return redirect(url_for("main"))
    return render_template('search.html', form=form)


# will be used later
# @app.route('/edit/<int:cert_id>', methods=['GET'])
# def edit(cert_id):
#     """
#     Return edit page
#     """
#     cert = Cert.query.filter_by(id=cert_id).one()
#
#     return render_template('edit.html', file_path=cert.filename)

@app.route('/edit', methods=['GET'])
def edit():
    """
    Return edit page
    """
    return render_template('edit.html')
