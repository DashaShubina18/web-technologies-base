from fastapi import FastAPI
from src.database import engine, Base
from src.routes import router
from src.config import static_files
from src.models import init_db
from src.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", static_files, name="static")
app.include_router(router)

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    init_db(db)
