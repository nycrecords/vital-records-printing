import os
from sqlalchemy import cast, String
from sqlalchemy.exc import SQLAlchemyError
from app import app, login_manager, db
from app.forms import SearchForm, LoginForm, PasswordForm, ReportForm
from app.models import Cert, User, Report
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    jsonify,
    flash,
)
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
)
from datetime import datetime

RESULT_SET_LIMIT = 20
WILDCARD_CHAR = "*"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['POST'])
def login():
    """
    Log in a user or flash an error message.
    If the user's password has expired, proceed with logging in
    but redirect to the change password page.
    """
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=(request.form.get('remember') is not None))
            # check if password has expired or is "password"
            if current_user.has_invalid_password:
                return redirect(url_for('password'))
        else:
            flash('Wrong username and/or password.', category="danger")
    return redirect('/')


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """
    Return the change password page and redirect to the home page
    if password change is successful.
    """
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        current_user.update_password(password_form.current_password.data,
                                     password_form.new_password.data)
        return redirect('/')
    return render_template('change_password.html', password_form=password_form)


@app.route('/', methods=['GET'])
@app.route('/search', methods=['POST'])
def search():
    """
    Return the search page or certificate row templates.
    """
    form = SearchForm()
    login_form = LoginForm()
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
                            cast(col, String).ilike(
                                value.replace(WILDCARD_CHAR, "%")
                            )
                        )
                    elif name in ("first_name", "last_name"):
                        filter_args.append(
                            col.ilike(value)
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

    return render_template('index.html', form=form, login_form=login_form)


@app.route("/years", methods=['GET'])
def years():
    """
    Return a range of available years to search by based on "type" and "county".
    """
    filters = {
        key: val for (key, val) in
        dict(
            type=request.args["type"],
            county=request.args["county"]
        ).items() if val
    }
    base_query = Cert.query.filter_by(**filters).filter(Cert.year != None)
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
    if cert.file_id is None:
        urls = [url_for('static', filename=os.path.join('img', "missing.png"))]
    else:
        if not cert.file.converted:
            cert.file.convert()
        urls = cert.file.pngs
    return jsonify({
        "data": {
            "urls": urls,
            "number": cert.number,
            "type": cert.type.title(),
            "name": cert.name,
            "year": cert.year,
            "county": cert.county.title(),
            "soundex": cert.soundex,
            "filename": cert.file.name if cert.file is not None else ""
        }
    })


@app.route('/report/<int:cert_id>', methods=['GET', 'POST'])
@login_required
def report(cert_id):
    """
    Return template for report page
    """
    cert = Cert.query.get(cert_id)
    if cert.file_id is None:
        urls = [url_for('static', filename=os.path.join('img', "missing.png"))]
    else:
        if not cert.file.converted:
            cert.file.convert()
        urls = cert.file.pngs

    form = ReportForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            form_completed = False
            for key, value in form.data.items():
                if value != "" and key is not 'csrf_token' and key is not 'submit':
                    form_completed = True
            if not form_completed:
                flash("Please complete at least one form field.", category="warning")
                return render_template('report_issue.html', form=form, cert=cert, urls=urls)
            else:
                form_fields = {
                    name: data for name, data in {
                    'county': form.county.data,
                    'month': form.month.data,
                    'day': form.day.data,
                    'year': form.year.data,
                    'age': form.age.data,
                    'number': form.number.data,
                    'soundex': form.soundex.data,
                    'first_name': form.first_name.data,
                    'last_name': form.last_name.data,
                    'comments': form.comments.data}.items()
                    if data
                }
                report = Report(cert_id=cert_id, user_id=current_user.id, values=form_fields)
                db.session.add(report)
                db.session.commit()
                flash("Your report has been submitted.", category="success")
                return redirect('/')
        else:
            flash("An error has occurred.")
            print(form.errors)
    return render_template('report_issue.html', form=form, cert=cert, urls=urls)


@app.route('/reported_issues', methods=['GET', 'POST'])
@login_required
def reported_issues():
    users = User.query.all()
    reports = Report.query.order_by(Report.cert_id.asc())
    certs=Cert.query.all()
    newList = {}  # strip out value from dict; a dict of key to list {cert_id:list}
    # list will look like [ attribute change 1, attribute change 2, etc , timestamp, firstname+lastname]



    default = 'comments'  # key default value

    for report in reports:# iterate through report db
        report_values = report.values
        #
        for key, value in report_values.items():

            #print(key + ": " + value)
            newList.setdefault(report.cert_id, []) #a dict of key to list
            if key == default:
                newList[report.cert_id].append(key + ": " + value)
            else:
                newList[report.cert_id].append(key + " should be :" + value)

        newList[report.cert_id].append(str(report.timestamp)[:10])#timestamp of the issue reported

        for user in users:#iterate through user db to find Report author
            if report.user_id==user.id:
                newList[report.cert_id].append(user.first_name + " " + user.last_name)






        print(newList)
        print("END")



    return render_template('reports_page.html', reports=reports, newList=newList, user=user)
