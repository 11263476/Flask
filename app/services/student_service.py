from sqlalchemy.future import select
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
