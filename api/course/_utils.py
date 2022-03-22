from .models import Course, CoursePrereqRelationships
from .serializers import CourseSerializer

def deleteAllCourses():
    Course.objects.all().delete()
    return True

def getOneCourse(id):
    item = Course.objects.get(id=id)
    serializer = CourseSerializer(item)
    if serializer.is_valid():
        serializer.save()
    else:
        print('ERROR ->>>' + serializer.errors)
        return False

def postOneCourse(data):
    serializer = CourseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print('ERROR ->>>' + serializer.errors)
        return False
