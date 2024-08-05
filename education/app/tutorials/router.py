from fastapi import APIRouter, Depends
from app.tutorials.dao import BlockDAO, ThemeDAO, LessonDAO
from app.users.dependencies import get_token

router = APIRouter(
    prefix="/block",
    tags=["Блок"],
)


@router.get("/{id_block}")
async def get_blocks(id_block: int):
    block = await BlockDAO.find_all(id=id_block)
    return block


@router.get("")
async def get_blocks():
    blocks = await BlockDAO.find_all()
    return blocks


@router.get("/sub{block_id}/themes")
async def get_blocks(block_id: int):
    themes = await ThemeDAO.find_all(block_id=block_id)
    return themes


@router.get("/sub{block_id}/themes/{theme_id}")
async def get_blocks(block_id: int, theme_id: int):
    theme = await ThemeDAO.find_all(block_id=block_id, id=theme_id)
    return theme


@router.get("/themes/lessons")
async def get_blocks():
    theme = await LessonDAO.find_all()
    return theme


@router.get("/themes/{theme_id}/lesson/{lesson_id}")
async def get_lesson(theme_id: int, lesson_id: int):
    lesson = await LessonDAO.find_one_or_none(id=lesson_id, theme_id=theme_id)
    return lesson.themes.block_id


@router.get("/{block_number}/{theme_number}/{lesson_number}")
def load1_lesson(block_number: int, theme_number: int, lesson_number: int):
    return fr"C:\Users\NoName\Desktop\FAST_IP_projects\learn_2\education\blocks\block_{block_number}\theme_{theme_number}\{lesson_number}.htm"
