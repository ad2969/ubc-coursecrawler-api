from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    key = serializers.CharField(max_length=8, required=True)
    name = serializers.CharField(max_length=255, required=True)
    faculty = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Department
        fields = ('__all__')