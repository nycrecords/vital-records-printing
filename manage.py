from flask_script import Manager

from app import app, db

manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()


# TODO: create user

if __name__ == "__main__":
    manager.run()
