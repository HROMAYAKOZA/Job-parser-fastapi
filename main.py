from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import uvicorn
from typing import List
import src.crud as crud
import src.schemas as schemas
from src.crud import add_jobs, add_resums
from src.parse_hh import hhru_parse_job, hhru_parse_resum
from src.database import db_helper, Base
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to db...")
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_helper.dispose()

# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000"
# ]

app = FastAPI(lifespan=lifespan)

app.state.PARSED_JOBS_SESSION = False
app.state.PARSED_RESUMS_SESSION = False
app.state.PARSED_PAGES = 3

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/jobs")
async def jobs(db: AsyncSession = Depends(db_helper.session_getter)):
    if not app.state.PARSED_JOBS_SESSION:
        # await add_jobs(db, hhru_parse_job("https://hh.ru/search/vacancy?text=&area=1"))
        for i in range(1,app.state.PARSED_PAGES+1):
            # print(f"parsing page {i}")
            datalist = hhru_parse_job(f"https://hh.ru/search/vacancy?text=&area=1&page={i}")
            await add_jobs(db, datalist)
        app.state.PARSED_JOBS_SESSION=True
    return await crud.list_jobs(db)

@app.get("/listall")
async def listalljobs(db: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.list_jobs(db) + crud.list_resums(db)

@app.post("/jobs_f", response_model=list[schemas.JobSchema])
async def listfilteredjobs(filters: schemas.Filters, db: AsyncSession = Depends(db_helper.session_getter)):
    print(filters)
    response = await crud.list_jobs_filter(db, filters)
    return response

@app.get("/resums")
async def resums(db: AsyncSession = Depends(db_helper.session_getter)):
    if not app.state.PARSED_RESUMS_SESSION:
        # await add_resums(db, hhru_parse_resum("https://hh.ru/search/resume?text=&area=1&items_on_page=100"))
        for i in range(1,app.state.PARSED_PAGES+1):
            datalist = hhru_parse_resum(f"https://hh.ru/search/resume?text=&area=1&items_on_page=100&page={i}")
            await add_resums(db, datalist)
        app.state.PARSED_RESUMS_SESSION=True
    return await crud.list_resums(db)

@app.post("/resums_f", response_model=list[schemas.ResumSchema])
async def listfilteredjobs(filters: schemas.FiltersResums, db: AsyncSession = Depends(db_helper.session_getter)):
    print(filters)
    response = await crud.list_resums_filter(db, filters)
    return response

@app.get("/statistics", response_model=schemas.Statistics)
async def statistics(db: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.statistics(db)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0",port=8000)
