from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.dependencies import get_current_user, get_token
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserLogin, SUserID
from app.users.models import Users

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email,
                       hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("course_access_token", access_token, httponly=True)
    return {"token": access_token, "user": user}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("course_access_token")


@router.post("/buy")
async def buy_course(user: SUserID = Depends(get_current_user)):
    if not user:
        return None
    else:
        await UsersDAO.buy(user_id=user.id)
        return {"access": "available"}


@router.get("/user_id")
async def get_user_id(user_id: Users.id = Depends(get_current_user)):
    try:
        return user_id
    except HTTPException:
        return None
