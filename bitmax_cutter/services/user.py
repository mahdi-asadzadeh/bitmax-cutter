from passlib.context import CryptContext
from bitmax_cutter.models.dbmodels import User

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(plain_password, hashed_password):
        return pwd_cxt.verify(plain_password, hashed_password)


def register(first_name: str, last_name: str, username: str, password: str, db):
    new_user = User(first_name=first_name, last_name=last_name, username=username, password=Hash.bcrypt(password))
    db.add(new_user)
    db.commit()
    return new_user


def login(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).one()
    check_pass = Hash.verify(password, user.password)
    if check_pass:
        return "123"
    else:
        return None 
