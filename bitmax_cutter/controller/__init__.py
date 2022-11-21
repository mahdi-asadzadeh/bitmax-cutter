import logging

import redis
from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError

from .user import route as user_route
from bitmax_cutter import __version__
from bitmax_cutter.core.errors import ok
from bitmax_cutter.core.config import get_redis
from bitmax_cutter.models.database import get_conn

logger=logging.getLogger('uvicorn.error')
route = APIRouter()
route.include_router(user_route, prefix="/user", tags=['User'])


@route.get("/status")
def home(r: redis.Redis = Depends(get_redis)):
    db_connection = is_db_available()
    redis_connection = is_redis_available(r)

    return ok({"version": __version__, "database": db_connection, "redis": redis_connection})


def is_db_available():
    try:
        db_conn = get_conn()
    except SQLAlchemyError as err:
        logger.exception(err.__cause__)
        logger.exception("DB connection error!")
        return "DB connection error!"
    except:
        logger.exception("DB connection error!")
        return "DB connection error!"
    else:
        return db_conn


def is_redis_available(r):
    try:
        r.ping()
    except:
        logger.exception("Redis connection error!")
        return "Redis connection error!"
    else:
        return r.info()
