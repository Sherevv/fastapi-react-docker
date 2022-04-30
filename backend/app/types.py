import strawberry
from typing import Optional, Union
from uuid import UUID


@strawberry.type
class Broker:
    id: UUID
    name: str
    portfolios: list['Portfolio']


@strawberry.type
class Portfolio:
    id: UUID
    name: str
    broker: Optional[Broker]
    broker_id: UUID


@strawberry.input
class UpdateBrokerPortfolio:
    id: Union[UUID, None] = None


@strawberry.input
class UpdatePortfolio:
    name: str
    broker: Optional[UUID] = None


@strawberry.input
class WhereID:
    id: UUID


@strawberry.input
class UpdatePortfolioInput:
    where: WhereID
    data: UpdatePortfolio


@strawberry.type
class DeletePortfolio:
    id: UUID
    portfolio: Portfolio


@strawberry.input
class DeleteItemInput:
    where: WhereID


@strawberry.type
class PortfolioOutput2:
    id: UUID


@strawberry.type
class PortfolioOutput:
    # id: UUID
    portfolio: PortfolioOutput2


@strawberry.input
class CreatePortfolio:
    name: str
    broker: UpdateBrokerPortfolio


@strawberry.input
class CreatePortfolioInput:
    data: CreatePortfolio



@strawberry.type
class BrokerOutput2:
    id: UUID


@strawberry.type
class BrokerOutput:
    broker: BrokerOutput2


@strawberry.input
class UpdateBroker:
    name: str


@strawberry.input
class CreateBroker:
    name: str


@strawberry.input
class WhereID:
    id: UUID


@strawberry.input
class UpdateBrokerInput:
    where: WhereID
    data: UpdateBroker


@strawberry.input
class CreateBrokerInput:
    data: CreateBroker
