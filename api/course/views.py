from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.redis.constants.datatypes import COURSE_SEARCH_COUNTER_DATA_TYPE, COURSE_DATA_TYPE
from api.redis.social import logCourse, getPopularCourses
from api.redis.utils import getAll, getOne, setMultiple, deleteAll
from .scrapers import courseScrapers

from api.utils.exceptions import apiExceptionHandler
from api.utils.response import ResponseThen

class CourseListView(APIView):
    @apiExceptionHandler
    def get(self, request, institution):
        response = getAll(institution, COURSE_DATA_TYPE)
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

        if method != "CLEAN":
            return Response({
                "status": "REQUEST ERROR",
                "msg": "invalid method"
            }, status = status.HTTP_400_BAD_REQUEST)
        else:
            response = deleteAll(institution, COURSE_DATA_TYPE)
            deleteAll(institution, COURSE_SEARCH_COUNTER_DATA_TYPE, override=True)

            return Response(response, status=response["code"])

class CourseDetailView(APIView):
    @apiExceptionHandler
    def get(self, request, institution, courseId):
        forceScrapeParam = request.query_params.get("forceScrape") # to force a scrape
        preventSaveParam = request.query_params.get("preventSave") # to prevent saving scraped data

        courseKey = courseId.upper()

        # if scraping is not forced, check if it already exists in the database
        if not forceScrapeParam:
            existingCourse = getOne(institution, COURSE_DATA_TYPE, courseKey)

            if existingCourse["data"]:
                return Response(existingCourse, status=existingCourse["code"])

        # scrape course information
        data, newData = courseScrapers["UBC"](courseKey)

        if preventSaveParam: # do not save scrape result
            return Response({
                "status": "SUCCESS",
                "data": data,
                "msg": "scraped, data will not be saved",
            }, status=status.HTTP_200_OK)
        
        def tempCallback():
            # save scrape result
            setMultiple(institution, COURSE_DATA_TYPE, newData)
            # log that this course has been queried once
            logCourse(institution, courseKey)

        return ResponseThen({
            "status": "SCRAPE SUCCESS",
            "data": data,
            "msg": f"scraped, {len(newData)} new data will be saved",
        }, tempCallback, status=status.HTTP_201_CREATED)
class PopularCourseListView(APIView):
    @apiExceptionHandler
    def get(self, request, institution):
        response = getPopularCourses(institution, 10)
        return Response(response, status=response["code"])
