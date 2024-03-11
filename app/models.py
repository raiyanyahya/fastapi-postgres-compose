# app/models.py
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    todos = relationship("TodoList", back_populates="owner")


class TodoItem(Base):
    __tablename__ = "todo_items"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    deadline = Column(DateTime)
    completed = Column(Boolean, default=False)
    todo_list_id = Column(Integer, ForeignKey("todo_lists.id"))
    todo_list = relationship("TodoList", back_populates="items")


class TodoList(Base):
    __tablename__ = "todo_lists"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    items = relationship("TodoItem", back_populates="todo_list")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
