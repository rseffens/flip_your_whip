from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models.user_models import User
import os
print( os.environ.get("FLASK_APP_API_KEY") )


class Car:
    def __init__(self, data):
        self.id =  data['id']
        self.year = data['year']
        self.make = data['make']
        self.model = data['model']
        self.vin = data['vin']
        self.description = data['description']
        self.price = data['price']
        self.photo = data['photo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # this will bring in the user ID to this page.
        self.user_id = data['user_id']


    @classmethod
    def create_car(cls, data):
        query = "insert into cars(year, make, model, vin, description, price, photo, created_at, updated_at, user_id)"
        query += "values( %(year)s, %(make)s, %(model)s, %(vin)s, %(description)s, %(price)s, %(photo)s, NOW() , NOW(), %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    @classmethod
    def edit_car(cls, data):
        # careful ensuring you list everyting correct, copy to ensure works.
        query = "update cars set year = %(year)s, make= %(make)s, model = %(model)s, vin = %(vin)s, description = %(description)s, price = %(price)s, photo = %(photo)s where id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete_car(cls,data):
        query = "delete from cars where id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_cars(cls):
        query = "select * from cars;"
        result = connectToMySQL(DATABASE).query_db(query)
        cars_db = []
        for row in result:
            cars_db.append( cls(row))
        return cars_db


    @classmethod
    # dashboard to list the user who created the item
    def get_all_cars(cls):
        query = "select * from cars join users on users.id = cars.user_id;"
        result = connectToMySQL(DATABASE).query_db(query)
        all_cars = []
        for row in result:
            car = cls(row)
            data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            car.user = User(data)
            all_cars.append(car)
        return all_cars   


    @classmethod
    # for the show one vehicle page to link together. 
    def get_one_car(cls, data):
        query = "select * from cars join users on cars.user_id = users.id where cars.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        one_car = []
        if results:
            car = cls(results[0])
            data = {
                'id' : results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'created_at' : results[0]['created_at'],
                'updated_at' : results[0]['updated_at']
            }
            car.user = User(data)
            one_car.append(car)
        return car


    @classmethod
    def get_one_by_id(cls, data):
        # finding a cars by id number pulled over from controller
        query = "select * from cars where id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            # below is used to say we are returning a single dictionary from a group of dictionaries
            return cls(result[0])
        return False


    @staticmethod
    def validate_car(car_form):
        is_valid = True


        if not car_form["year"]:
            is_valid = False
            flash("Date of sighting required", 'err_car_year')


        if len(car_form["make"]) < 1:
            is_valid = False
            flash("Make Required", 'err_car_make')

        if len(car_form["model"]) < 1:
            is_valid = False
            flash("Model Required", 'err_car_model')

        if len(car_form["vin"]) < 17:
            is_valid = False
            flash ("Vin needs to be 17 characters", 'err_car_vin')

        if len(car_form["description"]) < 1:
            is_valid = False
            flash("Description required", 'err_car_description')
        
        if len(car_form["price"]) < 1:
            is_valid = False
            flash("Price required", 'err_car_price')

        return is_valid