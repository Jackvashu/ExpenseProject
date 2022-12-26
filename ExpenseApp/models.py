from django.db import models
from django.utils.timezone import now

# Create your models here.

class Addmoney(models.Model):
    transType = models.CharField(max_length = 30 )
    quantity = models.BigIntegerField()
    transDate = models.DateField(default = now)
    catData = models.CharField( max_length = 50)
    transDisc = models.CharField(max_length=50)
    
    def __str__(self):
        return self.transType


#  for profile 
class Profile(models.Model):
    user = models.CharField(max_length=50)
    current_balance = models.CharField(max_length=10)
    budget = models.CharField(max_length=10)

    def __str__(self):
        return self.user
