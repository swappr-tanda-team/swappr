"""
Endpoints for my shifts
"""
from flask import Blueprint, url_for, redirect, render_template
from flask_login import login_required, current_user
from swappr.database import db_session
from swappr.models import Shift
from swappr.user import tanda_api
from swappr.shift import tanda_shift

manage = Blueprint('manage', __name__, url_prefix='/manage')


@manage.route('/')
@login_required
def manage_shifts():
    """
    List the shifts that belong to the user
    """
    # if not current_user.is_manager:
    #     return redirect(url_for('index'))
    # shifts = db_session.query(Shift)
    # dept_ids = []
    # for shift in shifts:
    #     dept_ids.append(shift.department_id)
    # authed_dept_ids = []
    # for dept_id in dept_ids:
    #     print(dept_id)
    #     managers = tanda_api.get_managers_for_department(dept_id)
    #     print(managers)
    #     for manager in managers:
    #         print(manager)
    #         print(current_user.employee_id)
    #         if manager['id'] == current_user.employee_id:
    #             authed_dept_ids.append(dept_id)
    #             break
    authed_shifts = [s for s in db_session.query(Shift).filter(Shift.taker is not None)]
    return render_template('manage/manage.html', authed_shifts=authed_shifts, respond_method=respond_to_shift)


@manage.route('/<shift_id>/<accepted>', methods=['POST'])
@login_required
def respond_to_shift(shift_id, accepted=True):
    shift = db_session.query(Shift).filter(Shift.schedule_id == shift_id).one()
    if shift is None:
        return
    if not accepted:
        shift.taker = None
        db_session.commit()
        return
    tanda_shift.replace_user_in_schedule(shift.employee_id, shift_id)
    db_session.delete(shift)
    db_session.commit()
