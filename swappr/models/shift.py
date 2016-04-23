from .base import Base
import sqlalchemy as sa

__all__ = ["Shift"]


class Shift(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    # employee_id = sa.Column(sa.Integer)
    start_time = sa.Column(sa.Integer)
    end_time = sa.Column(sa.Integer)
    # status = sa.Column(sa.TEXT)
    location = sa.Column(sa.TEXT)
    # tag = sa.Column(sa.TEXT)
    # break_start = sa.Column(sa.Integer)
    # break_end = sa.Column(sa.Integer)

    def __init__(self, id=None, employee_id=None, start_time=None, end_time=None):
        self.id = id
        self.employee_id = employee_id
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Shift %d>' % self.id



    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id


    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time


    def get_location(self):
        return self.location


