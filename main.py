from fastapi import FastAPI
from database import engine, Base
from routers import users
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

@app.get("/main")
def main():
    return {"message":"Welcome to main page of first application!"}

