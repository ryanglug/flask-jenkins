import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(override=True)


conn = psycopg2.connect(
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    dbname=os.getenv("DATABASE_NAME"),
)
cursor = conn.cursor()


with open("schema.sql", "r") as file:
    schema = file.read()
    statements = schema.split(";")
    for statement in statements:
        if statement.strip():
            cursor.execute(statement)


conn.commit()
cursor.close()
conn.close()
