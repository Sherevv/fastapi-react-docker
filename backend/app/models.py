from typing import Optional, List, Union
from uuid import UUID
import uuid
import strawberry
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel.sql.sqltypes import GUID


def fix_uuid() -> uuid.UUID:
    # Note: Work around UUIDs with leading zeros: https://github.com/tiangolo/sqlmodel/issues/25
    # by making sure uuid str does not start with a leading 0
    val = uuid.uuid4()
    while val.hex[0] == '0':
        val = uuid.uuid4()

    return val


class Portfolio(SQLModel, table=True):
    id: Optional[UUID] = Field(
        default_factory=fix_uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str
    broker_id: Optional[UUID] = Field(sa_column=Column('broker_id', GUID(),
                                                       ForeignKey('broker.id', name='fk_portfolio_broker_id')))
    # Field(default=None, foreign_key="broker.id")

    broker: Optional["Broker"] = Relationship(
        sa_relationship=RelationshipProperty("Broker",
                                             back_populates="portfolios",
                                             lazy='subquery'))

    # Field(sa_column=Column('broker_id', Integer, ForeignKey('broker.id', name='fk_portfolio_broker_id')))

    class Config:
        arbitrary_types_allowed = True


class Broker(SQLModel, table=True):
    id: Optional[UUID] = Field(
        default_factory=fix_uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str

    portfolios: List["Portfolio"] = Relationship(sa_relationship=RelationshipProperty("Portfolio",
                                                                                      back_populates="broker",
                                                                                      lazy='subquery'))
