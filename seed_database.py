"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb volunteer')
os.system('createdb volunteer')

model.connect_to_db(server.app)
model.db.create_all()





with open('data/organizations.json') as f:
    organization_data = json.loads(f.read())

organization_in_db=[]  #list of new organization objects stored in database


for organization in organization_data:

    organization_name = organization["organization_name"]
    organization_photo = organization["organization_photo"]
    organization_email= organization["organization_email"]
    organization_password = organization["organization_password"]


    new_org = crud.create_org(organization_name = organization_name, organization_photo = organization_photo, organization_email = organization_email, organization_password = organization_password)
    organization_in_db.append(new_org)
    model.db.session.add(new_org)
    model.db.session.commit()


with open ('data/volunteerOpportunity.json') as f:
    volunteer_opp_data = json.loads (f.read())

volunteer_opp_in_db = []

for volunteer_opp in volunteer_opp_data:  # volunteer_opp is a dictionary

    title = volunteer_opp["title"]
    opp_photo = volunteer_opp["opp_photo"]
    date_posted = volunteer_opp["date_posted"]
    content = volunteer_opp["content"]
    organization_id = volunteer_opp["organization_id"]

    new_volunteer_opportunity = crud.create_volunteer_opportunity(title= title, opp_photo=opp_photo, date_posted=date_posted, content=content, organization_id=organization_id)
    volunteer_opp_in_db.append(new_volunteer_opportunity)
    model.db.session.add(new_volunteer_opportunity)
    model.db.session.commit()



















    

# user = crud.create_vol("email", "password", "fname","lname" )
# model.db.session.add(user)
# model.db.session.commit()

# organization = crud.create_org("organization_name", "organization_photo", "organization_email", "organization_password")
# model.db.session.add(organization)
# model.db.session.commit()

# with open('data/listings.json') as f:
#     post_data = json.loads(f.read())


# listings_in_db = []

# for post in post_data:
#     organization_name, title, date_posted, content =(
#         post["organization_name"],
#         post["title"],
#         post["date_posted"],
#         post["content"],
#     )

#     date_posted = datetime.strptime(post["date_posted"], "%Y-%m-%d")
#     #so then I can use author
#     organization_name = model.Organization.query.first()

#     db_post = crud.create_volunteer_opportunity(organization_name, title,content,date_posted)
#     listings_in_db.append(db_post)

#     model.db.session.add_all(listings_in_db)
#     model.db.session.commit()