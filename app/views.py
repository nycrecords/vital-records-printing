import os
from sqlalchemy import cast, String
from sqlalchemy.exc import SQLAlchemyError
from app import app
from app.forms import SearchForm
from app.models import Cert
from flask import (
    render_template,
    request,
    url_for,
    jsonify,
)


RESULT_SET_LIMIT = 20
WILDCARD_CHAR = "*"

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/', methods=['GET'])
@app.route('/search', methods=['POST'])
def search():
    """
    Return search page or certificate row templates.
    """
    form = SearchForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # set filters
            filter_by_kwargs = {}
            filter_args = []
            for name, value, col in [
                ("type", form.type.data, Cert.type),
                ("county", form.county.data, Cert.county),
                ("year", form.year.data, Cert.year),
                ("number", form.number.data, Cert.number),
                ("first_name", form.first_name.data, Cert.first_name),
                ("last_name", form.last_name.data, Cert.last_name),
                ("soundex", form.soundex.data, Cert.soundex)
            ]:
                if value:
                    if WILDCARD_CHAR in value:
                        filter_args.append(
                            cast(col, String).like(
                                value.replace(WILDCARD_CHAR, "%")
                            )
                        )
                    else:
                        filter_by_kwargs[name] = value

            base_query = Cert.query.filter_by(**filter_by_kwargs).filter(*filter_args)

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
            for cert in base_query.slice(form.start.data, RESULT_SET_LIMIT + form.start.data).all():
                rows.append(render_template('certificate_row.html', certificate=cert))

            return jsonify({"data": rows})
        else:
            return jsonify({"errors": form.errors})

    return render_template('index.html', form=form)


@app.route("/years", methods=['GET'])
def years():
    filters = {
        key: val for (key, val) in
        dict(
            type=request.args["type"],
            county=request.args["county"]
        ).items() if val
    }
    base_query = Cert.query.filter_by(**filters)
    try:
        start = base_query.order_by(Cert.year.asc()).first()
        end = base_query.order_by(Cert.year.desc()).first()
        response_json = {
            "data": {
                "start": start.year,
                "end": end.year
            }
        }
    except (SQLAlchemyError, AttributeError):
        response_json = {}
    return jsonify(response_json)


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