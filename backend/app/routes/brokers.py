from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Broker
from app.db import get_session

router = APIRouter()


@router.get("/", response_model=List[Broker])
async def read_broker(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Broker))
    items = result.scalars().unique().all()
    return items


@router.post("/", response_model=Broker)
async def create_broker(*,
                        session: AsyncSession = Depends(get_session),
                        item: Broker):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
