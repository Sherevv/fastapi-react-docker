import strawberry

from app.db_request import get_portfolio_list, get_broker_list, get_portfolio, \
    get_broker, update_item, delete_item, create_item
from strawberry.fastapi import GraphQLRouter

from app.types import Portfolio, Broker, UpdatePortfolioInput, UpdatePortfolio, DeleteItemInput, DeletePortfolio, \
    CreatePortfolioInput, PortfolioOutput, UpdateBrokerInput, BrokerOutput, CreateBrokerInput
from app.models import Portfolio as PortfolioModel, Broker as BrokerModel


@strawberry.type
class Query:
    portfolios: list[PortfolioModel] = strawberry.field(resolver=get_portfolio_list)
    portfolio: Portfolio = strawberry.field(resolver=get_portfolio)
    brokers: list[Broker] = strawberry.field(resolver=get_broker_list)
    broker: Broker = strawberry.field(resolver=get_broker)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_portfolio(self, input: UpdatePortfolioInput | None) -> Portfolio:
        return await update_item(PortfolioModel, input)

    @strawberry.mutation
    async def delete_portfolio(self, input: DeleteItemInput | None) -> PortfolioOutput:
        item = await delete_item(PortfolioModel, input)
        return PortfolioOutput(portfolio=item)

    @strawberry.mutation
    async def create_portfolio(self, input: CreatePortfolioInput | None) -> PortfolioOutput:
        item = await create_item(PortfolioModel, input)
        return PortfolioOutput(portfolio=item)

    @strawberry.mutation
    async def update_broker(self, input: UpdateBrokerInput | None) -> Broker:
        return await update_item(BrokerModel, input)

    @strawberry.mutation
    async def delete_broker(self, input: DeleteItemInput | None) -> BrokerOutput:
        item = await delete_item(BrokerModel, input)
        return BrokerOutput(broker=item)

    @strawberry.mutation
    async def create_broker(self, input: CreateBrokerInput | None) -> BrokerOutput:
        item = await create_item(BrokerModel, input)
        return BrokerOutput(broker=item)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

graphql_app = GraphQLRouter(schema)
