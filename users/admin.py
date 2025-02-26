from django.contrib import admin
from users.models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # list_display = ['user__email', 'age']
    search_fields = ['user__email']
