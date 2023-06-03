import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Interval
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from ..database import Base


class ActiveGame(Base):
    __tablename__ = "activegames"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    generated_code = Column(Integer, unique=True, index=True, default=0)
    total_gamers = Column(Integer, default=0)

    game_id = Column(Integer, ForeignKey(
        "games.id", ondelete="CASCADE"), nullable=False)
    game = relationship("Game")

    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

    is_active = Column(Boolean, default=True)

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


class ActiveGamer(Base):
    __tablename__ = "activegamers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    generated_code = Column(Integer, ForeignKey(
        "activegames.generated_code", ondelete="CASCADE"), nullable=False)
    game = relationship("ActiveGame")

    username = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=False)
    points = Column(Integer, nullable=False, default=0)

    is_active = Column(Boolean, default=True)

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



