"""Projects router"""
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from db import get_db
from services.projects_service import ProjectService
import schemas

router = APIRouter()


@router.get("/projects", tags=["Projects"], response_model=List[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    workers = ProjectService.all(db)
    if workers and len(workers):
        return workers
    else:
        raise HTTPException(status_code=400, detail="Project are empty or don't exist")


@router.get("/projects/{project_id}", tags=["Projects"], response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by project_id"""
    worker = ProjectService.get_by_id(db, project_id)
    if worker:
        return worker
    else:
        raise HTTPException(
            status_code=400, detail="Project not found with the given project_id"
        )


@router.post("/projects", tags=["Projects"], response_model=schemas.Project)
async def create_project(
    project_request: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    """Create project with input data"""
    worker = await ProjectService.create(db, project_request)
    if worker:
        return worker
    else:
        raise HTTPException(status_code=400, detail="Can't create project")


@router.delete("/projects/{project_id}", tags=["Projects"])
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete project by project_id"""
    await ProjectService.delete(db, project_id)
    return f"Project {project_id} deleted!"


@router.put("/projects/{project_id}", tags=["Projects"], response_model=schemas.Project)
async def update_project(
    project_id: int,
    project_request: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    """Update project with input data"""
    db_project = ProjectService.get_by_id(db, project_id)
    if db_project:
        update_project_encoded = jsonable_encoder(project_request)
        db_project.name = update_project_encoded["name"]
        db_project.description = update_project_encoded["description"]
        db_project.end_date = update_project_encoded["end_date"]
        db_project.complexity_level = update_project_encoded["complexity_level"]
        return await ProjectService.update(db, db_project)
    else:
        raise HTTPException(
            status_code=400, detail="Project not found with the given project_id"
        )
