from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
class AppConfig(AppConfig):
    name = 'core'
    verbose_name = 'ConectemosChile'