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


def record_transaction(payer, total_amount, description):
    """Record a shared transaction and split equally."""
    if payer not in users:
        return None, "Invalid payer"

    if users[payer]["balance"] < total_amount:
        return None, "Insufficient balance"

    # Deduct amount from payer
    users[payer]["balance"] -= total_amount

    # Create transaction record
    transaction = {
        "id": str(uuid4()),
        "payer": payer,
        "total_amount": total_amount,
        "description": description,
        "split_amount": total_amount / 2,
    }
    transactions.append(transaction)

    # Record payer's transaction
    users[payer]["transactions"].append({
        "type": "payment",
        "description": description,
        "amount": -total_amount,
    })

    # Record share for the other user
    for uid in users:
        if uid != payer:
            users[uid]["transactions"].append({
                "type": "share",
                "description": description,
                "amount": total_amount / 2,
            })

    return transaction, None


def get_all_transactions():
    """Return all recorded transactions."""
    return transactions
