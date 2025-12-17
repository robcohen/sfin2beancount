# SimpleFIN 2 Beancount

SimpleFIN is a data format/protocol for getting read-only access to your bank account information.

`sfin2beancount` is a command line utility for converting [SimpleFIN account data](https://www.simplefin.org/protocol.html) into a format suitable for [Beancount](https://beancount.github.io/).

## Installation

```bash
pip install git+https://github.com/simplefin/sfin2beancount.git
```

## Example

Find your bank's SimpleFIN server.  If they don't have one, you can use the [SimpleFIN Bridge](https://bridge.simplefin.org/simple/).  The example below uses a demo account from the SimpleFIN Bridge.

Claim an access url (you do this once you have a Setup Token):

```bash
SETUP_TOKEN="aHR0cHM6Ly9icmlkZ2Uuc2ltcGxlZmluLm9yZy9zaW1wbGVmaW4vY2xhaW0vZGVtbw=="
CLAIM_URL=$(echo ${SETUP_TOKEN} | base64 --decode)
ACCESS_URL=$(curl -X POST $CLAIM_URL)
echo "$ACCESS_URL" > /tmp/access_url
```

Get some data in beancount format (do this daily or whatever):

```bash
curl "$(cat /tmp/access_url)/accounts" | sfin2beancount
```

which produces something like:

```beancount
2016-06-20 * "Gas Station"
  Assets:SimpleFIN-Demo-1-Savings  -44.37 USD
  Expenses:Uncategorized

2016-06-20 * "Gas Station"
  Assets:SimpleFIN-Demo-1-Checking  -4.82 USD
  Expenses:Uncategorized

2016-06-20 * "Good Person Reward"
  Assets:SimpleFIN-Demo-1-Savings  -19.72 USD
  Expenses:Uncategorized

2016-06-20 * "Good Person Reward"
  Assets:SimpleFIN-Demo-1-Checking  41.01 USD
  Income:Uncategorized
```
