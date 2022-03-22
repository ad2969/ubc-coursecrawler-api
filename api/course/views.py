from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

from .scrapers import scrapeCourseInformation

class CourseListView(APIView):
    def get(self, request):
        try:
            items = Course.objects.all()
            serializer = CourseSerializer(items, many=True)

            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseDetailView(APIView):
    def get(self, request, id=None):
        try:
            # item = Course.objects.get(id=id)
            # serializer = CourseSerializer(item)
            courseKey = id.lower().split('-')
            data = scrapeCourseInformation(courseKey[0],courseKey[1])
            print(data)

            return Response({
                    'status': 'success',
                    'data': data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
