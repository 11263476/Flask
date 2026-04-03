import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'viva-ready-secret-app-key'
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'secure-student-jwt-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False
    
    JWT_COOKIE_CSRF_PROTECT = False 
