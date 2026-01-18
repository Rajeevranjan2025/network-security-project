# from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware

# from app.routes import device, logs, rules
# from app.database.db import Base, engine


# app = FastAPI(title="Network Security Management System")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Base.metadata.create_all(bind=engine)

# app.include_router(device.router)
# app.include_router(logs.router)
# app.include_router(rules.router)

# @app.get("/")
# def home():
#     return {"message": "System Running Successfully"}



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import device, logs, rules, simulation
from app.database.db import Base, engine

app = FastAPI(title="Network Security Management System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(device.router)
app.include_router(logs.router)
app.include_router(rules.router)
app.include_router(simulation.router)

@app.get("/")
def home():
    return {"message": "System Running Successfully"}
