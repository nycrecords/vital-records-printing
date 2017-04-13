from collections import namedtuple
from itertools import combinations
from flask_script import Manager, Shell
from app import app, db
from app.models import Cert, File, User, History

manager = Manager(app)


@manager.command
def create_certificate_indexes():
    """
    Create db indexes (7) for table 'certificate'.
    This should be run *after* table population.
    Existing indexes will not be recreated.
    """
    from sqlalchemy.engine import reflection
    insp = reflection.Inspector.from_engine(db.engine)

    Index = namedtuple("Index", ["name_suffix", "attributes"])
    indexes = (
        Index("type_county_year", (Cert.type, Cert.county, Cert.year)),
        Index("type_year", (Cert.type, Cert.year)),
        Index("year", (Cert.year, )),
        Index("county", (Cert.county, )),
        Index("firstname", (Cert.first_name, )),
        Index("lastname", (Cert.last_name, )),
        Index("number", (Cert.number, )),
        Index("soundex", (Cert.soundex, ))
    )
    for i, index in enumerate(indexes):
        index_name = "idx_{}".format(index.name_suffix)
        if set(attr.key for attr in index.attributes) in (
            set(index["column_names"]) for index in insp.get_indexes(Cert.__tablename__)
        ):
            print("{}\tAlready Created, Skipping\t{}".format(i, index_name))
            continue
        print("{}\t{}".format(i, index_name))
        db.Index(index_name, *index.attributes).create(db.engine)


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
