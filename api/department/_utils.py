from django.shortcuts import get_object_or_404
from .models import Department
from .serializers import DepartmentSerializer

def getOneDepartment(id):
    try:
        item = get_object_or_404(Department, key=id.upper())
        return DepartmentSerializer(item).data

    except:
        return False

def createOneDepartment(data):
    try:
        data['key'] = data['key'].upper()
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return serializer.data

    except Exception as e:
        print('ERROR ->>> creating department.', '{}'.format(e))
        return False

def updateDepartment(id, data):
    try:
        item = get_object_or_404(Department, key=id.upper())
        item.name = data['name']
        item.faculty = data['faculty']
        return item

    except Exception as e:
        print('ERROR ->>> updating department.', '{}'.format(e))
        return False
