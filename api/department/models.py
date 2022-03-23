from django.db import models

class Department(models.Model):
    rkey = models.CharField(max_length=13, primary_key=True)
    key = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)

    def __str__(self):
        return self.key + ' - ' + self.name
