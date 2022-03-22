from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer
from django.shortcuts import get_object_or_404

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
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def post(self, request):
    #     serializer = DepartmentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'status': 'success',
    #             'data': serializer.data
    #         }, status = status.HTTP_201_CREATED)
    #     else:
    #         return Response({
    #             'status': 'error',
    #             'data': serializer.errors
    #         }, status = status.HTTP_400_BAD_REQUEST)

class DepartmentDetailView(APIView):
    def get(self, request, id=None):
        try:
            item = Department.objects.get(id=id)
            serializer = DepartmentSerializer(item)

            return Response({
                    'status': 'success',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def patch(self, request, id=None):
    #     item = Department.objects.get(id=id)
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
    #         item = get_object_or_404(Department, id=id)
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
