"""FastAPI main entrypoint of NoxU app."""

from fastapi import FastAPI
from app.api.routers import users, statuses, items
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(users.router)
app.include_router(statuses.router)
app.include_router(items.router)
