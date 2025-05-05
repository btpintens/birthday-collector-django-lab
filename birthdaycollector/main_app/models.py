from django.db import models
from datetime import date

# Create your models here.
class Birthday(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    sign = models.CharField(max_length=20)
    favoritecake = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name