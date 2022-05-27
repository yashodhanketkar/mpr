import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db():
    if g.db:
        g.db.close()


def init_db():
    db = get_db()
    with open(file="app/schema.sql", mode="r", encoding="utf-8") as schema_file:
        db.executescript(schema_file.read())
    close_db()
