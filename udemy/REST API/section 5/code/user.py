import sqlite3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
    @classmethod   
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() 
        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user
    
    @classmethod   
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() 
        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user
    
class UserRegister(Resource):
    def post(self):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
            
        data = UserRegister.validate_data(['username','password'],'This field cannot be left blank').parse_args()
        
        user_exists_query = "SELECT COUNT(*) FROM users WHERE username = ?"
        user_exists = cursor.execute(user_exists_query, (data['username'],)).fetchall()
                
        if user_exists[0][0] >= 1:
            return {'message': "A user with name '{}' already exists".format(data['username'])}, 400
        
        add_user_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(add_user_query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()
        
        return {'message': "User '{}' created succesfully.".format(data['username'])}, 201
    
    @classmethod
    def validate_data(self, fields, message):
        parser = reqparse.RequestParser()  
        for field in fields:
            parser.add_argument(field, 
                            type=str, 
                            required=True, 
                            help=message
        )
        return parser