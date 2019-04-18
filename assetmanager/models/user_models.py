from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.timezone import now
from django.contrib.auth.models import User
from enum import Enum


class UserType(Enum):
    REGULAR = ("regular", "Regular User")
    MANAGER = ("manager", "Manager")
    
    def __init__(self, val, desc):
        self.val = val
        self.desc = desc


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=20)
    
    USER_TYPES = [
        (UserType.REGULAR.val, UserType.REGULAR.desc),
        (UserType.MANAGER.val, UserType.MANAGER.desc)
    ]
    user_type = models.CharField(max_length=7, choices=USER_TYPES)
    
    class Meta:
        permissions = (
            ("create_manager", "Can create a user that is a manager."),
            ("create_regular_user", "Can create a regular user."),
        )
    