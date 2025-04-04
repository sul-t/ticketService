from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError, ExpiredSignatureError

from src.core.config import get_auth_data
from src.core.dao import UsersDAO
from src.core.model import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict) -> str:
    auth_data = get_auth_data()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    data.update({"exp": expire})
    return jwt.encode(data, auth_data["secret_key"], algorithm=auth_data["algorithm"])


def get_token(request: Request) -> str:
    token = request.cookies.get("user_jwt_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Токен не найден")
    return token


async def get_current_user(token: str = Depends(get_token), user_dao: UsersDAO = Depends(UsersDAO)) -> User:
    auth_data = get_auth_data()

    try:
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])

        if not (user_id := payload.get("sub")):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не найден ID пользователя")

        if not (user := await user_dao.get_user_by_id(str(user_id))):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не найден")

        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Токен истек")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не валидный токен!")
