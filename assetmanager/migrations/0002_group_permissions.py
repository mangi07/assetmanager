from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class MPermission:
    def __init__(self, codename, name):
        self.codename = codename
        self.name = name


class MGroup:
    """Permissions group containing a list of permissions
    
    Attributes:
        name (str): Name of permissions group.
        permissions (:obj:`list` of :obj:`MPermission`): Permissions in this group.
    """
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions


# TODO: add groups or permissions as needed
# TODO: read this in from config file shared with other code, such as code that calls has_perm
groups = [
    MGroup(
        "manager",
        [
            MPermission("create_regular_user", "Can create a regular user."),
        ]
    ),
    MGroup(
        "regular_user",
        [
        ]
    )
]

    
def group_permissions(apps, schema_editor):
    user = apps.get_model("auth", "User") # TODO: is this why 'auth.create_manager' and not 'assetmanager.create_manager' ?
    permission = apps.get_model("auth", "Permission")
    content_type = apps.get_model("contenttypes", "ContentType")
    uct = content_type.objects.get_for_model(user)
    db_alias = schema_editor.connection.alias
    
    for group in groups:
        g, created = Group.objects.get_or_create(name=group.name)
        for p in group.permissions:
            permission.objects.using(db_alias).create(codename=p.codename, name=p.name, content_type=uct)
            perm = Permission.objects.get(codename=p.codename)
            # TODO: figure out why these permissions are under 'auth' and not 'assetmanager'
            # Example: user.has_perm('auth.create_manager')
            g.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        # Dependencies to other migrations
        ('assetmanager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(group_permissions),
    ]


