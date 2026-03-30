from passlib.hash import bcrypt  # Import bcrypt for secure password hashing
from sqlalchemy.future import select  # Import select for queries
from app.db.models import User  # Import User model
from app.db.database import AsyncSessionLocal  # Import database session factory

# --- Auth Service: Handles secure user creation and validation ---

async def create_user(data):  # Function to register a new user
    async with AsyncSessionLocal() as session:
        # 1. Hash the password before saving (never save plain text!)
        hashed_pw = bcrypt.hash(data.password)
        
        # 2. Map the Pydantic data to a SQLAlchemy User model
        new_user = User(
            username=data.username,
            email=data.email,
            password_hash=hashed_pw,
            role="user" # Default role is always 'user'
        )
        
        # 3. Save to database
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def authenticate_user(username, password):  # Function to check login credentials
    async with AsyncSessionLocal() as session:
        # 1. Find the user by their username
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        # 2. Check if user exists and if the password matches the hash
        if user and bcrypt.verify(password, user.password_hash):
            return user # Return user if valid
            
        return None # Return None if login fails

async def get_all_users():  # Function to fetch all registered users for admin oversight
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

async def delete_user(user_id):  # Function to remove a user account
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
        return user
