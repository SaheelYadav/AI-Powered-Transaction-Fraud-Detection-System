from flask import Flask, render_template, request, jsonify
import numpy as np
import random
from datetime import datetime

app = Flask(__name__)

# Demo transaction generator
def generate_demo_transaction():
    return {
        "TransactionID": f"TX{random.randint(100000, 999999)}",
        "AccountID": f"AC{random.randint(100000, 999999)}",
        "TransactionAmount": round(random.uniform(10, 5000), 2),
        "TransactionDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TransactionType": random.choice(["Debit", "Credit"]),
        "Location": random.choice(["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX"]),
        "DeviceID": f"DEV{random.randint(100, 999)}",
        "MerchantID": f"MER{random.randint(1000, 9999)}"
    }

# Demo ML predictions
def predict_fraud_risk(transaction):
    amount = transaction["TransactionAmount"]
    base_risk = min(amount / 1000, 0.9)  # Higher amount = higher risk
    
    # Add some randomness
    risk = base_risk + random.uniform(-0.2, 0.2)
    risk = max(0, min(1, risk))
    
    return {
        "isolation_forest_score": risk * random.uniform(0.8, 1.2),
        "xgboost_probability": risk * random.uniform(0.9, 1.1),
        "gnn_probability": risk * random.uniform(0.7, 1.3),
        "composite_score": risk,
        "customer_risk_score": random.uniform(0.1, 0.9),
        "explanation": [
            {
                "feature": "TransactionAmount",
                "value": amount,
                "shap_value": risk * 0.3
            },
            {
                "feature": "TransactionType",
                "value": transaction["TransactionType"],
                "shap_value": risk * 0.1
            }
        ],
        "drift_detected": random.choice([True, False])
    }

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/transactions')
def get_transactions():
    # Generate demo transactions
    transactions = [generate_demo_transaction() for _ in range(20)]
    return jsonify(transactions)

@app.route('/api/analyze', methods=['POST'])
def analyze_transaction():
    data = request.get_json()
    
    # Validate input
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Generate demo prediction
    prediction = predict_fraud_risk(data)
    
    return jsonify(prediction)

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7860)
