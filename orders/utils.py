import json
import requests
import xmltodict

# метод получает курс доллара с помощью api центробанка


def get_dollar_exchange_rate():
    resp = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    decoded_resp = resp.content.decode('windows-1251')
    resp_json = json.loads(json.dumps(xmltodict.parse(decoded_resp)))
    for valute in resp_json['ValCurs']['Valute']:
        if valute['CharCode'] == 'USD':
            return(float(valute['Value'].replace(',', '.')))
