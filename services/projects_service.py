"""Module of Project controller"""
from sqlalchemy.orm import Session
from models.project import Project

from schemas import ProjectCreate


class ProjectService:
    """Project Service"""

    @staticmethod
    async def all(db: Session, per_page: int, page: int, order_by: str):
        """Get all projects"""
        if order_by == "cipher":
            order_obj = Project.cipher
        elif order_by == "name":
            order_obj = Project.name
        elif order_by == "complexity_level":
            order_obj = Project.complexity_level
        else:
            order_obj = Project.cipher
        return (
            db.query(Project)
            .order_by(order_obj)
            .slice(page * per_page, page * per_page + per_page)
            .all()
        )

    @staticmethod
    async def get_by_id(db: Session, id_: int):
        """Get project by id"""
        return db.query(Project).get(id_)

    @staticmethod
    async def get_by_name(db: Session, name: str):
        """Get project by name"""
        return db.query(Project).filter(Project.name == name).first()

    @staticmethod
    async def create(db: Session, project: ProjectCreate):
        """Create Project"""
        db_project = Project(
            name=project.name,
            description=project.description,
            end_date=project.end_date,
            complexity_level=project.complexity_level,
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    async def delete(db: Session, id_: int):
        """Delete Project"""
        db.delete(db.query(Project).get(id_))
        db.commit()

    @staticmethod
    async def update(db: Session, project_data):
        """Update Project"""
        updated_project = db.merge(project_data)
        db.commit()
        return updated_project
