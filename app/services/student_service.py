from sqlalchemy.future import select
from sqlalchemy import func
from app.db.models import Student
from app.db.database import AsyncSessionLocal

async def create_student(data):
    async with AsyncSessionLocal() as session:
        student = Student(**data.model_dump())
        session.add(student)
        await session.commit()
        await session.refresh(student)
        return student

async def get_students():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Student))
        return result.scalars().all()

async def get_student(student_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()

async def update_student(student_id, data):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()

        if not student:
            return None

        for key, value in data.model_dump().items():
            setattr(student, key, value)

        await session.commit()
        return student

async def delete_student(student_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalar_one_or_none()

        if student:
            await session.delete(student)
            await session.commit()

        return student

async def get_student_stats():
    async with AsyncSessionLocal() as session:
        total_students = (await session.execute(select(func.count(Student.id)))).scalar() or 0
        avg_age = round((await session.execute(select(func.avg(Student.age)))).scalar() or 0, 1)

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

async def search_students(query):
    async with AsyncSessionLocal() as session:
        search_filter = select(Student).where(
            (Student.name.ilike(f"%{query}%")) | 
            (Student.course.ilike(f"%{query}%"))
        )
        result = await session.execute(search_filter)
        return result.scalars().all()
