from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    phonenumber = models.CharField(max_length=15, default="")
    def __str__(self):
        return self.email

class ResetPasswordCode(models.Model):
    email = models.EmailField()
    resetcode = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.email