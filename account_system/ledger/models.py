from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    assign_date = models.DateTimeField()
    balance = models.IntegerField()
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    debit = models.IntegerField()
    credit = models.IntegerField()
    m_of_pay = models.CharField(max_length=200)

    # class Meta:
    #     ordering = ["updated", "created"]

    def __str__(self):
        return self.user.username
