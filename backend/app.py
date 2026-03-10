from flask import Flask, jsonify,send_from_directory
from flask_cors import CORS
from flask_restful import Api, Resource


from extensions import db, jwt
from config import Dev
from models import *
from routes import *

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(Dev)

    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    class Index(Resource):
        def get(self):
            return {"message": "Hello, World!"}
    api.add_resource(Index, "/")
    
    api.add_resource(StudentRegister, "/api/register/student")
    api.add_resource(CompanyRegister, "/api/register/company")
    
    api.add_resource(Login, "/api/login")

    api.add_resource(Companies, "/api/companies", "/api/companies/<int:company_id>")

    api.add_resource(Applications, "/api/application", "/api/application/<int:application_id>")

    api.add_resource(PlacementDrives, "/api/drives", "/api/drives/<int:drive_id>")

    api.add_resource(Students, "/api/students", "/api/students/<int:student_id>")

    

    @app.route("/resume_folder/<filename>")
    def get_resume(filename):
        print("UPLOAD_FOLDER:", app.config["UPLOAD_FOLDER"])
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app

app = create_app()

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(email="admin@gmail.com").first()

        if not admin:
            admin = User(email="admin@gmail.com", password="admin123", role="admin")
        
            db.session.add(admin)
            db.session.commit()

            print("Admin Created")
        else:
            print("Admin Already Exists")

    app.run(debug=True)