from rest_framework import serializers
from .models import Course, CoursePrereqRelationships, Department
from api.department.serializers import DepartmentSerializer
from api.department._utils import getOneDepartment

class CourseSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = Course
        fields = ('key')
class CourseSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=10, required=True)
    department = DepartmentSerializer(many=False, required=True)
    courseNum = serializers.IntegerField(required=True)
    coreqs = CourseSerializer(many = True, required=False)
    prereqs = CourseSerializer(many = True, required=False)

    class Meta:
        model = Course
        fields = ('__all__')

    def create(self, validated_data):
        departmentKey = validated_data.pop('department')
        departmentKey = departmentKey['key']
        prereqData = validated_data.pop('prereqs')
        # coreqData = validated_data.pop('coreqs')
        course = Course.objects.create(
            department=Department.objects.get(key=departmentKey),
            **validated_data
        )
        # for prereq in prereqData:

        return course

class CoursePrereqRelationshipsSerializer(serializers.ModelSerializer):
    group = serializers.IntegerField(default=0)
    numRequired = serializers.IntegerField(default=1)
    prereq = CourseSerializer(many=True, required=True)
    dependent = CourseSerializer(many=True, required=True)

    class Meta:
        model = CoursePrereqRelationships
        fields = ('__all__')
