from fastapi import FastAPI
from app.routers import property

app = FastAPI()

app.include_router(property.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}
