from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.booksDatabase
users = db["Users"]


class Register(Resource):
    def post(self):
        # Step 1 is to get posted data by the user
        posted_data = request.get_json()

        # Get the data
        username = posted_data["username"]
        password = posted_data["password"]  # "123xyz"

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Store username and pw into the database
        users.insert({
            "username": username,
            "password": hashed_pw,
            "book": "",
            "tokens": 6
        })

        return_json = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(return_json)


def verify_password(username, password):
    hashed_pw = users.find({
        "username": username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({
        "username": username
    })[0]["tokens"]
    return tokens


class Store(Resource):
    def post(self):
        # Step 1 get the posted data
        posted_data = request.get_json()

        # Step 2 is to read the data
        username = posted_data["username"]
        password = posted_data["password"]
        book = posted_data["book"]

        # Step 3 verify the username pw match
        correct_pw = verify_password(username, password)

        if not correct_pw:
            return_json = {
                "status": 302,
                "message": "Username/password incorrect"
            }
            return jsonify(return_json)
        # Step 4 Verify user has enough tokens
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            return_json = {
                "status": 301,
                "message": "Out of tokens"
            }
            return jsonify(return_json)

        # Step 5 store the book, take one token away  and return 200OK
        users.update({
            "username": username
        }, {
            "$set": {
                "book": book,
                "tokens": num_tokens - 1
            }
        })

        return_json = {
            "status": 200,
            "msg": "Book saved successfully"
        }
        return jsonify(return_json)


class Get(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]

        # Step 3 verify the username pw match
        correct_pw = verify_password(username, password)
        if not correct_pw:
            return_json = {
                "status": 302,
                "message": "Username/password incorrect"
            }
            return jsonify(return_json)

        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            return_json = {
                "status": 301,
                "message": "Out of tokens"
            }
            return jsonify(return_json)

        # MAKE THE USER PAY!
        users.update({
            "username": username
        }, {
            "$set": {
                "tokens": num_tokens - 1
            }
        })

        book = users.find({
            "username": username
        })[0]["book"]
        return_json = {
            "status": 200,
            "book": str(book)
        }

        return jsonify(return_json)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
