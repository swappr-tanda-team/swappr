"""
Views for the User model.
"""
from flask import Blueprint, render_template, url_for, redirect, session
from flask_login import login_required, login_user, logout_user
from swappr import login_manager, app
from swappr.database import db_session
from swappr.models import User
from . import tanda_api

user = Blueprint('user', __name__, url_prefix='/user')
auth = tanda_api.tanda_auth


@login_manager.user_loader
def user_loader(user_id):
    return db_session.query(User).filter(User.id == user_id).one()


@user.route('/')
@user.route('/account')
@login_required
def account():
    """
    View list of submissions for a given user and their total points
    """
    tanda_api.get_users()
    return render_template('user/account.html')


@user.route('/delete')
@login_required
def delete():
    """
    Admin only page to delete a user (for example troll account). Option to also delete all the users submissions or to
    keep them but prevent them from submitting further solutions.
    """
    return render_template('layout.html')


@user.route('/login')
def login():
    """
    Redirects to tanda oauth which redirects to /authorize
    """
    if app.testing:
        callback_url = url_for('user.authorize', _external=True)
    else:
        callback_url = 'TODO: put in the URL'
    return auth.authorize(callback=callback_url)

@user.route("/logout")
@login_required
def logout():
    """
    Logs out a user
    :return:
    """
    logout_user()
    return redirect(url_for('index'))


@user.route('/authorize')
def authorize():
    """
    Use information from tanda oauth log in to either create a new user or log in as an existing user.
    """
    resp = auth.authorized_response()
    if resp is None:
        return redirect(url_for('index'))
    session['tanda_oauth'] = resp
    user_info = auth.get('users/me', token=(resp["access_token"],)).data
    u = db_session.query(User).filter(User.employee_id == user_info['id']).first()
    if not u:
        u = User(user_info['name'], user_info['id'])
        db_session.add(u)
        db_session.commit()
    login_user(u, remember=True)
    return redirect(url_for('index'))

