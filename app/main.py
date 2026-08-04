from app.database import engine
from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(title="Medical Assistant API")
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the Medical Assistant API!"}