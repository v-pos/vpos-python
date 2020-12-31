import requests
import os
import json
import uuid

class Vpos:
    
    def new_payment(self, customer, amount, **kwargs):
        headers = self.__set_headers()
        host = self.__host()
        pos_id = kwargs.get('pos_id', self.__default_pos_id())
        callback_url = kwargs.get('callback_url', self.__default_refund_callback_url())
        payload = {'type':"payment", 'pos_id': pos_id, 'mobile': customer, 'amount': amount, 'callback_url': callback_url}
        response = requests.post(f"{host}/transactions", json=payload, headers=headers)
        return self.__return_vpos_object(response)

    def new_refund(self, transaction_id, **kwargs):
        supervisor_card = kwargs.get('supervisor_card', self.__default_supervisor_card())
        callback_url = kwargs.get('callback_url', self.__default_refund_callback_url())
        headers = self.__set_headers()
        host = self.__host()
        payload = {'type': "refund", 'parent_transaction_id': transaction_id, 'supervisor_card': supervisor_card, 'callback_url': callback_url}
        request = requests.post(f"{host}/transactions", json=payload, headers=headers)
        return self.__return_vpos_object(request)

    def get_transaction(self, transaction_id):
        host = self.__host()
        request = requests.get(f"{host}/transactions/{transaction_id}", headers=self.__set_headers())
        return self.__return_vpos_object(request)
    
    def get_transactions(self):
        host = self.__host()
        request = requests.get(f"{host}/transactions", headers=self.__set_headers())
        return self.__return_vpos_object(request)

    def get_request_id(self, request):
        host = self.__host()
        if request['location'] is None:
            requests.get(f"{host}/references/invalid", headers=self.__set_headers())
        else:
            if request['status'] == 202:
                request['location'].gsub("/api/v1/requests/", "")
            else:
                request['location'].gsub("/api/v1/transactions/", "")

    def get_request(self, request_id):
        host = self.__host()
        response = requests.get(f"{host}/requests/{request_id}", headers=self.__set_headers())
        return self.__return_vpos_object(response)

    def __return_vpos_object(self, response):
        code = response.status_code
        response_body = {'status': code}
        if code == 200 or code == 201:
            json_response = response.json()
            response_body['data'] = json_response
        elif code == 202 or code ==  303:
            response_body['location'] = response.headers['location']
        else:
            json_response = response.json()
            try:
                response_body['details'] = json_response.get('errors')
                response_body['message'] = json_response.get('message')
            except AttributeError as err:
                if err.args.__contains__('get') and err.args.__contains__('str'):
                    response_body['message'] = json_response
        return response_body

    def __set_headers(self):
        headers = {'Content-Type': "application/json", 'Accept': "application/json", 'Authorization': self.__set_token(), 'Idempotency-Key': uuid.uuid4().__str__()}
        return headers

    def __default_pos_id(self):
        pos_id = os.getenv("GPO_POS_ID")
        return int(f"{pos_id}")

    def __default_supervisor_card(self):
        supervisor_card = os.getenv("GPO_SUPERVISOR_CARD")
        return f"{supervisor_card}"

    def __set_token(self):
        token = os.getenv("MERCHANT_VPOS_TOKEN")
        return f"Bearer {token}"

    def __default_payment_callback_url(self):
        url = os.getenv("PAYMENT_CALLBACK_URL")
        return url

    def __default_refund_callback_url(self):
        url = os.getenv("REFUND_CALLBACK_URL")
        return url

    def __host(self):
        if os.getenv("VPOS_ENVIRONMENT") == "PRD":
            return "https://api.vpos.ao/api/v1"
        else:
            return "https://sandbox.vpos.ao/api/v1"