from backend.app import app
from flask import Flask, request, jsonify, redirect, url_for, session
from backend.models.user_model import *
from functools import wraps
from backend.Exceptions import *
from backend.services.user_services import *
import bcrypt
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
# @app.before_request
# def require_login():
#     protected_routes = ['/profile', '/add_plant', 'my_plants']
#     print(session)
#     if request.path in protected_routes and "user_id" not in session:
#         return redirect(url_for('login', next=request.url))

"""
UNAUTHENTICATED ROUTES
"""
@app.route('/signup', methods=['POST'])
def signup():
    try: 
        user_info = request.json
        username, password1, password2, email = user_info["username"], user_info["password1"], user_info["password2"], user_info["email"]
        if not username or not password1 or not password2 or not email:
            raise InvalidInputError("Missing fields - Please enter a valid username, password, and email")
        
        if password1 != password2:
            raise InvalidInputError("Passwords don't match")
        
        if not is_valid_email(email):
            raise InvalidInputError("Enter a valid email")
        password_bytes = password1.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8') 
        response = create_user(username, hashed_password, email)
        return jsonify(response), 201
        
        

    except KeyError as e:
        print(e)
        return jsonify({
            "error": {
                "code": 400, 
                "message": str(e)
            }
        }), 400
    except InvalidInputError as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500
    
def check_password(plain_text_password, hashed_password) -> bool:
    # Convert the plain text password to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Verify the password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    
@app.route('/login', methods=['POST'])
def login():
    try: 
        user_info = request.json
        email, password = user_info["email"], user_info["password"]
        if not email or not password:
            raise InvalidInputError("Missing email or password")
        result = login_user(email, password)
        if not result:
            raise Exception("No user exists")

        username, user_id, hashed_password = result
        if not check_password(password, hashed_password):
            raise InvalidPassword("Invalid password")

        session["user_id"] = user_id
        session["user_email"] = email
        return jsonify({"username": username, "email": email})
    except InvalidPassword as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401

    except Exception as e:
        print(e)
        print("ERROR IN LOGIN")

        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

"""
AUTHENTICATED ROUTES 
"""
@app.route('/add_plant', methods=["POST"])
def add_user_plant():
    try: 
        user_id = session["user_id"]
        req_info = request.json

        if "plant" not in req_info:
            raise InvalidInputError("Missing plant name for adding user plant")

        plant, nickname = req_info["plant"], req_info["nickname"] #nickname can be empty!
        token = add_plant_service(plant, nickname, user_id)
        return jsonify({"message": "Successfully added plant!", "token": token}), 201
        
    except InvalidInputError:
        return jsonify({
            "error": {
                "code": 401,
                "message": "Missing plant name"
            }
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500



@app.route('/my_plants', methods=['GET'])
def get_user_plants():
    try: 
        
        user_id = session["user_id"]
        result = get_plants(user_id) #result is a list of dictionaries that represent the current status of all the user's plants
        return jsonify(result)

    except InvalidInputError as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401

    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

@app.route('/my_tokens', methods=["GET"])
def get_user_tokens():
    try: 
        user_id = session["user_id"]
        tokens = get_tokens(user_id)
        return jsonify(tokens)

    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

@app.route('/fetch_trie', methods=["GET"])
def get_trie():
    try:
        with open('/Users/alexeiionov/Desktop/projects/PlantPal/backend/data_scrape/trie.json', 'r') as json_file:
            trie = json.load(json_file)
            return jsonify(trie), 201
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

@app.route('/add_calendar', methods=["POST"])
def add_event_to_calendar():
    try: 
        plant_info = request.json
        user_id = session["user_id"]
        user_email = session["user_email"]
        if "plant" not in plant_info or "nickname" not in plant_info:
            raise InvalidInputError("Missing fields in request")
        add_event_service(user_id, user_email, plant_info["plant"], plant_info["nickname"])
        return jsonify({"message": "successfully added water schedule to google calendar"}), 201
    except InvalidInputError as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401

        
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500
@app.route('/schedule_calendar', methods=["POST"])
def schedule_calendar():
    user_id = session["user_id"]
    user_email = session["user_email"]
    try:
        plant_info = request.json
        if "plant_nickname" not in plant_info:
            raise InvalidInputError("Missing plant nickname in post request")
        if "plant" not in plant_info:
            raise InvalidInputError("Missing plant common name in post request")
        
        plant_nickname = plant_info["plant_nickname"]
        plant = plant_info["plant"]
        add_event_service(user_id, user_email, plant, plant_nickname)
        return jsonify({
            "message": "Successfully added event to calendar"
        }), 201
    except InvalidInputError as e:
        print(e)
        return jsonify({
            "error": {
                "code": 401, 
                "message": str(e)
            }
        }), 401
    except Exception as e:
        print(e)
        return jsonify({
            "error": {
                "code": 500, 
                "message": str(e)
            }
        }), 500

