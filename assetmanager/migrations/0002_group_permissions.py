from django.db import migrations
#from .models import Asset, Location, Count
#from .models.user_models import UserType, ExtendedUser

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# TODO: refactor to read in some configuration data to make it more DRY

def my_make_permissions(apps, schema_editor):
    # Get models that we needs them
    user = apps.get_model("auth", "User")
    permission = apps.get_model("auth", "Permission")
    content_type = apps.get_model("contenttypes", "ContentType")
    # Get user content type object
    uct = content_type.objects.get_for_model(user)
    db_alias = schema_editor.connection.alias
    # Adding your custom permissions to User model:
    permission.objects.using(db_alias).bulk_create([
        permission(codename='create_manager', name='Can create a user that is a manager.', content_type=uct),
        permission(codename='create_regular_user', name='Can create a regular user.', content_type=uct),
    ])

    
def group_permissions(apps, schema_editor):
    my_make_permissions(apps, schema_editor)
    
    manager_group, created = Group.objects.get_or_create(name='manager')
    permission = Permission.objects.get(codename="create_manager")
    print(permission)
    manager_group.permissions.add(permission)
    
    # TODO: repetitious - needs refactor
    manager_group, created = Group.objects.get_or_create(name='regular_user')
    permission = Permission.objects.get(codename="create_regular_user")
    print(permission)
    manager_group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        # Dependencies to other migrations
        ('assetmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(group_permissions),
    ]