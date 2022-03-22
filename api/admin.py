from django.contrib import admin
from api.models import *

admin.site.register(Course)
admin.site.register(CoursePrereqRelationships)
admin.site.register(CoursePrereqProxy)
admin.site.register(Department)
