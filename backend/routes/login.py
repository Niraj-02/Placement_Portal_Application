from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from datetime import timedelta
import os

from models import User, Student, Company


class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")
        my_id = 0

        if not email or not password:
            return {"message": "Email and password are required"}, 400
        
        user = User.query.filter_by(email=email).first()

        if not user :
            return {"message": "User doesn't exist"}, 400
        
        if user.password != password:
            return {"message": "Incorrect password!! Please try again"},401
        
        if user.role == "company":
            company = Company.query.filter_by(user_id=user.id).first()

            if not company:
                return {"message": "Company profile not found"}, 404
            
            if company.status != "approved":
                return {"message": f"Company registration is {company.status}. Please wait for approval."}, 403
            
            if company.blacklist:
                return {"message": "Company is blacklisted. Contact support for more information."}, 403
        
        if user.role == "student":
            my_id = user.student.id
        elif user.role == "company":
            my_id = user.company.id
        else:
            my_id = 1
        
        access_token = create_access_token(
            identity=str(user.id), 
            expires_delta= timedelta(days=1),
            additional_claims={"role": user.role})
        
        response = {
            "message": "Login successful",
            "access_token": access_token,
            "role": user.role,
            "my_id": my_id
            }
        
        return response,200

        
