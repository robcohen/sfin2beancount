#!/usr/bin/env python3
"""Convert SimpleFIN JSON to Beancount format.

Reads SimpleFIN account data from stdin and writes Beancount transactions to stdout.
"""

import sys
import json
import argparse
from decimal import Decimal
from datetime import datetime


def sanitize_account_name(name):
    """Convert account name to valid Beancount account component."""
    # Replace spaces and special chars with hyphens
    clean = name.replace(' ', '-').replace('/', '-').replace('&', '-')
    # Remove consecutive hyphens
    while '--' in clean:
        clean = clean.replace('--', '-')
    # Strip leading/trailing hyphens
    return clean.strip('-')


def simplefin_to_beancount(data, default_expense='Expenses:Uncategorized',
                           default_income='Income:Uncategorized',
                           account_prefix='Assets'):
    """Convert SimpleFIN data to Beancount format.

    Args:
        data: Parsed SimpleFIN JSON data
        default_expense: Account for outflows
        default_income: Account for inflows
        account_prefix: Prefix for asset accounts

    Returns:
        Beancount-formatted string
    """
    all_trans = []

    for account in data.get('accounts', []):
        for transaction in account.get('transactions', []):
            transaction['_account'] = account
            all_trans.append(transaction)

    # Sort by posted date
    all_trans = sorted(all_trans, key=lambda x: x.get('posted', 0))

    lines = []
    for trans in all_trans:
        posted = trans.get('posted')
        if not posted:
            continue

        # Handle both timestamp and datetime formats
        if isinstance(posted, (int, float)):
            date_str = datetime.fromtimestamp(posted).strftime('%Y-%m-%d')
        else:
            date_str = str(posted)[:10]

        description = trans.get('description', 'Unknown')
        # Escape quotes in description
        description = description.replace('"', '\\"')

        amount = Decimal(str(trans.get('amount', 0)))
        account_name = trans['_account'].get('name', 'Unknown')
        currency = trans['_account'].get('currency', 'USD')

        asset_account = f"{account_prefix}:{sanitize_account_name(account_name)}"

        # Build transaction
        lines.append(f'{date_str} * "{description}"')

        if amount >= 0:
            # Income/deposit
            lines.append(f'  {asset_account}  {amount} {currency}')
            lines.append(f'  {default_income}')
        else:
            # Expense/withdrawal
            lines.append(f'  {asset_account}  {amount} {currency}')
            lines.append(f'  {default_expense}')

        lines.append('')

    return '\n'.join(lines)


def main(args=None):
    parser = argparse.ArgumentParser(
        description='Convert SimpleFIN JSON to Beancount format'
    )
    parser.add_argument(
        '--expense-account',
        default='Expenses:Uncategorized',
        help='Default expense account (default: Expenses:Uncategorized)'
    )
    parser.add_argument(
        '--income-account',
        default='Income:Uncategorized',
        help='Default income account (default: Income:Uncategorized)'
    )
    parser.add_argument(
        '--account-prefix',
        default='Assets',
        help='Prefix for asset accounts (default: Assets)'
    )

    args = parser.parse_args(args)

    try:
        stdin = sys.stdin.read()
        data = json.loads(stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f'Error parsing JSON: {e}\n')
        sys.exit(1)

    output = simplefin_to_beancount(
        data,
        default_expense=args.expense_account,
        default_income=args.income_account,
        account_prefix=args.account_prefix
    )
    sys.stdout.write(output)


if __name__ == '__main__':
    main()
