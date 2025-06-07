from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'


    def ready(self):
        from blog.utils import sync_db_to_redis
        sync_db_to_redis()