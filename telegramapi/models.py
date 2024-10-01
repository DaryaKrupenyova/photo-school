from django.db import models

# Create your models here.


class BugReports(models.Model):
    user = models.IntegerField(default=1)
