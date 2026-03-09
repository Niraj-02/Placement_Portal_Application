from flask_restful import Resource
from flask import request, current_app
from extensions import db
from models import User, Company
import os


class CompanyRegister(Resource):

    def post(self):
        
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        company_name = data.get("company_name")
        industry = data.get("industry")
        description = data.get("description")

        hr_name = data.get("hr_name")
        hr_email = data.get("hr_email")
        website = data.get("website")
        location = data.get("location")

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 409
        
        if Company.query.filter_by(company_name=company_name).first():
            return {"message": "Company already exists"}, 409
        
        user = User(
            email=email,
            password=password,
            role="company")
        
        db.session.add(user)
        db.session.commit()

        company = Company(
            company_name=company_name,
            industry=industry,
            description=description,
            user_id=user.id,
            hr_name=hr_name,
            hr_email=hr_email,
            website=website,
            location=location
        )
        
        db.session.add(company)
        db.session.commit()

        return {"message": "Company registered successfully. Awaiting Admin approval."}, 200