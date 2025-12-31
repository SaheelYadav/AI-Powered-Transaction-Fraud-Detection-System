from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import joblib
import numpy as np
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import torch
import mlflow
import threading
import time
from graph_models.gnn_model import load_gnn_model
from graph_models.data_loader import TransactionGraphBuilder
from reporting.generator import ReportGenerator
from profiling.builder import CustomerRiskProfiler
from drift.detector import ConceptDriftDetector
from models.automl.trainer import AutoMLTrainer
import os
import logging
import random

TRANSACTIONS = []
import random

def generate_dummy_transaction():
    return {
        "TransactionID": f"TX{random.randint(100000, 999999)}",
        "AccountID": f"AC{random.randint(10000, 99999)}",
        "TransactionAmount": round(random.uniform(10, 5000), 2),
        "TransactionDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TransactionType": random.choice(["Debit", "Credit"]),
        "Location": random.choice([
            "New York, NY", "Chicago, IL", "Miami, FL"
        ]),
        "RiskScore": round(random.uniform(0, 1), 2),
        "Status": random.choice(["Approved", "Flagged", "Pending Review"])
    }
def transaction_generator_loop():
    while True:
        txn = generate_dummy_transaction()
        TRANSACTIONS.insert(0, txn)

        # keep only latest 20 transactions
        if len(TRANSACTIONS) > 20:
            TRANSACTIONS.pop()

        time.sleep(random.randint(120, 300))  # 2–5 minutes

threading.Thread(
    target=transaction_generator_loop,
    daemon=True
).start()
# Preload initial transactions for better UX
for _ in range(5):
    TRANSACTIONS.append(generate_dummy_transaction())


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)

# Initialize components
iso_forest = joblib.load('trained_models/isolation_forest.pkl')
xgb = joblib.load('trained_models/xgboost.pkl')
# Load SHAP explainer if available (optional)
try:
    shap_explainer = joblib.load('trained_models/shap_explainer.pkl')
except FileNotFoundError:
    shap_explainer = None
    print("SHAP explainer not found. Continuing without explainability.")
gnn_model = load_gnn_model('models/gnn_model.pt')
graph_builder = TransactionGraphBuilder()
report_generator = ReportGenerator()
profiler = CustomerRiskProfiler()
drift_detector = ConceptDriftDetector()

# Feature names
features = ['TransactionAmount', 'TransactionDuration', 'LoginAttempts', 
            'AccountBalance', 'DaysSinceLastTransaction', 'TransactionSpeed',
            'AvgAmount', 'StdAmount', 'MaxAmount', 'AvgDuration', 'UniqueLocations',
            'AmountDeviation', 'DurationDeviation', 'TransactionType', 
            'Location', 'DeviceID', 'MerchantID', 'Channel', 'CustomerOccupation']

# Background tasks
def auto_retrain():
    while True:
        try:
            trainer = AutoMLTrainer("data/bank_transactions_data_2.csv")
            best_model, score = trainer.train_models()
            app.logger.info(f"AutoML retraining completed. Best model: {type(best_model).__name__} with score: {score:.4f}")
        except Exception as e:
            app.logger.error(f"AutoML retraining failed: {str(e)}")
        time.sleep(7 * 24 * 60 * 60)  # Run weekly

# Start background thread
retrain_thread = threading.Thread(target=auto_retrain, daemon=True)
retrain_thread.start()


# Initialize AutoML Trainer with proper error handling
try:
    automl_trainer = AutoMLTrainer("data/bank_transactions_data_2.csv")
    
    # Check if models exist, if not train initial models
    required_models = ['isolation_forest.pkl', 'xgboost.pkl', 'shap_explainer.pkl']
    if not all(os.path.exists(f"trained_models/{model}") for model in required_models):
        logger.info("Initial models not found, training initial models...")
        automl_trainer.train_models()
