# app/schemas.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class TodoItem(BaseModel):
    description: str
    deadline: Optional[datetime] = None  # Add the deadline attribute
    completed: bool


class TodoListBase(BaseModel):
    title: str


class TodoListCreate(TodoListBase):
    items: List[TodoItem]


class TodoList(TodoListBase):
    id: int
    owner_id: int
    items: List[TodoItem]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    todos: List[TodoList] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TodoItemCreate(BaseModel):
    description: str
    deadline: Optional[datetime] = None
    completed: bool = False
