from contextlib import asynccontextmanager

from fastapi import FastAPI

from chattychatty.bootstrap import bootstrap


@asynccontextmanager
async def lifespan(api: FastAPI):
    # Start up
    await bootstrap(api)
    yield
    # Shut down
    # await cleanup()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the chattychatty!"}
