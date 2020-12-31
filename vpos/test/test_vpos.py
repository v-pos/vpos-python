import pytest
from vpos.vpos import Vpos

class TestVpos:
    def test_should_create_a_new_payment_request_transaction(self):
        merchant = Vpos()
        payment = merchant.new_payment("992563019", "123.45")
        assert payment.get('status') == 202

    def test_should_not_create_a_new_payment_request_transaction_if_customer_format_is_invalid(self):
        merchant = Vpos()        
        payment = merchant.new_payment("99256301", "123.45")
        assert payment.get('status') == 400

    def test_should_not_create_a_new_payment_request_transaction_if_amount_format_is_invalid(self):
        merchant = Vpos()
        payment = merchant.new_payment("992563019", "123.45.01")
        assert payment.get('status') == 400


    def test_should_create_a_new_refund_request_transaction(self):
        merchant = Vpos()
        response = merchant.new_refund("1jYQryG3Qo4nzaOKgJxzWDs25Hv")
        assert response.get('status') == 202
          
    def test_should_not_create_a_new_refund_request_transaction_if_parent_transaction_id_is_not_present(self):
        merchant = Vpos()
        response = merchant.new_refund(None)
        assert response.get('status') == 400
      
    def test_should_not_create_a_new_refund_request_transaction_if_supervisor_card_is_invalid(self):
        merchant = Vpos()
        response = merchant.new_refund("1jYQryG3Qo4nzaOKgJxzWDs25Hv", supervisor_card = "123123123123123")
        assert response.get('status') == 202

        refund_id = response.get('location')[17:]
        refund_transaction = merchant.get_transaction(refund_id)
        assert refund_transaction.get('data').get('status') == "rejected"
        assert refund_transaction.get('data').get('status_reason') == 1003
    
    def test_should_get_all_transactions(self):
        merchant = Vpos()
        response = merchant.get_transactions()
        assert response.get('status') == 200
      
    def test_should_get_a_single_transaction(self):
        merchant = Vpos()
        response = merchant.get_transaction("1jYQryG3Qo4nzaOKgJxzWDs25Ht")
        assert response.get('status') == 200
          
    def test_should_not_get_a_non_existent_single_transaction(self):
        merchant = Vpos()
        response = merchant.get_transaction("1jYQryG3Qo4nzaOKgJxzWDs25H")
        assert response.get('status') == 404
    
    def test_should_get_a_running_single_request_status(self):
        merchant = Vpos()
        response = merchant.new_payment("925888553", "123.45")

        refund_id = response.get('location')[17:]

        response = merchant.get_request(refund_id)
        assert response.get('status') == 200
    
    # TODO test_should_get_a_completed_single_request_status
    