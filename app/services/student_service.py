from sqlalchemy.future import select  # Import select for building queries
from app.db.models import Student  # Import the Student database model
from app.db.database import AsyncSessionLocal  # Import our session factory

async def create_student(data):  # Function to create a new student record
    async with AsyncSessionLocal() as session:  # Start a new database session
        student = Student(**data.model_dump())  # Convert Pydantic data to a Student object
        session.add(student)  # Add the new student to the session
        await session.commit()  # Save the changes to the database
        await session.refresh(student)  # Refresh the object with its new ID from the DB
        return student  # Return the created student

async def get_students():  # Function to fetch all students
    async with AsyncSessionLocal() as session:  # Start a new database session
        result = await session.execute(select(Student))  # Execute a SELECT * query
        return result.scalars().all()  # Return the results as a list of objects

async def get_student(student_id):  # Function to fetch a single student by ID
    async with AsyncSessionLocal() as session:  # Start a new database session
        # Execute a filter query to find the student by ID
        result = await session.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()  # Return the student or None if not found

async def update_student(student_id, data):  # Function to update an existing student
    async with AsyncSessionLocal() as session:  # Start a new database session
        # Find the student first
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()

        if not student:  # If student doesn't exist, return None
            return None

        # Update the student's attributes with the new data
        for key, value in data.model_dump().items():
            setattr(student, key, value)

        await session.commit()  # Save the updates to the database
        return student  # Return the updated student

async def delete_student(student_id):  # Function to delete a student record
    async with AsyncSessionLocal() as session:  # Start a new database session
        # Find the student to delete
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()

        if student:  # If student exists, delete it
            await session.delete(student)
            await session.commit()  # Save the deletion to the database

        return student  # Return the deleted student (or None)
