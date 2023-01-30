from django.apps import AppConfig


class ServisasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servisas'

    def ready(self):
        from .signals import create_profile, save_profile
