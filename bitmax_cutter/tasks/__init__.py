import json
from typing import Union

from bitmax_cutter.core.config import get_redis
from bitmax_cutter.core.token import Auth
from bitmax_cutter.models import schemas
from bitmax_cutter.services import sample as service_sample
from bitmax_cutter.task_manager import app

r = get_redis().__next__()


@app.task(name="me.getSampleList")
def get_order_list():
    return service_order.get_sample_list(r)


