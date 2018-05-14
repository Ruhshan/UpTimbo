from django.db import models
from datetime import  timezone
# Create your models here.


class Site(models.Model):
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    url = models.URLField()
    interval = models.IntegerField(default=120)
    isalive = models.BooleanField(default=False)
    ismonitoring = models.BooleanField(default=True)
    isdeleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user+"@"+str(self.id)
