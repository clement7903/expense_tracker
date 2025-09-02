from data.data_store import users, transactions
from uuid import uuid4

def calculate_balances():
    """Calculate how much each user owes or is owed."""
    total_paid = {"A": 0, "B": 0}
    for t in transactions:
        total_paid[t["bill_payer"]] += t["total_amount"]

    total_spent = sum(total_paid.values())
    fair_share = total_spent / 2

    return {
        "A": total_paid["A"] - fair_share,
        "B": total_paid["B"] - fair_share,
    }


def record_transaction(bill_payer, counterparty, total_amount, description):
    """Record a shared transaction between bill_payer and counterparty, split equally."""
    if bill_payer not in users:
        return None, "Invalid bill_payer"
    if counterparty not in users:
        return None, "Invalid counterparty"
    if bill_payer == counterparty:
        return None, "Bill payer and counterparty must be different"

    if users[bill_payer]["balance"] < total_amount:
        return None, "Insufficient balance"

    split_amount = total_amount / 2

    # Deduct bill amount paid from bill_payer
    users[bill_payer]["balance"] -= total_amount

    # Create transaction record
    transaction = {
        "id": str(uuid4()),
        "bill_payer": bill_payer,
        "counterparty": counterparty,
        "total_amount": total_amount,
        "description": description,
        "split_amount": split_amount,
    }
    transactions.append(transaction)

    # Record bill_payer's credit amount
    users[bill_payer]["transactions"].append({
        "type": "interparty",
        "description": description,
        "amount": split_amount,
        "counterparty": counterparty,
    })
    
    # Record counterparty's owed amount
    users[counterparty]["transactions"].append({
        "type": "interparty",
        "description": description,
        "amount": -split_amount,
        "counterparty": bill_payer,
    })

    return transaction, None


def get_all_transactions():
    """Return all recorded transactions."""
    return transactions
