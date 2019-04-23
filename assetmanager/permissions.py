from .models import Asset, Location, Count
from .models.user_models import UserType, ExtendedUser

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType


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



def can_create_user(user, create_type):
    """check whether user can create the type of user given in data"""
    conditions = [
        user.is_superuser,
        
        (create_type == UserType.MANAGER.val and
        user.has_perm('assetmanager.create_manager')),
        
        (create_type == UserType.REGULAR.val and
        user.has_perm('assetmanager.create_regular_user'))
    ]
    return True in conditions
    

def set_permissions_group(user, user_type):
    if user_type == UserType.REGULAR.val:
        # TODO: allow regular user to only view some info and possibly change asset locations
        # Example: user.user_permissions.set(['assetmanager.change_location'])
        group = Group.objects.get(name="regular_user")
        user.groups.add(group)
        assert user.has_perm('auth.create_regular_user')
        
    if user_type == UserType.MANAGER.val:
        group = Group.objects.get(name="manager")
        user.groups.add(group)
        assert user.has_perm('auth.create_manager')

