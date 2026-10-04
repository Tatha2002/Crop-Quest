from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    ADMIN = "ADMIN"
    USER = "USER"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (USER, "User"),
    ]

    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]


    objects = UserManager()

    def __str__(self):
        return self.email
