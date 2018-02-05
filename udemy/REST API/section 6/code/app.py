from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'tym'
api = Api(app)

jwt = JWT(app, authenticate, identity) # new endpoint /auth

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1/itemt/<item name>
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5001)
