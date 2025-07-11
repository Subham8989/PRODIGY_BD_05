import os

class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
  JWT_TOKEN_LOCATION = ["cookies"]
  JWT_COOKIE_SECURE = True
  JWT_COOKIE_CSRF_PROTECT = False
  JWT_ACCESS_COOKIE_PATH = "/"
  JWT_REFRESH_COOKIE_PATH = "/refresh"