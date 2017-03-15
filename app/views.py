from app import app
from app.forms import SearchForm
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)


@app.route('/', methods=['GET', 'POST'])
def main():
    """
    Stuff
    """
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


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """
    Return edit page
    """

    return render_template('edit.html')
