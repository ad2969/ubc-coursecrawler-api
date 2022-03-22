from django.db import models

class Department(models.Model):
    key = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)

    def __str__(self):
        return self.key + ' - ' + self.name
