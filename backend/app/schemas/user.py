from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field(..., alias="email")
    username: str = Field(..., alias="username")


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None, alias="email")
    username: Optional[str] = Field(default=None, alias="username")


class UserInDB(UserBase):
    id: int = Field(..., alias="id")


class UserResponse(UserBase):
    id: int = Field(..., alias="id")

    # 自動変換が可能になります。これにより、ORM モデルをそのままAPIレスポンスとして使用できるようになります。
    class Config:
        orm_mode = True
