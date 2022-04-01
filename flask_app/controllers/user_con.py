from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_mod
from flask_bcrypt import Bcrypt
from flask_app.config.validator import Logged_in
import datetime
bcrypt = Bcrypt(app)

#----------------------------------
#-------------------------------------  Home Route
#----------------------------------

@app.route('/')
def homepage():
    return render_template('homepage.html')

#----------------------------------
# ------------------------------------  Register Process
#----------------------------------

@app.route('/register', methods=['POST'])
def registration():
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "confirm_password" : request.form["confirm_password"]
    }

    valid_form = user_mod.User.validate_registration(data)
    
    if not valid_form:
        return redirect('/')
    
    data['password'] = bcrypt.generate_password_hash(request.form['password'])

    user_id = user_mod.User.add_user(data)
    session["user_id"], session["first_name"] = user_id, data["first_name"]
    return redirect('/dashboard')

#----------------------------------
# ------------------------------------  Login Process
#----------------------------------

@app.route('/login', methods=['POST'])
def login():

    ####################  Process data from form  ####################
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }

    ####################  validate form data  ####################
    user = user_mod.User.validate_login(data)

    ####################  if user exists check password  ####################
    if user:
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash('Invalid Email or Password!')
            return redirect('/')
    else:
        flash('Invalid Email or Password!')
        return redirect('/')

    session['user_id'], session['user_first_name'] = user.id, user.first_name

    
    ####################  if login success, redir to dashboard   ####################
    return redirect('/dashboard')

#----------------------------------
# ------------------------------------  User Profile
#----------------------------------

@app.route('/dashboard')
def load_profile():
    if Logged_in.checker():
        date = (datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() % 7)).strftime('%d %b %y')
        return render_template('dashboard.html', date = date)
    else:
        return redirect('/')

#----------------------------------
# ------------------------------------  Settings Page
#----------------------------------

@app.route('/settings')
def settings():
    if Logged_in.checker():
        return render_template('settings.html')
    else:
        return redirect('/')

#----------------------------------
# ------------------------------------  Logout
#----------------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

