from app.dao.base import BaseDAO
from app.tutorials.models import Blocks, Themes, Lessons


class BlockDAO(BaseDAO):
    model = Blocks
    selection = model.themes


class ThemeDAO(BaseDAO):
    model = Themes
    selection = model.lessons


class LessonDAO(BaseDAO):
    model = Lessons
    selection = model.themes
