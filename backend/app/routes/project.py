from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.audit_logger import log_action
from database.pg_db import SessionLocal
from models.project import Project
from routes.deps import get_current_user
from schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create project
@router.post("",response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_project = Project(
        **project.dict(),
        user_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    log_action(
        db,
        action="CREATE",
        entity="PROJECT",
        entity_id=new_project.id,
        user_id=current_user.id,
        message="Project created"
    )

    db.refresh(new_project)
    return new_project

#Read
@router.get("/me",response_model=list[ProjectResponse])
def get_my_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    return db.query(Project).filter(Project.user_id == current_user.id).all()

#Update
@router.put("/{project_id}",response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project.dict().items():
        setattr(db_project, key, value)

    db.commit()
    log_action(
        db,
        action="UPDATE",
        entity="PROJECT",
        entity_id=db_project.id,
        user_id=current_user.id,
        message="Project updated"
    )


    db.refresh(db_project)
    return db_project

#Delete
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(db_project)
    log_action(
        db,
        action="DELETE",
        entity="PROJECT",
        entity_id=project_id,
        user_id=current_user.id,
        message="Project deleted"
    )

    db.commit()
    return {"msg": "Project deleted successfully"}