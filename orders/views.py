from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time

from .models import Order
from .utils import get_dollar_exchange_rate

def get_orders():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    resp = service.spreadsheets().values().get(spreadsheetId='1Qkuo4NopE1XbEO0TbeAUpI-QVXcxDKlJpnOEExFghgs', range="Лист1!B2:Z1000").execute()

    rows = resp['values']
    for row in rows:
        row[0] = int(row[0])
        row[1] = int(row[1])
        row[2] = datetime.strptime(row[2], '%d.%m.%Y')
    data = [dict(zip(['order_number','dollar_price','delivery_time'],row)) for row in rows]
    dollar_rate = get_dollar_exchange_rate()
    actual_data=[]
    for new_order in data:
        dollar_price = new_order['dollar_price']
        ruble_price = round(dollar_price*dollar_rate,3)
        order,created = Order.objects.update_or_create(order_number=new_order['order_number'], defaults={'dollar_price':dollar_price,
            'delivery_time':new_order['delivery_time'],'ruble_price':ruble_price})
        actual_data.append(order.order_number)
    all_orders = Order.objects.all()
    for order in all_orders:
        if order.order_number not in actual_data:
            order.delete()

def show_orders(request):
    orders = Order.objects.all().order_by('id').values()
    amount = len(orders)
    dollar_prices = [order['dollar_price'] for order in orders]
    ruble_prices = [order['ruble_price'] for order in orders]
    total_dollar_price = sum(dollar_prices)
    total_ruble_price = sum(ruble_prices)
    return render(request,'orders.html',{'total_dollar_price':total_dollar_price,'total_ruble_price':total_ruble_price,'orders':orders})

def refresh_orders_every_hour():
    schedule.every(1).minute.do(get_orders)
    while True:
        schedule.run_pending()
        time.sleep(1)