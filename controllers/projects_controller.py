"""Module of Project controller"""
from sqlalchemy.orm import Session
from models.project import Project

from schemas import ProjectCreate


class ProjectController:
    """Project controller"""

    @staticmethod
    def all(db: Session):
        """Get all projects"""
        return db.query(Project).order_by(Project.cipher).all()

    @staticmethod
    def get_by_id(db: Session, id_: int):
        """Get project by id"""
        return db.query(Project).get(id_)

    @staticmethod
    async def create(db: Session, project: ProjectCreate):
        """Create Project"""
        db_project = Project(
            name=project.name,
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
