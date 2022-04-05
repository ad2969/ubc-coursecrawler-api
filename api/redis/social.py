from rest_framework import status

from .db import redis_instance
from .constants.datatypes import COURSE_SEARCH_COUNTER_DATA_TYPE
from api.utils.response import ResponseError

def logCourse(institution: str, courseKey: str):
    try:
        # "ZADD" arguments
        # name Union[bytes, str, memoryview]
        # mapping Mapping[AnyKeyT, any] --> dict of the key-values to add/update
        # nx forces ZADD to only create new elements and not to update scores for elements that already exist.
        # xx forces ZADD to only update scores of elements that already exist. New elements will not be added.
        # ch modifies the return value to be the numbers of elements changed. Changed elements include new elements that were added and elements whose scores changed.
        # incr modifies ZADD to behave like ZINCRBY. In this mode only a single element/score pair can be specified and the score is the amount the existing score will be incremented by. When using this mode the return value of ZADD will be the new score of the element.
        # https://redis-py.readthedocs.io/en/stable/commands.html?highlight=zincr#redis.commands.core.CoreCommands.zadd
        queryString = f"{institution}:{COURSE_SEARCH_COUNTER_DATA_TYPE}"
        redis_instance.zadd(queryString, {courseKey: 1}, False, False, False, True)
        return True

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDIS ERROR: INCR",
            f"problem with updating counter for {courseKey} to redis -- {str(e)}"
        )

def getPopularCourses(institution: str, num: int = 10):
    try:
        queryString = f"{institution}:{COURSE_SEARCH_COUNTER_DATA_TYPE}"
        sortedCourses = redis_instance.zrange(queryString, -1-num, -1, True, True)
        count = len(sortedCourses)
        
        return {
            "status": "SUCCESS",
            "code": status.HTTP_200_OK,
            "count": count,
            "msg": f"found {count} items",
            "data": sortedCourses,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDIS ERROR: GET",
            f"problem with getting popular courses from redis -- {str(e)}"
        )
