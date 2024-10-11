from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserInDB(UserBase):
    id: int


class UserResponse(UserBase):
    id: int

    # 自動変換が可能になります。これにより、ORM モデルをそのままAPIレスポンスとして使用できるようになります。
    class Config:
        orm_mode = True
