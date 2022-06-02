from flask import redirect, render_template, request, session, flash, json, jsonify
from flask_app import app
from flask_app.models.user_models import User
from flask_app.models.car_models import Car
from flask_app.controllers import car_controllers
from flask_bcrypt import Bcrypt
import os
print( os.environ.get("FLASK_APP_API_KEY") )

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    else:
        return render_template("index.html")


@app.route("/create", methods = ["POST"])
def create_user():
    is_valid = User.validate_registration(request.form)

    if not is_valid: 
        return redirect('/')

    encrypted_password = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : encrypted_password
    }
    # the below 2 lines create session from create
    user_id = User.create_user(data)
    
    session['user_id'] = user_id
    
    return redirect ("/dashboard")


@app.route("/login", methods = ["POST"])
def login_user():
    data = {
        'email': request.form['login_email']
    }    
    # we need this below line to set up session down at the bottom
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("Email is not registered", "err_users_login_user_email")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash("Invalid Password", "err_users_log_password")
        return redirect("/")
    # below is setting up the code, saying in the user_in_db select the id
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route("/logout")
def logout_user():
    session.clear()
    return redirect('/')