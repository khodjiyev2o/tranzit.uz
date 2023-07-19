from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, full_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("User must have a phone!")
        if not full_name:
            raise ValueError("User must have a full name!")
        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, full_name, password):
        if not password:
            raise ValueError("Super User must have  password!")
        user = self.create_user(phone=phone, password=password, full_name=full_name)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
