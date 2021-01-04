# vPOS Python

![package](https://github.com/nextbss/vpos-python/workflows/package/badge.svg?branch=main)
[![](https://img.shields.io/badge/nextbss-opensource-blue.svg)](https://www.nextbss.co.ao)

This python package allows you to interact with the vPOS API

## Installation

```python
pip install vpos
```

## Configuration
| Variable | Description | Required |
| --- | --- | --- |
| `GPO_POS_ID` | The Point of Sale ID provided by EMIS | true |
| `GPO_SUPERVISOR_CARD` | The Supervisor card ID provided by EMIS | true |
| `MERCHANT_VPOS_TOKEN` | The API token provided by vPOS | true |
| `PAYMENT_CALLBACK_URL` | The URL that will handle payment notifications | false |
| `REFUND_CALLBACK_URL` | The URL that will handle refund notifications | false |
| `VPOS_ENVIRONMENT` | The vPOS environment, leave empty for `sandbox` mode and use `"prd"` for `production`.  | false |


Don't have this information? [Talk to us](suporte@vpos.ao)

## Use

### Get all transactions
This method retrieves all transactions

```python
import vpos
transactions = vpos.get_transactions()
```

### Get a specific Transaction
Retrieves a transaction given a valid transaction ID
```python
import vpos
transaction = vpos.get_transaction("1kTFGhJH8i58uD9MdJpMjWnoE")
```

### New Payment
```python
import vpos
transactions = vpos.new_payment("900111222", "123.45")
```
| Argument | Description | Type |
| --- | --- | --- |
| `mobile` | The mobile number of the client who will pay | `string`
| `amount` | The amount the client should pay, eg. "259.99", "259,000.00" | `string`


### Request Refund
```python
import vpos
transaction = vpos.new_refund("1jHbXEbRTIbbwaoJ6w06nLcRG7X")
```

### Poll Transaction Status
Poll the status of a transaction given a valid `request_id`. 

Note: The `request_id` in this context is essentially the `transaction_id` of an existing request. 

```python
import vpos
transaction = vpos.get_request("1jHbXEbRTIbbwaoJ6w06nLcRG7X")
```

| Argument | Description | Type |
| --- | --- | --- |
| `request_id` | The ID of transaction you wish to poll | `string`


### Have any doubts?
In case of any doubts, bugs, or the like, please leave an issue. We would love to help.

License
----------------

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).