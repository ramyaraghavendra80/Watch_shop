from django.apps import AppConfig


class WatchshopAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watchshop_app'


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from . import signals
