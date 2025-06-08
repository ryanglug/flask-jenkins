import psycopg2
from flask import g
import os

import psycopg2.extras


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            dbname=os.getenv("DATABASE_NAME"),
        )
    return g.db


def close_db():
    db = g.pop("test_db", None)
    if db is not None:
        db.close()


def find_user(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user


def create_user(username, hashedPassword):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *",
        (username, hashedPassword),
    )
    user = cursor.fetchone()
    db.commit()
    cursor.close()
    return user


def store_refresh_token(token, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO refresh_tokens (token, user_id) VALUES (%s, %s)", (token, user_id)
    )
    db.commit()
    cursor.close()


def verify_refresh_token(refresh_token):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT user_id FROM refresh_tokens WHERE token = %s", (refresh_token,)
    )
    token = cursor.fetchone()
    cursor.close()
    return token


def create_comment(content, user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO comments (content, user_id) VALUES (%s, %s) RETURNING *",
        (content, user_id),
    )
    comment = cursor.fetchone()
    db.commit()
    cursor.close()
    return comment


def get_comments(user_id):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM comments WHERE user_id = %s", (user_id,))
    comments = cursor.fetchall()

    cursor.close()
    return comments
