from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime
from schemas.user import UserCreate , UserLogin
from models.user import User 
from database.pg_db import Base, engine
from database.pg_db import SessionLocal


routes = APIRouter(tags=["auth"])


Base.metadata.create_all(bind=engine)
SECRET_KEY = "8b21aee3c92b57e91315fafaad69118aa49323bd4edbdb30eb2e5227e62af6d9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@routes.post("/register")
async def register_user(user: UserCreate, db : Session =Depends(get_db)):

    existing_user = db.query(User).filter((User.email == user.email) | (User.name == user.name)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    
    new_user = User(name=user.name, email=user.email, hashed_password=pwd_context.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User registered successfully"}

# @routes.post("/login")
# async def login_user(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter((User.name == user.name)).first()

#     if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid password")
    
#     token = create_access_token({"sub" : db_user.name})
#     return {"access_token": token, "token_type": "bearer"}

@routes.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.name == form_data.username
    ).first()

    if not db_user or not pwd_context.verify(
        form_data.password, db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.name}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

