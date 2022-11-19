from typing import Optional, Union, List, Dict
from pydantic import BaseModel


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True

    error: bool
    number: Optional[int]
    message: Union[List, Dict, str]
