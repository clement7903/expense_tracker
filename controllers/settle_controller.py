from data.data_store import users
from controllers.transactions_controller import calculate_balances

def settle_balance(payer, payee, amount):
    """Handle settlement between two users."""
    if payer not in users or payee not in users:
        return "Invalid users"

    if users[payer]["balance"] < amount:
        return "Insufficient balance"

    # Update balances
    users[payer]["balance"] -= amount
    users[payee]["balance"] += amount

    # Record transactions for both users
    users[payer]["transactions"].append({
        "type": "settle",
        "description": f"Paid {payee}",
        "amount": -amount,
    })
    users[payee]["transactions"].append({
        "type": "settle",
        "description": f"Received from {payer}",
        "amount": amount,
    })

    return None

def get_user_balance(username):
    """Return the balance of a particular user."""
    if username not in users:
        return "Invalid user"
    return users[username]["balance"]

def get_amount_owed(payer, payee):
    """Return how much payer owes to payee."""
    if payer not in users or payee not in users:
        return "Invalid users"
    amount_owed = 0.0
    for t in users[payer]["transactions"]:
        if t.get("type") == "settle" and t.get("description") == f"Paid {payee}":
            amount_owed += abs(t.get("amount", 0))
        if t.get("type") == "payment" and t.get("counterparty") == payee:
            amount_owed += abs(t.get("amount", 0))
    for t in users[payee]["transactions"]:
        if t.get("type") == "share" and t.get("counterparty") == payer:
            amount_owed -= abs(t.get("amount", 0))
    return amount_owed
