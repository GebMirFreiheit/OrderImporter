from django.apps import AppConfig
import os
import multiprocessing


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready (self):
        from .views import refresh_orders_every_hour
        if os.environ.get('RUN_MAIN', None) != 'true':
            x = multiprocessing.Process(target=refresh_orders_every_hour, args=())
            x.daemon=True
            x.start()
