import re
from flask import Blueprint, jsonify, request,session, render_template
from pymongo import MongoClient

mongo = MongoClient('mongodb+srv://meherarchana2004:Meher$5061@cluster0.7rzumah.mongodb.net/')

def is_valid_password(password):
    
    if len(password) < 8:
        return False

    
    if not any(char.isupper() for char in password):
        return False

    
    if not any(char.islower() for char in password):
        return False

    
    if not any(char.isdigit() for char in password):
        return False

    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

def is_valid_username(username, mongo):
    collection = mongo.db.usersa
    data = {"username": username}
    search = collection.find_one(data)
    print(search)#none
    return search
    


def allowed_file(filename):
    # Add more file extensions if you want to support other video formats
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4'}
#check this
def is_valid_email(email):
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# def filter_videos_by_user(currentuser,mongo):
#     collection = mongo.db.videos
#     data = {"createdBy": currentuser}
#     search = collection.find_one(data)
#     return list(search)
def filter_videos_by_user(currentuser, mongo):
    collection = mongo.db.videoss
    data = {"createdBy": currentuser}
    search = collection.find(data)  # This will return a cursor for all matching documents
    return list(search)  # Convert the cursor to a list of documents

def loggedin_user():
    # Check if the user is logged in
    if "user" in session:
        # Remove the user from the session
        session.pop("user", None)
        return render_template("logIn.html")
    else:
        return jsonify({'error': "User not logged in"}), 401


