from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """ User Extended Model """

    is_manager = models.BooleanField(default=False)
    account = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=244, blank=True, null=True)
