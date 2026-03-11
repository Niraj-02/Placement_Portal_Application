from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from extensions import db
from models import PlacementDrive, Company, Student, Application
from datetime import datetime, timezone

def application_formatter(application):
    return {
        "id": application.id,
        "student_id": application.student_id,
        "student_name": application.student.name,
        "placement_drive_id": application.placement_drive_id,
        "placement_drive_name": application.drive.job_title,
        "company_name": application.drive.company.company_name,
        "status": application.status,
        "applied_at": application.applied_at.isoformat() if application.applied_at else None,
        "updated_at": application.updated_at.isoformat()
    }


class Applications(Resource):

    @jwt_required()
    def post(self):

        claims = get_jwt()
        role = claims.get("role")
        user_id = get_jwt_identity()

        if role != "student":
            return {"message": "Only students can apply"}, 403

        data = request.get_json()
        drive_id = data.get("drive_id")

        if not drive_id:
            return {"message": "Drive ID required"}, 400

        drive = PlacementDrive.query.get_or_404(drive_id)

        if drive.status != "approved":
            return {"message": "Drive not approved"}, 403

        if drive.hiring_status == "completed":
            return {"message": "Drive already completed"}, 400
        # deadline = datetime.fromisoformat(data["application_deadline"]).replace(tzinfo=timezone.utc)
        if drive.application_deadline < datetime.utcnow():
            return {"message": "Application deadline passed"}, 400

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message": "Student not found"}, 404

        if student.blacklist:
            return {"message": "Student is blacklisted"}, 403

        application = Application(
            student_id=student.id,
            placement_drive_id=drive.id
        )

        db.session.add(application)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Already applied to this drive"}, 409

        return {"message": "Application submitted successfully"}, 201
    
    @jwt_required()
    def patch(self, application_id=None):

        claims = get_jwt()
        role = claims.get("role")
        user_id = get_jwt_identity()
        

        if role != "company":
            return {"message": "Only companies can update application status"}, 403

        if not application_id:
            return {"message": "Application ID required"}, 400

        app = Application.query.get_or_404(application_id)

        company = Company.query.filter_by(user_id=user_id).first()
        if not company:
            return {"message": "Company not found"}, 404

        drive = PlacementDrive.query.get_or_404(app.placement_drive_id) #getting drive from placement_drive_id

        if drive.company_id != company.id:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        status = data.get("status")

        allowed = {"shortlisted", "interview", "selected", "rejected", "placed"}

        if status not in allowed:
            return {"message": "Invalid application status"}, 400

        app.status = status

        db.session.commit()

        return {"message": "Application status updated"}, 200
    

    @jwt_required()
    def get(self, application_id=None):
        claims = get_jwt()
        role = claims.get("role")
        user_id = get_jwt_identity()

        drive_id = request.args.get("drive_id", type=int)

        # Getting specific applications
        if application_id:
            app = Application.query.get_or_404(application_id)

            # For Admin
            if role == "admin":
                return application_formatter(app) ,200
        

            # For Company
            if role == "company":
                company = Company.query.filter_by(user_id=user_id).first()

                if not company:
                    return {"message": "Company not found"}, 404
                
                drive = PlacementDrive.query.get_or_404(app.placement_drive_id)

                if drive.company_id != company.id:
                    return {"message": "Unauthorized"}, 403
                
                return application_formatter(app),200
            
            # For student
            if role == "student":
                student = Student.query.filter_by(user_id=user_id).first()

                if not student:
                    return {"message": "Student not found"}, 404

                if app.student_id != student.id:
                    return {"message": "Unauthorized"}, 403
                
                return application_formatter(app),200
            

        # Getting a list of applications
        if role == "student":
            student = Student.query.filter_by(user_id=user_id).first()

            if not student:
                return {"message": "Student not found"}, 404
            
            apps = Application.query.filter_by(student_id=student.id).all()

        
        # Applications for company per their drive

        elif role == "company":

            company = Company.query.filter_by(user_id=user_id).first()

            if not company:
                return {"message": "Company not found"}, 404
            
            if not drive_id:
                return {"message": "Placement drive ID required"}, 400
        
        
            drive = PlacementDrive.query.get_or_404(drive_id)

            if drive.company_id != company.id:
                return {"message": "Unauthorized"}, 403
            
            apps = Application.query.filter_by(placement_drive_id=drive_id).all()
            
        
        # For admins
        elif role == "admin":
            query = Application.query

            if drive_id:
                query = query.filter_by(placement_drive_id=drive_id)
            
            apps = query.all()
            
        else:
            return {"message": "Unauthorized access!!"}, 403
        
        result = []
        for app in apps:
            result.append(application_formatter(app))

        return result,200
