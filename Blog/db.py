import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext


# Checks if the database has been initialised and if not connects to it
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(

            # Refers to the app.py database config
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Closes the database if it is open
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# Gathers the sql data from the schema file and creates tables in the db
def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


# Creates the database
@click.command("init.db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("DATABASE INITIALISED")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
