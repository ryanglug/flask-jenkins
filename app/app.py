from flask import Flask, Blueprint
from auth import register, login, refresh
from api import post_comment, get_user, comments
from db import close_db
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:1234",
        "http://localhost:2000",
        "http://20.90.166.46",
        "https://20.90.166.46",
    ],
)


@app.teardown_appcontext
def teardown_db(exception):
    close_db()


api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.post("/register")(register)
api_bp.post("/login")(login)
api_bp.get("/refresh")(refresh)
api_bp.get("/user")(get_user)
api_bp.get("/comment")(comments)
api_bp.post("/comment")(post_comment)

app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
