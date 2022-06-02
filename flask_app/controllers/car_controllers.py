from flask import redirect, render_template, request, session, jsonify, json
from flask_app import app
from flask_app.models.car_models import Car
from flask_app.models.user_models import User
from flask_app.controllers import user_controllers
import os
print( os.environ.get("FLASK_APP_API_KEY") )

@app.route("/dashboard")
def welcome_user():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : session["user_id"]
    }
    user = User.get_one({'id' : session['user_id']})
    cars = Car.get_all_cars()
    return render_template('dashboard.html', user = user, cars = cars)

@app.route("/car/add")
def add():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id' : session['user_id']})
    return render_template('add.html', user = user)

@app.route("/car/create", methods = ["POST"])
def create_car():
    is_valid = Car.validate_car(request.form)
    print(request.form)
    if not is_valid:
        return jsonify(err='invalid'), 400
    Car.create_car(request.form)
    print(request.form)
    return jsonify(messsage = "success"), 200

@app.route("/car/update/<int:id>", methods = ["POST"])
def update_car(id):
    is_valid = Car.validate_car(request.form)
    print(id)
    if not is_valid:
        return jsonify(err='invalid'), 400
    Car.edit_car(request.form)
    print(request.form)
    return jsonify(messsage = "success"), 200

# the id has to do with the recipe id
@app.route("/car/edit/<int:id>")
def edit(id):
    # once session but in , the next two lines are needed for validation
    if 'user_id' not in session:
        return redirect('/')
    data= {
        "id" : session["user_id"]
    }
    user = User.get_one(data)
    car = Car.get_one_by_id({'id' : id})
    return render_template('edit.html', user = user, car=car)


@app.route('/car/delete/<int:id>')
def delete_car(id):
    # this is saying that the id we are passing through should be the id listed on teh class method
    Car.delete_car({"id" : id})
    return redirect('/dashboard')


@app.route('/car/show/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/')    
    data= {
        "id": id
    }
    # this is identifying the user on the page from session
    user = User.get_one({'id' : session['user_id']})
    # this is then pulling the specific recipy, which will then be shown on the show page
    car = Car.get_one_car(data)
    return render_template('show.html', user = user, car = car)

@app.route('/car/vin/<int:id>')
def vin(id):
    if 'user_id' not in session:
        return redirect('/')    
    data= {
        "id": id
    }
    # this is identifying the user on the page from session
    # this is then pulling the specific recipy, which will then be shown on the show page
    car = Car.get_one_car(data)
    return render_template('vin.html', car = car)



@app.route('/upload-image', methods=["GET", "POST"])
def upload_image():
    return render_template("upload_image.html")