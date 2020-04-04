from django.apps import AppConfig


class CodenamesConfig(AppConfig):
    name = 'codenames'

    def ready(self):
        from . import signals
