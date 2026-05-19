from fastapi import FastAPI

from src.database import Base, engine, SessionLocal
from src.models import init_db
from src.routes import router


app = FastAPI()


Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


app.include_router(router)