import getpass
from django.core.management.base import BaseCommand, CommandError
from accounts.models import User, normalize_phone
class Command(BaseCommand):
    help = "Create an administrator interactively."
    def handle(self, *args, **options):
        phone=input("Phone number: "); name=input("Full name: "); password=getpass.getpass("Password: "); confirm=getpass.getpass("Confirm password: ")
        if password != confirm: raise CommandError("Passwords do not match.")
        if len(password) < 8: raise CommandError("Password must be at least 8 characters.")
        if User.objects.filter(phone_number=normalize_phone(phone)).exists(): raise CommandError("An account already exists for this phone number.")
        User.objects.create_superuser(phone_number=phone, name=name, password=password)
        self.stdout.write(self.style.SUCCESS("Administrator created."))
