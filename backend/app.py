from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource


from extensions import db
from config import Dev
from models import *


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Dev)

    db.init_app(app)

    api = Api(app)

    class Index(Resource):
        def get(self):
            return {"message": "Hello, World!"}
    api.add_resource(Index, "/")

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