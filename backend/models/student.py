from extensions import db 
from datetime import datetime,timezone

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    name = db.Column(db.String(100), nullable = False)    
    branch = db.Column(db.String(50), nullable = False)
    cgpa = db.Column(db.Float, nullable = False)
    year_of_passing = db.Column(db.String(20), nullable = False)

    skills = db.Column(db.Text, nullable = False)

    blacklist = db.Column(db.Boolean, default = False)

    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    applications = db.relationship("Application", backref="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.name}>"
