from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from access.models import Size, Gender, Color, Category


class Command(BaseCommand):
    help = 'Create default user groups'

    def handle(self, *args, **kwargs):
        group_names = [
            ("Admin", ['add_accessassignment', 'change_accessassignment', 'delete_accessassignment', 'view_accessassignment', 'add_clothingitem', 'change_clothingitem', 'delete_clothingitem', 'view_clothingitem']),
            ("Employee", ['add_clothingitem', 'change_clothingitem', 'delete_clothingitem', 'view_clothingitem', 'add_order', 'change_order', 'delete_order', 'view_order']),
            ("Student Employee", ['add_clothingitem', 'change_clothingitem', 'delete_clothingitem', 'view_clothingitem', 'add_order', 'change_order', 'delete_order', 'view_order']),
        ]

        sizes = [
            "X-Small",
            "Small",
            "Medium",
            "Large",
            "X-Large",
            "2XL",
            "3XL",
            "4",
            "6",
            "8",
            "10",
            "12",
            "14",
            "16",
            "18",
            "20",
            "22",
            "24",
            "26",
            "28",
            "30",
            "32",
            "34",
            "36",
            "38",
            "40",
            "42",
            "44",
            "46",
            "48",
        ]

        genders = [
            "Genderless",
            "Male",
            "Female",
        ]

        colors = [
            "Red",
            "Blue",
            "Green",
            "Yellow",
            "Black",
            "White",
            "Gray",
            "Pink",
            "Purple",
            "Orange",
            "Brown",
            "Beige",
            "Navy",
            "Maroon",
            "Teal",
            "Olive",
            "Multi Color",
            "Other"
        ]

        categories = [
            "Jacket",
            "Skirt",
            "Dress",
            "Shirt",
            "Pants",
            "Belt",
            "Tie",
            "Outfit",

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

        for size in sizes:
            size, created = Size.objects.get_or_create(size_value=size)

        for gender in genders:
            gender, created = Gender.objects.get_or_create(gender_name=gender)

        for color in colors:
            color, created = Color.objects.get_or_create(color_name=color)

        for category in categories:
            category, created = Category.objects.get_or_create(category_name=category)