from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas
from ..game import models as game_models
from ..auth import oauth2
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

    new_user = models.User(password=hashed_password, email=user.email, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", status_code=status.HTTP_200_OK)
def get_user(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == int(current_user.id), models.User.is_active == True).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with this [{current_user.id}] does not found")

    user_games = db.query(game_models.Game).filter(game_models.Game.owner_id == user.id).all()

    if not user_games:
        user_games = list()

    games = list()
    for game in user_games:
        game_dict = dict()
        game_dict['id'] = game.id
        game_dict['title'] = game.title
        game_dict['type'] = game.type
        game_dict['cover_image'] = game.cover_image
        game_dict['created_at'] = game.created_at
        games.append(game_dict)

    user_dict = dict()
    user_dict['id'] = user.id
    user_dict['username'] = user.username
    user_dict['email'] = user.email
    user_dict['first_name'] = user.first_name
    user_dict['last_name'] = user.last_name
    user_dict['language'] = user.language
    user_dict['games'] = games

    return user_dict
