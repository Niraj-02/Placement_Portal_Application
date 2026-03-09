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

        if not email or not password:
            return {"message": "Email and password are required"}, 400
        
        user = User.query.filter_by(email=email).first()

        if not user :
            return {"message": "User doesn't exist"}, 400
        
        if user.password != password:
            return {"message": "Incorrect password!! Please try again"},401
        
        access_token = create_access_token(
            identity=user.id, 
            expires_delta= timedelta(days=1),
            additional_claims={"role": user.role})
        
        response = {
            "message": "Login successful",
            "access_token": access_token,
            "role": user.role
            }
        
        return response,200

        
