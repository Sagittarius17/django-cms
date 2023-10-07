from .models import SimpleUser

def get_user_profile(user_id):
    try:
        return SimpleUser.objects.get(id=user_id)
    except SimpleUser.DoesNotExist:
        return None
