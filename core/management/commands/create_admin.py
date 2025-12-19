from django.core.management.base import BaseCommand

from core.models import Role, User, UserRole


class Command(BaseCommand):
    help = 'Создаёт суперпользователя-админа'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True)
        parser.add_argument('--password', type=str, required=True)
        parser.add_argument('--first-name', type=str, default='Admin')
        parser.add_argument('--last-name', type=str, default='User')

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Администратор'},
        )
        user = User.objects.create(
            email=options['email'],
            first_name=options['first_name'],
            last_name=options['last_name'],
            is_active=True,
        )
        user.set_password(options['password'])
        user.save()
        UserRole.objects.get_or_create(user=user, role=admin_role)
        self.stdout.write(
            self.style.SUCCESS(f'Админ успешно создан: {user.email}'),
        )
