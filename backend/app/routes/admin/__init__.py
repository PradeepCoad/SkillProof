from fastapi import APIRouter

from routes.admin import auth, logs, users, skill, questions

router = APIRouter()

router.include_router(auth.router)
router.include_router(logs.router)
router.include_router(users.router)
router.include_router(skill.router)
router.include_router(questions.router)