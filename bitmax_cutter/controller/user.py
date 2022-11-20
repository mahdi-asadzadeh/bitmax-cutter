from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound
from bitmax_cutter.models.database import get_db
from bitmax_cutter.models.schemas import RegisterUser, LoginUser, UpdateUser
from bitmax_cutter.core.errors import ErrorCode
from bitmax_cutter.core.errors import ok, bad_request, not_found
from bitmax_cutter.services.user import register, login

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
        token = login(username=user.username, password=user.password, db=db)
        return ok({"token": token})
    except NoResultFound as e:
        return not_found(ErrorCode.NOT_FOUND_USER)


@route.put("/update")
def update_user(user: UpdateUser):
    pass
