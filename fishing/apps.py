from django.apps import AppConfig


class FishingConfig(AppConfig):
    name = 'fishing'

    def ready(self):
        import fishing.signals
