from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario requiere un email.")

        email = self.normalize_email(email)
        user = self.model(email = email, name = name, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, name, password, **extra_fields):
        user = self.create_user(email = email, name = name, password = password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_superadmin = True

        user.save(using = self._db)

        return user
