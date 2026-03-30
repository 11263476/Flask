from sqlalchemy.future import select  # Import select for building queries
from sqlalchemy import func  # Import func for aggregations (avg, count, etc.)
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

async def get_student_stats():  # Function to calculate dashboard analytics
    async with AsyncSessionLocal() as session:
        # Total Students Count
        total_result = await session.execute(select(func.count(Student.id)))
        total_students = total_result.scalar() or 0

        # Average Age
        avg_age_result = await session.execute(select(func.avg(Student.age)))
        avg_age = round(avg_age_result.scalar() or 0, 1)

        # Top Course (Most popular)
        top_course_result = await session.execute(
            select(Student.course, func.count(Student.id))
            .group_by(Student.course)
            .order_by(func.count(Student.id).desc())
            .limit(1)
        )
        top_course_data = top_course_result.first()
        top_course = top_course_data[0] if top_course_data else "N/A"

        return {
            "total_students": total_students,
            "avg_age": avg_age,
            "top_course": top_course
        }

async def search_students(query):  # Function to filter students by name or course
    async with AsyncSessionLocal() as session:
        # Use ILIKE for case-insensitive search on Name or Course
        search_filter = select(Student).where(
            (Student.name.ilike(f"%{query}%")) | 
            (Student.course.ilike(f"%{query}%"))
        )
        result = await session.execute(search_filter)
        return result.scalars().all()
