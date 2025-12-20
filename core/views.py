import jwt
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import AccessRule, BusinessElement, User, UserRole
from core.permissions import check_permission
from core.serializers import (AccessRuleSerializer, RegisterSerializer,
                              UserUpdateSerializer)


@extend_schema(
    request=RegisterSerializer,
    responses=settings.USER_RESPONSES_SCHEMA_201,
    description='Регистрация нового пользователя',
    tags=['Аутентификация'],
)
@api_view(['POST'])
def register(request):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created'}, status=201)
    return Response(serializer.errors, status=400)


@extend_schema(
    request=settings.USER_REQUEST_SCHEMA,
    responses=settings.USER_RESPONSES_SCHEMA,
    examples=settings.EXAMPLES_LOGIN,
    tags=['Аутентификация'],
)
@api_view(['POST'])
def login(request):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email, is_active=True)
        if user.check_password(password):
            token = jwt.encode(
                {'user_id': user.id},
                settings.SECRET_KEY,
                algorithm='HS256',
            )
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)


@extend_schema(tags=['Аутентификация'])
@api_view(['POST'])
def logout(request):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    return Response({'message': 'Logged out'})


@extend_schema(
    request=UserUpdateSerializer,
    responses=settings.USER_RESPONSES_SCHEMA_201,
    description='Обновление профиля пользователя',
    tags=['Аутентификация'],
)
@api_view(['PATCH'])
def update_profile(request):
    """
    Обновление профиля текущего пользователя.
    Требуется аутентификация по JWT.
    """
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    serializer = UserUpdateSerializer(
        request.user,
        data=request.data,
        partial=True,
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@extend_schema(tags=['Аутентификация'])
@api_view(['DELETE'])
def delete_account(request):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    user = request.user
    user.is_active = False
    user.save()
    return Response({'message': 'Account deactivated'})


@extend_schema(
    responses={200: settings.PRODUCT_SCHEMA},
    description='Список доступных продуктов',
    tags=['Продукты'],
)
@api_view(['GET', 'POST'])
def products_list(request):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    element_name = 'products'
    try:
        element = BusinessElement.objects.get(name=element_name)
    except BusinessElement.DoesNotExist:
        return Response({'error': 'Resource not configured'}, status=404)

    if request.method == 'GET':
        user = request.user
        user_roles = UserRole.objects.filter(user=user).values_list(
            'role_id',
            flat=True,
        )
        rules = AccessRule.objects.filter(
            role_id__in=user_roles,
            element=element,
        )
        can_read = any(rule.read_all or rule.read_own for rule in rules)
        if not can_read:
            return Response({'error': 'Access denied'}, status=403)
        result = []
        for p in settings.MOCK_PRODUCTS:
            try:
                check_permission(user, element_name, 'read', p['owner_id'])
                result.append(p)
            except Exception:
                pass
        return Response(result)
    elif request.method == 'POST':
        check_permission(request.user, element_name, 'create')
        return Response({'message': 'Product created'}, status=201)


@extend_schema(
    responses={200: settings.PRODUCT_SCHEMA},
    description='Список доступных продуктов',
    tags=['Продукты'],
)
@api_view(['PUT', 'DELETE'])
def product_detail(request, product_id):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    element_name = 'products'
    try:
        product = next(
            p for p in settings.MOCK_PRODUCTS if p['id'] == int(product_id)
        )
    except StopIteration:
        return Response({'error': 'Not found'}, status=404)
    owner_id = product['owner_id']
    if request.method == 'PUT':
        check_permission(request.user, element_name, 'update', owner_id)
        return Response({'message': 'Product updated'})
    elif request.method == 'DELETE':
        check_permission(request.user, element_name, 'delete', owner_id)
        return Response({'message': 'Product deleted'})


@extend_schema(tags=['Администрирование'])
@api_view(['GET', 'POST'])
def access_rules(request):
    if not request.user:
        return Response({'error': 'Authentication required'}, status=401)
    check_permission(request.user, 'access_rules', 'read')
    if request.method == 'GET':
        rules = AccessRule.objects.all()
        serializer = AccessRuleSerializer(rules, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        check_permission(request.user, 'access_rules', 'create')
        serializer = AccessRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
