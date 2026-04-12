from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.router import router

app = FastAPI(title="Products API")

app.include_router(router)


@app.get("/error", tags=["debug"])
def cause_error():
    raise RuntimeError("Something went wrong on server")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
