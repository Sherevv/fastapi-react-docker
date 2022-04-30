from typing import List
from uuid import UUID

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.models import Portfolio, Broker, PortfolioRead
from app.schema import graphql_app

app = FastAPI(title="FastAPI, Docker and others")
app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World1"}


@app.get("/portfolio/", response_model=List[Portfolio])
async def read_portfolio(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Portfolio))
    items = result.scalars().all()
    return items


@app.get("/portfolio/{portfolio_id}", response_model=Portfolio)
async def read_portfolioo(*,
                          portfolio_id: UUID,
                          session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Portfolio).where(Portfolio.id == portfolio_id))
    session.expunge_all()
    items = result.scalars().all()
    return items


@app.post("/portfolio/", response_model=Portfolio)
async def create_portfolio(*,
                           session: AsyncSession = Depends(get_session),
                           item: Portfolio):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@app.get("/broker/", response_model=List[Broker])
async def read_broker(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Broker))
    items = result.scalars().all()
    return items


@app.post("/broker/", response_model=Broker)
async def create_broker(*,
                        session: AsyncSession = Depends(get_session),
                        item: Broker):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
