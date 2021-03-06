"""
Endpoints for my shifts
"""
from flask import Blueprint, render_template, url_for, redirect, session, request
from flask_oauthlib.client import OAuth
from flask_login import login_required, current_user
from swappr import login_manager, app
from swappr.database import db_session
from swappr.models import User
from swappr.user.tanda_api import tanda_auth
from . import tanda_shift
import pprint
from calendar import day_name
from datetime import datetime
from datetime import timedelta

shift = Blueprint('shift', __name__, url_prefix='/shift')


@shift.route('/me')
@login_required
def user_shifts():
    """
    List the shifts that belong to the user
    """
    delta = 0
    if "delta" in request.args:
        delta = int(request.args.get("delta"))
        upcoming_shifts = tanda_shift.fetch_current_user_shifts_for_date(delta)
    else:
        upcoming_shifts = tanda_shift.fetch_current_user_upcoming_shifts()

    return render_template('shift/your_shifts.html', upcoming_shifts=upcoming_shifts, days=day_name,
                           datetime=datetime, delta=delta, timedelta=timedelta)

@shift.route('/offer/<int:id>', methods=['POST'])
@login_required
def offer(id):
    tanda_shift.offer_this_shift(id)
    return "Added shift " + str(id)

@shift.route('/available')
@login_required
def available_shifts():
    """
    List the shifts that are available to be taken
    """
    shifts = tanda_shift.fetch_offered_shifts()
    shifts.extend(tanda_shift.fetch_vacant_shifts())
    return render_template('shift/available_shifts.html', available_shifts=shifts, days=day_name,
                           datetime=datetime, timedelta=timedelta, user=current_user)

@shift.route('accept/<int:id>/<int:user_id>', methods=['POST'])
@login_required
def accept(id, user_id):
    tanda_shift.take_offered_shift(id, user_id)
    return "Shift " + str(id) + " accepted by " + str(user_id)