from sqlalchemy import Column, Integer, String
from database import Base

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    domain = Column(String)
    target_role = Column(String)
    skills = Column(String) 

class AcademiaDB(Base):
    __tablename__ = "academia"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    institution_type = Column(String)

class IndustryDB(Base):
    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    industry = Column(String)