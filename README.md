# vPOS Python

[![package](https://github.com/v-pos/vpos-python/actions/workflows/python-package.yml/badge.svg)](https://github.com/v-pos/vpos-python/actions/workflows/python-package.yml)
[![](https://img.shields.io/badge/nextbss-opensource-blue.svg)](https://www.nextbss.co.ao)

This python library helps you easily interact with the vPOS API,
Allowing merchants apps/services to request a payment from a client through his/her mobile phone number.

The service currently works for solutions listed below:

EMIS GPO (Multicaixa Express)

Want to know more about how we are empowering merchants in Angola? See our [website](https://vpos.ao)

### Features
- Simple interface
- Uniform plain old objects are returned by all official libraries, so you don't have
to serialize/deserialize the JSON returned by our API.

### Documentation
Does interacting directly with our API service sound better to you? 
See our documentation on [developer.vpos.ao](https://developer.vpos.ao)

## Installation

```python
pip install vpos
```

## Configuration
This python library requires you set up the following environment variables on your machine before interacting with
the API using this library:

| Variable | Description | Required |
| --- | --- | --- |
| `GPO_POS_ID` | The Point of Sale ID provided by EMIS | true |
| `GPO_SUPERVISOR_CARD` | The Supervisor card ID provided by EMIS | true |
| `MERCHANT_VPOS_TOKEN` | The API token provided by vPOS | true |
| `PAYMENT_CALLBACK_URL` | The URL that will handle payment notifications | false |
| `REFUND_CALLBACK_URL` | The URL that will handle refund notifications | false |
| `VPOS_ENVIRONMENT` | The vPOS environment, leave empty for `sandbox` mode and use `'PRD'` for `production`.  | false |

or using one of the optional arguments

| Variable | Description | Required |
| --- | --- | --- |
| `pos_id` | The Point of Sale ID provided by EMIS | false |
| `supervisor_card` | The Supervisor card ID provided by EMIS | false |
| `token` | The API token provided by vPOS | false |
| `payment_callback_url` | The URL that will handle payment notifications | false |
| `refund_callback_url` | The URL that will handle refund notifications | false |
| `environment` | The vPOS environment, leave empty for `sandbox` mode and use `'PRD'` for `production`.  | false |

Don't have this information? [Talk to us](suporte@vpos.ao)

## Use

### create instance
Creates a new instance of Vpos
```python
import vpos
merchant = Vpos()
# or use optional arguments
merchant = Vpos(token='your_token_here', environment='PRD')
```

### Get all transactions
This method retrieves all transactions
```python
transactions = merchant.get_transactions()
```

### Get a specific Transaction
Retrieves a transaction given a valid transaction ID
```python
transaction = merchant.get_transaction('1kTFGhJH8i58uD9MdJpMjWnoE')
```

### New Payment
```python
transactions = merchant.new_payment('900111222', '123.45')
```
| Argument | Description | Type |
| --- | --- | --- |
| `mobile` | The mobile number of the client who will pay | `string`
| `amount` | The amount the client should pay, eg. "259.99", "259000.00" | `string`


### Request Refund
```python
transaction = merchant.new_refund('1jHbXEbRTIbbwaoJ6w06nLcRG7X')
```

### Poll Transaction Status
Poll the status of a transaction given a valid `request_id`. 

Note: The `request_id` in this context is essentially the `transaction_id` of an existing request. 

```python
transaction = merchant.get_request('1jHbXEbRTIbbwaoJ6w06nLcRG7X')
```

| Argument | Description | Type |
| --- | --- | --- |
| `request_id` | The ID of transaction you wish to poll | `string`


### Have any doubts?
In case of any doubts, bugs, or the like, please leave an issue. We would love to help.

License
----------------

The library is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
