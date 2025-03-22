from fastapi import APIRouter, HTTPException, status, Response, Depends


from src.core.auth import hash_password, verify_password, create_jwt_token, get_current_user
from src.core.dao import UsersDAO
from src.core.schemas import SUserRegister
from src.core.model import User


router = APIRouter(prefix="", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(response: Response, user: SUserRegister, user_dao: UsersDAO = Depends(UsersDAO)) -> dict[str, str]:
    if await user_dao.get_user_by_name(name=user.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует!")

    user_added = await user_dao.add_user(name=user.name, password=hash_password(user.password))

    jwt_token = create_jwt_token({"sub": str(user_added.id)})
    response.set_cookie(key="user_jwt_token", value=jwt_token, httponly=True)

    return {"Authorization": f"Bearer {jwt_token}"}


@router.post("/signin")
async def signin(response: Response, user: SUserRegister, user_dao: UsersDAO = Depends(UsersDAO)) -> dict[str, str]:
    user_from_db = await user_dao.get_user_by_name(name=user.name)

    if not user_from_db or not verify_password(user.password, user_from_db.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль!")

    jwt_token = create_jwt_token({"sub": str(user_from_db.id)})
    response.set_cookie(key="user_jwt_token", value=jwt_token, httponly=True)

    return {"Authorization": f"Bearer {jwt_token}"}


@router.get("/")
async def check_jwt(user: User = Depends(get_current_user)) -> str:
    return user.name
