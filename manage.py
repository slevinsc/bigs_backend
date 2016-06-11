# __author__ = 'Slevin'
from flask_script import Manager

from app import create_app, db
from app.models.user import User

app = create_app('default')


@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    user_data = User(username='test', pwd='000000')
    print user_data.password
    db.session.add(user_data)
    db.session.commit()


manager = Manager(app)
if __name__ == '__main__':
    manager.run()
