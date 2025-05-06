from django.db import models
from datetime import date


class Party(models.Model):
    theme = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    presents = models.BooleanField(default=False)
    
    def __str__(self):
        return self.theme


class Birthday(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    sign = models.CharField(max_length=20)
    favoritecake = models.CharField(max_length=100)
    parties = models.ManyToManyField(Party)
    
    def __str__(self):
        return self.name
    

    
