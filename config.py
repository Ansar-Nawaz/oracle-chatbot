import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    PDF_PATH = os.path.join(BASE_DIR, "data", "error-messages.pdf")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "oracle_errors.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "a-very-secret-key")
