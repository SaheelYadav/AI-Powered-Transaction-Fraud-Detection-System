from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global transaction storage
TRANSACTIONS = []

def generate_dummy_transaction():
    """Generate a realistic dummy transaction"""
    return {
        "TransactionID": f"TX{random.randint(100000, 999999)}",
        "AccountID": f"AC{random.randint(10000, 99999)}",
        "TransactionAmount": round(random.uniform(10, 5000), 2),
        "TransactionDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TransactionType": random.choice(["Debit", "Credit"]),
        "Location": random.choice(["New York, NY", "Chicago, IL", "Miami, FL", "Los Angeles, CA"]),
        "RiskScore": round(random.uniform(0, 1), 2),
        "Status": random.choice(["Approved", "Flagged", "Pending Review"])
    }

def generate_fraud_score(transaction_data):
    """Generate a simple fraud score based on transaction features"""
    amount = float(transaction_data.get('TransactionAmount', 0))
    
    # Simple risk factors
    risk_score = 0.1  # Base risk
    
    # High amount increases risk
    if amount > 1000:
        risk_score += 0.3
    elif amount > 500:
        risk_score += 0.2
    
    # Random factor for realism
    risk_score += random.uniform(0, 0.3)
    
    # Cap between 0 and 1
    return min(max(risk_score, 0), 1)

# Pre-populate with some transactions
for _ in range(10):
    TRANSACTIONS.append(generate_dummy_transaction())

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/transactions')
def get_recent_transactions():
    """Get recent transactions"""
    days = request.args.get('days', default=1, type=int)
    cutoff = datetime.now() - timedelta(days=days)
    
    filtered = [
        t for t in TRANSACTIONS
        if datetime.strptime(t['TransactionDate'], "%Y-%m-%d %H:%M:%S") >= cutoff
    ]
    
    return jsonify(filtered)

@app.route('/api/analyze', methods=['POST'])
def analyze_transaction():
    """Analyze a transaction for fraud"""
    try:
        data = request.json
        
        # Generate fraud score
        fraud_score = generate_fraud_score(data)
        
        # Generate explanation
        explanation = [
            {
                "feature": "TransactionAmount",
                "value": float(data.get('TransactionAmount', 0)),
                "impact": "High" if float(data.get('TransactionAmount', 0)) > 1000 else "Low"
            },
            {
                "feature": "TransactionType",
                "value": data.get('TransactionType', 'Unknown'),
                "impact": "Medium"
            },
            {
                "feature": "Location",
                "value": data.get('Location', 'Unknown'),
                "impact": "Low"
            }
        ]
        
        # Determine risk level
        if fraud_score > 0.7:
            risk_level = "High"
        elif fraud_score > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return jsonify({
            "fraud_score": round(fraud_score, 3),
            "risk_level": risk_level,
            "explanation": explanation,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error analyzing transaction: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/stats')
def get_stats():
    """Get transaction statistics"""
    if not TRANSACTIONS:
        return jsonify({
            "total_transactions": 0,
            "high_risk": 0,
            "medium_risk": 0,
            "low_risk": 0,
            "avg_amount": 0
        })
    
    total = len(TRANSACTIONS)
    high_risk = len([t for t in TRANSACTIONS if t['RiskScore'] > 0.7])
    medium_risk = len([t for t in TRANSACTIONS if 0.4 < t['RiskScore'] <= 0.7])
    low_risk = total - high_risk - medium_risk
    avg_amount = np.mean([t['TransactionAmount'] for t in TRANSACTIONS])
    
    return jsonify({
        "total_transactions": total,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "avg_amount": round(avg_amount, 2)
    })

# Background thread to generate transactions
import threading
import time

def transaction_generator():
    """Background thread to generate transactions"""
    while True:
        try:
            txn = generate_dummy_transaction()
            TRANSACTIONS.insert(0, txn)
            
            # Keep only last 50 transactions
            if len(TRANSACTIONS) > 50:
                TRANSACTIONS.pop()
                
            time.sleep(random.randint(30, 120))  # 30 seconds to 2 minutes
            
        except Exception as e:
            logger.error(f"Error generating transaction: {str(e)}")
            time.sleep(60)

# Start background thread
threading.Thread(target=transaction_generator, daemon=True).start()

if __name__ == '__main__':
    # Create required directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting AI Fraud Detection System on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
