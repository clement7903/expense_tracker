from data.data_store import users, transactions
from uuid import uuid4

def calculate_balances():
    """Calculate how much each user owes or is owed."""
    total_paid = {"A": 0, "B": 0}
    for t in transactions:
        total_paid[t["payer"]] += t["total_amount"]

    total_spent = sum(total_paid.values())
    fair_share = total_spent / 2

    return {
        "A": total_paid["A"] - fair_share,
        "B": total_paid["B"] - fair_share,
    }


def record_transaction(payer, payee, total_amount, description):
    """Record a shared transaction between payer and payee, split equally."""
    if payer not in users:
        return None, "Invalid payer"
    if payee not in users:
        return None, "Invalid payee"
    if payer == payee:
        return None, "Payer and payee must be different"

    if users[payer]["balance"] < total_amount:
        return None, "Insufficient balance"

    split_amount = total_amount / 2

    # Deduct amount from payer
    users[payer]["balance"] -= total_amount
    # Credit split amount to payee
    users[payee]["balance"] += split_amount

    # Create transaction record
    transaction = {
        "id": str(uuid4()),
        "payer": payer,
        "payee": payee,
        "total_amount": total_amount,
        "description": description,
        "split_amount": split_amount,
    }
    transactions.append(transaction)

    # Record payer's transaction
    users[payer]["transactions"].append({
        "type": "payment",
        "description": description,
        "amount": -total_amount,
        "counterparty": payee,
    })

    # Record payee's share
    users[payee]["transactions"].append({
        "type": "share",
        "description": description,
        "amount": split_amount,
        "counterparty": payer,
    })

    return transaction, None


def get_all_transactions():
    """Return all recorded transactions."""
    return transactions
