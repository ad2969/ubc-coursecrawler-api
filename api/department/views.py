import os
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer
from .scrapers import scrapeDepartmentInformation
from ._utils import getOneDepartment, createOneDepartment, updateDepartment
# from django.shortcuts import get_object_or_404

class DepartmentListView(APIView):
    def get(self, request):
        try:
            items = Department.objects.all()
            serializer = DepartmentSerializer(items, many=True)

            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # admin use, requires secret
    def post(self, request):
        if 'secret' not in request.data or 'method' not in request.data:
            return Response({
                'status': 'request error',
                'data': 'no method or secret'
            }, status = status.HTTP_400_BAD_REQUEST)

        try:
            method = request.data['method']

            if method != 'SCRAPE' and method != 'CLEAN':
                return Response({
                    'status': 'request error',
                    'data': 'invalid method'
                }, status = status.HTTP_400_BAD_REQUEST)

            if request.data['secret'] != os.getenv('API_SECRET'):
                return Response({
                    'status': 'request error',
                    'data': 'invalid secret'
                }, status = status.HTTP_400_BAD_REQUEST)

            if method == 'SCRAPE':
                departments = scrapeDepartmentInformation()
                for department in departments:
                    existing = getOneDepartment(department['key'])
                    if existing: updateDepartment(department['key'], department)
                    else: createOneDepartment(department)

                return Response({
                    'status': 'success',
                    'data': 'updated department tables'
                }, status = status.HTTP_201_CREATED)

            elif method == 'CLEAN':
                Department.objects.all().delete()

                return Response({
                    'status': 'success',
                    'data': 'deleted department tables'
                }, status = status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'internal error',
                'data': e,
            }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class DepartmentDetailView(APIView):
    def get(self, request, id=None):
        try:
            item = getOneDepartment(id)

            return Response({
                    'status': 'success' if item else 'not found',
                    'data': item
                }, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def patch(self, request, id=None):
    #     item = Department.objects.get(key=id)
    #     serializer = DepartmentSerializer(item, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'status': 'success'
    #         }, status = status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response({
    #             'status': 'error',
    #             'data': serializer.errors
    #         }, status = status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, id=None):
    #     if id:
    #         item = get_object_or_404(Department, key=id)
    #         item.delete()
    #         return Response({
    #             'status': 'success',
    #             'data': 'department ' + id + ' deleted',
    #         }, status = status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response({
    #             'status': 'error',
    #             'data': 'failed to delete department ' + id,
    #         }, status = status.HTTP_400_BAD_REQUEST)
