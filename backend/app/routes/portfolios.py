from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session

from app.models import Portfolio

router = APIRouter()


@router.get("/", response_model=List[Portfolio])
async def read_portfolio(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Portfolio))
    items = result.scalars().unique().all()
    return items


@router.get("/{portfolio_id}", response_model=Portfolio)
async def read_portfolioo(*,
                          portfolio_id: UUID,
                          session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Portfolio).where(Portfolio.id == portfolio_id))
    session.expunge_all()
    items = result.scalars().unique().all()
    return items


@router.post("/", response_model=Portfolio)
async def create_portfolio(*,
                           session: AsyncSession = Depends(get_session),
                           item: Portfolio):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
