import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Dev:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "someweirdocreatedjwtandnowihavetolearnthis"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "resume_folder")