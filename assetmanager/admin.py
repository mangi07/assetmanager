from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Asset, Location, Count
from .models.user_models import ExtendedUser

# Register your models here.
admin.site.register(Asset)
admin.site.register(Location)
admin.site.register(Count)


# Define an inline admin descriptor for extended user model
# which acts a bit like a singleton
class ExtendedUserInline(admin.StackedInline):
    model = ExtendedUser
    can_delete = False
    verbose_name_plural = 'extended user'

# Define a new ManagerUser admin
class ExtendedUserAdmin(BaseUserAdmin):
    inlines = (ExtendedUserInline,)

# Re-register ManagerUserAdmin
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
admin.site.register(ExtendedUser)
