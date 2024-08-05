from typing import List

from sqlalchemy.orm import Mapped, relationship

from app.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean


class Blocks(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, nullable=False)
    block_name = Column(String, nullable=False)

    available = Column(Boolean, nullable=False, default=False)

    themes: Mapped[list["Themes"]] = relationship(
        back_populates="blocks",
        primaryjoin="Blocks.id == Themes.block_id",
        order_by="Themes.id.asc()"
    )


class Themes(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    theme_name = Column(String, nullable=False)

    available = Column(Boolean, nullable=False, default=False)

    blocks: Mapped["Blocks"] = relationship(
        back_populates="themes",
        primaryjoin="Blocks.id == Themes.block_id",
        order_by="Blocks.id.desc()"
    )

    lessons: Mapped[List["Lessons"]] = relationship(
        back_populates="themes",
        primaryjoin="Lessons.theme_id == Themes.id",
    )


class Lessons(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, nullable=False)
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=False)
    lesson_name = Column(String, nullable=False)
    theory_source = Column(String, nullable=False)
    practice_source = Column(String, nullable=False)

    available = Column(Boolean, nullable=True, default=False)

    themes: Mapped["Themes"] = relationship(
        back_populates="lessons",
        primaryjoin="Lessons.theme_id == Themes.id",
        order_by="Themes.id.desc()"
    )
