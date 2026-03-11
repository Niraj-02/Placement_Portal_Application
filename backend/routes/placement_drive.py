from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from extensions import db
from models import PlacementDrive, Company
from datetime import datetime, timezone


def validate_status(status):
    allowed = {"pending", "approved", "rejected"}
    return status in allowed


class PlacementDrives(Resource):

    @jwt_required()
    def post(self):

        claims = get_jwt()
        user_id = get_jwt_identity()

        if claims["role"] != "company":
            return {"message": "Only companies can create placement drives"}, 403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message": "Company not found"}, 404

        if company.status != "approved":
            return {"message": "Company not approved yet"}, 403

        if company.blacklist:
            return {"message": "Company is blacklisted"}, 403

        data = request.get_json()

        try:
            start_date = datetime.fromisoformat(data["start_date"]).replace(tzinfo=timezone.utc)
            deadline = datetime.fromisoformat(data["application_deadline"]).replace(tzinfo=timezone.utc)
        except:
            return {"message": "Invalid date format"}, 400

        if deadline <= datetime.now(timezone.utc):
            return {"message": "Deadline must be in the future"}, 400

        placement_drive = PlacementDrive(
            company_id=company.id,

            start_date=start_date,
            application_deadline=deadline,

            openings_count=data.get("openings_count", 1),
            bond_details=data.get("bond_details"),

            job_title=data.get("job_title"),
            job_type=data.get("job_type"),
            job_description=data.get("job_description"),
            skills_required=data.get("skills_required"),

            eligibility_criteria=data.get("eligibility_criteria"),
            eligible_branches=data.get("eligible_branches"),
            min_cgpa=data.get("min_cgpa"),
            eligible_year=data.get("eligible_year"),

            salary=data.get("salary"),
            location=data.get("location")
        )

        db.session.add(placement_drive)
        db.session.commit()

        return {
            "message": "Placement drive created successfully. Awaiting admin approval"
        }, 201


    @jwt_required()
    def get(self, drive_id=None):

        claims = get_jwt()
        role = claims.get("role")

        if drive_id:

            drive = PlacementDrive.query.get_or_404(drive_id)

            if role == "company":
                user_id = get_jwt_identity()
                company = Company.query.filter_by(user_id=user_id).first()

                if not company:
                    return {"message": "Company not found"}, 404

                if drive.company_id != company.id:
                    return {"message": "Unauthorized"}, 403

            if role == "student" and drive.status != "approved":
                return {"message": "Placement drive not approved yet"}, 403

            return {
                "id": drive.id,
                "company_id": drive.company_id,
                "company_name": drive.company.company_name,

                "start_date": drive.start_date.isoformat(),
                "application_deadline": drive.application_deadline.isoformat(),

                "openings_count": drive.openings_count,
                "bond_details": drive.bond_details,

                "job_title": drive.job_title,
                "job_type": drive.job_type,
                "job_description": drive.job_description,
                "skills_required": drive.skills_required,

                "eligibility_criteria": drive.eligibility_criteria,
                "eligible_branches": drive.eligible_branches,
                "min_cgpa": drive.min_cgpa,
                "eligible_year": drive.eligible_year,

                "salary": drive.salary,
                "location": drive.location,

                "status": drive.status,
                "hiring_status": drive.hiring_status
            }, 200

        ApprovalStatus = request.args.get("status")
        HiringStatus = request.args.get("hiring_status")

        if ApprovalStatus not in {"approved", "pending", "rejected", None}:
            return {"message": "Wrong status received"}, 400

        if HiringStatus not in {"upcoming", "ongoing", "completed", None}:
            return {"message": "Wrong hiring status received"}, 400

        if role == "student":
            query = PlacementDrive.query.filter_by(status="approved")\
                .filter(PlacementDrive.hiring_status != "completed")

        elif role == "company":
            userID = get_jwt_identity()
            company = Company.query.filter_by(user_id=userID).first()

            if not company:
                return {"message": "Company not found"}, 404

            query = PlacementDrive.query.filter_by(company_id=company.id)

        elif role == "admin":
            query = PlacementDrive.query

            if ApprovalStatus:
                query = query.filter_by(status=ApprovalStatus)

            if HiringStatus:
                query = query.filter_by(hiring_status=HiringStatus)

        drives = query.all()

        result = []

        for drive in drives:
            result.append({
                "id": drive.id,
                "company_id": drive.company_id,
                "company_name": drive.company.company_name,

                "start_date": drive.start_date.isoformat(),
                "application_deadline": drive.application_deadline.isoformat(),

                "openings_count": drive.openings_count,
                "bond_details": drive.bond_details,

                "job_title": drive.job_title,
                "job_type": drive.job_type,
                "job_description": drive.job_description,
                "skills_required": drive.skills_required,

                "eligibility_criteria": drive.eligibility_criteria,
                "eligible_branches": drive.eligible_branches,
                "min_cgpa": drive.min_cgpa,
                "eligible_year": drive.eligible_year,

                "salary": drive.salary,
                "location": drive.location,

                "status": drive.status,
                "hiring_status": drive.hiring_status
            })

        return result, 200


    @jwt_required()
    def patch(self, drive_id=None):

        claims = get_jwt()
        role = claims.get("role")
        data = request.get_json() or {}

        if not drive_id:
            return {"message": "Drive ID is required"}, 400

        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message": "Placement drive not found"}, 404

        # Admin approval
        if role == "admin":

            status = data.get("status")

            if not validate_status(status):
                return {"message": "Invalid status"}, 400

            drive.status = status
            db.session.commit()

            return {"message": "Placement drive status updated successfully"}, 200

        # Mark drive completed
        if role in {"admin", "company"}:

            if role == "company":
                userID = get_jwt_identity()
                company = Company.query.filter_by(user_id=userID).first()

                if drive.company_id != company.id:
                    return {"message": "You can only update your own placement drives"}, 403

            drive.hiring_status = "completed"
            db.session.commit()

            return {"message": "Placement drive marked as completed"}, 200