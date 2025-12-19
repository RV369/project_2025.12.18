from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from core.models import AccessRule, BusinessElement, UserRole


def check_permission(user, element_name, action, obj_owner_id=None):
    if not user:
        raise AuthenticationFailed('Authentication required.')
    try:
        element = BusinessElement.objects.get(name=element_name)
    except BusinessElement.DoesNotExist:
        raise PermissionDenied('Resource not configured.')
    user_role_ids = UserRole.objects.filter(user=user).values_list(
        'role_id',
        flat=True,
    )
    rules = AccessRule.objects.filter(
        role_id__in=user_role_ids,
        element=element,
    )
    for rule in rules:
        if action == 'read':
            if rule.read_all or (rule.read_own and obj_owner_id == user.id):
                return True
        elif action == 'create' and rule.create:
            return True
        elif action == 'update':
            if rule.update_all or (
                rule.update_own and obj_owner_id == user.id
            ):
                return True
        elif action == 'delete':
            if rule.delete_all or (
                rule.delete_own and obj_owner_id == user.id
            ):
                return True
    raise PermissionDenied('Access denied.')
