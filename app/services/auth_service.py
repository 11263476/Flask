from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.future import select
from app.db.models import User
from app.db.database import AsyncSessionLocal

async def create_user(data):
    async with AsyncSessionLocal() as session:
        hashed_pw = generate_password_hash(data.password)
        
        new_user = User(
            username=data.username,
            email=data.email,
            password_hash=hashed_pw,
            role="user"
        )
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def authenticate_user(username, password):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        if user and check_password_hash(user.password_hash, password):
            return user
            
        return None

async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

async def delete_user(user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
        return user
