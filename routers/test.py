"""Test router"""
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from db import get_db
from services.test_service import TestService
import schemas

router = APIRouter()


@router.get("/test", tags=["Test"])
async def get_join(db: Session = Depends(get_db)):
    data = await TestService.get_join_of_workers_and_orders(db)
    return data
