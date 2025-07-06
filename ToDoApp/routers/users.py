from fastapi import Depends, HTTPException, Path, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos, Users
from database import SessionLocal
from pydantic import BaseModel, Field
from routers.auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
        # only code before yield is executed before sending a respone and later code is run after sending a response
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class UserProfileUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    phone_number: str = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: str
    phone_number: str
    is_active: bool


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/user/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put('/user/phone/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency,
                               phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()


@router.get('/me', status_code=status.HTTP_200_OK)
async def get_current_user_profile(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user_profile(user: user_dependency, db: db_dependency,
                              profile_update: UserProfileUpdate):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    # Update only the fields that are provided
    if profile_update.first_name is not None:
        user_model.first_name = profile_update.first_name
    if profile_update.last_name is not None:
        user_model.last_name = profile_update.last_name
    if profile_update.phone_number is not None:
        user_model.phone_number = profile_update.phone_number
    
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    
    return user_model