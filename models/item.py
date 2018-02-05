import sqlite3
from db import db
from flask_restful import reqparse


class ItemModel(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        var = cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name = name
        return var

    @classmethod
    def validate_data(cls, fields, message):
        parser = reqparse.RequestParser()
        for field in fields:
            parser.add_argument(field,
                            type=str,
                            required=True,
                            help=message
        )
        return parser
