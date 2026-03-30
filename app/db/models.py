from sqlalchemy import Column, Integer, String, DateTime  # Import SQL column types
from datetime import datetime  # Import datetime for timestamps
from .database import Base  # Import the Base class from our database config

class Student(Base):  # Define the Student model which inherits from Base
    __tablename__ = "students"  # Specify the name of the database table

    id = Column(Integer, primary_key=True, index=True)  # Primary key with an index
    name = Column(String)  # Column for the student's name
    email = Column(String, unique=True)  # Column for unique email addresses
    age = Column(Integer)  # Column for the student's age
    course = Column(String)  # Column for the enrolled course
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp when the record is created

class User(Base):  # Define the User model for authentication and roles
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)  # Stores the hashed password
    role = Column(String(20), default="user")  # 'admin' or 'user' roles
    created_at = Column(DateTime, default=datetime.utcnow)
