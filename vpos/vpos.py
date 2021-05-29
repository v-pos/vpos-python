"""
Module contains Vpos class
"""
import os
import uuid

import requests


class Vpos:
    """
    A Class used to represent the vPOS Api

    ...
    Methods
    ----------
    new_payment(customer, amount, **kwargs):
        Creates a new payment
    new_refund(transaction_id, **kwargs):
        Creates a new Refund
    get_transaction(transaction_id):
        Gets a single transaction
    get_transactions():
        Gets a alls transactions
    get_request_id(request):
        Gets a requests id
    get_request(request_id):
        Gets a single request
    """

    # pylint: disable=R0913
    def __init__(self, environment=None, token=None, pos_id=None,
                 supervisor_card=None, payment_callback_url=None,
                 refund_callback_url=None):
        """
        __init__ Creates a new instance os `Vpos` Class

        With params from environment variable or optionaly defined
        in the method

        Parameters
        ----------
        environment : `str`, optional
            The vPOS environment, leave empty for `sandbox` mode and use
            `PRD` for `production`, by default is the environment variable
        token : `str`, optional
            Token generated at vpos site dashboard,
            by default is the environment variable
        pos_id : `str`, optional
            Merchant POS ID provided by EMIS, by default is the environment
            variable
        supervisor_card : `str`, optional
            Merchant Supervisor Card number provided by EMIS,
            by default is the environment variable
        payment_callback_url : `str`, optional
            Merchant application JSON endpoint to accept the callback
            payment response, by default is the environment variable
        refund_callback_url : `str`, optional
            Merchant application JSON endpoint to accept the callback
            refund response, by default is the environment variable
        """
        self.environment = environment if environment is not None else "SBX"
        self.token = token if token is not None else self.__set_token()
        self.pos_id = pos_id if pos_id is not None else self.__default_pos_id()
        self.supervisor_card = supervisor_card if supervisor_card is not None \
            else self.__default_supervisor_card()
        self.payment_callback_url = payment_callback_url \
            if payment_callback_url is not None else \
            self.__default_payment_callback_url()
        self.refund_callback_url = refund_callback_url \
            if refund_callback_url is not None else \
            self.__default_refund_callback_url()

    def new_payment(self, customer, amount, **kwargs):
        """Creates a new payment

        Given a customer cellphone and the amount return a new payment
        Parameters
        ----------
        customer  : `str`
            The phone number for the customer being charged
        amount : `str`
            The amount of money being charged
        **kwargs
            Aditional arguments passed to the function

        Keyword Args
        ------------
        pos_id : `str`
            the point of sale identification it defaults
            to the 'GPO_POS_ID' environment var
        callback_url : `str`
            the callback url it defaults to 'PAYMENT_CALLBACK_URL'
            environment var

        Returns
        -------
        response : `dict`
            A dictionary containing either the payment
            info or an error response
        """
        headers = self.__set_headers()
        host = self.__host()

        pos_id = kwargs.get('pos_id', self.pos_id)
        callback_url = kwargs.get(
            'callback_url', self.refund_callback_url)
        payload = {'type': "payment", 'pos_id': pos_id,
                   'mobile': customer, 'amount': amount,
                   'callback_url': callback_url}
        response = requests.post(f"{host}/transactions", json=payload,
                                 headers=headers)
        return self.__return_vpos_object(response)

    def new_refund(self, parent_transaction_id, **kwargs):
        """creates a new refund transaction

        Creates a refund transaction given the parent transaction id

        Parameters
        ----------
        parent_transaction_id : `str`
            This is a string value of the transaction id you're
            requesting to be refunded.

        Keyword Args
        ------------
        supervisor_card : `str`
            A 16 characters string digits representing the supervisor card
            provided by EMIS it defaults to GPO_SUPERVISOR_CARD environment var
        callback_url : `str`
            the callback url it defaults to 'PAYMENT_CALLBACK_URL'
            environment var

        Returns
        -------
        `dict`
            a dictionary with status, message and location
        """
        supervisor_card = kwargs.get(
            'supervisor_card', self.supervisor_card)
        callback_url = kwargs.get(
            'callback_url', self.refund_callback_url)
        headers = self.__set_headers()
        host = self.__host()
        payload = {
            'type': "refund", 'parent_transaction_id': parent_transaction_id,
            'supervisor_card': supervisor_card, 'callback_url': callback_url}
        request = requests.post(
            f"{host}/transactions", json=payload, headers=headers)
        return self.__return_vpos_object(request)

    def get_transaction(self, transaction_id):
        """Gets a single transaction

        Given the transaction id or and error object if the
        transaction was not found

        Parameters
        ----------
        transaction_id : `str`
            The id of the transaction to retrieve

        Returns
        -------
        `dict`
            A dictionary containing the transaction data
        """
        host = self.__host()
        request = requests.get(
            f"{host}/transactions/{transaction_id}",
            headers=self.__set_headers())
        return self.__return_vpos_object(request)

    def get_transactions(self):
        """Retrieves all transactions

        In the account

        Returns
        -------
            a object containg the transactions data
        """
        host = self.__host()
        request = requests.get(
            f"{host}/transactions", headers=self.__set_headers())
        return self.__return_vpos_object(request)

    def get_request_id(self, response):
        """return the id in a response containing a location attribute

        Given a response dict

        Parameters
        ----------
        response : `dict`
            A dictionary containg a location attribute

        Returns
        -------
        `str`
            A request id
        """
        host = self.__host()
        request_id = ""
        if response['location'] is None:
            request_id = requests.get(
                f"{host}/references/invalid", headers=self.__set_headers())
        else:
            if response['status'] == 202:
                request_id = response['location'].gsub("/api/v1/requests/", "")
            else:
                request_id = response['location'].gsub(
                    "/api/v1/transactions/", "")
        return request_id

    def get_request(self, request_id):
        """retrieves a request

        Given its id

        Parameters
        ----------
        request_id : `str`
            The id returned in a new transaction request

        Returns
        -------
        `dict`
            dictionary containing a response object
        """
        host = self.__host()
        response = requests.get(
            f"{host}/requests/{request_id}", headers=self.__set_headers())
        return self.__return_vpos_object(response)

    @staticmethod
    def __return_vpos_object(response: requests.Response):
        code = response.status_code
        response_body = {'status_code': code}
        if code in (200, 201):
            json_response = response.json()
            response_body['data'] = json_response
        elif code in (202, 303):
            response_body['location'] = response.headers['location']
        else:
            json_response = response.json()
            try:
                response_body['details'] = json_response.get('errors')
                response_body['message'] = json_response.get('message')
            except AttributeError as err:
                if err.args.__contains__('get') \
                        and err.args.__contains__('str'):
                    response_body['message'] = json_response
        return response_body

    def __set_headers(self):
        headers = {'Content-Type': "application/json",
                   'Accept': "application/json",
                   'Authorization': f"Bearer {self.token}",
                   'Idempotency-Key': uuid.uuid4().__str__()}
        return headers

    @staticmethod
    def __default_pos_id():
        pos_id = os.getenv("GPO_POS_ID")
        return int(f"{pos_id}")

    @staticmethod
    def __default_supervisor_card():
        supervisor_card = os.getenv("GPO_SUPERVISOR_CARD")
        return f"{supervisor_card}"

    @staticmethod
    def __set_token():
        token = os.getenv("MERCHANT_VPOS_TOKEN")
        return token

    @staticmethod
    def __default_payment_callback_url():
        url = os.getenv("PAYMENT_CALLBACK_URL")
        return url

    @staticmethod
    def __default_refund_callback_url():
        url = os.getenv("REFUND_CALLBACK_URL")
        return url

    def __host(self):
        if self.environment == "PRD":
            return "https://api.vpos.ao/api/v1"

        return "https://sandbox.vpos.ao/api/v1"
