from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_mod
from flask_bcrypt import Bcrypt
from flask_app.config.validator import Logged_in
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
    session["user_id"] = user_id
    return redirect('/paintings')

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

    session['user_id'] = user.id
    
    ####################  if login success, redir to dashboard   ####################
    return redirect('/paintings')

#----------------------------------
# ------------------------------------  User Profile
#----------------------------------

@app.route('/paintings')
def load_profile():
    if Logged_in.checker():
        data = {"id": session["user_id"]}
        user = user_mod.User.get_user(data)
        paintings = painting_mod.Painting.get_paintings_with_artists()
        return render_template('dashboard.html', user = user, paintings = paintings)
    else:
        return redirect('/')

#----------------------------------
# ------------------------------------  Logout
#----------------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

