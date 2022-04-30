from typing import Optional

import strawberry
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.db import async_session
from app.db_request import get_portfolio_list, create_portfolio, get_broker_list, get_portfolio, update_portfolio, \
    get_broker
from strawberry.fastapi import GraphQLRouter

from app.types import Portfolio, Broker, UpdatePortfolioInput, UpdatePortfolio, DeleteItemInput, DeletePortfolio, \
    CreatePortfolioInput, PortfolioOutput, UpdateBrokerInput, BrokerOutput, CreateBrokerInput
from app.models import Portfolio as PortfolioModel, Broker as BrokerModel


@strawberry.type
class Query:
    portfolios: list[Portfolio] = strawberry.field(resolver=get_portfolio_list)
    portfolio: Portfolio = strawberry.field(resolver=get_portfolio)
    brokers: list[Broker] = strawberry.field(resolver=get_broker_list)
    broker: Broker = strawberry.field(resolver=get_broker)


@strawberry.type
class Mutation:
    #create_portfolio: Portfolio = strawberry.field(resolver=create_portfolio)
    #update_portfolio: updatePortfolioInput = strawberry.field(resolver=update_portfolio)

    @strawberry.mutation
    async def update_portfolio(self, input: UpdatePortfolioInput | None) -> Portfolio:
        query = select(PortfolioModel).options(joinedload('*'))
        query = query.where(PortfolioModel.id == input.where.id)
        async with async_session() as session:
            result = await session.execute(query)
            item = result.scalars().unique().one()
            item.name = input.data.name
            if input.data.broker:
                item.broker_id = input.data.broker
            else:
                item.broker_id = None

            session.add(item)
            await session.commit()
            await session.refresh(item)
        return item

    @strawberry.mutation
    async def delete_portfolio(self, input: DeleteItemInput | None) -> PortfolioOutput:
        query = select(PortfolioModel)
        query = query.where(PortfolioModel.id == input.where.id)
        async with async_session() as session:
            result = await session.execute(query)
            item = result.scalars().unique().one()
            await session.delete(item)
            await session.commit()
        return PortfolioOutput(portfolio=item)

    @strawberry.mutation
    async def create_portfolio(self, input: CreatePortfolioInput | None) -> PortfolioOutput:
        item = PortfolioModel(name=input.data.name)
        if input.data.broker.id:
            item.broker_id = input.data.broker.id
        async with async_session() as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return PortfolioOutput(portfolio=item)

    @strawberry.mutation
    async def update_broker(self, input: UpdateBrokerInput | None) -> Broker:
        query = select(BrokerModel).options(joinedload('*'))
        query = query.where(BrokerModel.id == input.where.id)
        async with async_session() as session:
            result = await session.execute(query)
            item = result.scalars().unique().one()
            item.name = input.data.name
            session.add(item)
            await session.commit()
            await session.refresh(item)
        return item

    @strawberry.mutation
    async def delete_broker(self, input: DeleteItemInput | None) -> BrokerOutput:
        query = select(BrokerModel)
        query = query.where(BrokerModel.id == input.where.id)
        async with async_session() as session:
            result = await session.execute(query)
            item = result.scalars().unique().one()
            await session.delete(item)
            await session.commit()
        return BrokerOutput(broker=item)

    @strawberry.mutation
    async def create_broker(self, input: CreateBrokerInput | None) -> BrokerOutput:
        item = BrokerModel(name=input.data.name)
        async with async_session() as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return BrokerOutput(broker=item)



schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

graphql_app = GraphQLRouter(schema)
