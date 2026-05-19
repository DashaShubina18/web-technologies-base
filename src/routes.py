from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User, Item, Detail, Tag
from src.schemas import UserCreate, UserSubmission
from src.auth import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter()
templates = Jinja2Templates(directory="templates")


USER_DATA = {
    "name": "Дар'я",
    "email": "shubinad268@gmail.com",
    "phone": "+380988749569",
    "telegram": "qxwsvm",
    "bio": "Студентка ВНТУ, вивчаю системний аналіз. Захоплююся програмуванням, проєктуванням баз даних та створенням сучасних веб-додатків",
    "role": "Системний аналітик",
    "skills": ["Python", "SQL", "System Analysis", "FastAPI", "Git"]
}



@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.name == user.name).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    db_user = User(
        name=user.name,
        hashed_password=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "msg": "User created",
        "name": db_user.name
    }
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.name == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.hashed_password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.name})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/profile")
def read_profile(current_user: str = Depends(get_current_user)):
    return {
        "name": current_user,
        "message": "This is a protected profile route"
    }



@router.get("/ping")
def ping():
    return {"message": "server works"}


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()

    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users
        }
    )


@router.post("/users/create")
def create_user(name: str = Form(...), db: Session = Depends(get_db)):
    user = User(name=name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "msg": "User created",
        "name": user.name
    }


@router.get("/items")
def list_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).all()

    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "items": items
        }
    )


@router.post("/items/create")
def create_item(
    name: str = Form(...),
    owner_id: int = Form(...),
    db: Session = Depends(get_db)
):
    item = Item(name=name, owner_id=owner_id)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "msg": "Item created",
        "name": item.name
    }


@router.get("/details")
def list_details(request: Request, db: Session = Depends(get_db)):
    details = db.query(Detail).all()

    return templates.TemplateResponse(
        "details.html",
        {
            "request": request,
            "details": details
        }
    )


@router.post("/details/create")
def create_detail(
    description: str = Form(...),
    item_id: int = Form(...),
    db: Session = Depends(get_db)
):
    detail = Detail(description=description, item_id=item_id)

    db.add(detail)
    db.commit()
    db.refresh(detail)

    return {
        "msg": "Detail created",
        "description": detail.description
    }


@router.get("/tags")
def list_tags(request: Request, db: Session = Depends(get_db)):
    tags = db.query(Tag).all()

    return templates.TemplateResponse(
        "tags.html",
        {
            "request": request,
            "tags": tags
        }
    )


@router.post("/tags/create")
def create_tag(name: str = Form(...), db: Session = Depends(get_db)):
    tag = Tag(name=name)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return {
        "msg": "Tag created",
        "name": tag.name
    }


@router.get("/public-profile")
def show_profile(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": USER_DATA
        }
    )



class EmailRequest(BaseModel):
    email: str


def handle_submission(data: UserSubmission):
    return f"Повідомлення від {data.name} з email {data.email} успішно отримано."


@router.post("/api/message")
async def handle_message(data: EmailRequest):
    return {
        "status": "success",
        "message": f"Привіт, {USER_DATA['name']}! Твій email ({data.email}) успішно отримано сервером через Fetch API."
    }


@router.post("/api/submit")
async def submit_form(data: UserSubmission):
    result = handle_submission(data)

    return {
        "status": "success",
        "data": data,
        "result": result
    }