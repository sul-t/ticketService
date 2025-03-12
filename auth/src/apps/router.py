from fastapi import APIRouter, HTTPException, status, Response, Depends

from src.core.auth import get_password_hash, verify_password, create_jwt_token, get_current_user

from src.core.dao import UsersDAO
from src.core.schemas import SUserRegister
from src.core.model import User



router = APIRouter(prefix='', tags=['Auth'])


@router.post('/singup')
async def signup(user: SUserRegister):
    first_or_none_user = await UsersDAO.find_user(name=user.name)

    if first_or_none_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует!'
        )
    

    user.password = get_password_hash(password=user.password)
    await UsersDAO.create_user(name=user.name, password=user.password)

    return {"message": "Пользователь успешно создан!"}

@router.post('/signin')
async def signin(responce: Response, user: SUserRegister):
    first_or_none_user = await UsersDAO.find_user(name=user.name)

    if not first_or_none_user or not verify_password(user.password, first_or_none_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль!'
        )
    

    jwt_token = create_jwt_token({"sub": str(first_or_none_user.id)})
    responce.set_cookie(key="user_jwt_token", value=jwt_token, httponly=True)

    return {'jwt_token': jwt_token}

@router.get('/')
async def check_jwt(user_data: User = Depends(get_current_user)):
    return user_data

    

