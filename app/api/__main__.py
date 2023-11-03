"""FastAPI main entrypoint of NoxU app."""

from fastapi import FastAPI
from app.api.routers import analyse

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(analyse.router)
