from rest_framework import status
from api.utils.response import ResponseError

from .db import redis_instance

def getAll(prefix: str):
    try:
        keys = redis_instance.scan_iter(match=f'{prefix}:*')
        items = redis_instance.mget(*keys)
        count = len(items)
        
        return {
            'status': 'SUCCESS',
            'code': status.HTTP_200_OK,
            'count': count,
            'msg': f'found {count} items',
            'data': items,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'REDUS ERROR: GET',
            f'problem with getting {prefix} from redis -- {str(e)}'
        )

def getOne(prefix: str, key: str):
    try:
        value = redis_instance.get(f'{prefix}:{key}')

        if not value:
            return {
                'status': 'SUCCESS',
                'code': status.HTTP_204_NO_CONTENT,
                'msg': f'key {prefix}:{key} not found',
                'data': None,
            }

        return {
            'status': 'SUCCESS',
            'code': status.HTTP_200_OK,
            'msg': f'key {prefix}:{key} found',
            'data': value,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'REDUS ERROR: GET',
            f'problem with getting {prefix}{key} from redis -- {str(e)}'
        )

def setMultiple(prefix: str, data: dict):
    try:
        count = len(data)
        print("YAYEET")
        print(data)
        redis_instance.mset(data)

        return {
            'status': 'SUCCESS',
            'code': status.HTTP_201_CREATED,
            'count': count,
            'msg': f'found {count} items',
            'data': None,
        }
    
    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'REDIS ERROR: SET',
            f'problem with setting multiple {prefix} to redis -- {str(e)}'
        )

def setOne(prefix: str, key: str, body: str):
    try:
        redis_instance.set(key, body)
    
    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'REDIS ERROR: SET',
            f'problem with setting {prefix}:{key} to redis -- {str(e)}'
        )

def deleteAll(prefix: str, override = False):
    try:
        key = prefix if override else f'{prefix}:*'
        keys = redis_instance.keys(key)
        count = len(keys)
        if count: redis_instance.delete(*keys)
        
        return {
            'status': 'SUCCESS',
            'code': status.HTTP_205_RESET_CONTENT,
            'count': count,
            'msg': f'deleted {count} items',
            'data': None,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'REDUS ERROR: DELETE',
            f'problem with deleting all {prefix} from redis -- {str(e)}'
        )
