from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

from .managers import UserProfileManager
# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique = True, max_length=15)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    image = models.ImageField(upload_to="dir/user/", blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add = True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)


    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "last_name", "username"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_name(self):
        return self.name

    def get_last_name(self):
        return self.last_name


    # def get_absolute_url(self):
    #     return reverse("users", kwargs = {"pk": self.id})

    def __str__(self):
        return self.email
