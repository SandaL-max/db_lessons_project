from sqlalchemy.orm import Session
from models.project import Project

from schemas import ProjectBase, ProjectCreate


class ProjectController:
    @staticmethod
    def all(db: Session):
        return db.query(Project).order_by(Project.cipher).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Project).get(id)

    @staticmethod
    async def create(db: Session, project: ProjectCreate):
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
    async def delete(db: Session, id: int):
        db.delete(db.query(Project).get(id))
        db.commit()

    @staticmethod
    async def update(db: Session, project_data):
        updated_project = db.merge(project_data)
        db.commit()
        return updated_project
