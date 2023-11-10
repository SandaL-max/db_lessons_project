"""Programm entry point"""
import socket
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db import engine, Base
from routers import workers, projects, orders

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(workers.router)
app.include_router(projects.router)
app.include_router(orders.router)


# Testing
@app.get("/", include_in_schema=False)
async def docs_redirect():
    """Redirect from / to /docs"""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    uvicorn.run(
        app="main:app", host=ip_address, port=8000, log_level="info", reload=True
    )
