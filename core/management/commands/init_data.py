from django.core.management.base import BaseCommand

from core.models import AccessRule, BusinessElement, Role


class Command(BaseCommand):
    help = 'Инициализирует роли, бизнес-элементы и правила доступа'

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Полный доступ ко всем ресурсам'},
        )
        user_role, _ = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Доступ только к своим объектам'},
        )

        products, _ = BusinessElement.objects.get_or_create(
            name='products',
            defaults={'description': 'Товары в системе'},
        )
        access_rules_el, _ = BusinessElement.objects.get_or_create(
            name='access_rules',
            defaults={'description': 'Правила управления доступом'},
        )

        AccessRule.objects.get_or_create(
            role=admin_role,
            element=products,
            defaults={
                'read_all': True,
                'create': True,
                'update_all': True,
                'delete_all': True,
            },
        )
        AccessRule.objects.get_or_create(
            role=admin_role,
            element=access_rules_el,
            defaults={'read_all': True, 'create': True},
        )

        AccessRule.objects.get_or_create(
            role=user_role,
            element=products,
            defaults={
                'read_own': True,
                'create': True,
                'update_own': True,
                'delete_own': True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS('✅ Начальные данные успешно загружены!'),
        )
