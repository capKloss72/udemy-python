import sqlite3
from flask_restful import Resource, Api, reqparse

class ItemModel(object):

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return True if row else False

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
