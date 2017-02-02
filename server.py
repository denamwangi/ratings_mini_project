"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():

    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    if User.query.filter_by(email=email).first() is None:
        user = User(email=email,
                    password=password,
                    age=age,
                    zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        return "You are now registered! yay!"
        # RETURN REDIRECT THING HERE
    else:
        return "Username taken."


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        print "check 1"

        if user:
            if password == user.password:
                print "this is working!"
                session['user'] = user.user_id
                return 'You are now logged in'
            else:
                return 'That password is incorrect!'
        else:
            print "not registered"
            return 'That email has not been registered.'

        # if email == User.query.filter_by(email=email).first().email) and (session['password'] == User.query.filter_by(password=password).first().password):
        #     print "check 2"
        #     flash("You were successfully logged in")
        #     print session
        #     return redirect(url_for('index'))

        # else:
        #     print "check 3"
        #     flash("Invalid credentials")
        #     return redirect('/login')

    return render_template('login.html')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
