from fastapi import APIRouter
from app.routes.brokers import router as brokers_router
from app.routes.portfolios import router as portfolios_router
from app.routes.tasks import router as tasks_router

router = APIRouter()
router.include_router(brokers_router, prefix="/broker", tags=["brokers"])
router.include_router(
    portfolios_router, prefix="/portfolio", tags=["portfolios"])
router.include_router(tasks_router, prefix="/task", tags=["tasks"])
