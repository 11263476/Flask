import os  # Import OS module to interact with environment variables

class Config:  # Define a class to hold application configurations
    # Set the secret key for sessions, defaulting to a fallback string if not in environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
