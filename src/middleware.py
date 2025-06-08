from flask import request, jsonify
import jwt
from auth import ACCESS_SECRET

def authenticate_token_middleware(f):
  def wrapper(*args, **kwargs):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer"):
      return jsonify({"error": "Unauthorized"}), 401
    
    token = auth_header.split(" ")[1]

    try:
      payload = jwt.decode(token, ACCESS_SECRET,  algorithms=["HS256"])
      request.user = payload

    except jwt.ExpiredSignatureError:
      return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
      return jsonify({"error": "Invalid Token"}), 401
    
    return f(*args, **kwargs)
  
  wrapper.__name__ = f.__name__
  return wrapper