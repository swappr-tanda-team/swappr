from .base import Base
import sqlalchemy as sa

__all__ = ["User"]


class User(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    employee_id = sa.Column(sa.Integer)

    def __init__(self, name=None, email=None, employee_id=None):
        self.name = name
        self.email = email
        self.employee_id = employee_id

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
