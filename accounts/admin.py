from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ConstomUser, UserHealth


    

admin.site.register(ConstomUser)
admin.site.register(UserHealth)
