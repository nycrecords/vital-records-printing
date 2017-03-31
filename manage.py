from flask_script import Manager, Shell

from app import app, db
from app.models import Cert, File

manager = Manager(app)

DB_INDEX_ARGS = frozenset((
    ("idx_year_county_type", Cert.year, Cert.county, Cert.type),
    ("idx_first_county_type", Cert.first_name, Cert.county, Cert.type),
    ("idx_last_county_type", Cert.last_name, Cert.county, Cert.type),
    ("idx_soundex_county_type", Cert.soundex, Cert.county, Cert.type),
    ("idx_number_county_type", Cert.number, Cert.county, Cert.type),
))


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()


@manager.command
def create_certificate_indices():
    for args in DB_INDEX_ARGS:
        print("Creating '{}' ...".format(args[0]))
        db.Index(*args).create(bind=db.engine)


@manager.command
def drop_certificate_indices():
    for args in DB_INDEX_ARGS:
        print("Dropping '{}' ...".format(args[0]))
        db.Index(*args).drop(bind=db.engine)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        Cert=Cert,
        File=File,
    )

manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manager.run()
