from pydantic import BaseModel, EmailStr, Field



class SUser(BaseModel):
    name: str
    role: str
    password: str


class SUserRegister(BaseModel):
    name: EmailStr = Field(..., description='Адрес электронной почты')
    password: str = Field(..., min_length=5, max_length=18, description='Пароль от 5 до 18 знаков')