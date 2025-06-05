from flask import Flask
from auth import register, login, refresh
from api import post_comment, get_user, comments
from db import close_db
from flask_cors import CORS

app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.teardown_appcontext
def teardown_db(exception):
    close_db()


app.config["DATABASE"] = "auth.db"

app.post("/register")(register)
app.post("/login")(login)
app.get("/refresh")(refresh)
app.get("/user")(get_user)
app.get("/comment")(comments)
app.post("/comment")(post_comment)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
