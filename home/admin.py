from django.contrib import admin

# Register your models here.
from .models import Profile, Reset_token, Tutorprofile, Course_code

admin.site.register(Profile)
admin.site.register(Tutorprofile)
admin.site.register(Reset_token)
admin.site.register(Course_code)