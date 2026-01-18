from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes import device, logs, rules, simulation, network
from app.database.db import Base, engine

app = FastAPI(title="Network Security Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(device.router)
app.include_router(logs.router)
app.include_router(rules.router)
app.include_router(simulation.router)
app.include_router(network.router)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")
