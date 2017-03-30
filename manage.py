from flask_script import Manager

from app import app, db

from app.models import User

manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()


@manager.command
def create_user(first_name, last_name, username=None):
    db.session.add(User(username or (first_name[0]+last_name).lower(),
                        'password',
                        first_name,
                        last_name))
    db.session.commit()


if __name__ == "__main__":
    manager.run()
