import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import models
from database import engine, SessionLocal

# ----- Cargar variables de entorno (.env) -----
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ----- Iniciar app -----
app = FastAPI(title="Users API", version="1.0.0")

# ----- Crear tablas -----
models.Base.metadata.create_all(bind=engine)

# ----- Dependencia DB -----
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ----- Seguridad por header -----
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ----- Esquema Pydantic -----
class User(BaseModel):
    user_name: str = Field(min_length=1)
    user_id : int
    user_email: str = Field(min_length=1, max_length=100)
    age: Optional[int] = Field(None, gt=0)
    recommendations: List[str]= Field(min_items=1)
    ZIP: Optional[str] = None

# ----- Endpoints -----
@app.post("/api/v1/users/", tags=["users"])
def create_user(user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    existing_user = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail=f"The email '{user.user_email}' is already registered.")
    
    new_user = models.Users(
        user_name=user.user_name,
        user_id = user.user_id,
        user_email=user.user_email,
        age=user.age,
        recommendations = user.recommendations,
        ZIP=user.ZIP
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put("/api/v1/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    new_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if new_user is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    new_user.user_name = user.user_name
    new_user.user_email = user.user_email
    new_user.age = user.age
    new_user.recommendations = user.recommendations
    new_user.ZIP = user.ZIP

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/v1/users/{user_id}", tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    new_user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if new_user is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    return new_user

@app.delete("/api/v1/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    db.query(models.Users).filter(models.Users.user_id == user_id).delete()
    db.commit()
    return {"deleted_id": user_id}


