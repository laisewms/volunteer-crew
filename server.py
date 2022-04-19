from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db


app = Flask(__name__)

#how can I hide it
app.secret_key = "dev"

#fake data for testing
posts = [
    {
        'author': 'Red Blue',
        'title' : 'help needed',
        'content': 'first post, this is a test.',
        'date_posted' : 'April 19, 2018'
    },

    {
        'author': 'Help Org',
        'title' : 'help needed this weekend',
        'content': 'this is another test for a volunteer role this weekend. ',
        'date_posted' : 'April 18, 2018'
    }
]


@app.route("/")
def homepage():
    """View homepage."""


    return render_template('homepage.html', title='Home',posts=posts)


@app.route("/about")
def about():
    """View homepage."""


    return render_template('about.html', title='About')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
