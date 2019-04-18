from .models import Asset, Location, Count
from .models.user_models import UserType, ExtendedUser

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# TODO: work on this as script to add permission groups to DB using python manage.py ??
manager_group, created = Group.objects.get_or_create(name='manager')
permission = Permission.objects.get(codename="create_manager")
print(permission)
manager_group.permissions.add(permission)
#exit()


# TODO: create permissions for save, update, view, and delete
def can_update_items(model, data, user):
    """field-level permissions possible, here"""
    if model == Asset:
        if user.has_perm('assetmanager.change_asset'):
            return True
    elif model == Location:
        if user.has_perm('assetmanager.change_location'):
            return True
    return False



def can_create_user(user):
    """check whether user can create the type of user given in data"""
    conditions = [
        user.is_superuser,
        
        (user_type == UserType.MANAGER.val and
        user.has_perm('assetmanager.create_manager')),
        
        (user_type == UserType.REGULAR.val and
        user.has_perm('assetmanager.create_regular_user'))
    ]
    return True in conditions
    
    
# TODO: function to add permissions based on user type
def set_permissions_group(user, user_type):
    if user_type == UserType.REGULAR.val:
        user.user_permissions.set(['assetmanager.change_location'])
    if user_type == UserType.MANAGER.val:
        user.user_permissions.set(['assetmanager.create_regular_user'])
