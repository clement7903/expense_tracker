from flask import Blueprint, request, jsonify
from controllers.settle_controller import settle_balance, get_user_balance, get_amount_owed
from controllers.transactions_controller import calculate_balances

settle_bp = Blueprint("settle", __name__)

@settle_bp.route("/settle", methods=["POST"])
def settle_payment():
    """API: Settle outstanding balance"""
    data = request.get_json()
    payer = data.get("payer")
    payee = data.get("payee")
    amount = data.get("amount")

    if not payer or not payee or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    error = settle_balance(payer, payee, amount)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": f"{payer} paid {amount} to {payee}",
        "current_balances": calculate_balances(),
    })

@settle_bp.route("/balance/<username>", methods=["GET"])
def balance_enquiry(username):
    """API: Get balance for a particular user"""
    balance = get_user_balance(username)
    if balance == "Invalid user":
        return jsonify({"error": "Invalid user"}), 404
    return jsonify({"username": username, "balance": balance})

@settle_bp.route("/owed/<payer>/<payee>", methods=["GET"])
def amount_owed_enquiry(payer, payee):
    """API: Get amount payer owes to payee"""
    amount = get_amount_owed(payer, payee)
    if amount == "Invalid users":
        return jsonify({"error": "Invalid users"}), 404
    return jsonify({"payer": payer, "payee": payee, "amount_owed": amount})
