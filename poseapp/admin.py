from django.contrib import admin
# from django.contrib.auth.models import User

from .models import APIKey, User

admin.site.register(User)
admin.site.register(APIKey)

# Register your models here.
