from fastapi import FastAPI
from . import models
from .database import engine
from .routers import todo, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the TODO List API!"}


app.include_router(user.router)
app.include_router(todo.router)
