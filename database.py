from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://neondb_owner:npg_YpKE8uUVzaW9@ep-weathered-river-amz1g1x2-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Create engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(bind=engine)

# Base class (VERY IMPORTANT)
Base = declarative_base()