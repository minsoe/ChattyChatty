from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bootstrap.bootstrap import bootstrap


@asynccontextmanager
async def lifespan(api: FastAPI):
    await bootstrap(api)
    yield

app = FastAPI(lifespan=lifespan)