except Exception as e:
    logger.error(f"Failed to initialize AutoML trainer: {str(e)}")
    raise

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_transaction():
    data = request.json
    
    # Update customer profile
    profiler.update_profile(data['AccountID'], {
        'amount': float(data['TransactionAmount']),
        'type': data['TransactionType'],
        'date': data['TransactionDate']
    })
    
    # Get customer stats
    cust_profile = profiler.get_risk_profile(data['AccountID'])
    cust_stats = {
        'AvgAmount': cust_profile.get('avg_amount', 150.0),
        'StdAmount': cust_profile.get('std_amount', 75.0),
        'MaxAmount': cust_profile.get('max_amount', 1000.0),
        'AvgDuration': cust_profile.get('avg_duration', 120.0),
        'UniqueLocations': cust_profile.get('unique_locations', 3)
    }
    
    # Create feature vector
    transaction_date = datetime.strptime(data['TransactionDate'], '%Y-%m-%d %H:%M:%S')
    prev_date = datetime.strptime(data['PreviousTransactionDate'], '%Y-%m-%d %H:%M:%S')
    
    features_dict = {
        'TransactionAmount': float(data['TransactionAmount']),
        'TransactionDuration': float(data['TransactionDuration']),
        'LoginAttempts': int(data['LoginAttempts']),
        'AccountBalance': float(data['AccountBalance']),
        'DaysSinceLastTransaction': (datetime.now() - prev_date).days,
        'TransactionSpeed': float(data['TransactionAmount']) / float(data['TransactionDuration']),
        'AvgAmount': cust_stats['AvgAmount'],
        'StdAmount': cust_stats['StdAmount'],
        'MaxAmount': cust_stats['MaxAmount'],
        'AvgDuration': cust_stats['AvgDuration'],
        'UniqueLocations': cust_stats['UniqueLocations'],
        'AmountDeviation': (float(data['TransactionAmount']) - cust_stats['AvgAmount']) / cust_stats['StdAmount'],
        'DurationDeviation': (float(data['TransactionDuration']) - cust_stats['AvgDuration']) / cust_stats['AvgDuration'],
        'TransactionType': 0 if data['TransactionType'] == 'Debit' else 1,
        'Location': hash(data['Location']) % 100,
        'DeviceID': hash(data['DeviceID']) % 100,
        'MerchantID': hash(data['MerchantID']) % 100,
        'Channel': {'ATM': 0, 'Online': 1, 'Branch': 2}.get(data['Channel'], 0),
        'CustomerOccupation': {'Student': 0, 'Doctor': 1, 'Engineer': 2, 'Retired': 3}.get(data['CustomerOccupation'], 0)
    }
    
    # Convert to DataFrame for prediction
    X = pd.DataFrame([features_dict], columns=features)
    
    # Check for concept drift
    drift_detector.add_data(X.values[0])
    
    # Get predictions
    iso_score = -iso_forest.decision_function(X)[0]
    xgb_prob = xgb.predict_proba(X)[0, 1]
    
    # GNN prediction
    graph_data = graph_builder.add_transaction(data)
    with torch.no_grad():
        gnn_prob = gnn_model(graph_data.x, graph_data.edge_index).item()
    
    explanation = []
    
    # --- SHAP explanations ---
    explanation = []
    
    if shap_explainer is not None:
        shap_values = shap_explainer.shap_values(X)
        for i, feature in enumerate(features):
            explanation.append({
                'feature': feature,
                'value': X.iloc[0, i],
                'shap_value': shap_values[0][i]
            })
    
    # Sort explanation (works even if empty)
    explanation.sort(key=lambda x: abs(x['shap_value']), reverse=True)
    
    # Composite score weighted by customer risk profile
    cust_risk = cust_profile['risk_score'] if cust_profile else 0.5
    composite_score = (
        iso_score * 0.4 +
        xgb_prob * 0.4 +
        gnn_prob * 0.2
    ) * (0.5 + cust_risk)
    
    return jsonify({
        'isolation_forest_score': float(iso_score),
        'xgboost_probability': float(xgb_prob),
        'gnn_probability': float(gnn_prob),
        'composite_score': float(composite_score),
        'customer_risk_score': float(cust_risk),
        'explanation': explanation[:5],
        'drift_detected': drift_detector.drift_count > 0
    })


from datetime import timedelta

@app.route('/api/transactions')
def get_recent_transactions():
    days = request.args.get('days', default=1, type=int)
    cutoff = datetime.now() - timedelta(days=days)

    filtered = [
        t for t in TRANSACTIONS
        if datetime.strptime(
            t['TransactionDate'], "%Y-%m-%d %H:%M:%S"
        ) >= cutoff
    ]

    return jsonify(filtered)



@app.route('/api/reports/sar', methods=['POST'])
def generate_sar():
    payload = request.json
    transactions = payload.get("transactions", TRANSACTIONS)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 800, "Suspicious Activity Report (SAR)")
    pdf.drawString(50, 780, f"Generated: {datetime.now()}")

    y = 750
    for tx in transactions:
        pdf.drawString(
            50, y,
            f"{tx['TransactionID']} | {tx['AccountID']} | "
            f"Amount: {tx['TransactionAmount']} | Risk: {tx['RiskScore']}"
        )
        y -= 18
        if y < 50:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="SAR_Report.pdf",
        mimetype="application/pdf"
    )

@app.route('/api/customer/<customer_id>/profile')
def get_customer_profile(customer_id):
    profile = profiler.get_risk_profile(customer_id)
    if profile:
        return jsonify(profile)
    return jsonify({"error": "Customer not found"}), 404

@app.route('/api/models/retrain', methods=['POST'])
def trigger_retraining():
    try:
        trainer = AutoMLTrainer("data/bank_transactions_data_2.csv")
        best_model, score = trainer.train_models()
        return jsonify({
            "status": "success",
            "best_model": type(best_model).__name__,
            "score": score
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/drift/status')
def get_drift_status():
    return jsonify({
        "drift_detected": drift_detector.drift_count > 0,
        "drift_count": drift_detector.drift_count
    })

if __name__ == '__main__':
    # Create required directories
    import os
    os.makedirs("reports", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Initialize MLflow
    mlflow.set_tracking_uri("http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0')