from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db_test import find_user, create_user, store_refresh_token, verify_refresh_token
import jwt
import datetime
import os

env = os.getenv("ENVIRONMENT")

ACCESS_SECRET = "access_secret"
REFRESH_SECRET = "refresh_secret"


def create_tokens(user):
    access_payload = {
        "id": user[0],
        "username": user[1],
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=15),
    }
    refresh_payload = {
        "id": user[0],
        "username": user[1],
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=7),
    }

    access_token = jwt.encode(access_payload, ACCESS_SECRET, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET, algorithm="HS256")

    return access_token, refresh_token


def lite_register():
    # Get username from body
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    print("username", username, "password", password)

    if not username:
        return jsonify({"error": "No username supplied"}), 400

    if not password:
        return jsonify({"error": "No password supplied"}), 400

    user = find_user(username)
    # Check if user already exits
    if user:
        return jsonify({"error": "Not allowed"}), 400

    password_hash = generate_password_hash(password)

    # Create a user with the hashed pass
    create_user(username, password_hash)

    return "", 204


def lite_login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if not username:
        return jsonify({"error": "No username supplied"}), 400

    if not password:
        return jsonify({"error": "No password supplied"}), 400

    user = find_user(username)

    if not user:
        return jsonify({"error": "Invalid Login"}), 400

    valid_password = check_password_hash(user[2], password)

    if not valid_password:
        return jsonify({"error": "Not valid credentials"}), 400

    # Valid user generate tokens
    access_token, refresh_token = create_tokens(user)

    # Store the refresh token
    store_refresh_token(refresh_token, user[0])

    # Attach refresh to cookie and access as json
    response = make_response({"access": access_token})

    is_production = env == "Production"

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="Strict",
        secure=False if is_production else True,
        max_age=24 * 60 * 60 * 7,
    )

    response.status_code = 200

    return response


def lite_refresh():
    # Get refresh from cookies
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "No refresh token supplied"}), 400

    # Find the token in our db
    user_id = verify_refresh_token(refresh_token)

    if not user_id:
        return jsonify({"error": "Invalid token"}), 400

    try:
        # Verify the token
        user = jwt.decode(refresh_token, REFRESH_SECRET, algorithms="HS256")

        print("user", user, type(user))

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 400

    access_payload = {
        "id": user["id"],
        "username": user["username"],
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=15),
    }

    access_token = jwt.encode(access_payload, ACCESS_SECRET, algorithm="HS256")

    return jsonify({"access": access_token}), 200
