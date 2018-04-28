from django.db import models

# Create your models here.


class Site(models.Model):
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    interval = models.IntegerField(default=120)
    isalive = models.BooleanField(default=False)
    ismonitoring = models.BooleanField(default=True)

    def __str__(self):
        return self.user+"@"+self.name
