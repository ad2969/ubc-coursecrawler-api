from django.db import models
from api.department.models import Department

class Course(models.Model):
    key = models.CharField(max_length=10, primary_key=True)
    department = models.ForeignKey(Department, blank=False, on_delete=models.CASCADE)
    courseNum = models.IntegerField(blank=False)
    coreqs = models.ManyToManyField('self', symmetrical=True, null=True, blank=True)
    
    def __str__(self):
        return self.key

class CoursePrereqRelationships(models.Model):
    group = models.IntegerField(default=0)
    numRequired = models.IntegerField(default=1)
    prereq = models.ForeignKey(Course, related_name='prereq', on_delete=models.CASCADE)
    dependent = models.ForeignKey(Course, related_name='dependent', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('prereq', 'dependent'),)
