import enum
from typing import Union, Optional
from functools import wraps


from fastapi import HTTPException, Depends
from jose import jwt, JWTError, constants
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from .config import get_settings, Settings

role_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Operation not permitted",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate request token",
    headers={"WWW-Authenticate": "Bearer"},
)


class Role(enum.Enum):
    user = 'USER'
    admin = 'ADMIN'


class Auth(BaseModel):
    user_id: int
    kyc_level: int = 0
    phone_number: str = ""
    email: Optional[str] = ""
    user_type: str

    def __json__(self, **options):
        return self.json()


def auth_required(permissions):
    def outer_wrapper(function):
        @wraps(function)
        def inner_wrapper(*args, **kwargs):
            if 'user' in kwargs:
                if kwargs['user'].user_type in permissions:
                    return function(*args, **kwargs)
                else:
                    raise role_exception
            else:
                raise forbidden_exception

        return inner_wrapper

    return outer_wrapper


def get_current_user(request: Request, settings: Settings = Depends(get_settings)) -> Union[Auth, None]:
    if 'authorization' in request.headers:

        try:
            key = settings.jwt_pubkey
            tkn = request.headers['Authorization'].split(' ')[1]
            payload = jwt.decode(tkn, key,
                                 algorithms=[constants.ALGORITHMS.ES256, ])
            username: str = payload.get("user_id")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = payload
        if user is None:
            raise credentials_exception
        return Auth(user_id=payload['user_id'], kyc_level=payload['kyc_level'],
                    email=payload['email'], phone_number=payload['phone_number'], user_type=payload['user_type'])
    return None
