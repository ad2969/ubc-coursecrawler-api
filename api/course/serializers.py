from rest_framework import serializers
from .models import Course, CoursePrereqRelationships
from api.department.serializers import DepartmentSerializer

class CourseSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=8, required=True)
    department = DepartmentSerializer(many=False, required=True)
    courseNum = serializers.IntegerField(required=True)
    prereqs = serializers.SlugRelatedField(
        many = True,
        slug_field=CoursePrereqRelationships.dependent,
        read_only=True,
    )
    dependents = serializers.SlugRelatedField(
        many = True,
        slug_field=CoursePrereqRelationships.prereq,
        read_only=True,
    )
    coreqs = serializers.SlugRelatedField(
        many = True,
        slug_field=Course.key,
        read_only=True,
    )

    class Meta:
        model = Course
        fields = ('__all__')

class CoursePrereqRelationshipsSerializer(serializers.ModelSerializer):
    group = serializers.IntegerField(default=0)
    numRequired = serializers.IntegerField(default=1)
    prereq = CourseSerializer(many=True, required=True)
    dependent = CourseSerializer(many=True, required=True)

    class Meta:
        model = CoursePrereqRelationships
        fields = ('__all__')
