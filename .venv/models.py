#S1 : IMPORT LIBARARIES
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base
from database import engine 
from database import Base

# Create Patient Class
class Patient(Base):

       __tablename__ = "patients"

       id = Column(String, primary_key=True, index=True)
       name = Column(String)
       age = Column(Integer)

# Create User class

class User(Base):

       __tablename__ = "users"  #Use double underscore for tablename 

       email = Column(String, primary_key=True, index=True)
       name = Column(String)
       hashed_password = Column(String, nullable=False)
       is_active = Column(Boolean, default=True)

