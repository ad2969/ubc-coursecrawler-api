import traceback
from rest_framework import status
from rest_framework.response import Response

from api.redis.constants.institutions import INSTITUTION_CODES
from api.utils.response import ResponseError
class InstitutionNotImplemented(Exception):
    def __init__(self, message = "Scraping has not been implemented for that institution"):
        self.message = message
        super().__init__(self.message)
        
class PageError(Exception):
    def __init__(self, message = "Internal error"):
        self.message = message
        super().__init__(self.message)

"""
Decorator for handling all kinds of functions
"""
def apiExceptionHandler(func):
    def handler(*args, institution, **kwargs):
        try:
            # check if institution has been implemented and turn into uppercase letters
            institutionKey = institution.upper()
            if institutionKey not in INSTITUTION_CODES: raise InstitutionNotImplemented

            # run the actual function
            return func(*args, institution=institutionKey, **kwargs)

        except InstitutionNotImplemented as e:
            return Response({
                "status": "NOT FOUND",
                "data": e.message,
            }, status=status.HTTP_404_NOT_FOUND)

        except PageError as e:
            return Response({
                "status": "INTERNAL ERROR",
                "msg": e.message,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ResponseError as e:
            return Response({
                "status": e.status,
                "data": e.message,
            }, status=e.statusCode)

        except Exception as e:
            traceback.print_exc()
            return Response({
                "status": "INTERNAL ERROR",
                "data": e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return handler