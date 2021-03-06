from .base import Base
import sqlalchemy as sa

__all__ = ["User"]


class User(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    utc_offset = sa.Column(sa.Integer)
    time_zone = sa.Column(sa.Text)
    employee_id = sa.Column(sa.Integer)
    is_manager = sa.Column(sa.Boolean)

    def __init__(self, name=None, employee_id=None, utc_offset=None, time_zone=None):
        self.name = name
        self.employee_id = employee_id
        self.utc_offset = utc_offset
        self.time_zone = time_zone
        self.is_manager = False

    def __repr__(self):
        return '<User %r>' % self.name

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
