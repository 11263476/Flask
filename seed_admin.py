import asyncio
import sys
from werkzeug.security import generate_password_hash
from app.db.models import User
from app.db.database import AsyncSessionLocal
from sqlalchemy.future import select

async def seed_admin(username, email, password):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"User '{username}' already exists. Updating to new secure hash...")
            existing_user.password_hash = generate_password_hash(password)
            existing_user.email = email
            await session.commit()
            print(f"Success! Admin user '{username}' has been updated.")
        else:
            hashed_pw = generate_password_hash(password)
            admin_user = User(
                username=username,
                email=email,
                password_hash=hashed_pw,
                role="admin"
            )
            session.add(admin_user)
            await session.commit()
            print(f"Success! Admin user '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python seed_admin.py <username> <email> <password>")
    else:
        asyncio.run(seed_admin(sys.argv[1], sys.argv[2], sys.argv[3]))
