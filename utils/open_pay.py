import os, openpay
from datetime import datetime, timedelta

class Open_Pay:
    def __init__(self):
        openpay.api_key = os.environ.get('OPENPAY_PRIVATE_KEY')
        openpay.verify_ssl_certs = False
        openpay.merchant_id = os.environ.get('OPENPAY_ID')
        openpay.production = False
        openpay.country = 'mx'

    def create_client(self, user, domicilio):
        client = openpay.Customer.create(
            name = user.first_name,
            email = user.email,
            address = {
                "city": domicilio.municipio,
                "state": domicilio.estado,
                "line1": f"{domicilio.calle} {domicilio.ne}",
                "postal_code": domicilio.cp,
                "line2": domicilio.colonia,
                "line3": domicilio.referencia if domicilio.referencia else '',
                "country_code": "MX",
            },
            last_name = user.last_name,
            phone_number = user.celular,
        )
        return client

    def pago_referencia(self, cliente_id, concepto, monto):
        fecha = datetime.now()
        fecha_formato = fecha.strftime("%Y-%m-%dT%H:%M:%S")
        fecha_plazo = fecha + timedelta(days=30)
        fecha_p_formato = fecha_plazo.strftime("%Y-%m-%dT%H:%M:%S")
        user = openpay.Customer.retrieve(cliente_id)
        charge = user.charges.create(
            method = "store",
            amount = monto,
            description = concepto,
            order_id = f"oid-{fecha_formato}",
            due_date = fecha_p_formato
        )
        return charge
