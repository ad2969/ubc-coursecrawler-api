from django.shortcuts import get_object_or_404
from api.department._utils import getOneDepartment
from .models import Course, CoursePrereqRelationships
from .serializers import CourseSerializer, CoursePrereqRelationshipsSerializer

def getOneCourse(id, fullData=False):
    try:
        item = get_object_or_404(Course, key=id.upper())
        if fullData:
            data = CourseSerializer(item).data
            prereqs = CoursePrereqRelationships.objects.get(dependent=id.upper())
            return data
        else:
            return CourseSerializer(item).data

    except:
        return False

def recursivelyGetPrereqs(course):
    course = getOneCourse(course)

def createOneCourse(data):
    try:
        print('CREATING COURSE')
        department = getOneDepartment(data['department'])
        serializer = CourseSerializer(data={
            'key': data['key'].upper(),
            'department': department,
            'courseNum': data['courseNum'],
            'coreqs': data['coreqs'],
        })
        if serializer.is_valid():
            print('** course VALID!')
            serializer.save()

        print('# course either saved/not saved')
        # do prereqs and dependents
        for prereq in data['prereqs']:
            prereqSerializer = CoursePrereqRelationshipsSerializer(data=prereq)
            if prereqSerializer.is_valid():
                print('** prereq VALID!')
                # prereqSerializer.save()

        # do coreqs
        return serializer.data

    except Exception as e:
        print('ERROR ->>> creating course.', '{}'.format(e))
        return False

def updateCourse(id, data):
    try:
        item = get_object_or_404(Course, key=id.upper())
        item.department = data['department']
        item.courseNum = data['courseNum']
        # do prereqs and dependents
        # do coreqs
        return item

    except Exception as e:
        print('ERROR ->>> updating course.', '{}'.format(e))
        return False

def saveMultipleCourses(courseList):
    try:
        print('SAVE MULTIPLE')
        for course in courseList:
            existingCourse = getOneCourse(course['key'])
            if existingCourse: updateCourse(course['key'], course)
            else: createOneCourse(course)
        return True

    except:
        return False
