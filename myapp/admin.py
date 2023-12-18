# admin.py
from django.contrib import admin
from .models import UserProfile,HtmlPost

admin.site.register(UserProfile)
admin.site.register(HtmlPost)