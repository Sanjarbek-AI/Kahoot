import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from ..database import Base


class Game(Base):
    __tablename__ = "games"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)
    language = Column(String, nullable=True, default='uz')
    type = Column(String, nullable=True, default='private')

    is_active = Column(Boolean, default=True)

    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False
                      )
    owner = relationship("User")

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("(now() AT TIME ZONE 'Asia/Tashkent')")
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("(now() AT TIME ZONE 'Asia/Tashkent')")
    )


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    cover_image = Column(String, nullable=True)
    time = Column(Integer, default=20)

    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)

    correct_option = Column(String, default='x', nullable=False)

    is_active = Column(Boolean, default=True)

    game_id = Column(Integer, ForeignKey(
        "games.id", ondelete="CASCADE"), nullable=False
                     )
    game = relationship("Game")
