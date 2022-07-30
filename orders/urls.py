from django import views
from django.urls import path

from . import views

urlpatterns = [
    path('',views.show_orders,name='show_orders')
]