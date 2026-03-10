from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import os

from extensions import db
from models import Student

def student_formatter(student):
    return {
        "id": student.id,
        "name": student.name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "year_of_passing": student.year_of_passing,
        "skills": student.skills,
        "resume": student.resume,
        "blacklist": student.blacklist,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat()
    }

def parse_blacklist(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    return None

class Students(Resource):

    @jwt_required()
    def get(self, student_id=None):

        claims = get_jwt()
        role = claims.get("role")
        user_id = get_jwt_identity()

        #Specific Student
        if student_id:
            student = Student.query.get_or_404(student_id)

            if role == "admin":
                return student_formatter(student),200
            
            if role == "student":
                my_student = Student.query.filter_by(user_id=user_id).first()

                if not my_student:
                    return {"message": "Student not found!"}, 404

                if student_id != my_student.id:
                    return {"message": "Unauthorized"}, 403
                
                return student_formatter(student),200
            
            return {"message": "Unauthorized"}, 403
        
        #Student list for admin dash
        if role != "admin":
            return {"message": "Unauthorized access!!"}, 403
        
        student_list = Student.query.all()
        result = []

        for s in student_list:
            result.append(student_formatter(s))

        return result,200
    

    @jwt_required()
    def patch(self, student_id=None):
        
        claims = get_jwt()
        role = claims.get("role")
        user_id = get_jwt_identity()

        if not student_id:
            return {"message": "Student ID is required"}, 400
        
        student = Student.query.get_or_404(student_id)

        

        # Admin blacklisting student
        if role == "admin":
            data = request.get_json()
            blacklist_content = parse_blacklist(data.get("blacklist"))

            if blacklist_content is True:
                student.blacklist = True
            elif blacklist_content is False:
                student.blacklist = False
            else:
                pass

            db.session.commit()
            return {"message": "Student blacklist status updated successfully"}, 200


        # Student update
        if role == "student":
            my_student = Student.query.filter_by(user_id=user_id).first()

            if not my_student:
                return {"message": "Student not found"}, 404

            if student.id != my_student.id:
                return {"message": "Unauthorized"}, 403
            
            cgpa = request.form.get("cgpa")
            skills = request.form.get("skills")
            resume = request.files.get("resume")

            if cgpa:
                cgpa = float(cgpa)
                if cgpa < 0 or cgpa > 10:
                    return {"message": "CGPA must be between 0 and 10"}, 400
                student.cgpa = float(cgpa)
            if skills:
                student.skills = skills
            
            if resume:
                if not resume.filename.endswith('.pdf'):
                    return {"message": "Resume must be a PDF file."}, 400
                
                filename = f"student_{student.id}.pdf"
                filepath = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )        
                resume.save(filepath)
                student.resume = filename
            
            db.session.commit()

            return {"message": "Student profile updated successfully"}, 200