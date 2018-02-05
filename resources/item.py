from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT
from flask_jwt import jwt_required
from security import authenticate, identity
from resources.user import UserRegister
from models.item import ItemModel
import sqlite3


class Item(Resource):

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1],
                            'price': row[2]}}
        return {'message': "'{}'item not found".format(name)}

    def post(self, name):
        data = ItemModel.validate_data(['price'],'This field cannot be left blank').parse_args()

        if ItemModel.find_by_name(name) != True:
            return {'message': "'{}' does not exists".format(name)}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (data['price'], name))
        connection.commit()
        if connection.total_changes > 0:
            connection.close()
            return {'message': "'{}' was added with a price of {}".format(name,data['price'])}, 201
        return {'message': "'{}' was not added".format(name)}, 400

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        if connection.total_changes > 0:
            connection.close()
            return {'message': "'{}' item deleted".format(name)}
        return {'message': "'{}' item was not deleted".format(name)}

    def put(self, name):
        data = ItemModel.validate_data(['price'],'This field cannot be left blank').parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(NULL, ?, ?)"
        cursor.execute(query, (name, data['price']))
        connection.commit()
        if connection.total_changes > 0:
            connection.close()
            return {'message': "'{}' was updated by {}".format(name,data['price'])}, 201
        return {'message': "'{}' was not updated".format(name)}, 400


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[1],
                         'price':row[2]})

        connection.close()

        return items
