# todo.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from ..crud import get_current_user

router = APIRouter()


@router.post("/todos/", response_model=schemas.TodoList)
def create_todo_list(
    todo: schemas.TodoListCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_todo_list(db=db, todo=todo, user_id=current_user.id)


@router.get("/todos/", response_model=List[schemas.TodoList])
def read_todo_lists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todo_lists = crud.get_todo_lists(db, skip=skip, limit=limit)
    return todo_lists


@router.get("/todos/{todo_id}", response_model=schemas.TodoList)
def read_todo_list(todo_id: int, db: Session = Depends(get_db)):
    db_todo_list = crud.get_todo_list(db, todo_id=todo_id)
    if db_todo_list is None:
        raise HTTPException(status_code=404, detail="TodoList not found")
    return db_todo_list


@router.put("/todos/{todo_id}", response_model=schemas.TodoList)
def update_todo_list(
    todo_id: int, todo_list: schemas.TodoListCreate, db: Session = Depends(get_db)
):
    return crud.update_todo_list(db=db, todo_id=todo_id, todo_list=todo_list)


@router.delete("/todos/{todo_id}", response_model=schemas.TodoList)
def delete_todo_list(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo_list(db=db, todo_id=todo_id)


@router.post("/todos/{todo_list_id}/items/", response_model=schemas.TodoItem)
def create_todo_item(
    todo_list_id: int,
    item: schemas.TodoItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    todo_list = crud.get_todo_list(db, todo_list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="TODO list not found")
    if todo_list.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to add items to this TODO list",
        )
    return crud.create_todo_item(db=db, todo_item=item, todo_list_id=todo_list_id)
