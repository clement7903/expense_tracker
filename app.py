from flask import Flask
from routes.user_routes import user_bp
from routes.transaction_routes import transaction_bp
from routes.settle_routes import settle_bp


app = Flask(__name__)

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(settle_bp)

if __name__ == "__main__":
    app.run(debug=True)
