from django.contrib import admin

# Register your models here.
from .models import Session, Review

admin.site.register(Session)
admin.site.register(Review)