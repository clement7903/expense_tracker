from flask import Blueprint, jsonify
from controllers.user_controller import get_users

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["GET"])
def fetch_users():
    """API: Get both users and their transactions"""
    return jsonify(get_users())
