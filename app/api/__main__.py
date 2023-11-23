"""FastAPI main entrypoint of NoxU app."""

from fastapi import FastAPI
from app.api.routers import analyse, users, items, orders, order_content, production_log, qrcodes
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(analyse.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(orders.router)
app.include_router(order_content.router)
app.include_router(production_log.router)
