from flask import Blueprint, request, jsonify
from controllers.settle_controller import settle_balance
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
