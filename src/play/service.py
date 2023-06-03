from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import code_generator
from ..game import models as game_models
from ..database import get_db
from ..auth import oauth2

router = APIRouter(
    prefix="/play",
    tags=['Active Games']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ActiveGameOut)
def create_game(active_game: schemas.ActiveGameCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    game = db.query(game_models.Game).filter(game_models.Game.id == active_game.game_id).first()

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"game with this [ {active_game.game_id} ] does not found")

    user_game = db.query(models.ActiveGame).filter(
        models.ActiveGame.game_id == active_game.game_id,
        models.ActiveGame.owner_id == current_user.id,
        models.ActiveGame.is_active == True).first()

    if user_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"you already stated this games")

    random_code = code_generator(db)

    new_active_game = models.ActiveGame(owner_id=current_user.id, generated_code=random_code, **active_game.dict())
    db.add(new_active_game)
    db.commit()
    db.refresh(new_active_game)

    return new_active_game


@router.get("/", status_code=status.HTTP_200_OK)
def get_active_game(code: int, db: Session = Depends(get_db)):
    active_game = db.query(models.ActiveGame).filter(models.ActiveGame.generated_code == code).first()
    if not active_game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"active game with this code [ {code} ] does not found")
    game = db.query(game_models.Game).filter(game_models.Game.id == active_game.game_id).first()
    questions = db.query(game_models.Question).filter(game_models.Question.game_id == active_game.game_id).all()
    questions_list = list()
    for question in questions:
        question_dict = dict()
        question_dict['id'] = question.id
        question_dict['generated_code'] = active_game.generated_code
        question_dict['cover_image'] = question.cover_image
        question_dict['option_a'] = question.option_a
        question_dict['option_b'] = question.option_b
        question_dict['option_c'] = question.option_c
        question_dict['option_d'] = question.option_d
        questions_list.append(question_dict)

    data = dict({
        "title": game.title,
        "type": game.type,
        "generated_code": active_game.generated_code,
        "cover_image": game.cover_image,
        "owner_id": game.owner_id,
        "description": game.description,
        "is_active": game.is_active,
        "total_slides": len(questions_list),
        "questions": questions_list,
    })

    return data


@router.get("/gamers/", status_code=status.HTTP_200_OK, response_model=List[schemas.ActiveGamersOut])
def get_all_gamers(code: int, db: Session = Depends(get_db)):
    game = db.query(models.ActiveGame).filter(models.ActiveGame.generated_code == code).first()
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"active game with this code [ {code} ] does not found")
    gamers = db.query(models.ActiveGamer).filter(models.ActiveGamer.generated_code == code). \
        order_by(models.ActiveGamer.points.desc()).all()
    return gamers


@router.post("/join/", status_code=status.HTTP_201_CREATED)
def create_gamer(active_gamer: schemas.ActiveGamerCreate, db: Session = Depends(get_db)):
    active_gamer_query = db.query(models.ActiveGamer).filter(
        models.ActiveGamer.generated_code == active_gamer.generated_code,
        models.ActiveGamer.username == active_gamer.username)

    if active_gamer_query.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"you are already in thus game")

    new_gamer = models.ActiveGamer(**active_gamer.dict())
    db.add(new_gamer)
    db.commit()
    db.refresh(new_gamer)

    return {"status": True, "detail": "User joined successfully"}


@router.put("/answer/", status_code=status.HTTP_200_OK)
def gamer_answer(answer: schemas.GamerAnswer, db: Session = Depends(get_db)):
    question = db.query(game_models.Question).filter(game_models.Question.id == answer.question_id).first()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"question with this [ {answer.question_id} ] does not found")

    gamer = db.query(models.ActiveGamer).filter(
        models.ActiveGamer.username == answer.username,
        models.ActiveGamer.generated_code == answer.code
    )

    if not gamer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user does not found")

    answer_check = db.query(game_models.GamerAnswer).filter(
        game_models.GamerAnswer.generated_code == answer.code,
        game_models.GamerAnswer.username == answer.username,
        game_models.GamerAnswer.question_id == answer.question_id
    ).first()

    if answer_check:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f"you already answer this question")

    if answer.correct_option.lower() not in ['option_a', 'option_b', 'option_c', 'option_d']:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"correct_option is not valid")

    new_answer = game_models.GamerAnswer(
        generated_code=answer.code, username=answer.username, question_id=answer.question_id
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    gamer_data = gamer.first()

    if answer.correct_option.lower() == question.correct_option.lower():
        gamer.update({'points': gamer_data.points + 100}, synchronize_session=False)
        db.commit()
        return {"answer": True}

    else:
        return {"answer": False}
    