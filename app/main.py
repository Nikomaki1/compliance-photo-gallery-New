from fastapi import FastAPI
from app.routers import property
from app.database import engine, Base
from app.models import orm_models

# This generates the SQLite database file and tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}
