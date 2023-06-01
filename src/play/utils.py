import random
from . import models


def code_generator(db):
    random_code = random.randint(1000000, 9999999)
    game = db.query(models.ActiveGame).filter(models.ActiveGame.generated_code == random_code).first()
    if game:
        code_generator(db)
    return random_code
