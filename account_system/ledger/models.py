from django.db import models
from django.contrib.auth.admin import User 

# Create your models here.
class User(models.Model) :
    user = models.ForeignKey(User,)
    updated = models.DateTimeField(auto_now=True)
    current_date = models.DateTimeField(auto_now_add=True)
    assign_date = models.DateTimeField()
    balance  =models.IntegerField()
    category = models.CharField(max_lenght= 200)
    description = models.CharField(max_lenght= 200)
    debit = models.IntegerField()
    credit = models.IntegerField()

    def __str__(self) :
        return self.name

    
