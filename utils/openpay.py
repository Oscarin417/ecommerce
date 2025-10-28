import os, json, requests
from datetime import datetime, timedelta

class OpenPay:
    def __init__(self):
        self.merchant_id = os.environ.get('OPENPAY_ID')
        self.api_key = os.environ.get('OPENPAY_PRIVATE_KEY')
        self.country = 'mx'
        self.url = f'https://sandbox-api.openpay.mx/v1/{self.merchant_id}/customers'
        self.header:dict = {
            "Content-type": "application/json",
            "Authorization": "Basic c2tfNWY2YzlhMTM4OGZlNDc4MWJhOGU4NjZmZTVhMTRmNWY6"
        }

    def create_client(self, user:object, domicilio:object):
        payload:dict = {
            'name': user.first_name,
            'email': user.email,
            'address': {
                "city": domicilio.municipio,
                "state": domicilio.estado,
                "line1": f"{domicilio.calle} {domicilio.ne}",
                "postal_code": domicilio.cp,
                "line2": domicilio.colonia,
                "line3": domicilio.referencia if domicilio.referencia else '',
                "country_code": "MX",
            },
            'last_name': user.last_name,
            'phone_number': user.celular,
        }

        response = requests.post(url=self.url, headers=self.header, data=json.dumps(payload))
        return response.json()

    def pago_referencia(self, cliente_id:int, concepto:str, monto:float):
        fecha:datetime = datetime.now()
        fecha_formato = fecha.strftime("%Y-%m-%dT%H:%M:%S")
        fecha_plazo = fecha + timedelta(minutes=3)
        fecha_p_formato = fecha_plazo.strftime("%Y-%m-%dT%H:%M:%S")
        paylod:dict = {
            'method': "store",
            'amount': monto,
            'description': concepto,
            'order_id': f"oid-{fecha_formato}",
            'due_date': fecha_p_formato
        }
        response = requests.post(url=f'{self.url}/{cliente_id}/charges',
                                 headers=self.header,
                                 data=json.dumps(paylod))
        return response.json()
