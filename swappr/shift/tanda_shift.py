"""
Methods for interacting with Tanda shifts
"""
from flask import session
from flask_login import current_user
from swappr.user.tanda_api import tanda_auth
from swappr.database import db_session
from swappr.models import Shift

#Might be benificial to cache roster?

def fetch_current_user_upcoming_shifts():
    shift_info = tanda_auth.get('rosters/current').data
    valid_shifts = []
    if not shift_info or "schedules" not in shift_info:  #Make sure we don't access empty dictionary
        return valid_shifts
    for i in range(len(shift_info["schedules"])):
        #at this point, we examining all the schedules for a particular day
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
    shift = tanda_auth.get('schedules/' + id, "true").data
    shift_offer = Shift(shift["id"], shift["user_id"], shift["start"], shift["finish"], shift["location"])
    db_session.add(shift_offer)

def fetch_offered_shifts():
    shifts = []
    shifts = db_session.query(Shift)
    return shifts

