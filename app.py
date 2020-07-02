import json

import datetime
# import jwt
from flask import jsonify, request, Response

from BookModel import *

# app.config['SECRET_KEY'] = 'corona'


# @app.route('/login')
# def get_token():
#     expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
#     token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
#     return token


# GET all
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


# GET By Isbn
@app.route("/books/<int:isbn>")
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


def validBookObject(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


# POST
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book Object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':0.00,'isbn':1234567890}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json');
        return response


def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


# PUT by isbn
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Valid book Object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':0.00,'isbn':1234567890}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", status=204)
    return response


def valid_patch_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


# PATCH by isbn
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if not valid_patch_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book Object passed in request",
            "helpString": "Data passed in similar to this {'name':'bookname','price':0.00,'isbn':1234567890}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
    updated_book = {}
    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])

    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(json)
    return response


# DELETE by isbn
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204)
        return response

    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response


app.run(port=5000)
