from .models import Asset, Location, Count

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
    