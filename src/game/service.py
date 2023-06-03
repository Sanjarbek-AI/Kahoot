from typing import List

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas, utils
from ..database import get_db
from ..auth import oauth2
from datetime import timedelta

router = APIRouter(
    prefix="/games",
    tags=['Games']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.GameOut)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    if game.type.lower() != "public" and game.type.lower() != "private":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="type value is not valid status [public, private]")

    new_game = models.Game(owner_id=current_user.id, **game.dict())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game


@router.post("/all/", status_code=status.HTTP_201_CREATED)
def create_game_all(game: schemas.GameAllCreate, db: Session = Depends(get_db),
                    current_user=Depends(oauth2.get_current_user)):
    if game.type.lower() != "public" and game.type.lower() != "private":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="type value is not valid status [public, private]")

    new_game = models.Game(owner_id=current_user.id, title=game.title, description=game.description,
                           cover_image=game.cover_image, type=game.type)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    for question in game.questions:
        try:
            if question.correct_option.lower() not in ['option_a', 'option_b', 'option_c', 'option_d']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"correct option [{question.correct_option}] is not valid value [a, b, c, d]")

            new_question = models.Question(
                game_id=new_game.id,
                title=question['title'],
                cover_image=question['image'],
                option_a=question['option_a'],
                option_b=question['option_b'],
                option_c=question['option_c'],
                option_d=question['option_d'],
                time=question['time'],
                correct_option=question['correct_option']
            )
            db.add(new_question)
            db.commit()
            db.refresh(new_question)
        except Exception as exs:
            print(exs)

    return {"success": "Created", "id": new_game.id}


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.GameOut])
def get_all_games(db: Session = Depends(get_db),
                  current_user=Depends(oauth2.get_current_user)):
    games = db.query(models.Game).filter(models.Game.type == 'public').all()

    if not games:
        games = list()

    return games


@router.get("/{id}/", status_code=status.HTTP_200_OK)
def get_one_game(id: int, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    game = db.query(models.Game).filter(models.Game.id == id).first()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"game with this {id} does not found")

    questions = db.query(models.Question).filter(models.Question.game_id == id).all()

    data = dict({
        "title": game.title,
        "type": game.type,
        "cover_image": game.cover_image,
        "owner_id": game.owner_id,
        "description": game.description,
        "is_active": game.is_active,
        "total_questions": len(list(questions)),
        "questions": list(questions),
    })
    return data


@router.post("/question/", status_code=status.HTTP_201_CREATED, response_model=schemas.QuestionOut)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db),
                    current_user=Depends(oauth2.get_current_user)):
    game = db.query(models.Game).filter(models.Game.id == question.game_id).first()

    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"game with this {question.game_id} "
                                                                          f"does not found")
    if current_user.id != game.owner_id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"you are not changing your own game")

    if question.correct_option.lower() not in ['option_a', 'option_b', 'option_c', 'option_d']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"correct option [{question.correct_option}] is not valid value [a, b, c, d]")

    new_question = models.Question(**question.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question
