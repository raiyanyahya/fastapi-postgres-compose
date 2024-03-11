# app/crud.py
import os
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import models, schemas, database
from .security import get_password_hash, verify_password

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoList).offset(skip).limit(limit).all()


def get_todo_list(db: Session, todo_id: int):
    return db.query(models.TodoList).filter(models.TodoList.id == todo_id).first()


def create_user_todo(db: Session, todo: schemas.TodoListCreate, user_id: int):
    db_todo = models.TodoList(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def create_todo_item(db: Session, todo_item: schemas.TodoItemCreate, todo_list_id: int):
    db_todo_item = models.TodoItem(**todo_item.dict(), todo_list_id=todo_list_id)
    db.add(db_todo_item)
    db.commit()
    db.refresh(db_todo_item)
    return db_todo_item


def create_todo_list(db: Session, todo: schemas.TodoListCreate, user_id: int):
    db_todo = models.TodoList(title=todo.title, owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    for item in todo.items:
        db_item = models.TodoItem(
            description=item.description,
            deadline=item.deadline,
            todo_list_id=db_todo.id,
        )
        db.add(db_item)

    db.commit()
    return db_todo


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
