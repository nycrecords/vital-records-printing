from flask_script import Manager

from app import app, db
from app.models import Cert

manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
