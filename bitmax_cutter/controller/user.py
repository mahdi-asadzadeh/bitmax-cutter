from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from bitmax_cutter.core.config import settings
from bitmax_cutter.core.errors import ErrorCode, ok, bad_request, not_found
from bitmax_cutter.core.authentication import create_access_token, get_current_user
from bitmax_cutter.models.database import get_db
from bitmax_cutter.models.schemas import RegisterUser, LoginUser, UpdateUser, TokenData
from bitmax_cutter.services.user import register, login, update, get_balance_binance

route = APIRouter()


@route.post("/register")
def register_user(user: RegisterUser, db: sessionmaker = Depends(get_db)):
    try:
        new_user = register(first_name=user.first_name,last_name=user.last_name, username=user.username, password=user.password, db=db)
        return ok({"id": new_user.id, "username": new_user.username, "first_name": new_user.first_name, "last_name": new_user.last_name})
        
    except IntegrityError as e:
        return bad_request(ErrorCode.DUPLICATE_USER)

@route.post("/login")
def login_user(user: LoginUser, db: sessionmaker = Depends(get_db)):
    try:
        user = login(username=user.username, password=user.password, db=db)
        access_token_expires = timedelta(minutes=settings.token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        ) 
        return ok({"access_token": access_token, "token_type": "bearer"})

    except NoResultFound as e:
        return not_found(ErrorCode.NOT_FOUND_USER)

@route.put("/update")
def update_user(data: UpdateUser, current_user: TokenData = Depends(get_current_user), db: sessionmaker = Depends(get_db)):
    try:
        user = update(current_user.username, data.first_name, data.last_name, db)
        return ok({"id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name})
   
    except NoResultFound as e:
        return not_found(ErrorCode.NOT_FOUND_USER)

@route.get("/balance/{address}")
def get_balance(address: str):
    try:
        balance = get_balance_binance(address)
        return ok({"balance": balance})

    except Exception as e:
        return bad_request(ErrorCode.INVALID_ADDRESS)
