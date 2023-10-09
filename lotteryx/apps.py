from django.apps import AppConfig


class LotteryxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lotteryx'
    
    def ready(self):
        pass  # Import the tasks module to ensure it's loaded
