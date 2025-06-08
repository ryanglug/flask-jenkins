from flask import Flask, Blueprint
from auth import register, login, refresh
from auth_test import lite_register, lite_login, lite_refresh
from api import post_comment, get_user, comments
from api_test import lite_comments, lite_get_user, lite_post_comment
from db_test import close_db
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


if app.config["TESTING"]:
    api_bp.post("/register")(lite_register)
    api_bp.post("/login")(lite_login)
    api_bp.get("/refresh")(lite_refresh)
    api_bp.get("/user")(lite_get_user)
    api_bp.get("/comment")(lite_comments)
    api_bp.post("/comment")(lite_post_comment)

else:
    api_bp.post("/register")(register)
    api_bp.post("/login")(login)
    api_bp.get("/refresh")(refresh)
    api_bp.get("/user")(get_user)
    api_bp.get("/comment")(comments)
    api_bp.post("/comment")(post_comment)

app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
