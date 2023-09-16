from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_backend.api'

    def ready(self):
        # This imports the signals module to ensure everything gets connected.
        import django_backend.api.signals