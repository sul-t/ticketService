from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    name: EmailStr
    password: str = Field(..., min_length=5, max_length=18, description="Пароль от 5 до 18 знаков")
