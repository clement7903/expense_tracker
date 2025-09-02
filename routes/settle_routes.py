from flask import Blueprint, request, jsonify
from controllers.settle_controller import settle_balance, get_user_balance, get_amount_owed
from controllers.transactions_controller import calculate_balances

settle_bp = Blueprint("settle", __name__)

@settle_bp.route("/settle", methods=["POST"])
def settle_payment():
    """API: Settle outstanding balance"""
    data = request.get_json()
    settler = data.get("settler")
    counterparty = data.get("counterparty")
    amount = data.get("amount")

    if not settler or not counterparty or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    error = settle_balance(settler, counterparty, amount)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": f"{settler} paid ${amount} to {counterparty}",
    })

@settle_bp.route("/balance/<username>", methods=["GET"])
def balance_enquiry(username):
    """API: Get balance for a particular user"""
    balance = get_user_balance(username)
    if balance == "Invalid user":
        return jsonify({"error": "Invalid user"}), 404
    return jsonify({"username": username, "balance": balance})

@settle_bp.route("/owed/<target>/<counterparty>", methods=["GET"])
def amount_owed_enquiry(target, counterparty):
    """API: Get amount target owes to counterparty"""
    amount = get_amount_owed(target, counterparty)
    if amount == "Invalid users":
        return jsonify({"error": "Invalid users"}), 404
    return jsonify({"target": target, "counterparty": counterparty, "amount_owed": amount})
