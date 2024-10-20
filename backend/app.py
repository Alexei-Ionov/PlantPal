import os
from flask import Flask, session
from flask_cors import CORS
from backend.database.db import init_connection_pool
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
session_key = os.getenv('FLASK_SESSION_KEY')
app = Flask(__name__)
app.secret_key = session_key
#CORS(app)  # Enable CORS for all routes
# CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "GET", "OPTIONS"]}})
CORS(app, supports_credentials=True)  # Allow credentials to be included
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # This requires HTTPS

from backend.routes import *

if __name__ == "__main__":
    init_connection_pool()
    app.run(debug=True)
