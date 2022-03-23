from rest_framework import serializers
from .models import Course, CoursePrereqRelationships

class CoursePrereqRelationshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePrereqRelationships
        fields = ('__all__')

class CourseSerializer(serializers.ModelSerializer):
    prereqs = CoursePrereqRelationshipsSerializer(many = True, required=False)

    class Meta:
        model = Course
        fields = ('__all__')
