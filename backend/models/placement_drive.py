from extensions import db
from datetime import datetime, timezone
from sqlalchemy import Enum



class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key = True)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable = False)

    job_title = db.Column(db.String(100), nullable = False)
    job_type = db.Column(db.String(50), nullable = False) #on-site / remote / hybrid
    job_description = db.Column(db.Text, nullable = False)
    eligibility_criteria = db.Column(db.Text, nullable = False)
    eligible_branches = db.Column(db.String(200), nullable = False)
    min_cgpa = db.Column(db.Float, nullable = False)
    eligible_year = db.Column(db.String(20), nullable = False)
    application_deadline = db.Column(db.DateTime, nullable = False)
    salary = db.Column(db.Float, nullable = False)
    location = db.Column(db.String(100), nullable = False)

    status = db.Column(Enum("pending", "approved", "rejected", name="drive_approval"), default = "pending")

    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    applications = db.relationship("Application", backref="drive", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Placement Drive {self.job_title} , Company ID: {self.company_id}>"
    