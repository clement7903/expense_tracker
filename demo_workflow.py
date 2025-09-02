import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def pretty_print(title, response):
    print(f"\n=== {title} ===")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

# 1. Get both users' transactions and balances
pretty_print("Get Users", requests.get(f"{BASE_URL}/users"))

# 2. Record a bill payment (between users)
bill_payload = {
    "bill_payer": "A",
    "counterparty": "B",
    "total_amount": 100,
    "description": "Dinner with B at Marche"
}
pretty_print("Record Bill Payment (User)", requests.post(f"{BASE_URL}/transactions", json=bill_payload))

# 3. List all past transactions (for all users)
pretty_print("List Transactions", requests.get(f"{BASE_URL}/transactions"))

# 4. Check how much one user owes another before settling
pretty_print("Amount Owed by B to A BEFORE Settle", requests.get(f"{BASE_URL}/owed/B/A"))

# 5. Settle outstanding balance
settle_payload = {
    "counterparty": "A",
    "settler": "B",
    "amount": 50
}
pretty_print("Settle Balance", requests.post(f"{BASE_URL}/settle", json=settle_payload))

# 6. Enquire individual user balance
pretty_print("Balance Enquiry (A)", requests.get(f"{BASE_URL}/balance/A"))
pretty_print("Balance Enquiry (B)", requests.get(f"{BASE_URL}/balance/B"))

# 7. Tries to settle, despite having no outstanding balance
settle_payload = {
    "counterparty": "A",
    "settler": "B",
    "amount": 50
}
pretty_print("Settle Balance", requests.post(f"{BASE_URL}/settle", json=settle_payload))
