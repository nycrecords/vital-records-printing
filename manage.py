from collections import namedtuple
from itertools import combinations
from flask_script import Manager, Shell
from app import app, db
from app.models import Cert, File, User, History

manager = Manager(app)


@manager.command
def create_certificate_indexes(check_existing=False):
    """
    Create db indexes for table 'certificate'.
    
    This should be run *after* table population and is expected to take a while to complete.
    
    Indexes are *almost* all the possible combinations of the certificate 
    columns that correspond to searchable fields:
        type, county, year, first_name, last_name, number, soundex
    for a total of 64 indexes.
    
    Since 'type' is always included in the search query, it will always be part
    of every combination:
        type
        type, county
        type, year
        ...
        type, county, year
        type, county, soundex
        ...
    
    :param check_existing: Check for and skip existing indices
    """
    if check_existing:
        from sqlalchemy.engine import reflection
        insp = reflection.Inspector.from_engine(db.engine)

    Col = namedtuple("Col", ["string", "attr"])
    cols = {
        Col("type", Cert.type),
        Col("county", Cert.county),
        Col("year", Cert.year),
        Col("number", Cert.number),
        Col("first", Cert.first_name),
        Col("last", Cert.last_name),
        Col("soundex", Cert.soundex),
    }
    count = 0
    for length in range(1, len(cols) + 1):
        for comb in combinations(cols, length):
            if Col('type', Cert.type) in comb:
                index_name = "idx_{}".format("_".join((col.string for col in comb)))
                count += 1
                if check_existing and set(col.attr.key for col in comb) in (
                    set(index["column_names"]) for index in insp.get_indexes(Cert.__tablename__)
                ):
                    print("{}\tSKIPPING\t{}".format(count, index_name))
                    continue
                print("{}\t{}".format(count, index_name))
                db.Index(index_name, *(col.attr for col in comb)).create(db.engine)


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
