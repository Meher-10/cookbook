import re
from pymongo import MongoClient

mongo = MongoClient('mongodb+srv://meherarchana2004:Meher$5061@cluster0.7rzumah.mongodb.net/')

def is_valid_password(password):
    # Check the length of the password
    if len(password) < 8:
        return False

    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # Check if the password contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # Check if the password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # Check if the password contains at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

def is_valid_username(username, mongo):
    collection = mongo.db.usersa
    data = {"username": username}
    search = collection.find_one(data)
    return search

