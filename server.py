from flask import Flask, render_template, request, flash, session, redirect
from model import Organization, connect_to_db, db
import crud
import cloudinary.uploader
import os



CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dbh6sbsv3"


app = Flask(__name__)
app.secret_key = "dev"



@app.route("/")
@app.route("/home")
def homepage():
    """View homepage."""

    return render_template('homepage.html', title='Home')


@app.route("/login")
def log_in():
    """Display log in template"""

    return render_template('login.html')

@app.route("/logout")
def log_out():
    """ Will log out the user"""
    session.clear()
    return redirect("/")

@app.route("/login",methods=["POST"])
def process_log_in():
    """log in"""

    email= request.form.get("email")
    password =request.form.get("password")
    user_type = request.form.get("user_type")

    if user_type == "volunteer":

        user = crud.get_vol_by_email(email)

        if not user or user.password != password:
            flash("email or password incorret. try again")
            return redirect("/login")

        else:
            session['user_id']= user.user_id
            flash(f"welcome back {user.fname}")
            return redirect("/opportunities")

    elif user_type == "organization":
        organization = crud.get_org_by_email(email)

        if not organization or organization.organization_password != password:
            flash("email or password incorrect. try again")
            return redirect("/login")

        else:
            session['organization_id']= organization.organization_id
            flash(f"welcome back {organization.organization_name}")
            return redirect("/oportunities")
    else:   
        flash(f"Please select volunteer or organization")
        return redirect("/login")

@app.route("/register")
def register():
    """Open to register page"""

    return render_template("register.html")

@app.route("/register",methods=["POST"])
def register_volunteer():
    """Register a volunteer"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    if user_type == 'volunteer':
        check_user = crud.get_vol_by_email(email)

        if check_user:
            flash("Email already in use")
            return redirect("/register")
    
        else: 
            user = crud.create_vol(fname = fname, lname = lname, email = email, password= password)
            db.session.add(user)
            db.session.commit()
            flash(f"{fname} your account was created successfully")

        return redirect("/")

    elif user_type == 'organization':

        organization_name = request.form.get("fname")
        organization_email = request.form.get("email")
        organization_password = request.form.get("password")


        check_organization = crud.get_org_by_email(organization_email)

        if check_organization:
            flash("Email already in use")

            return redirect("/register")

        else: 
            check_organization = crud.create_org(organization_name=organization_name, organization_email=organization_email, organization_password=organization_password)
            db.session.add(check_organization)
            db.session.commit()
            flash(f"{organization_name} your account was created successfully")

        return redirect("/")

    else:
        flash(f"Please select Volunteer or Organization when signing up")
        return redirect("/register")

# NAAAAAAO APAGAAR ESSE CARALHOOOOOOOO
@app.route("/opportunities")
def volunteer_opportunity():
    """ make sure the user doesnt go to pages withou log in"""


    volunteer_opps = crud.get_all_volunteer_opportunities()
    volunteer_opps = volunteer_opps[::-1]

    # check_logged_user = session.get('user')
    # user = crud.get_vol_by_email(check_logged_user)

    # if user is None:
    #     flash("You must log in")
    #     return redirect("/login")   

    # else:
    
    return render_template("volunteer-opportunities.html", volunteer_opps = volunteer_opps)

@app.route("/profile")
def profile():
    """View user profile"""

    return render_template('profile.html')

@app.route("/organizations")
def organizations():
    """View user profile"""

    return render_template('organizations.html')

@app.route("/volunteers")
def volunteers():
    """View user profile"""

    return render_template('volunteers.html')

@app.route("/dash-vol", methods=["GET"])
def vol_dash():
    """ list of all volunteer opportunities"""


    user = crud.get_vol_by_email(session["volunteer_email"])

    if not user:
        return redirect("/")

    opts = crud.get_all_volunteer_opportunities()

    return render_template("dash.html", list_of_opportunities = opts)




@app.route("/new_post", methods=["POST"])
def register_opportunity():

    title = request.json.get("title")
    content = request.json.get("content")
    opp_photo = request.json.get('opp_photo')

    # title = request.form.get("title")
    # content = request.form.get("content")
    # opp_photo = request.files.get('opp_photo')


    print("******************")
    print(title)
    print(content)
    print(opp_photo)
    print("******************")



    if opp_photo:

        result = cloudinary.uploader.upload(opp_photo,
                                            api_key=CLOUDINARY_KEY,
                                            api_secret=CLOUDINARY_SECRET,
                                            cloud_name=CLOUD_NAME)
        img_url = result['secure_url']
    else:
        img_url = None
    
    print("******************")
    print(img_url)
    print("******************")
    
    # organization_id = request.form.get("organization_id")

    # WILL GET THIS WITH THE SESSION

    if 'organization_id' in session:
        new_opp = crud.create_volunteer_opportunity(title=title,opp_photo=img_url,content=content, organization_id=session['organization_id'])
    
        db.session.add(new_opp)
        db.session.commit()
        flash("Your message has been posted")
        

    return redirect("/opportunities")



# @app.route("/new_post")
# def new_post():
#     if 'user_id' in session:
#        return redirect("/opportunities") 

#     return redirect("/")


@app.route("/opportunities-listed/<organization_id>")
def opportunities_listed(organization_id):
    """ It will display opportunities by id """

    org = crud.get_org_by_id(organization_id)

    return render_template("display_by_id.html", org = org)








# navbar related links
    
@app.route("/about")
def about():
    """View about page"""


    return render_template('about.html', title='About')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
