from django.apps import AppConfig


class NotifConfig(AppConfig):
    name = 'notif'
    def ready(self):
        import notif.signals
        