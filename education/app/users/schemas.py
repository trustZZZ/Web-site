from pydantic import BaseModel, EmailStr


class SUserID(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    verified_email: bool | None = None


class SUserRegister(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class SUserLogin(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
