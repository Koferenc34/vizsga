from django.db import models
from django.contrib.auth.models import User
 

class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=200)
