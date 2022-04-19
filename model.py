from pyexpat import model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import false

db = SQLAlchemy ()

class User(db.Model):
    """ User profile """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String(10), nullable=False)
    lname = db.Column(db.String(25), nullable = False)
    city = db.Column(db.String, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    posts = db.relationship('Post', backref='author', lazy=True)
    

    def __repr__(self):
        return f"<User email={self.email} fname={self.fname} image={self.img_file}>"

class Post(db.Model):
    """ Posts/listings """

    __tablename__= "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    def __repr__(self):
        return f"<Post title={self.title} date={self.date_posted}>"

    

class Volunteer(db.Model):
    """Create Volunteers""" 

    __tablename__ = "volunteers"

    volunteer_id = db.Column (db.Integer, autoincrement = True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)

    user = db.relationship('User', backref = 'volunteers')
    post = db.relationship('Post', backref = 'volunteers')

    def __repr__(self):
        return f"<Volunteer id={self.volunteer_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///volunteering", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)



