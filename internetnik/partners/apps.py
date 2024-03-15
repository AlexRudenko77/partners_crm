from django.apps import AppConfig


class PartnersConfig(AppConfig):
    verbose_name = "База данных"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'partners'
    
    def ready(self):
        import partners.signals 
