from extensions import db
from datetime import datetime, timezone
from sqlalchemy import Enum



class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'

    id = db.Column(db.Integer, primary_key = True)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable = False)

    start_date = db.Column(db.DateTime, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable = False)    

    openings_count = db.Column(db.Integer, default=1)
    bond_details = db.Column(db.String(255), nullable=True)

    job_title = db.Column(db.String(100), nullable = False)
    job_type = db.Column(db.String(50), nullable = False) #on-site / remote / hybrid
    job_description = db.Column(db.Text, nullable = False)
    skills_required = db.Column(db.String(255), nullable=True)

    eligibility_criteria = db.Column(db.Text, nullable = False)
    eligible_branches = db.Column(db.String(200), nullable = False)
    min_cgpa = db.Column(db.Float, nullable = False)
    eligible_year = db.Column(db.String(20), nullable = False)

    salary = db.Column(db.Float, nullable = False)
    location = db.Column(db.String(100), nullable = False)

    status = db.Column(Enum("pending", "approved", "rejected", name="approval_status"), default = "pending", nullable=False)

    hiring_status = db.Column(Enum("upcoming","ongoing", "completed", name="drive_status"), default = "upcoming", nullable=False)

    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    applications = db.relationship("Application", backref="drive", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Placement Drive {self.job_title} , Company ID: {self.company_id}>"
    