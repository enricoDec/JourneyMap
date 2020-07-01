from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_active', False)

        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_active=extra_fields.get('is_active'),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user
