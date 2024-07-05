# from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Job, Resum
from src.schemas import Filters, FiltersResums, Statistics
from sqlalchemy import func, or_, select, update

async def add_jobs(db: AsyncSession, datalist):
    for data in datalist:
        check = await db.execute(select(Job).filter(Job.link == data[7]))
        if check.scalars().first() is None:
            # print(data)
            db_jobs = Job(title=data[0],min_price=int(data[1]),experience=data[2],company=data[3],city=data[4], req_resume=data[5],remote=data[6],link=data[7])
            db.add(db_jobs)
    await db.commit()

async def list_jobs(db: AsyncSession):
    result = await db.execute(select(Job).limit(500))
    return result.scalars().all()

async def list_jobs_filter(db: AsyncSession, filter: Filters):
    if filter.city == "":
        if filter.req_resume:
            result = await db.execute(select(Job).filter(filter.salary<=Job.min_price,filter.experience<=Job.experience,Job.req_resume==False,filter.remote==Job.remote).limit(100))
        else:
            result = await db.execute(select(Job).filter(filter.salary<=Job.min_price,filter.experience<=Job.experience,filter.remote==Job.remote).limit(100))
    else:
        if filter.req_resume:
            result = await db.execute(select(Job).filter(filter.salary<=Job.min_price,filter.experience<=Job.experience,Job.req_resume==False,filter.remote==Job.remote, Job.city.like(filter.city)).limit(100))
        else:
            result = await db.execute(select(Job).filter(filter.salary<=Job.min_price,filter.experience<=Job.experience,filter.remote==Job.remote, Job.city.like(filter.city)).limit(100))
    return result.scalars().all()

async def statistics_job(db: AsyncSession):
    total_jobs = await db.execute(select(func.count()).select_from(Job))
    return total_jobs

async def add_resums(db: AsyncSession, datalist):
    for data in datalist:
        check = await db.execute(select(Resum).filter(Resum.link == data[6]))
        if check.scalars().first() is None:
            # print(data)
            db_resums = Resum(title=data[0],age=data[1],salary=data[2],experience=data[3],status=data[4], last_company=data[5],link=data[6])
            db.add(db_resums)
        else:
            await db.execute(update(Resum).filter(Resum.link==data[6]).values(status=data[4]))
    await db.commit()

async def list_resums(db: AsyncSession):
    result = await db.execute(select(Resum).limit(500))
    return result.scalars().all()

async def list_resums_filter(db: AsyncSession, filter: FiltersResums):
    if filter.status:
        result = await db.execute(select(Resum).filter(filter.max_salary>=Resum.salary,filter.experience<=Resum.experience,\
                                                       or_(Resum.status=="Активно ищет работу", Resum.status=="Рассматривает предложения", Resum.status=="Предложили работу, решает")).\
                                                        limit(100))
    else:
        result = await db.execute(select(Resum).filter(filter.max_salary>=Resum.salary,filter.experience<=Resum.experience).limit(100))
    return result.scalars().all()

async def statistics_resum(db: AsyncSession):
    total_resums = await db.execute(select(func.count()).select_from(Resum))
    return total_resums

async def statistics(db: AsyncSession):
    total_jobs = await db.execute(select(func.count()).select_from(Job))
    total_resums = await db.execute(select(func.count()).select_from(Resum))
    total_jobs, total_resums = total_jobs.scalar_one(), total_resums.scalar_one()
    return Statistics(jobs=total_jobs, resums=total_resums, summ=total_jobs + total_resums)