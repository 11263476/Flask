import asyncio # To run our async functions
import sys # To read command line arguments
from passlib.hash import bcrypt # For hashing
from app.db.models import User
from app.db.database import AsyncSessionLocal
from sqlalchemy.future import select

# --- Seed Admin Script: A private tool to create your first Admin user ---

async def seed_admin(username, email, password):
    async with AsyncSessionLocal() as session:
        # 1. Check if user already exists
        result = await session.execute(select(User).where(User.username == username))
        if result.scalar_one_or_none():
            print(f"Error: User '{username}' already exists!")
            return

        # 2. Hash and Save
        hashed_pw = bcrypt.hash(password)
        admin_user = User(
            username=username,
            email=email,
            password_hash=hashed_pw,
            role="admin" # Here we manually set the 'admin' role!
        )
        
        session.add(admin_user)
        await session.commit()
        print(f"Success! Admin user '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python seed_admin.py <username> <email> <password>")
    else:
        asyncio.run(seed_admin(sys.argv[1], sys.argv[2], sys.argv[3]))
