from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create default user groups'

    def handle(self, *args, **kwargs):
        group_names = [
            ("Admin", ['add_accessassignment', 'change_accessassignment', 'delete_accessassignment', 'view_accessassignment']),
            ("Employee", []),
            ("Student Employee", [])
        ]
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name[0])
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name[0]}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name[0]}" already exists'))
            for perm in group_name[1]:
                self.stdout.write(self.style.WARNING(f'Permission "{perm}" added'))
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)