import asyncio  # Import asyncio for running asynchronous code
from app.db.database import engine, Base  # Import database engine and base class
from app.db.models import Student  # Import models to ensure they are registered with Base

async def init_db():  # Function to initialize the database
    async with engine.begin() as conn:  # Start a connection with the database engine
        # Run the command to create all tables defined across our models
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":  # Ensure the script runs only when executed directly
    asyncio.run(init_db())  # Use asyncio to run the initialization function
