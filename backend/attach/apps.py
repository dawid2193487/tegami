from django.apps import AppConfig


class AttachConfig(AppConfig):
    name = 'attach'
    
    def ready(self):
        import attach.signals