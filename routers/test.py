"""Test router"""
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from db import get_db
from services.test_service import TestService

router = APIRouter()


@router.get("/test", tags=["Test"])
async def get_join(
    per_page: int = 10,
    page: int = 0,
    db: Session = Depends(get_db),
):
    """get join of workers and orders"""
    data = await TestService.get_join_of_workers_and_orders(db, per_page, page)
    if data:
        return data
    else:
        raise HTTPException(status_code=400, detail="Join is empty or doesn't exist")


@router.get("/test/count", tags=["Test"])
async def get_orders_count(
    per_page: int = 10,
    page: int = 0,
    db: Session = Depends(get_db),
):
    """get orders count"""
    data = await TestService.get_orders_count_for_workers(db, per_page, page)
    if data:
        return data
    else:
        raise HTTPException(status_code=400, detail="Workers with orders don't exist")


@router.get("/test/comlexity_level", tags=["Test"])
async def get_workers_with_complexity_level(
    complexity_level: int,
    per_page: int = 10,
    page: int = 0,
    db: Session = Depends(get_db),
):
    """get workers with given comlexity level or bigger than that"""
    data = await TestService.get_workers_with_complexity_level(
        db, complexity_level, per_page, page
    )
    if data:
        return data
    else:
        raise HTTPException(
            status_code=400,
            detail="Workers with given complexity level are empty or doesn't exist",
        )


@router.get("/test/update", tags=["Test"])
async def update_workers(new_post: str, db: Session = Depends(get_db)):
    """Update get of workers, whose real end date is less than deadline date"""
    await TestService.update_post(db, new_post)
    return "Workers are updated"


@router.get("/test/generate_workers/{quantity}", tags=["Generators"])
async def generate_workers_by_quantity(quantity: int, db: Session = Depends(get_db)):
    """Generate some workers"""
    return await TestService.generate_workers_by_quantity(db, quantity)


@router.get("/test/generate_projects/{quantity}", tags=["Generators"])
async def generate_projects_by_quantity(quantity: int, db: Session = Depends(get_db)):
    """Generate some projects"""
    return await TestService.generate_projects_by_quantity(db, quantity)


@router.get("/test/generate_orders/{quantity}", tags=["Generators"])
async def generate_orders_by_quantity(
    quantity: int,
    project_id_start: int,
    project_id_end: int,
    worker_id_start: int,
    worker_id_end: int,
    db: Session = Depends(get_db),
):
    """Generate some workers"""
    return await TestService.generate_orders_by_quantity(
        db,
        quantity,
        (project_id_start, project_id_end),
        (worker_id_start, worker_id_end),
    )


@router.get("/test/get_median_of_salaries", tags=["Test"])
async def get_salary_median(db: Session = Depends(get_db)):
    """Get median of salaries"""
    data = await TestService.get_salary_median(db)
    if data:
        return data
    else:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong when median has calculated",
        )
