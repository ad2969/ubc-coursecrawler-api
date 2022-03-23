import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.utils.exceptions import PageError
from api.utils.response import ResponseThen, ResponseError
from api.redis.prefixes import COURSE_PREFIX
from api.redis.utils import getAll, getOne, setMultiple, deleteAll
from .scrapers import scrapeCourseInformation

class CourseListView(APIView):
    def get(self, request):
        try:
            response = getAll(COURSE_PREFIX)
            return Response(response, status=response['code'])

        except ResponseError as e:
            return Response({
                'status': e.status,
                'data': e.message,
            }, status=e.statusCode)

        except Exception as e:
            return Response({
                'status': 'INTERNAL ERROR',
                'data': e,
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

            if method != 'CLEAN':
                return Response({
                    'status': 'REQUEST ERROR',
                    'msg': 'invalid method'
                }, status = status.HTTP_400_BAD_REQUEST)
            else:
                response = deleteAll(COURSE_PREFIX)

                return Response(response, status=response['code'])

        except ResponseError as e:
            return Response({
                'status': e.status,
                'msg': e.message,
            }, status=e.statusCode)

        except Exception as e:
            traceback.print_exc()
            return Response({
                'status': 'INTERNAL ERROR',
                'msg': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseDetailView(APIView):
    def get(self, request, id=None):
        forceScrapeParam = request.query_params.get('forceScrape') # to force a scrape
        preventSaveParam = request.query_params.get('preventSave') # to prevent saving scraped data

        try:
            courseKey = id.split('-')
            
            # if exists in the database
            if not forceScrapeParam:
                existingCourse = getOne(COURSE_PREFIX, id.upper())

                # if exists in redis
                if existingCourse['data']:
                    return Response(existingCourse, status=existingCourse['code'])

            # scrape course information
            data, newData = scrapeCourseInformation(courseKey[0],courseKey[1])

            if preventSaveParam: # do not save scrape result
                return Response({
                    'status': 'SUCCESS',
                    'data': data,
                    'msg': 'scraped, data will not be saved',
                }, status=status.HTTP_200_OK)
            
             # save scrape result
            def tempCallback(): setMultiple(COURSE_PREFIX, newData)
            return ResponseThen({
                'status': 'SCRAPE SUCCESS',
                'data': data,
                'msg': f'scraped, {len(newData)} new data will be saved',
            }, tempCallback, status=status.HTTP_201_CREATED)

        except PageError as e:
            return Response({
                'status': 'INTERNAL ERROR',
                'msg': e.message,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ResponseError as e:
            return Response({
                'status': e.status,
                'data': e.message,
            }, status=e.statusCode)

        except Exception as e:
            return Response({
                'status': 'INTERNAL ERROR',
                'data': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
