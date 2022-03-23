import os
import redis
from django.conf import settings

redis_db = os.getenv('REDIS_DB')
redis_pw = os.getenv('REDIS_PASS')

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=redis_pw,
    db=0,
)
