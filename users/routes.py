
from flask import Blueprint, jsonify, request
from .Utils import is_valid_password, is_valid_username, mongo

routes_bp= Blueprint('routes',__name__)

@routes_bp.route('/register', methods=['POST'])
def save_cred():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        validUser = is_valid_username(username, mongo)
        validPass = is_valid_password(password)

        if validUser:
            raise Exception("INVALID USERNAME")
        if not validPass:
            raise Exception("The password must contain one uppercase letter, one digit, one special character, and have a minimum length of 8 characters.")

        data = {"username": username, "password": password}
        collection = mongo.db.usersa
        insert = collection.insert_one(data)
        print(insert.inserted_id)  # Printing the inserted document ID (Optional)

        return jsonify({'success': "Data inserted successfully!"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@routes_bp.route('/login', methods=['GET'])
def get_cred():
    try:
        username = request.args["username"]
        password = request.args["password"]
        loginCreds = is_valid_username(username, mongo)
        print(loginCreds)
        if(loginCreds):
            if(username != loginCreds['username'] or password != loginCreds['password']):
                raise Exception("INVALID USER Credentials!")
            return jsonify({'success': "Valid Credentials!!!"}), 200
        else:
            raise Exception("INVALID USER Credentials!")
    except Exception as e:
        return jsonify({'error': str(e)}), 400
