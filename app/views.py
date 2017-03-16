from app import app
from app.forms import SearchForm
from app.models import Cert
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
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
        if form.validate_on_submit():
            filters = {}
            for name, value in {
                "type": form.type.data,
                "county": form.county.data,
                "year": form.year.data,
                "number": form.number.data,
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "soundex": form.soundex.data
            }.items():
                if value:
                    filters[name] = value

            # TODO: .order_by(Cert.soundex.asc()) or .desc()
            rows = []
            for cert in Cert.query.filter_by(**filters).limit(10).all():
                rows.append(render_template('certificate_row.html', certificate=cert))

            return jsonify({"data": rows})
        else:
            return jsonify({"errors": form.errors})

    return render_template('search.html', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """
    Return edit page
    """
    return render_template('edit.html')
