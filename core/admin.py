from django.contrib import admin
from core.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from anagrafica.models import Staff

class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'staff'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StaffInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(MotivationalPhrase)