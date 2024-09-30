from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    password: str


class UserResponse(UserBase):
    id: int

    # 自動変換が可能になります。これにより、ORM モデルをそのままAPIレスポンスとして使用できるようになります。
    class Config:
        orm_mode = True
