import os
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.redis.constants.datatypes import DEPARTMENT_DATA_TYPE
from api.redis.utils import getAll, getOne, setMultiple, deleteAll
from .scrapers import departmentScrapers

from api.utils.exceptions import apiExceptionHandler

class DepartmentListView(APIView):
    @apiExceptionHandler
    def get(self, request, institution):
        response = getAll(institution, DEPARTMENT_DATA_TYPE)
        return Response(response, status=response["code"])

    # admin use, requires secret
    @apiExceptionHandler
    def post(self, request, institution):
        if "secret" not in request.data or "method" not in request.data:
            return Response({
                "status": "REQUEST ERROR",
                "msg": "no method or secret"
            }, status = status.HTTP_400_BAD_REQUEST)

        method = request.data["method"]

        if method != "SCRAPE" and method != "CLEAN":
            return Response({
                "status": "REQUEST ERROR",
                "msg": "invalid method"
            }, status = status.HTTP_400_BAD_REQUEST)

        if request.data["secret"] != os.getenv("API_SECRET"):
            return Response({
                "status": "REQUEST ERROR",
                "msg": "invalid secret"
            }, status = status.HTTP_400_BAD_REQUEST)

        if method == "SCRAPE":
            departments = departmentScrapers["UBC"]()
            response = setMultiple(institution, DEPARTMENT_DATA_TYPE, {
                val["rkey"] : json.dumps(val)
                for val in departments
            })

            return Response(response, status=response["code"])

        elif method == "CLEAN":
            response = deleteAll(institution, DEPARTMENT_DATA_TYPE)

            return Response(response, status=response["code"])

class DepartmentDetailView(APIView):
    @apiExceptionHandler
    def get(self, request, institution, deptId):
        response = getOne(institution, DEPARTMENT_DATA_TYPE, deptId.upper())
        return Response(response, status=response["code"])
