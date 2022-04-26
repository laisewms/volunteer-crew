from email.policy import default
from enum import unique
from pyexpat import model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import false

db = SQLAlchemy ()


class Organization(db.Model):
    """ Organization """

    __tablename__="organizations"

    organization_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    organization_name = db.Column(db.String(120), unique=True)
    organization_photo = db.Column(db.String(40), nullable =False, default='default.png')
    organization_email = db.Column(db.String(150), nullable =False)
    organization_password = db.Column(db.String(35), nullable =False)

    volunteer_opportunity = db.relationship("VolunteerOpportunity", back_populates ="organizations")
 


    def __repr__(self):
        return f"<Organization organization_id={self.organization_id}, organization_name={self.organization_name}, email={self.organization_email} >"
    
class VolunteerOpportunity(db.Model):
    """ Posts/listings """

    __tablename__= "volunteer_opportunity"

    volunteer_opt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    opp_photo = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.organization_id'), nullable=False)

    users = db.relationship("User", secondary="user_volunteer_task", backref="volunteer_opportunity")

    organizations = db.relationship("Organization", back_populates ="volunteer_opportunity")
    
    def __repr__(self):
        return f"<Volunteer Opportunity: title={self.title}, date={self.date_posted}, content={self.content} >"


class UserVolunteerTask(db.Model):
    """ Organization """

    __tablename__="user_volunteer_task"

    user_task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    volunteer_opt_id = db.Column(db.Integer, db.ForeignKey('volunteer_opportunity.volunteer_opt_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f"<User_volunteer_task: user_task_id={self.user_task_id} >"



class User(db.Model):
    """ User profile """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String(10), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
   
    
    def __repr__(self):
        return f"<User: email={self.email}, fname={self.fname}, lname={self.lname}>"





def connect_to_db(flask_app, db_uri="postgresql:///volunteer", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)



