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
import pprint

shift = Blueprint('shift', __name__, url_prefix='/shift')


@shift.route('/me')
@login_required
def user_shifts():
    """
    List the shifts that belong to the user
    """
    shift_info = tanda_auth.get('rosters/current', token=(session["tanda_oauth"]["access_token"],)).data
    valid_shifts = []
    for i in range(len(shift_info["schedules"])):
    	#at this point, we examining all the schedules for a particular day
    	for j in range(len(shift_info["schedules"][i]["schedules"])):
    		sched_item = shift_info["schedules"][i]["schedules"][j]
    		if (sched_item["user_id"] == current_user.employee_id):
    			sched_item["date"] = shift_info["schedules"][i]["date"]
    			valid_shifts.append(sched_item)
    print(valid_shifts)
    return render_template('user/account.html')