from middleware import authenticate_token_middleware
from flask import request, jsonify
from db import create_comment

@authenticate_token_middleware
def post_comment():
  # Get data
  data = request.get_json()
  content = data["content"]
  # Extract user from request
  user = request.user

  print("user", user)

  #Create the comment
  create_comment(content, user["id"])

  return jsonify({"message": "Created comment successfully"}), 200