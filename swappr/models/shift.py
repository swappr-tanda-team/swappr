from .base import Base
import sqlalchemy as sa

__all__ = ["Shift"]


class Shift(Base):
    schedule_id = sa.Column(sa.Integer, primary_key=True)
    employee_id = sa.Column(sa.Integer)
    employee_name = sa.Column(sa.Text)
    start_time = sa.Column(sa.Integer)
    adjusted_start = sa.Column(sa.Integer)
    end_time = sa.Column(sa.Integer)
    adjusted_finish = sa.Column(sa.Integer)
    # status = sa.Column(sa.TEXT)
    location = sa.Column(sa.TEXT)
    # tag = sa.Column(sa.TEXT)
    # break_start = sa.Column(sa.Integer)
    # break_end = sa.Column(sa.Integer)
    department_id = sa.Column(sa.Integer)
    # employee id of taker
    taker = sa.Column(sa.Integer)
    taker_name = sa.Column(sa.Text)

    def __init__(self, schedule_id, taker=None, employee_id=None, start_time=None, end_time=None, location=None,
                 department_id=None, employee_name=None, taker_name=None):
        self.schedule_id = schedule_id
        self.employee_id = employee_id
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.department_id = department_id
        self.taker = taker
        self.employee_name = employee_name
        self.taker_name = taker_name

    def __repr__(self):
        return '<Shift %d>' % self.schedule_id



    def get_schedule_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.schedule_id


    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time


    def get_location(self):
        return self.location

    def get_employee_id(self):
        return self.employee_id

    def get_department_id(self):
        return self.department_id

    def is_taken(self):
        return self.taken
