from data.data_store import users
from controllers.transactions_controller import calculate_balances
from datetime import datetime as Datetime

def settle_balance(settler, counterparty, amount):
    """Handle settlement between two users."""
    if settler not in users or counterparty not in users:
        return "Invalid users"

    if users[settler]["balance"] < amount:
        return "Insufficient balance"

    """Prevent oversettlement"""
    if get_amount_owed(settler, counterparty) < amount:
        return "Settlement amount exceeds debt owed"

    # Update balances
    users[settler]["balance"] -= amount  # Settler pays back
    users[counterparty]["balance"] += amount  # Counterparty receives money

    # Record transactions for both users
    users[settler]["transactions"].append({
        "type": "settlement",
        "counterparty": counterparty,
        "description": f"Pays {amount} to {counterparty}",
        "amount": -amount,
        "date": Datetime.now().isoformat()
    })
    users[counterparty]["transactions"].append({
        "type": "settlement",
        "counterparty": settler,
        "description": f"Received {amount} from {settler}",
        "amount": amount,
        "date": Datetime.now().isoformat()
    })

    return None

def get_user_balance(username):
    """Return the balance of a particular user."""
    if username not in users:
        return "Invalid user"
    return users[username]["balance"]

def get_amount_owed(target, counterparty):
    """Return how much target owes to counterparty."""
    if target not in users or counterparty not in users:
        return "Invalid users"
    amount_owed_by_target_to_counterparty = 0.0
    amount_settled_with_counterparty = 0.0
    for t in users[target]["transactions"]:
        if t.get("type") == "interparty" and t.get("counterparty") == counterparty and t.get("amount") < 0:
            amount_owed_by_target_to_counterparty += abs(t.get("amount"))
        if t.get("type") == "settlement" and t.get("counterparty") == counterparty:
            amount_settled_with_counterparty += abs(t.get("amount"))

    # Amount owed to target - settled by counterparty
    amount_owed = amount_owed_by_target_to_counterparty - amount_settled_with_counterparty

    return max(amount_owed, 0.0)
