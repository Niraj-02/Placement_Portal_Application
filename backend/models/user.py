from extensions import db
from datetime import datetime, timezone
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(70), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)

    role = db.Column(Enum("admin", "student", "company", name="user_roles"), nullable = False)
   
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    student = db.relationship("Student", backref="user", uselist=False, cascade="all, delete-orphan")
    company = db.relationship("Company", backref="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"