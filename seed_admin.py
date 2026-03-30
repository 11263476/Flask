import asyncio # To run our async functions
import sys # To read command line arguments
from werkzeug.security import generate_password_hash # For secure hashing
from app.db.models import User
from app.db.database import AsyncSessionLocal
from sqlalchemy.future import select

# --- Seed Admin Script: A private tool to create your first Admin user ---

async def seed_admin(username, email, password):
    async with AsyncSessionLocal() as session:
        # 1. Check if user already exists
        result = await session.execute(select(User).where(User.username == username))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            # Delete the existing user so we can re-create them with the new hash
            print(f"User '{username}' already exists. Deleting and re-creating with new secure hash...")
            await session.delete(existing_user)
            await session.commit()

        # 2. Hash and Save
        hashed_pw = generate_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            password_hash=hashed_pw,
            role="admin" # Here we manually set the 'admin' role!
        )
        
        session.add(admin_user)
        await session.commit()
        print(f"Success! Admin user '{username}' (re)created with new secure hash.")
        print(f"Success! Admin user '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python seed_admin.py <username> <email> <password>")
    else:
        asyncio.run(seed_admin(sys.argv[1], sys.argv[2], sys.argv[3]))
