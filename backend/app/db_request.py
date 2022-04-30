from typing import Optional
from uuid import UUID

import strawberry
from sqlalchemy.orm import joinedload
from strawberry.scalars import JSON
from sqlmodel import select
from app.graphql import prepare_query
from app.models import Portfolio, Broker
from app.db import async_session
from app.types import UpdatePortfolioInput


async def create_portfolio(name: str):
    item = Portfolio(name=name)
    async with async_session() as session:
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item


async def update_portfolio(input: UpdatePortfolioInput) -> UpdatePortfolioInput:
    query = select(Portfolio).options(joinedload('*'))
    query = query.where(Portfolio.id == input.where.id)
    async with async_session() as session:
        result = await session.execute(query)
        item = result.scalars().one()
        item.name = input.data.name
        item.broker_id = input.data.broker.id

        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item


async def get_portfolio_list(
                         name: str | None = None,
                         sort: str | None = None,
                         start: int | None = None,
                         limit: int | None = None,
                         where: Optional[JSON] = None
                         ):
    query = select(Portfolio).options(joinedload('*'))
    query = prepare_query(query, sort, start, limit, where)

    if name:
        query = query.where(Portfolio.name == name)

    async with async_session() as session:
        result = await session.execute(query)
        session.expunge_all()
        items = result.scalars().unique().all()

    return items


async def get_portfolio(id: strawberry.ID):
    query = select(Portfolio).options(joinedload('*'))
    #query = prepare_query(query, None, None, None, None)
    query = query.where(Portfolio.id == id)

    async with async_session() as session:
        result = await session.execute(query)
        session.expunge_all()
        item = result.scalars().first()

    return item


async def get_broker_list(
        name: str | None = None,
        sort: str | None = None,
        start: int | None = None,
        limit: int | None = None,
        where: Optional[JSON] = None
):
    query = select(Broker)
    query = prepare_query(query, sort, start, limit, where)

    if name:
        query = query.where(Broker.name == name)

    async with async_session() as session:
        result = await session.execute(query)
        session.expunge_all()
        items = result.scalars().unique().all()

    return items


async def get_broker(id: strawberry.ID):
    query = select(Broker).options(joinedload('*'))
    query = query.where(Broker.id == id)

    async with async_session() as session:
        result = await session.execute(query)
        session.expunge_all()
        item = result.scalars().first()

    return item

