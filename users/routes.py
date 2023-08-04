
from flask import Blueprint, jsonify, request,session, render_template
from .Utils import is_valid_password, is_valid_username, mongo,allowed_file,is_valid_email,filter_videos_by_user,loggedin_user
import os
import re
import base64
from bson.objectid import ObjectId
routes_bp= Blueprint('routes',__name__)

@routes_bp.route('/register', methods=['POST'])
def save_cred():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        email=request.form.get("email")
        


        validUser = is_valid_username(username, mongo)
        validPass = is_valid_password(password)
        validEmail = is_valid_email(email)

        if validUser:
            raise Exception("INVALID USER")
        if not validPass:
            raise Exception("The password must contain one uppercase letter, one digit, one special character, and have a minimum length of 8 characters.")
        if not validEmail:
            raise Exception("Invalid email")

        data = {"username": username, "password": password,"email":email}
        collection = mongo.db.usersa
        insert = collection.insert_one(data)
        print(insert)#<pymongo.results.InsertOneResult object at 0x0000017484193310>
        print(insert.inserted_id)  # 64c8ca1059b34db238462dea

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
            session["user"]=username
            print(session["user"])

            return jsonify({'success': "Valid Credentials!!!"}), 200
        else:
            raise Exception("INVALID USER Credentials!")
        
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# @routes_bp.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         title = request.form.get('title')
#         description = request.form.get('desc')
#         video_file = request.files['video_file']
        
#         tags = request.form.getlist('tags')

        

#         if video_file and allowed_file(video_file.filename):
#             # Save the uploaded video to the 'uploads' folder
#             # filename = secure_filename(video_file.filename)
#             filename = video_file.filename
            
#             video_data = video_file.read()
#             # print(video_data)

#             # Convert the binary data to base64 encoding
#             video_data_base64 = base64.b64encode(video_data)

#             # Store video information in the database
#             data = {
                
#                 'title': title,
#                 'description': description,
#                 'video_data': video_data_base64.decode('utf-8'),
#                 'filename': filename,
#                 'tags': tags, 
#                 'ratings': [], 
#                 'createdBy':session["user"]
#             }
#             mongo.db.videoss.insert_one(data)

#             return jsonify({'success': "uploaded successfully"}), 200
#     return jsonify({'error': "error"}), 400


@routes_bp.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('desc')
        video_file = request.files.get('video_file')  # Use 'get' to handle missing file gracefully
        
        tags = request.form.getlist('tags')

        if video_file and allowed_file(video_file.filename):
            # Save the uploaded video to the 'uploads' folder
            # filename = secure_filename(video_file.filename)
            filename = video_file.filename
            
            video_data = video_file.read()

            # Convert the binary data to base64 encoding
            video_data_base64 = base64.b64encode(video_data).decode('utf-8')

            # Store video information in the database
            data = {
                'title': title,
                'description': description,
                'video_data': video_data_base64,  # No need to decode, keep it as a string
                'filename': filename,
                'tags': tags, 
                'ratings': [], 
                'createdBy': session["user"]
            }
            mongo.db.videoss.insert_one(data)

            return jsonify({'success': "uploaded successfully"}), 200

    return jsonify({'error': "Bad Request: Missing or invalid 'video_file'"}), 400




@routes_bp.route('/rate', methods=['POST'])
def rate_video():
    try:
        video_id = request.form.get('video_id')
        rating = float(request.form.get('rating'))

        # Update the video's rating in the database
        mongo.db.videoss.update_one(
            {"_id": ObjectId(video_id)},
            {"$push": {"ratings": rating}}
        )

        return jsonify({'success': "Video rated successfully!"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@routes_bp.route('/myvideos', methods=['GET'])
def displayMyVideos():
    # Fetch all videos created by the logged-in user from the database
    videos = filter_videos_by_user(session["user"], mongo)

    allVideos = []
    for video in videos:
        video_id = str(video["_id"])
        del video["_id"]
        # allVideos[video_id] = video
        allVideos.append(video)

    return jsonify(allVideos), 200




# @routes_bp.route('/display', methods=['GET'])
# def display():
#     # Fetch all videos from the database
#     videos = mongo.db.videoss.find({})
#     search_query = request.args.get('search_query')
#     print(search_query)

#     # If search query is provided, filter videos based on tags
#     if search_query:
#         # Use a regular expression to search for tags containing the search query
#         regex = re.compile(re.escape(search_query), re.IGNORECASE)
#         videos = mongo.db.videoss.find({'tags': regex})

#     allVideos = {}
#     for video in videos:
#         video_id = str(video["_id"])
#         del video["_id"]
#         allVideos[video_id] = video

#     return allVideos, 200
# @routes_bp.route('/display', methods=['GET'])
# def display():
#     # Fetch all videos from the database
#     videos = mongo.db.videoss.find({})
#     search_query = request.args.get('search_query')
#     print(search_query)

#     # If search query is provided, filter videos based on tags
#     if search_query:
#         # Use a regular expression to search for tags containing the search query
#         regex = re.compile(re.escape(search_query), re.IGNORECASE)
#         videos = mongo.db.videoss
# .find({'tags': regex})

#     allVideos = []
#     for video in videos:
#         video_data = {
#             'video_url': video['video_data'],  # Replace 'video_url' with the appropriate key for your video URL
#             'title': video['title'],
#             'description': video['description'],
#             'tags': video['tags'],
#             'created_by': video['created_by']
#         }
#         allVideos.append(video_data)

#     return jsonify(allVideos), 200


@routes_bp.route('/display', methods=['GET'])
def display():
    # Fetch all videos from the database
    videos = mongo.db.videoss.find({})
    search_query = request.args.get('search_query')
    print(search_query)

    # If search query is provided, filter videos based on tags
    if search_query:
        # Use a regular expression to search for tags containing the search query
        regex = re.compile(re.escape(search_query), re.IGNORECASE)
        videos = mongo.db.videoss.find({'tags': regex})

    allVideos = []
    for video in videos:
        video_id = str(video["_id"])
        video["_id"] = video_id

        # Calculate the average rating for the video
        ratings = video.get('ratings', [])
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
        else:
            avg_rating = 0.0

        # Add the average rating to the video data
        video['avg_rating'] = avg_rating

        allVideos.append(video)

    return jsonify(allVideos), 200



@routes_bp.route('/logout')
def logout():
    try:
        return loggedin_user()
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# @routes_bp.route('/login', methods=['POST'])
# def get_cred():
#     try:
#         username = request.form["username"]
#         password = request.form["password"]
#         loginCreds = is_valid_username(username, mongo)
#         print(loginCreds)
#         if loginCreds:
#             if username != loginCreds['username'] or password != loginCreds['password']:
#                 raise Exception("INVALID USER Credentials!")
#             session["user"] = username
#             print(session["user"])

#             return jsonify({'success': "Valid Credentials!!!"}), 200
#         else:
#             raise Exception("INVALID USER Credentials!")
            

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


