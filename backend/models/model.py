"""Simple fallback file in case of any errors."""


# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timezone
# from sqlalchemy import UniqueConstraint, Enum

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key = True)

#     email = db.Column(db.String(70), unique = True, nullable = False)
#     password = db.Column(db.String(120), nullable = False)

#     role = db.Column(Enum("admin", "student", "company", name="user_roles"), nullable = False)
   
#     created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

#     student = db.relationship("Student", backref="user", uselist=False, cascade="all, delete-orphan")
#     company = db.relationship("Company", backref="user", uselist=False, cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"<User {self.email}>"


# class Student(db.Model):
#     __tablename__ = 'students'

#     id = db.Column(db.Integer, primary_key = True)

#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

#     name = db.Column(db.String(100), nullable = False)    
#     branch = db.Column(db.String(50), nullable = False)
#     cgpa = db.Column(db.Float, nullable = False)
#     year_of_passing = db.Column(db.String(20), nullable = False)

#     skills = db.Column(db.Text, nullable = False)

#     resume = db.Column(db.String(200), nullable = True)

#     blacklist = db.Column(db.Boolean, default = False)

#     created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

#     applications = db.relationship("Application", backref="student", cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"<Student {self.name}>"


# class Company(db.Model):
#     __tablename__ = 'companies'

#     id = db.Column(db.Integer, primary_key = True)

#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

#     company_name = db.Column(db.String(100), nullable = False)
#     industry = db.Column(db.String(50), nullable = False)
#     description = db.Column(db.Text, nullable = False)

#     created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

#     status = db.Column(Enum("pending", "approved", "rejected", name="company_approval"), default = "pending")
#     blacklist = db.Column(db.Boolean, default = False)

#     drives = db.relationship("PlacementDrive", backref="company", cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"<Company {self.company_name} , Status: {self.status}>"


# class PlacementDrive(db.Model):
#     __tablename__ = 'placement_drives'

#     id = db.Column(db.Integer, primary_key = True)

#     company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable = False)

#     job_title = db.Column(db.String(100), nullable = False)
#     job_type = db.Column(db.String(50), nullable = False) #on-site / remote / hybrid
#     job_description = db.Column(db.Text, nullable = False)
#     eligibility_criteria = db.Column(db.Text, nullable = False)
#     eligible_branches = db.Column(db.String(200), nullable = False)
#     min_cgpa = db.Column(db.Float, nullable = False)
#     eligible_year = db.Column(db.String(20), nullable = False)
#     application_deadline = db.Column(db.DateTime, nullable = False)
#     salary = db.Column(db.Float, nullable = False)
#     location = db.Column(db.String(100), nullable = False)

#     status = db.Column(Enum("pending", "approved", "rejected", name="drive_approval"), default = "pending")

#     created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

#     applications = db.relationship("Application", backref="drive", cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"<Placement Drive {self.job_title} , Company ID: {self.company_id}>"
    

# class Application(db.Model):
#     __tablename__ = 'applications'

#     id = db.Column(db.Integer, primary_key = True)

#     student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable = False)
#     placement_drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable = False)

#     status = db.Column(Enum("applied", "shortlisted", "interview", "selected", "rejected", "placed", name="application_status"), default = "applied")

#     applied_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

#     def __repr__(self):
#         return f"<Application Student ID: {self.student_id} , Placement Drive ID: {self.placement_drive_id} , Status: {self.status}>"
    
#     __table_args__ = (db.UniqueConstraint("student_id", "placement_drive_id", name = "unique_student_drive_application"),)