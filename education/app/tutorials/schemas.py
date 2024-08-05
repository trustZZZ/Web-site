from pydantic import BaseModel


class SBlocks(BaseModel):
    id: int | None = None
    block_name: str | None = None
    themes: list | None = None


class SThemes(BaseModel):
    id: int | None = None
    id_block: int | None = None
    lesson: str | None = None
    theory_source: str | None = None
    practice_source: str | None = None
