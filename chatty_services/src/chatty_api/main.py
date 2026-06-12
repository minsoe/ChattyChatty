from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from chatty_api.bootstrap import bootstrap


@asynccontextmanager
async def lifespan(api: FastAPI):
    # Start up
    await bootstrap(api)
    yield
    # Shut down


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the chattychatty!"}
