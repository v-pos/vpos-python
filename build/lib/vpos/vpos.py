import requests
import os
import json
import uuid

class Vpos:
    @classmethod
    def new_payment(cls, customer, amount, pos_id: __default_pos_id(), callback_url: __default_payment_callback_url()):
        headers = cls.__set_headers()
        payload = {'type':"payment", 'pos_id': pos_id, 'mobile': customer, 'amount': amount, 'callback_url': callback_url}
        request = requests.post(f"{cls.__host()}/transactions", json=payload, headers=headers)
        return cls.__return_vpos_object(request)

    @classmethod
    def new_refund(cls, transaction_id, supervisor_card: __default_supervisor_card(), callback_url: __default_refund_callback_url()):
        headers = cls.__set_headers()
        payload = {'type': "refund", 'parent_transaction_id': transaction_id, 'supervisor_card': supervisor_card, 'callback_url': callback_url}
        request = requests.post(f"{cls.__host()}/transactions", json=payload, headers=headers)
        return cls.__return_vpos_object(request)

    @classmethod
    def get_transaction(cls, transaction_id):
        request = requests.get(f"{cls.__host()}/transactions/{transaction_id}", headers=cls.__set_headers())
        return cls.__return_vpos_object(request)
    
    @classmethod
    def get_transactions(cls):
        request = requests.get(f"{cls.__host()}/transactions", headers=cls.__set_headers())
        return cls.__return_vpos_object(request)

    @classmethod
    def get_request_id(cls, request):
        if request['location'] is None:
            requests.get(f"{cls.__host()}/references/invalid", headers=cls.__set_headers())
        else:
            if request['status'] == 202:
                request['location'].gsub("/api/v1/requests/", "")
            else:
                request['location'].gsub("/api/v1/transactions/", "")

    @classmethod
    def get_request(cls, request_id):
        request = requests.get(f"{cls.__host()}/requests/{request_id}", headers=cls.__set_headers())
        cls.__return_vpos_object(request)

    @classmethod
    def __return_vpos_object(cls, request):
        code = request.response.code.to_i
        if code == 200 or code == 201:
            return {'status': request.response.code.to_i, 'message': request.response.message, 'data': request.parsed_response}
        elif code == 202 or code ==  303:
            return {'status': request.response.code.to_i, 'message': request.response.message, 'location': request.headers["location"]}
        else:
            return {'status': request.response.code.to_i, 'message': request.response.message, 'details': request.parsed_response["errors"]}

    @classmethod
    def __set_headers(cls):
        content = {}
        headers = {'Content-Type': "application/json", 'Accept': "application/json", 'Authorization': cls.__set_token(), 'Idempotency-Key': uuid.uuid4()}
        content[:headers] = headers
        return content

    @classmethod
    def __default_pos_id(cls):
        pos_id = os.environ["GPO_POS_ID"]
        return f"{pos_id}".to_i

    @classmethod
    def __default_supervisor_card(cls):
        supervisor_card = os.environ["GPO_SUPERVISOR_CARD"]
        return f"{supervisor_card}"

    @classmethod
    def __set_token(cls):
        token = os.environ["MERCHANT_VPOS_TOKEN"]
        return f"Bearer {token}"

    @classmethod
    def __default_payment_callback_url(cls):
        url = os.environ["PAYMENT_CALLBACK_URL"]
        return url

    @classmethod
    def __default_refund_callback_url(cls):
        url = os.environ["REFUND_CALLBACK_URL"]
        return url

    @classmethod
    def __host(cls):
        if os.environ["VPOS_ENVIRONMENT"] == "prd":
            return "https://api.vpos.ao/api/v1"
        else:
            return "https://sandbox.vpos.ao/api/v1"