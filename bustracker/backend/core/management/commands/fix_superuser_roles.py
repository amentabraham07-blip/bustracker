from django.core.management.base import BaseCommand
from core.models import User


class Command(BaseCommand):
    help = 'Ensures all superusers have role=admin and is_approved=True'

    def handle(self, *args, **options):
        fixed = 0
        for user in User.objects.filter(is_superuser=True):
            changed = False
            if user.role != 'admin':
                user.role = 'admin'
                changed = True
            if not user.is_approved:
                user.is_approved = True
                changed = True
            if changed:
                user.save(update_fields=['role', 'is_approved'])
                fixed += 1
                self.stdout.write(f'  Fixed: {user.username}')
        if fixed:
            self.stdout.write(self.style.SUCCESS(f'Fixed {fixed} superuser(s).'))
        else:
            self.stdout.write('All superusers already have role=admin.')
