from rest_framework import status
from api.department._utils import getOneDepartment
from api.utils.response import ResponseError
from .models import Course, CoursePrereqRelationships
from .serializers import CourseSerializer, CoursePrereqRelationshipsSerializer

def getOneCourse(id, fullData=False):
    try:
        item = Course.objects.get(key=id.upper())
        if not item: return False

        if fullData:
            prereqs = CoursePrereqRelationships.objects.filter(dependent__in=[id.upper()])
            item['prereqs'] = prereqs

        return item

    except Exception as e:
        print('ERROR ->>> getting course.', '{}'.format(e))
        return False

def recursivelyGetPrereqs(course):
    course = getOneCourse(course)

def createOneCourse(data):
    try:
        existing = Course.get(key=id.upper())
        if existing: raise ResponseError(status.HTTP_409_CONFLICT, 'KEY CONFLICT', 'course key already exists')

        department = getOneDepartment(data['department'])
        if not department: raise ResponseError(status.HTTP_404_NOT_FOUND, 'NOT FOUND', 'department key no match')

        serializer = CourseSerializer(data={
            'key': data['key'].upper(),
            'department': department,
            'courseNum': data['courseNum'],
            'coreqs': data['coreqs'],
        })
        if serializer.is_valid():
            serializer.save()

        # do prereqs and dependents
        for prereq in data['prereqs']:
            prereqSerializer = CoursePrereqRelationshipsSerializer(data=prereq)
            if prereqSerializer.is_valid():
                prereqSerializer.save()

        # do coreqs
        return serializer.data

    except Exception as e:
        print('ERROR ->>> creating course.', '{}'.format(e))
        raise e

def updateCourse(id, data):
    try:
        item = Course.get(key=id.upper())
        if not item: raise ResponseError(status.HTTP_404_NOT_FOUND, 'NOT FOUND', 'course key no match')

        item.department = data['department']
        item.courseNum = data['courseNum']
        # do prereqs and dependents
        # do coreqs
        return item

    except Exception as e:
        print('ERROR ->>> updating course.', '{}'.format(e))
        raise e

def saveMultipleCourses(courseList):
    try:
        for course in courseList:
            existingCourse = getOneCourse(course['key'])
            if existingCourse: updateCourse(course['key'], course)
            else: createOneCourse(course)
        return True

    except Exception as e:
        print('ERROR ->>> saving scraoe data.', '{}'.format(e))
        raise e
