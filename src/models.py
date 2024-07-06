from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    min_price = Column(Integer)
    experience = Column(Integer)
    company = Column(String)
    city = Column(String)
    req_resume = Column(Boolean)
    remote = Column(Boolean)
    link = Column(String)

class Resum(Base):
    __tablename__ = "resums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    age = Column(Integer)
    salary = Column(Integer)
    experience = Column(Integer)
    status = Column(String)
    last_company = Column(String)
    link = Column(String)