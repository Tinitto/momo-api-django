from django.apps import AppConfig


class MomoRequestsConfig(AppConfig):
    name = 'momo_requests'

    def ready(self):
        import momo_requests.signals
