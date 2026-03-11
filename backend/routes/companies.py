from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from extensions import db, jwt
import os

from models import Company, User

def validate_status(status):
    allowed_status = {"pending", "approved", "rejected"}

    if status and status not in allowed_status:
        return None

    return status

def parse_blacklist(value):
    if value is None:
        return None

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    return None

class Companies(Resource):

    @jwt_required()
    def get(self, company_id=None):

        claims = get_jwt()
        role = claims.get("role") if claims else None

        #Querying single company for checking it out
        if company_id:
            company = Company.query.get(company_id)

            if not company:
                return {"message": "Company not found"}, 404
            
            if role == "admin":
                return {
                "id": company.id,
                "name": company.company_name,
                "description": company.description,
                "industry":company.industry,
                "hr_name": company.hr_name,
                "hr_email": company.hr_email,
                "website": company.website,
                "location": company.location,
                "email": company.user.email,
                "status": company.status
            }, 200
            
            if company.blacklist:
                return {"message": "Company is blacklisted. Contact support for more information."}, 403
            
            if company.status != "approved":
                return {"message": f"Company registration is {company.status}. Please wait for approval."}, 403
            
            return {
                "id": company.id,
                "name": company.company_name,
                "description": company.description,
                "industry":company.industry,
                "hr_name": company.hr_name,
                "hr_email": company.hr_email,
                "website": company.website,
                "location": company.location,
                "email": company.user.email,
                "status": company.status
            }, 200
        
        #Querying a list of companies for admin and student dash
        status = validate_status(request.args.get("status"))
        blacklist_flag = parse_blacklist(request.args.get("blacklist"))
                
        #students can only see approved and non-blacklisted companies
        if role != "admin":
            query = Company.query.filter_by(status="approved", blacklist=False)

        else:
            query = Company.query
            if status:
                query = query.filter_by(status=status)
            
            if blacklist_flag is not None:
                query = query.filter_by(blacklist=blacklist_flag)
                    
        companies = query.all()        
        
        result = []

        for company in companies:
            result.append({
                "id": company.id,
                "company_name": company.company_name,
                "description": company.description,
                "hr_name": company.hr_name,
                "hr_email": company.hr_email,
                "website": company.website,
                "location": company.location,
                "email": company.user.email,
                "status": company.status,
                "industry":company.industry
            })

        return result, 200
    
    @jwt_required()
    def patch(self,company_id=None):
        claims = get_jwt()

        role = claims.get("role") 

        data = request.get_json()
        print(data)

        #Admin stuff
        if role == "admin":

            if not company_id:
                return {"message": "Company ID is required"}, 400
            
            company = Company.query.get(company_id)

            if not company:
                return {"message": "Company not found"}, 404
            
            status = validate_status(data.get("status"))
            blacklist = parse_blacklist(data.get("blacklist"))

            if status is not None:                
                company.status = status
            
            if blacklist is not None:                
                company.blacklist = blacklist
            
            db.session.commit()

            return {"message": "Company status updated successfully"}, 200
        
        #Company stuff
        if role == "company":
            user_id = get_jwt_identity()

            company = Company.query.filter_by(user_id=user_id).first()

            if not company:
                return {"message": "Company not found"}, 404
            

            if "company_name" in data:
                company.company_name = data["company_name"]

            if "industry" in data:
                company.industry = data["industry"]

            if "description" in data:
                company.description = data["description"]

            if "hr_name" in data:
                company.hr_name = data["hr_name"]

            if "hr_email" in data:
                company.hr_email = data["hr_email"]

            if "website" in data:
                company.website = data["website"]

            if "location" in data:
                company.location = data["location"]
            
            db.session.commit()

            return {"message": "Company profile updated successfully"}, 200
        
        return {"message": "Unauthorized"}, 403