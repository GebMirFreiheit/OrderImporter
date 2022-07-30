from django.apps import AppConfig
import os
import multiprocessing


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    #перегружается метод ready, чтобы при загрузке приложения создавался подпроцесс, в котором будет выполняться периодическая задача
    def ready (self):
        from .views import refresh_orders_every_minute
        if os.environ.get('RUN_MAIN', None) != 'true':
            x = multiprocessing.Process(target=refresh_orders_every_minute, args=())
            x.daemon=True
            x.start()
