from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth import service as auth
from src.users import service as user
from src.game import service as game
from src.play import service as play

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(game.router)
app.include_router(play.router)
