import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def populate_test_data():
    db = get_db()

    with current_app.open_resource('test_data.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_test_data_command)
    app.cli.add_command(add_user_command)


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('populate-db')
@with_appcontext
def populate_test_data_command():
    """Populate database with example entries."""
    populate_test_data()
    click.echo('Database populated.')


def add_user(username, password):
    db = get_db()
    if db.execute(
        'SELECT id FROM user where username = ?', (username,)
    ).fetchone() is not None:
        print("Error: User {0} already exists.".format(username))
        return

    db.execute(
        'INSERT INTO user (username, password) values (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()


@click.command('add-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def add_user_command(username, password):
    """Add user to user database."""
    add_user(username, password)
    click.echo('Added user {0}.'.format(username))
