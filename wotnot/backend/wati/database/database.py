
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Fetch values
backend_url = os.getenv("BACKEND_URL")
database_url = os.getenv("DATABASE_URL")

# SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:Denmarks123$@localhost/wati_clone'


SQLALCHEMY_DATABASE_URL = database_url

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Denmarks123$@localhost/wati_clone'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()



# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True,pool_recycle=120,pool_pre_ping=True,pool_size=30 )

# Create a session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    
)

# Base class for declarative models
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

