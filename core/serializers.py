from rest_framework import serializers

from core.models import AccessRule, Role, User, UserRole


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AccessRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    password_repeat = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('Пароли не совпадают.')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_repeat', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user_role, created = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Обычный пользователь'},
        )
        UserRole.objects.create(user=user, role=user_role)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'middle_name']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'middle_name': {'required': False, 'allow_blank': True},
        }

    def validate_email(self, value):
        if (
            User.objects.filter(email=value)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.',
            )
        return value
