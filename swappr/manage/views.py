"""
Endpoints for my shifts
"""
from flask import Blueprint, url_for, redirect, render_template
from flask_login import login_required, current_user
from swappr.database import db_session
from swappr.models import Shift
from swappr.user import tanda_api

manage = Blueprint('manage', __name__, url_prefix='/manage')


@manage.route('/')
@login_required
def manage_shifts():
    """
    List the shifts that belong to the user
    """
    if not current_user.is_manager:
        return redirect(url_for('index'))
    shifts = db_session.query(Shift)
    dept_ids = []
    for shift in shifts:
        dept_ids.append(shift.department_id)
    authed_dept_ids = []
    for dept_id in dept_ids:
        managers = tanda_api.get_managers_for_department(dept_id)
        for manager in managers:
            if manager['id'] == current_user.employee_id:
                authed_dept_ids.append(dept_id)
                break
    authed_shifts = db_session.query(Shift).filter(Shift.department_id in authed_dept_ids and not Shift.taken)
    return render_template('manage/manage.html', authed_shifts=authed_shifts)


def respond_to_shift(shift_id, accepted=True):
    if not accepted:
        shift = db_session.query(Shift).filter(Shift.schedule_id == shift_id).one()
        shift.taker = None
    pass
