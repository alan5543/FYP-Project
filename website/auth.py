# Import the flask routing and POST/GET
from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.sql.expression import true

# Import the database processing
from .models import User
from . import db
from sqlalchemy.engine import url
from werkzeug.security import generate_password_hash, check_password_hash

# Import the Login system manager
from flask_login import login_user, logout_user, login_required, current_user

# Set up the blueprint for routing
auth = Blueprint('auth', __name__)
from . import constants

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # print the login account in the console
    data = request.form
    print(data)

    # POST means user have entered the account
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # find the record of that user
        user = User.query.filter_by(email=email).first()
        if user:
            # check the password is correct or not
            if check_password_hash(user.password, password):
                flash(constants.LOGIN_SUCCESS_MSG, category='success')
                # remember the user has been logged in
                login_user(user, remember=True)

                # route to the home page
                return redirect(url_for('views.home'))
            else:
                # if the password is wrong
                flash(constants.LOGIN_WRONG_PW, category='error')
        else:
            # if the user account is not existed
            flash(constants.LOGIN_NOT_EXIST, category='error')

    # route back to the login page if any failed
    return render_template("login.html", boolean = True, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # for log out and route back to the login page
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign', methods=['GET', 'POST'])
def sign():
    # POST means user input and register for a new account
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        # create a temp user to check whether it is a existed account
        user = User.query.filter_by(email=email).first()

        # valid and error handling
        if user:
            flash(constants.EMAIL_EXIST_ERR, category='error')
        elif len(email) < 4 :
            flash(constants.EMAIL_SHORT_ERR, category='error')
        elif len(name) < 2 :
            flash(constants.EMAIL_NAME_ERR, category='error')
        elif len(password) < 7:
            flash(constants.EMAIL_PW_ERR, category='error')
        elif password != cpassword:
            flash(constants.EMAIL_MATCH_ERR, category='error')
        else:
            # valid account and sent to database
            newUser = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(newUser)
            db.session.commit()

            # flash a success message
            flash(constants.REGISTER_SUCCESS_MSG, category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)