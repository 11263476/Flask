from pydantic import BaseModel  # Import the base class for Pydantic models

class StudentCreate(BaseModel):  # Define a schema for creating or updating a student
    name: str  # Student's name must be a string
    email: str  # Student's email must be a string
    age: int  # Student's age must be an integer
    course: str  # Student's course must be a string


class StudentResponse(StudentCreate):  # Define a schema for sending student data back to the user
    id: int  # Include the unique database ID in the response

    class Config:  # Internal configuration for Pydantic
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy objects
