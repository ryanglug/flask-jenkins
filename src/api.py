from middleware import authenticate_token_middleware
from flask import request, jsonify
from db import create_comment, get_comments


@authenticate_token_middleware
def post_comment():
    # Get data
    data = request.get_json()
    content = data["content"]

    if not content:
        return jsonify({"error": "Missing comment content"}), 400
    # Extract user from request
    user = request.user

    # Create the comment
    create_comment(content, user["id"])

    return jsonify({"message": "Created comment successfully"}), 200


@authenticate_token_middleware
def get_user():
    user = request.user

    return jsonify({"user": user}), 200


@authenticate_token_middleware
def comments():
    user = request.user

    comments = get_comments(user["id"])

    return jsonify({"comments": comments}), 200
