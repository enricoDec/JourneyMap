from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'Users'

    def ready(self):
        # Django convention, don't ask why
        import Users.signals
