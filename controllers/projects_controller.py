from sqlalchemy.orm import Session
from models.project import Project

class ProjectController:
    
    @staticmethod
    def all(db: Session):
        projects = db.query(Project).order_by(Project.cipher).all()
        projects_list = []
        for project in projects:
            projects_list.append(project.to_dict())
        return projects_list
    
    @staticmethod
    def get_by_id(db: Session, id: int):
        project = db.query(Project).get(id)
        if project:
            return project.to_dict()
        else:
            return None