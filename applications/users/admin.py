from django.contrib import admin
from . import models
# Register your models here.
class AdminUserProfile(admin.ModelAdmin):
    list_display = (
        "id",
        "email"
    )
admin.site.register(models.UserProfile, AdminUserProfile)
