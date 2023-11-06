
from app.api.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/analyse",
                   tags=["Analyse"], responses={404: {"description": "Not found"}})
