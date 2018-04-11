#!/usr/bin/python3

"""
    The upper level interface.

    This interface sends requests to the manager.

    For deployment structure should be:

    uranus/
        config.ini  # Config file
        uranus.wsgi  # WSGI file for apache2
        logs/
        uranus/
            static/
            templates/
            __init__.py

    ALL Parameters description available on the README.md file!
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    from uranus.units import units
    from uranus.units import manager as man
    from uranus.units import codes
except ImportError:
    from units import units
    from units import manager as man
    from units import codes

app = Flask(__name__)
CORS(app)  # Cross-origin resource sharing


@app.route('/')
def index():
    return jsonify({"guest": "Read docs. Unable to access without token"})


@app.route('/<token>/login')
def login(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    email = request.args.get("email")
    password = request.args.get('password')

    response = man.login_user(email, password)

    if response["ok"]:
        return jsonify(response)

    return jsonify(codes.wrong_login_data)


@app.route('/<token>/getUser')
def get_user(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    user_id = request.args.get("id")

    response = man.fetch_user(user_id)

    if response["ok"]:
        return jsonify(response)

    return jsonify(codes.wrong_user_id)


@app.route('/<token>/getUsers')
def get_users(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    debtors = units.boolean(request.args.get("debtors"))
    count = units.int_converter(request.args.get("count"))
    offset = units.int_converter(request.args.get("offset"))

    if debtors:
        response = man.fetch_debtors(count, offset)
    else:
        response = man.fetch_users(count, offset)

    if response["ok"]:
        return jsonify(response)

    return jsonify(codes.unknown_error)


@app.route('/<token>/getGenres')
def get_genres(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    count = units.int_converter(request.args.get("count"))
    offset = units.int_converter(request.args.get("offset"))

    response = man.get_genres(count, offset)

    if response["ok"]:
        return jsonify(response)

    return jsonify(codes.unknown_error)


@app.route('/<token>/getDocument')
def get_document(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = units.int_converter(request.args.get("id"))

    response = man.fetch_document(doc_id)

    if response["ok"]:
        return jsonify(response)

    return jsonify(codes.document_not_exist)


@app.route('/<token>/getDocuments')
def get_documents(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    user_id = units.int_converter(request.args.get("id"))
    for_user = units.int_converter(request.args.get("for_user"))
    count = units.int_converter(request.args.get("count"))
    offset = units.int_converter(request.args.get("offset"))
    genre = request.args.get("genre")

    if user_id:
        response = man.fetch_user_taken_books(user_id)
    elif for_user:
        response = man.fetch_documents_for_user(for_user)
    elif genre:
        response = man.fetch_documents_by_genre(genre)
    else:
        response = man.fetch_documents(count, offset)

    if response["ok"]:
        return jsonify(response)
    else:
        return jsonify(codes.unknown_error)


@app.route('/<token>/bookDocument')
def book_document(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = units.int_converter(request.args.get("doc_id"))
    user_id = units.int_converter(request.args.get("user_id"))

    response = man.book_document(doc_id, user_id)

    return jsonify(response)


@app.route('/<token>/renewDocument')
def renew_document(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = units.int_converter(request.args.get("doc_id"))
    user_id = units.int_converter(request.args.get("user_id"))

    response = man.renew_document(doc_id, user_id)

    return jsonify(response)


@app.route('/<token>/returnDocument')
def return_document(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = request.args.get("doc_id")
    user_id = request.args.get("user_id")

    response = man.return_document(doc_id, user_id)

    return jsonify(response)


@app.route('/<token>/createDocument')
def create_document(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_type = units.int_converter_with_def_0(request.args.get("type"))
    title = request.args.get("title")
    description = request.args.get("description")
    year = units.int_converter(request.args.get("year"))
    price = units.int_converter(request.args.get("price"))
    copies = units.int_converter_with_def_0(request.args.get("copies"))
    authors = request.args.get("authors")
    bestseller = units.boolean(request.args.get("bestseller"))
    reference = units.boolean(request.args.get("reference"))
    publisher = request.args.get("publisher")
    genre = request.args.get("genre")
    isbn = request.args.get("isbn")
    image = request.args.get("image")

    if title is None or authors is None or doc_type is None:
        return jsonify(codes.insufficient_data_to_create_document)

    response = man.create_document(doc_type, title, description, year, price, copies, authors,
                                   bestseller, reference, publisher, genre, isbn, image)

    if response["ok"]:
        return jsonify(response)
    elif response["code"] == 425:
        return jsonify(codes.document_already_exist)
    elif response["code"] == 426:
        return jsonify(codes.invalid_document_data)
    elif response["code"] == 429:
        return jsonify(codes.insufficient_data_to_create_document)

    return jsonify(codes.unknown_error)


@app.route('/<token>/createUser')
def create_user(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    email = request.args.get("email")
    password_hash = request.args.get("password")
    name = request.args.get("name")
    u_type = units.int_converter_with_def_0(request.args.get("type"))
    phone = request.args.get("phone")
    address = request.args.get("address")
    user_image = request.args.get("user_image")

    response = man.create_user(email, password_hash, name, u_type, phone, address, user_image)

    if response["ok"]:
        return jsonify(response)
    elif response["code"] == 427:
        return jsonify(codes.user_already_exist)
    elif response["code"] == 428:
        return jsonify(codes.invalid_user_data)

    return jsonify(codes.unknown_error)


@app.route('/<token>/changeDocumentData')
def change_document_data(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = units.int_converter(request.args.get("id"))

    doc_type = units.int_converter(request.args.get("type"))
    title = request.args.get("title")
    description = request.args.get("description")
    year = units.int_converter(request.args.get("year"))
    price = units.int_converter(request.args.get("price"))
    copies = units.int_converter(request.args.get("copies"))
    authors = request.args.get("authors")
    bestseller = units.boolean(request.args.get("bestseller"))
    reference = units.boolean(request.args.get("reference"))
    publisher = request.args.get("publisher")
    genre = request.args.get("genre")
    isbn = request.args.get("isbn")
    image = request.args.get("image")

    response = man.update_document(doc_id, doc_type, title, description, year, price, copies, authors, bestseller,
                                   reference, publisher, genre, isbn, image)

    return jsonify(response)


@app.route('/<token>/changeUserData')
def change_user_data(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    user_id = request.args.get("id")
    email = request.args.get("email")
    password_hash = request.args.get("passwd_hash")
    name = request.args.get("name")
    u_type = units.int_converter(request.args.get("type"))
    phone = request.args.get("phone")
    address = request.args.get("address")
    user_image = request.args.get("user_image")

    response = man.update_user(user_id, email, password_hash, name,
                               u_type, phone, address, user_image)

    return jsonify(response)


@app.route('/<token>/deleteDocument')
def delete_document(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = units.int_converter(request.args.get("id"))

    response = man.delete_document(doc_id)

    return jsonify(response)


@app.route('/<token>/deleteUser')
def delete_user(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    user_id = units.int_converter(request.args.get("id"))

    response = man.delete_user(user_id)

    return jsonify(response)


@app.route('/<token>/getBriefUserInfo')
def get_brief_user_info(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    user_id = units.int_converter(request.args.get("id"))

    response = man.get_brief_user_info(user_id)

    return jsonify(response)


@app.route('/<token>/search')
def search(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    query = request.args.get("q")
    user_id = units.int_converter(request.args.get("id"))

    response = man.search(query, user_id)

    return jsonify(response)


@app.route('/<token>/outstandingDocRequest')
def outstanding_doc_request(token):
    if not man.check_token(token):
        return jsonify(codes.wrong_token)

    doc_id = units.int_converter(request.args.get("id"))

    response = man.outstanding_request(doc_id)

    return jsonify(response)


if __name__ == '__main__':
    app.run()
