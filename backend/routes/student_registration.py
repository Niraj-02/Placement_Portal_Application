from flask_restful import Resource
from flask import request, current_app
from extensions import db
from models import User, Student
import os

class StudentRegister(Resource):

    def post(self):

        email = request.form.get("email")
        password = request.form.get("password")

        name = request.form.get("name")
        branch = request.form.get("branch")
        cgpa = float(request.form.get("cgpa"))
        year_of_passing = request.form.get("year_of_passing")
        skills = request.form.get("skills")

        resume = request.files.get("resume")

        if not resume:
            return {"message": "Resume file is missing!"},400
        
        
        if not resume.filename.endswith(".pdf"):
            return {"message": "Resume must be a PDF file."}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 409

        user = User(
            email=email,
            password=password,
            role="student"
        )

        db.session.add(user)
        db.session.commit()


        student = Student(
            user_id=user.id, # Exists cuz we did session.add so we can pull it from there without querying the user
            name=name,
            branch=branch,
            cgpa=cgpa,
            year_of_passing=year_of_passing,
            skills=skills
        )

        db.session.add(student)
        db.session.commit()

        if resume:
            filename = f"student_{student.id}.pdf"

            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            resume.save(filepath)

            student.resume = filename
            db.session.commit()


        return {"message": "Student registered successfully"}, 201
    




