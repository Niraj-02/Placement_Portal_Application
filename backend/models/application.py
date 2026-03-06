from extensions import db
from datetime import datetime, timezone
from sqlalchemy import Enum 


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key = True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable = False)
    placement_drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable = False)

    status = db.Column(Enum("applied", "shortlisted", "interview", "selected", "rejected", "placed", name="application_status"), default = "applied")

    applied_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Application Student ID: {self.student_id} , Placement Drive ID: {self.placement_drive_id} , Status: {self.status}>"
    
    __table_args__ = (db.UniqueConstraint("student_id", "placement_drive_id", name = "unique_student_drive_application"),)