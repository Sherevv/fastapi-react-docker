from typing import Optional
from uuid import UUID

import strawberry
from sqlalchemy.orm import joinedload, selectinload
from strawberry.scalars import JSON
from sqlmodel import select, SQLModel
from app.graphql import WhereParser
from app.models import Portfolio, Broker
from app.db import async_session
from app.types import Portfolio as PortfolioType


async def update_item(model, input):
    query = select(model)
    query = query.where(model.id == input.where.id)

    async with async_session() as session:
        result = await session.execute(query)
        item = result.scalars().unique().one()
        for key, value in dict(input.data.__dict__).items():
            setattr(item, key, value)
        session.add(item)
        await session.commit()
        await session.refresh(item)
    return item


async def delete_item(model, input):
    query = select(model)
    query = query.where(model.id == input.where.id)
    async with async_session() as session:
        result = await session.execute(query)
        item = result.scalars().unique().one()
        await session.delete(item)
        await session.commit()
    return item


async def create_item(model, input):
    item = model()
    for key, value in dict(input.data.__dict__).items():
        setattr(item, key, value)
    async with async_session() as session:
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item


async def get_list(
                    model,
                    sort: str | None = None,
                    start: int | None = None,
                    limit: int | None = None,
                    where: Optional[JSON] = None
            ) -> list:

    query = select(model)
    print(model)
    query = WhereParser(model, query, sort, start, limit, where).prepare_query()

    async with async_session() as session:
        result = await session.execute(query)
        session.expunge_all()
        items = result.scalars().unique().all()

        return items


async def get_by_id(model, id: strawberry.ID):
    query = select(model)
    query = query.where(model.id == id)

    async with async_session() as session:
        result = await session.execute(query)
        session.expunge_all()
        item = result.scalars().first()

    return item


async def get_portfolio_list(
                         sort: str | None = None,
                         start: int | None = None,
                         limit: int | None = None,
                         where: Optional[JSON] = None
                         ) -> list[PortfolioType]:

    return await get_list(Portfolio, sort, start, limit, where)


async def get_portfolio(id: strawberry.ID):
    return await get_by_id(Portfolio, id)


async def get_broker_list(
            sort: str | None = None,
            start: int | None = None,
            limit: int | None = None,
            where: Optional[JSON] = None
    ):

    return await get_list(Broker, sort, start, limit, where)


async def get_broker(id: strawberry.ID):
    return await get_by_id(Broker, id)

