"""
Main entry point views.
"""
import flask

from flask import url_for, redirect
from . import app
from .database import db_session
from .models import User


@app.route('/')
def index():
    return redirect(url_for("shift.user_shifts"))


@app.route('/addBob')
def test_db_with_bob():
    u = User("Bobby", "bob@example.com")
    db_session.add(u)
    db_session.commit()
    return flask.render_template('layout.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
