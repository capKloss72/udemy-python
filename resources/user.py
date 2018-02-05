import sqlite3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from models.user import UserModel


class UserRegister(Resource):
    @property
    def post(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        data = UserRegister.validate_data(['username','password'],'This field cannot be left blank').parse_args()

        user_exists_query = "SELECT COUNT(*) FROM users WHERE username = ?"
        cursor.execute(user_exists_query, (data['username'],)).fetchall()

        if UserModel.find_by_username(data['username']):
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
