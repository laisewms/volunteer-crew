from pyexpat import model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy ()

class User(db.Model):
    """ User profile """

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    city = db.Column(db.String)
    
    organizations = db.relationship('Organization', secondary = "users_organizations", back_populates="users")
    # users = db.relationship('User', back_populates="users")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email} fname={self.fname} lname={self.lname}>"



class Organization(db.Model):
    """Table for Organizations and entities"""

    __tablename__ = "organizations"
    
    org_id = db.Column (db.Integer, autoincrement = True, primary_key=True)
    org_name = db.Column (db.String, nullable=False)
    org_contact = db.Column (db.String, nullable=False)
    org_leader = db.Column (db.String)
    org_details = db.Column (db.String)
    
    users = db.relationship('User', secondary = "users_organizations", back_populates="organizations")


    def __repr__(self):
        return f"<Organization org_id={self.org_id}  org_name={self.org_name} org_contact={self.org_contact} >"


class UsersOrganization(db.Model):
    """Users oganization - middle table"""

    __tablename__ = "users_organizations"

    
    users_org_id = db.Column (db.Integer, autoincrement = True, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organizations.org_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))



    def __repr__(self):
        return f"<Users organization id={self.users_org_id}>"


class Volunteer(db.Model):
    """Create Volunteers"""

    __tablename__ = "volunteers"


    volunteer_id = db.Column (db.Integer, autoincrement = True, primary_key=True)
    user_listing_id = db.Column(db.Integer, db.ForeignKey("listings.user_listing_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
   
    # listings = db.relationship('Listing', back_populates="volunteers")
    # users = db.relationship('User', back_populates="volunteers")

    def __repr__(self):
        return f"<Volunteer volunteer_id={self.volunteer_id}>"

class Listing(db.Model):
    """Volunteering listing roles"""

    __tablename__ = "listings"

    user_listing_id = db.Column (db.Integer, autoincrement = True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    org_id = db.Column(db.Integer, db.ForeignKey("organizations.org_id"))
    written_text = db.Column (db.String, nullable=False)
    media_location = db.Column (db.String, nullable=False)


    # organizations = db.relationship('Organization', back_populates="listings")
    # users = db.relationship('User', back_populates="listings")

    def __repr__(self):
        return f"<Listing listing_id={self.volunteer_id}>"


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



