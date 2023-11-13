"""Test router"""
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from db import get_db
from services.test_service import TestService

router = APIRouter()


@router.get("/test", tags=["Test"])
async def get_join(db: Session = Depends(get_db)):
    """Get join of workers and orders"""
    data = await TestService.get_join_of_workers_and_orders(db)
    return data


@router.get("/test/count", tags=["Test"])
async def get_orders_count(db: Session = Depends(get_db)):
    """Get join of workers and orders"""
    data = await TestService.get_orders_count_for_workers(db)
    return data


@router.get("/test/comlexity_level", tags=["Test"])
async def get_workers_with_complexity_level(
    complexity_level: int, db: Session = Depends(get_db)
):
    """Get workers with given comlexity level or bigger than that"""
    data = await TestService.get_workers_with_complexity_level(db, complexity_level)
    return data


@router.get("/test/update", tags=["Test"])
async def update_workers(new_post: str, db: Session = Depends(get_db)):
    """Update post of workers, whose real end date is less than deadline date"""
    await TestService.update_post(db, new_post)
    return "Workers are updated"
