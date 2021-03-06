from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def crete_user(user: schemas.UserCreate, db : Session = Depends(get_db)):
    user.password = utils.hashed(user.password)

    user_email = db.query(models.User).filter(models.User.email == user.email).first()

    if user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"email: {user.email} already exist")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db : Session = Depends(get_db)):
    user_query= db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return user