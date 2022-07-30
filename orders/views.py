from django.shortcuts import render
from datetime import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import time

from .models import Order
from .utils import get_dollar_exchange_rate

#метод получает данные из Google-таблицы и соответственно обновляет данные в БД
def get_orders():
    #аутентификация в сервисном аккаунте Google
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    #получение данных из таблицы
    resp = service.spreadsheets().values().get(spreadsheetId='1Qkuo4NopE1XbEO0TbeAUpI-QVXcxDKlJpnOEExFghgs', range="Лист1!B2:Z1000").execute()

    rows = resp['values']
    actual_data=[] #список номеров актуальных заказов (т.е. тех, которые на момент запроса есть в таблице)
    #номер заказа и цена переводятся в int, срок поставки в date
    for row in rows:
        row[0] = int(row[0])
        row[1] = int(row[1])
        row[2] = datetime.strptime(row[2], '%d.%m.%Y')
        actual_data.append(row[0])
    data = [dict(zip(['order_number','dollar_price','delivery_time'],row)) for row in rows]
    dollar_rate = get_dollar_exchange_rate()
    for new_order in data:
        dollar_price = new_order['dollar_price']
        ruble_price = round(dollar_price*dollar_rate,3)
        order,created = Order.objects.update_or_create(order_number=new_order['order_number'], defaults={'dollar_price':dollar_price,
            'delivery_time':new_order['delivery_time'],'ruble_price':ruble_price})
    all_orders = Order.objects.all()
    #удаление отсутствующих в таблице заказов
    for order in all_orders:
        if order.order_number not in actual_data:
            order.delete()

#метод использует html темплейт, чтобы вывести таблицу заказов и их суммарную стоимость
def show_orders(request):
    orders = Order.objects.all().order_by('id').values()
    dollar_prices = [order['dollar_price'] for order in orders]
    ruble_prices = [order['ruble_price'] for order in orders]
    total_dollar_price = sum(dollar_prices)
    total_ruble_price = sum(ruble_prices)
    return render(request,'orders.html',{'total_dollar_price':total_dollar_price,'total_ruble_price':total_ruble_price,'orders':orders})

#метод используется для шедулинга задач
def refresh_orders_every_minute():
    schedule.every(1).minute.do(get_orders)
    while True:
        schedule.run_pending()
        time.sleep(1)
