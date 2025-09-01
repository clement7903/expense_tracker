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
