import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import request, g, redirect
import jwt
from functools import wraps
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get secret from environment variables with fallback
SECRET = os.getenv('SECRET_KEY')

# Create a false hash for the password to prevent timing attacks
false_hash = pbkdf2_sha256.hash("")


def get_user_with_credentials(email, password):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT email, name, password FROM users where email=?''',
                    (email,))
        row = cur.fetchone()
        # If the user does not exist, the password is checked against a false hash
        # to prevent timing attacks.
        if row is None:
            pbkdf2_sha256.verify(password, false_hash)
            return None
        email, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()


def logged_in():
    token = request.cookies.get('auth_token')
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        g.user = data['sub']
        return True
    except jwt.InvalidTokenError:
        return False


def create_token(email):
    now = datetime.utcnow()
    payload = {'sub': email, 'iat': now, 'exp': now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not logged_in():
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
