"""db.py

Creates database for the system. Also works as connection for said
database.
"""


import sqlite3

from flask import current_app, g


def get_db():
    """Gets the database connection from flask application

    returns:
        g.db (database): The database connection from context
    """
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db():
    """Closes the database connection"""
    if g.db:
        g.db.close()


def init_db():
    """Initiate the database for flask application"""
    db = get_db()
    with open(file="app/schema.sql", mode="r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())
    close_db()
