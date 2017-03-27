import os
from app import app
from app.forms import SearchForm
from app.models import Cert
from flask import (
    render_template,
    request,
    url_for,
    jsonify,
)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/', methods=['GET'])
@app.route('/search', methods=['POST'])
def search():
    """
    Return search page
    """
    limit = 20
    form = SearchForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # set filters
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

            base_query = Cert.query.filter_by(**filters)

            # set ordering
            for field, col in [
                (form.year_sort, Cert.year),
                (form.number_sort, Cert.number),
                (form.first_name_sort, Cert.first_name),
                (form.last_name_sort, Cert.last_name),
                (form.soundex_sort, Cert.soundex)
            ]:
                if field.data != 'none':
                    if field.data == 'asc':
                        base_query = base_query.order_by(col.asc())
                    else:
                        base_query = base_query.order_by(col.desc())
                    break

            # render rows
            rows = []
            for cert in base_query.slice(form.start.data, limit + form.start.data).all():
                rows.append(render_template('certificate_row.html', certificate=cert))

            return jsonify({"data": rows})
        else:
            return jsonify({"errors": form.errors})

    return render_template('index.html', form=form)


@app.route('/certificate/<int:cert_id>', methods=['GET'])
def image(cert_id):
    """
    Return certificate data.
    """
    cert = Cert.query.get(cert_id)
    if not os.path.exists(cert.filename):  # TODO: use actual file path
        src = url_for('static', filename=os.path.join('img', "missing.jpg"))
    else:
        src = url_for('static', filename=os.path.join('img', cert.filename))  # TODO: actual fle path
    return jsonify({
        "data": {
            "src": src,
            "number": cert.number,
            "type": cert.type.title(),
            "name": cert.name,
            "year": cert.year,
            "county": cert.county.title(),
            "soundex": cert.soundex,
        }
    })