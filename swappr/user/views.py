"""
Views for the User model.
"""
from flask_oauthlib.client import OAuthException
from flask import Blueprint, render_template, url_for, redirect, session, request
from flask_login import login_required, login_user, logout_user
from swappr import login_manager, app
from swappr.database import db_session
from swappr.models import User
from . import tanda_api
import os

user = Blueprint('user', __name__, url_prefix='/user')
auth = tanda_api.tanda_auth


@login_manager.user_loader
def user_loader(user_id):
    try:
        return db_session.query(User).filter(User.id == user_id).one()
    except:
        session.clear()

@user.route('/')
def index():
    return redirect(url_for('user.login'))


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
    callback_url = url_for('user.authorize', _external=True)
    if ('REDIRECT_URI' in os.environ):
        callback_url=os.environ['REDIRECT_URI']
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
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message
    session['oauth_token'] = (resp['access_token'], '')
    user_info = auth.get('users/me').data
    u = db_session.query(User).filter(User.employee_id == user_info['id']).first()
    if not u:
        real_user_info = auth.get('users/' + str(user_info["id"]), token=(resp["access_token"],)).data
        u = User(user_info['name'], user_info['id'], user_info["utc_offset"], user_info["time_zone"])
        manager_levels = ["organisation_admin", "payroll_officer", "roster_manager"]
        is_manager = False
        if ("user_levels" in real_user_info):        
            for i in range(len(real_user_info["user_levels"])):
                if (real_user_info["user_levels"][i] in manager_levels):
                    is_manager = True
                    break
        u.is_manager = is_manager
        db_session.add(u)
        db_session.commit()
    login_user(u, remember=True)
    return redirect(url_for('index'))

