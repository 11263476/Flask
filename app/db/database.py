from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Import Async features for database
from sqlalchemy.orm import sessionmaker, declarative_base  # Import session management tools

# Define the connection URL for the SQLite database using aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///./students.db"

# Create the asynchronous engine to connect to the database
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory to generate new database sessions on demand
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create a base class for our models to inherit from
Base = declarative_base()
