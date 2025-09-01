from flask import Blueprint, request, jsonify
from controllers.transactions_controller import record_transaction, get_all_transactions, calculate_balances

transaction_bp = Blueprint("transactions", __name__)

@transaction_bp.route("/transactions", methods=["GET"])
def fetch_transactions():
    """API: Get all transactions"""
    return jsonify({"transactions": get_all_transactions()})


@transaction_bp.route("/transactions", methods=["POST"])
def create_transaction():
    """API: Record a new group transaction"""
    data = request.get_json()
    payer = data.get("payer")
    payee = data.get("payee")
    total_amount = data.get("total_amount")
    description = data.get("description", "Shared expense")

    if not payer or not payee or not total_amount:
        return jsonify({"error": "Missing required fields"}), 400

    transaction, error = record_transaction(payer, payee, total_amount, description)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Transaction recorded successfully",
        "transaction": transaction,
        "current_balances": calculate_balances(),
    })
