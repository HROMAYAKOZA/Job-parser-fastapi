from pydantic import BaseModel, ConfigDict
from typing import Optional

class Filters(BaseModel):
    salary: int
    city: str
    experience: int
    remote: bool
    req_resume: bool

class JobSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    min_price: int
    experience: int
    city: str
    remote: bool
    req_resume: bool
    link: str

class FiltersResums(BaseModel):
    max_salary: int
    experience: int
    status: bool

class ResumSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    salary: int
    experience: int
    status: Optional[str]="Неизвестно"
    last_company: Optional[str]="Неизвестно"
    link: str

class Statistics(BaseModel):
    jobs: int
    resums: int
    summ: int