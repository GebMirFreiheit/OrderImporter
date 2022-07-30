from django.db import models

class Order(models.Model):
    order_number = models.IntegerField(unique=True)
    dollar_price = models.IntegerField()
    ruble_price = models.FloatField()
    delivery_time = models.DateField()
