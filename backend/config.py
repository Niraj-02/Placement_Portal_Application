class Dev:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "someweirdocreatedjwtandnowihavetolearnthis"

    UPLOAD_FOLDER = "resume_folder"