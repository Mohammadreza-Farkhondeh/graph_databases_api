from fastapi import FastAPI, Request
from middlewares import set_client

app = FastAPI()


@app.middleware("http")
async def orient_middle_ware(request: Request, call_next):
    await set_client(request)
    response = await call_next(request)
    return response
