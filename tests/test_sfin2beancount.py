import json

from sfin2beancount import simplefin_to_beancount


def test_basic():
    sample = json.dumps({
        "accounts": [{
            "name": "Savings",
            "currency": "USD",
            "transactions": [{
                "posted": 793065600,
                "description": "Gas Station",
                "amount": "-14.55"
            }]
        }]
    })
    out = simplefin_to_beancount(json.loads(sample))
    assert '1995-02-17' in out or '1995-02-18' in out  # timezone variance
    assert 'Gas Station' in out
    assert 'Assets:Savings' in out
    assert '-14.55 USD' in out
    assert 'Expenses:Uncategorized' in out


def test_credit():
    sample = json.dumps({
        "accounts": [{
            "name": "Savings",
            "currency": "USD",
            "transactions": [{
                "posted": 793065600,
                "description": "Deposit",
                "amount": "500.00"
            }]
        }]
    })
    out = simplefin_to_beancount(json.loads(sample))
    assert 'Deposit' in out
    assert 'Assets:Savings' in out
    assert '500.00 USD' in out
    assert 'Income:Uncategorized' in out
