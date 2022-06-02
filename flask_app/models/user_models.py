from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import os
print( os.environ.get("FLASK_APP_API_KEY") )

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_user(cls, data):
        query = "insert into users(first_name, last_name, email, password)"
        query += "values(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "select * from users where id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_user(cls):
        query = "select * from users;"
        result = connectToMySQL(DATABASE).query_db(query)
        user_db = []
        for row in result:
            user_db.append( cls(row))
        return user_db

    @classmethod
    def get_all_users(cls):
        query = "select * from users;"
        results = connectToMySQL(DATABASE).query_db(query)
        return results

    @classmethod
    def get_one_by_email(cls, data):
        query = "select * from users where email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False
        

    @staticmethod
    def validate_registration(user_form):
        is_valid = True

        if len(user_form["first_name"]) < 3:
            is_valid = False
            flash("Must have first name, with at least 2 characters", 'err_users_first_name')

        if len(user_form["last_name"]) < 3:
            is_valid = False
            flash("Must have first name, with at least 2 characters", 'err_users_last_name')

        if len(user_form["email"]) < 3:
            flash("Must have email", 'err_users_email')
            is_valid = False
        elif not EMAIL_REGEX.match(user_form['email']): 
            flash("Invalid email address", 'err_users_email')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({ 'email' : user_form['email'] })
            if potential_user: 
                flash("Email aready in use", 'err_users_email')
                is_valid = False

        if len(user_form["password"]) < 8:
            flash("Requires a password, minimum 8 characters", 'err_users_password')
            is_valid = False

        if not user_form['password'] == user_form['password1']:
            flash("The passwords dont match", 'err_users_password1')
            is_valid = False
        return is_valid
        


    @staticmethod
    def validate_session(email_session):
        if 'email' in email_session:
            return True
        else:
            return False