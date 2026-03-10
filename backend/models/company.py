from extensions import db
from datetime import datetime, timezone
from sqlalchemy import Enum


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    company_name = db.Column(db.String(100), nullable = False)
    industry = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable = False)

    hr_name = db.Column(db.String(100), nullable = False)
    hr_email = db.Column(db.String(100), nullable = False)
    website = db.Column(db.String(200))
    location = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    status = db.Column(Enum("pending", "approved", "rejected", name="company_approval"), default = "pending")
    blacklist = db.Column(db.Boolean, default = False)

    drives = db.relationship("PlacementDrive", backref="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company {self.company_name} , Status: {self.status}>"