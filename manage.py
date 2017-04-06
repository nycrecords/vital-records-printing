from flask_script import Manager, Shell

from app import app, db
from app.models import Cert, File, User, History

manager = Manager(app)

DB_INDEX_ARGS = frozenset((
    ("idx_year_county_type", Cert.year, Cert.county, Cert.type),
    ("idx_first_county_type", Cert.first_name, Cert.county, Cert.type),
    ("idx_last_county_type", Cert.last_name, Cert.county, Cert.type),
    ("idx_soundex_county_type", Cert.soundex, Cert.county, Cert.type),
    ("idx_number_county_type", Cert.number, Cert.county, Cert.type),

    # nCr n=7 r=1
    ("idx_type", Cert.type),
    # nCr n=7 r=2
    ("idx_type_county", Cert.type, Cert.county),
    ("idx_type_year", Cert.type, Cert.year),
    ("idx_type_number", Cert.type, Cert.number),
    ("idx_type_first", Cert.type, Cert.first_name),
    ("idx_type_last", Cert.type, Cert.last_name),
    ("idx_type_soundex", Cert.type, Cert.soundex),
    # nCr n=7 r=3
))

Combination = {
    "type": Cert.type,
    "county": Cert.county,
    "year": Cert.year,
    "number": Cert.number,
    "first": Cert.first_name,
    "last": Cert.last_name,
    "soundex": Cert.soundex,
}

from itertools import combinations

@manager.command
def combination():
    for i in range(1, len(Combination)+1):
        bunchaCombs = list(combinations(Combination, i))
        print('---------------------------------')
        for comb in bunchaCombs:
            for search_field in comb:
                if search_field == 'type':
                    print(comb)
                    # base = "idx" + ("_{}" * i)
                    # for a_search_field in comb:
                    #     base.format(a_search_field)
                    # print(base)

@manager.command
def create_user(first_name, last_name, username=None):
    """
    Create a new user with password 'password'.
        
    :param first_name: User's first name 
    :param last_name: User's last name
    :param username: User's desired username
        default: first letter of first_name + last name (all lowercase)
    """
    db.session.add(
        User(
            username or (first_name[0] + last_name).lower(),
            'password',
            first_name,
            last_name
        )
    )
    db.session.commit()


@manager.command
def create_certificate_indices():
    """ Create db indices for table `certificate`. """
    for args in DB_INDEX_ARGS:
        print("Creating '{}' ...".format(args[0]))
        db.Index(*args).create(bind=db.engine)


@manager.command
def drop_certificate_indices():
    """ Drop db indices for table `certificate`. """
    for args in DB_INDEX_ARGS:
        print("Dropping '{}' ...".format(args[0]))
        db.Index(*args).drop(bind=db.engine)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        Cert=Cert,
        File=File,
        User=User,
        History=History,
    )


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
