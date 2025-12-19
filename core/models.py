import bcrypt
from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_anonymous = False
    is_authenticated = True

    class Meta:
        app_label = 'core'

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(),
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8'),
        )

    def __str__(self):
        return self.email


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    read_own = models.BooleanField(default=False)
    read_all = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    update_own = models.BooleanField(default=False)
    update_all = models.BooleanField(default=False)
    delete_own = models.BooleanField(default=False)
    delete_all = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'element')
