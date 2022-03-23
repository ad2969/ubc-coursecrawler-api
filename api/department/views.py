import os
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.utils.response import ResponseError
from api.redis.utils import getAll, getOne, setMultiple, deleteAll
from api.redis.prefixes import DEPARTMENT_PREFIX
from .scrapers import scrapeDepartmentInformation

class DepartmentListView(APIView):
    def get(self, request):
        try:
            response = getAll(DEPARTMENT_PREFIX)
            return Response(response, status=response['code'])

        except ResponseError as e:
            return Response({
                'status': e.status,
                'msg': e.message,
            }, status=e.statusCode)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'internal error',
                'msg': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # admin use, requires secret
    def post(self, request):
        if 'secret' not in request.data or 'method' not in request.data:
            return Response({
                'status': 'REQUEST ERROR',
                'msg': 'no method or secret'
            }, status = status.HTTP_400_BAD_REQUEST)

        try:
            method = request.data['method']

            if method != 'SCRAPE' and method != 'CLEAN':
                return Response({
                    'status': 'REQUEST ERROR',
                    'msg': 'invalid method'
                }, status = status.HTTP_400_BAD_REQUEST)

            if request.data['secret'] != os.getenv('API_SECRET'):
                return Response({
                    'status': 'REQUEST ERROR',
                    'msg': 'invalid secret'
                }, status = status.HTTP_400_BAD_REQUEST)

            if method == 'SCRAPE':
                departments = scrapeDepartmentInformation()
                response = setMultiple(DEPARTMENT_PREFIX, {
                    val['rkey'] : json.dumps(val)
                    for val in departments
                })

                return Response(response, status=response['code'])

            elif method == 'CLEAN':
                response = deleteAll(DEPARTMENT_PREFIX)

                return Response(response, status=response['code'])

        except ResponseError as e:
            return Response({
                'status': e.status,
                'msg': e.message,
            }, status=e.statusCode)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'internal error',
                'msg': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DepartmentDetailView(APIView):
    def get(self, request, id=None):
        try:
            response = getOne(DEPARTMENT_PREFIX, id.upper())
            return Response(response, status=response['code'])

        except ResponseError as e:
            return Response({
                'status': e.status,
                'msg': e.message,
            }, status=e.statusCode)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'internal error',
                'msg': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
