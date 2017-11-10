from django.contrib import admin

# Register your models here.
from .models import Profile, Reset_token

admin.site.register(Profile)
admin.site.register(Reset_token)