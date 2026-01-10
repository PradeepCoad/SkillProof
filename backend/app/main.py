from fastapi import FastAPI
from routes import auth, user, project, skill
from database.pg_db import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.routes, prefix="/auth")
app.include_router(user.router)
app.include_router(project.router)
app.include_router(skill.router)