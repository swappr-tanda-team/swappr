"""
Endpoints for my shifts
"""
from flask import Blueprint, render_template, url_for, redirect, session
from flask_oauthlib.client import OAuth
from flask_login import login_required, current_user
from swappr import login_manager, app
from swappr.database import db_session
from swappr.models import User
from swappr.user.tanda_api import tanda_auth
from . import tanda_shift
import pprint
from calendar import day_name

shift = Blueprint('shift', __name__, url_prefix='/shift')


@shift.route('/me')
@login_required
def user_shifts():
    """
    List the shifts that belong to the user
    """
    upcoming_shifts = tanda_shift.fetch_current_user_upcoming_shifts()
    return render_template('shift/your_shifts.html', upcoming_shifts=upcoming_shifts, days=day_name)