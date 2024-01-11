from django.db import models
import os
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    @staticmethod
    def create_user(self, email):
        ListUserManager.objects.create(email=email)

    @staticmethod
    def create_superuser(self, email):
        ListUserManager.objects.create(email=email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["email", "height"]

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == os.getenv("ADMIN_EMAIL")

    @property
    def is_active(self):
        return True

