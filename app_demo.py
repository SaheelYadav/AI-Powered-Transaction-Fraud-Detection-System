from flask import Flask, render_template, request, jsonify
import numpy as np
import random
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Global transactions list (like your main app)
TRANSACTIONS = []

# Demo transaction generator (same as your main app)
def generate_demo_transaction():
    risk = round(random.uniform(0.05, 0.95), 2)
    return {
        "TransactionID": f"TX{random.randint(100000, 999999)}",
        "AccountID": f"AC{random.randint(10000, 99999)}",
        "TransactionAmount": round(random.uniform(10, 5000), 2),
        "TransactionDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TransactionType": random.choice(["Debit", "Credit"]),
        "Location": random.choice(["New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX"]),
        "DeviceID": f"DEV{random.randint(100, 999)}",
        "MerchantID": f"MER{random.randint(1000, 9999)}",
        "RiskScore": risk,
        "Status": "Flagged" if risk > 0.7 else "Approved"
    }

# Background transaction generator (like your main app)
def transaction_generator_loop():
    while True:
        txn = generate_demo_transaction()
        TRANSACTIONS.insert(0, txn)
        
        # keep only latest 20 transactions
        if len(TRANSACTIONS) > 20:
            TRANSACTIONS.pop()
        
        time.sleep(random.randint(120, 300))  # 2–5 minutes

# Start background thread (like your main app)
threading.Thread(
    target=transaction_generator_loop,
    daemon=True
).start()

# Preload initial transactions for better UX (like your main app)
for _ in range(20):
    TRANSACTIONS.append(generate_demo_transaction())

print(f"Started with {len(TRANSACTIONS)} initial transactions")

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
    # Return current transactions from global list (like your main app)
    return render_template('dashboard.html')

@app.route('/api/transactions')
def get_transactions():
    # Get days parameter from query string
    days = request.args.get('days', default=7, type=int)
    
    # Return transactions from global list (like your main app)
    # Filter by days if needed
    if days > 0:
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        filtered_transactions = [txn for txn in TRANSACTIONS 
                            if datetime.strptime(txn["TransactionDate"], "%Y-%m-%d %H:%M:%S").timestamp() > cutoff_time]
    else:
        filtered_transactions = TRANSACTIONS
    
    return jsonify(filtered_transactions)

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
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "transactions_count": len(TRANSACTIONS),
        "background_thread_running": True
    })

@app.route('/api/debug')
def debug_info():
    return jsonify({
        "transactions": TRANSACTIONS,
        "count": len(TRANSACTIONS),
        "message": f"Debug info - {len(TRANSACTIONS)} transactions available"
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=7860)
