from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from .scrapers import scrapeCourseInformation
from ._utils import saveMultipleCourses, getOneCourse
from api.utils.response import ResponseThen, ResponseError

class CourseListView(APIView):
    def get(self, request):
        try:
            items = Course.objects.all()
            json = CourseSerializer(items, many=True)

            return Response({
                'status': 'success',
                'data': json.data
            }, status=status.HTTP_200_OK)

        except ResponseError as e:
            return Response({
                'status': e.status,
                'data': e.message,
            }, status=e.statusCode)

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
            courseKey = id.split('-')
            
            # if exists in the database
            if not forceScrapeParam:
                existingCourse = getOneCourse(id, True)

                # if exists in the database
                if existingCourse:
                    # recursivelyGetPrereqs(existingCourse)
                    json = CourseSerializer

                    return Response({
                        'status': 'success',
                        'data': existingCourse
                    }, status=status.HTTP_200_OK)

            # scrape course information
            data, fullData = scrapeCourseInformation(courseKey[0],courseKey[1])

            if preventSaveParam: # do not save scrape result
                return Response({
                    'status': 'success',
                    'data': data
                }, status=status.HTTP_200_OK)
            else: # save scrape result
                def tempCallback(): saveMultipleCourses(fullData.values())
                return ResponseThen({
                    'status': 'scrape success',
                    'data': data
                }, tempCallback, status=status.HTTP_201_CREATED)

        except ResponseError as e:
            return Response({
                'status': e.status,
                'data': e.message,
            }, status=e.statusCode)

        except Exception as e:
            return Response({
                'status': 'internal error',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
