from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
# admin.site.register(User,Causes)

admin.site.register(Cause)
admin.site.register(Vote)

# Register your models here.
