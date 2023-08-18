from django.contrib import admin

from .models import CustomUser, LoginAttempt

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(LoginAttempt)
class CustomUserAdmin(admin.ModelAdmin):
    pass