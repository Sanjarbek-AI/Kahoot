from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas
from ..database import get_db
from ..auth.utils import hash

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    if user.password1 != user.password2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password1 is not equal to password2")

    check_user = db.query(models.User).filter(models.User.email == user.email).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"user with this email is already exists {user.email}")

    hashed_password = hash(user.password1)

    new_user = models.User(password=hashed_password, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
