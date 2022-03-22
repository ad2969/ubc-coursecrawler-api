from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from .scrapers import scrapeCourseInformation
from ._utils import getOneCourse, saveMultipleCourses
from api.utils.response import ResponseThen

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
        forceScrapeParam = request.query_params.get('forceScrape') # to force a scrape
        preventSaveParam = request.query_params.get('preventSave') # to prevent saving scraped data

        try:
            # item = Course.objects.get(id=id)
            # serializer = CourseSerializer(item)
            courseKey = id.split('-')
            existing = getOneCourse(courseKey)

            if existing and not forceScrapeParam:
                data = existing

                return Response({
                    'status': 'success',
                    'data': data
                }, status=status.HTTP_200_OK)
            else:
                data, fullData = scrapeCourseInformation(courseKey[0],courseKey[1])
                if not preventSaveParam:
                    def tempCallback(): saveMultipleCourses(fullData.values())

                    return ResponseThen({
                        'status': 'success',
                        'data': data
                    }, tempCallback, status=status.HTTP_201_CREATED)

                return Response({
                    'status': 'success',
                    'data': data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
