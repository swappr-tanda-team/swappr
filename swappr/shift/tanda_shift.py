"""
Methods for interacting with Tanda shifts
"""
from flask import session
from flask_login import current_user
from swappr.user.tanda_api import tanda_auth
from swappr.database import db_session
from swappr.models import Shift
import swappr.god_request
import json
import datetime

#Might be benificial to cache roster?

def fetch_current_user_upcoming_shifts():
    shift_info = tanda_auth.get('rosters/current').data
    valid_shifts = []
    if not shift_info or "schedules" not in shift_info:  # Make sure we don't access empty dictionary
        return valid_shifts
    for i in range(len(shift_info["schedules"])):
        # at this point, we examining all the schedules for a particular day
        for j in range(len(shift_info["schedules"][i]["schedules"])):
            sched_item = shift_info["schedules"][i]["schedules"][j]
            if (sched_item["user_id"] == current_user.employee_id):
                sched_item["date"] = shift_info["schedules"][i]["date"]
                sched_item["adjusted_start"] = sched_item["start"] + current_user.utc_offset
                sched_item["adjusted_finish"] = sched_item["finish"] + current_user.utc_offset
                valid_shifts.append(sched_item)
    return valid_shifts

def fetch_current_user_shifts_for_date(delta):
    target_date = (datetime.datetime.now() + datetime.timedelta(int(delta))).strftime('%Y-%m-%d')
    shift_info = tanda_auth.get('rosters/on/{}'.format(target_date)).data
    valid_shifts = []
    if not shift_info or "schedules" not in shift_info:  # Make sure we don't access empty dictionary
        return valid_shifts
    for i in range(len(shift_info["schedules"])):
        # at this point, we examining all the schedules for a particular day
        for j in range(len(shift_info["schedules"][i]["schedules"])):
            sched_item = shift_info["schedules"][i]["schedules"][j]
            if (sched_item["user_id"] == current_user.employee_id):
                sched_item["date"] = shift_info["schedules"][i]["date"]
                sched_item["adjusted_start"] = sched_item["start"] + current_user.utc_offset
                sched_item["adjusted_finish"] = sched_item["finish"] + current_user.utc_offset
                valid_shifts.append(sched_item)
    return valid_shifts

def fetch_vacant_shifts():
    shift_info = tanda_auth.get('rosters/current').data
    vacant_shifts = []
    if not shift_info or "schedules" not in shift_info:
        return vacant_shifts
    for i in range(len(shift_info["schedules"])):
        #at this point, we examining all the schedules for a particular day
        for j in range(len(shift_info["schedules"][i]["schedules"])):
            sched_item = shift_info["schedules"][i]["schedules"][j]
            if (sched_item["user_id"] == None):
                sched_item["date"] = shift_info["schedules"][i]["date"]
                sched_item["adjusted_start"] = sched_item["start"] + current_user.utc_offset
                sched_item["adjusted_finish"] = sched_item["finish"] + current_user.utc_offset
                vacant_shifts.append(sched_item)
    return vacant_shifts

def offer_this_shift(id):
    shift = tanda_auth.get('schedules/' + str(id)).data
    shift_offer = Shift(shift["id"], None, shift["user_id"], shift["start"], shift["finish"], None, shift["department_id"])
    db_session.add(shift_offer)
    db_session.commit()

def fetch_offered_shifts():
    shifts = db_session.query(Shift).filter(Shift.taker is None)
    actual_shifts = [shift for shift in shifts]
    print("Shift is:")
    print(actual_shifts)
    for shift in actual_shifts:
        shift["adjusted_start"] = shift["start"] + current_user.utc_offset
        shift["adjusted_finish"] = shift["finish"] + current_user.utc_offset
    return actual_shifts

def take_offered_shift(shift_id, taker_id):
    shift = db_session.query(Shift).filter(Shift.schedule_id == shift_id).one()
    shift.taker = taker_id
    db_session.commit()

#this method can only be called by a manager!!!
def replace_user_in_schedule(user_id, schedule_id):
    print(current_user.is_manager)
    result = None
    url_path = 'schedules/' + str(schedule_id)
    data = {
        'user_id': user_id
    }
    json_data = json.dumps(data)
    print(json_data)
    if (current_user.is_manager):
        #clear to proceed as current user - probably
        result = tanda_auth.put(url_path, data=data).data
    else:
        #switch to god mode
        result = swappr.god_request.put(url_path, data=data).json()
    print(result)
    if ("error" in result):
        return False
    return result["user_id"] == user_id
