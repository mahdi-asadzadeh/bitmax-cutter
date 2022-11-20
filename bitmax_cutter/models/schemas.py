from typing import Optional, Union, List, Dict
from pydantic import BaseModel


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True

    error: bool
    number: Optional[int]
    message: Union[List, Dict, str]


class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class LoginUser(BaseModel):
    username: str
    password: str


class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    