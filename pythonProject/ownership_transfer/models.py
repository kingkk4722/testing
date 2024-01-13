# ownership_transfer/models.py

from django.db import models
from django.contrib.auth.models import User


class Ownership(models.Model):
    model = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    IMEI_Number = models.CharField(max_length=15,unique=True,default='000000000000000')
    transfer_otp = models.CharField(max_length=10, null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.model}'s {self.owner.username} ({self.IMEI_Number})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
