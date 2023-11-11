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
