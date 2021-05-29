from vpos.vpos import Vpos


class TestVpos:
    # Payments
    # # Positives
    def test_should_create_a_new_payment_request_transaction(self):
        merchant = Vpos()
        payment = merchant.new_payment('992563019', '123.45')

        assert payment.get('status_code') == 202

    # # Negatives
    def test_should_not_create_a_payment_if_customer_format_is_invalid(self):
        merchant = Vpos()
        payment = merchant.new_payment('99256301', '123.45')

        assert payment.get('status_code') == 400

    def test_should_not_create_a_payment_if_amount_format_is_invalid(self):
        merchant = Vpos()
        payment = merchant.new_payment('992563019', '123.45.01')

        assert payment.get('status_code') == 400

    def test_should_not_create_a_payment_if_token_is_invalid(self):
        merchant = Vpos(token='1jYQryG3Qo4nzaOKgJxzWDs25Hv')
        payment = merchant.new_payment('925888553', '123.45')

        assert payment.get('status_code') == 401

    # Refunds
    # # Positives
    def test_should_create_a_refund_request_transaction(self):
        merchant = Vpos()
        response = merchant.new_refund('1jYQryG3Qo4nzaOKgJxzWDs25Hv')

        assert response.get('status_code') == 202

    # # Negatives
    def test_should_not_create_refund_if_parent_transaction_id_is_blank(self):
        merchant = Vpos()
        response = merchant.new_refund(None)

        assert response.get('status_code') == 400

    def test_should_not_create_a_refund_if_token_is_invalid(self):
        merchant = Vpos(token='1jYQryG3Qo4nzaOKgJxzWDs25Hv')
        refund = merchant.new_refund('1jYQryG3Qo4nzaOKgJxzWDs25Hv')

        assert refund.get('status_code') == 401

    def test_should_not_create_a_refund_if_supervisor_card_is_invalid(self):
        merchant = Vpos()
        response = merchant.new_refund(
            '1jYQryG3Qo4nzaOKgJxzWDs25Hv', supervisor_card='123123123123123')

        assert response.get('status_code') == 202

        refund_id = response.get('location')[17:]
        refund_transaction = merchant.get_transaction(refund_id)

        assert refund_transaction.get('data').get('status') == "rejected"
        assert refund_transaction.get('data').get('status_reason') == 1003

    # Transactions
    # # Positives
    def test_should_get_all_transactions(self):
        merchant = Vpos()
        response = merchant.get_transactions()

        assert response.get('status_code') == 200

    def test_should_get_a_single_transaction(self):
        merchant = Vpos()
        response = merchant.get_transaction('1jYQryG3Qo4nzaOKgJxzWDs25Ht')

        assert response.get('status_code') == 200

    # # Negatives
    def test_should_not_get_a_single_transaction_if_not_existent(self):
        merchant = Vpos()
        response = merchant.get_transaction('1jYQryG3Qo4nzaOKgJxzWDs25H')

        assert response.get('status_code') == 404

    def test_should_not_get_a_single_transaction_if_token_is_invalid(self):
        merchant = Vpos(token='1jYQryG3Qo4nzaOKgJxzWDs25Hv')
        transaction = merchant.get_transaction('1jYQryG3Qo4nzaOKgJxzWDs25Ht')

        assert transaction.get('status_code') == 401

    def test_should_not_get_all_transactions_if_token_is_invalid(self):
        merchant = Vpos(token='1jYQryG3Qo4nzaOKgJxzWDs25Hv')
        transactions = merchant.get_transactions()

        assert transactions.get('status_code') == 401

    # Requests
    # # Positives
    def test_should_get_a_running_single_request_status(self):
        merchant = Vpos()
        response = merchant.new_payment('925888553', '123.45')
        refund_id = response.get('location')[17:]
        response = merchant.get_request(refund_id)

        assert response.get('status_code') == 200

    # # Negatives
    def test_should_not_get_running_single_request_status_if_token_is_invalid(
            self):
        initial_merchant = Vpos()
        second_merchant = Vpos(token='1jYQryG3Qo4nzaOKgJxzWDs25Hv')
        response = initial_merchant.new_payment('925888553', '123.45')
        refund_id = response.get('location')[17:]
        response = second_merchant.get_request(refund_id)

        assert response.get('status_code') == 401
