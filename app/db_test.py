import sqlite3
from flask import current_app, g


def get_db():
    print("getting db")
    if "test_db" not in g:
        g.test_db = sqlite3.connect(current_app.config["DATABASE"])
        g.test_db.row_factory = sqlite3.Row
    return g.test_db


def close_db():
    db = g.pop("test_db", None)
    if db is not None:
        db.close()


def find_user(username):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cur.fetchone()


def create_user(username, hashedPassword):
    db = get_db()
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashedPassword),
    )
    db.commit()


def store_refresh_token(token, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO refresh_tokens (token, user_id) VALUES (?, ?)", (token, user_id)
    )
    db.commit()


def verify_refresh_token(refresh_token):
    db = get_db()
    cur = db.execute(
        "SELECT user_id FROM refresh_tokens WHERE token = ?", (refresh_token,)
    )
    return cur.fetchone()


def create_comment(content, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO comments (content, user_id) VALUES (?, ?)", (content, user_id)
    )
    db.commit()


def get_comments(user_id):
    db = get_db()
    curs = db.execute("SELECT * FROM comments WHERE user_id = ?", (user_id,))
    rows = curs.fetchall()

    comments = [dict(row) for row in rows]

    return comments
