from rest_framework import status
from api.utils.response import ResponseError
from .models import Department
from .serializers import DepartmentSerializer

def getOneDepartment(id):
    try:
        item = Department.objects.get(key=id.upper())
        if not item: return False
        else: return item

    except Exception as e:
        print('ERROR ->>> getting department.', '{}'.format(e))
        return False

def createOneDepartment(data):
    try:
        existing = Department.objects.get(key=id.upper())
        if existing: raise ResponseError(status.HTTP_409_CONFLICT, 'KEY CONFLICT', 'department key already exists')

        data['key'] = data['key'].upper()
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return serializer.data

    except Exception as e:
        print('ERROR ->>> creating department.', '{}'.format(e))
        raise e

def updateDepartment(id, data):
    try:
        item = Department.objects.get(key=id.upper())
        if not item: raise ResponseError(status.HTTP_404_NOT_FOUND, 'NOT FOUND', 'department key no match')

        item.name = data['name']
        item.faculty = data['faculty']
        item.save()
        return item

    except Exception as e:
        print('ERROR ->>> updating department.', '{}'.format(e))
        raise e
