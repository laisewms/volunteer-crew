from email.policy import default



"""CRUD operations."""
from calendar import c
from model import VolunteerOpportunity, db, User, Organization, connect_to_db,UserVolunteerTask


def create_vol(fname, lname, email, password):


    new_user = User(fname = fname, lname=lname, email=email, password=password)


    return new_user

def create_org(organization_name, organization_email,organization_password, organization_photo = 'default.png'):

    new_org = Organization(organization_name = organization_name, organization_photo = organization_photo, organization_email = organization_email, organization_password = organization_password)

    return new_org




def log_in_org(organization_email, organization_password):


    organizations = Organization(organization_email=organization_email, organization_password=organization_password)


    return organizations

def get_vol_by_email(email):


    return User.query.filter(User.email == email).first()


def get_org_by_id(organization_id):

    return Organization.query.get(organization_id)


def get_org_by_email(organization_email):


    return Organization.query.filter(Organization.organization_email == organization_email).first()


#can I list my FK too?
def create_volunteer_opportunity(title,opp_photo,content, organization_id):

    volunteer_opportunity = VolunteerOpportunity(title = title,opp_photo = opp_photo,content = content, organization_id = organization_id) 

    return volunteer_opportunity

def get_all_volunteer_opportunities():

    return VolunteerOpportunity.query.all()



 

    



















if __name__ == '__main__':
    from server import app
    connect_to_db(app)