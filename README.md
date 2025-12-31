🛡️ AI-Powered Transaction Fraud Detection System
📌 Project Overview

The AI-Powered Transaction Fraud Detection System is a real-time financial fraud monitoring platform designed to detect, analyze, and report suspicious transactions using Machine Learning, Graph Neural Networks (GNNs), and Explainable AI (SHAP).

The system continuously ingests transactions, evaluates fraud risk using multiple models, visualizes insights through an interactive dashboard, and generates Suspicious Activity Reports (SAR) in PDF format.

This project follows industry-grade architecture and demonstrates concepts from:

Cybersecurity

Machine Learning

Data Science

Web Application Development

Model Monitoring & Drift Detection

🎯 Key Objectives

Detect fraudulent financial transactions in real time

Combine multiple ML models for higher accuracy

Provide explainability for fraud predictions

Visualize risk trends and transaction networks

Generate regulatory-ready SAR reports

Support continuous model monitoring and improvement

🧠 System Architecture

Frontend

HTML5, CSS3, Bootstrap 5

Chart.js (Risk charts & trends)

Vis.js (Transaction network graph)

JavaScript (Real-time updates)

Backend

Flask (Python web framework)

REST APIs for data exchange

Background threads for live transaction simulation

Machine Learning

Isolation Forest (Anomaly Detection)

XGBoost (Supervised Fraud Classification)

Graph Neural Network (Relationship-based fraud detection)

SHAP (Explainable AI)

Other Components

Concept Drift Detection

AutoML-based retraining

SAR PDF generation using ReportLab

🧩 Core Features
🔹 Real-Time Transaction Monitoring

Live transaction feed

Automatic refresh every few seconds

Risk-based color coding

🔹 Fraud Detection Models

Isolation Forest – Detects anomalies

XGBoost – Predicts fraud probability

GNN – Detects suspicious account-merchant-device relationships

🔹 Composite Risk Scoring

A weighted risk score combining:

Isolation Forest score

XGBoost probability

GNN probability

Customer risk profile

🔹 Explainable AI (SHAP)

Displays top contributing risk features

Improves transparency and trust

Helps analysts understand why a transaction is flagged

🔹 Risk Visualization Dashboard

Risk distribution (Low / Medium / High)

Average risk trends

Top risk indicators

Interactive transaction table

🔹 Transaction Network Graph

Visualizes relationships between:

Accounts

Merchants

Devices

Helps identify fraud rings and suspicious behavior

🔹 Suspicious Activity Report (SAR)

One-click SAR generation

Automatically includes high-risk transactions

Downloadable PDF report

🔹 Concept Drift Detection

Monitors data distribution changes

Flags model drift risks

Supports long-term model reliability

📁 Project Directory Structure

AI-Powered-Transaction-Fraud-Detection-System/
│
├── app.py                         # Flask backend
├── templates/
│   └── dashboard.html             # Frontend dashboard
│
├── trained_models/
│   ├── isolation_forest.pkl
│   ├── xgboost.pkl
│   └── shap_explainer.pkl
│
├── graph_models/
│   ├── gnn_model.py
│   └── data_loader.py
│
├── models/
│   └── automl/
│       └── trainer.py
│
├── drift/
│   └── detector.py
│
├── profiling/
│   └── builder.py
│
├── reporting/
│   └── generator.py
│
├── data/
│   └── bank_transactions_data_2.csv
│
└── README.md
⚙️ Installation & Setup (Local Execution)

1️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Application
python app.py

4️⃣ Access the Dashboard

Open your browser and visit:

http://127.0.0.1:5000

🧪 How the System Works (Execution Flow)

Dummy or real transactions are generated

Data is sent to backend APIs

ML models compute fraud risk

SHAP explains model decisions

Dashboard updates in real time

High-risk transactions trigger SAR reports

📊 APIs Overview
Endpoint	Method	Description
/api/transactions	GET	Fetch recent transactions
/api/analyze	POST	Analyze a transaction
/api/reports/sar	POST	Generate SAR PDF
/api/drift/status	GET	Concept drift status
🔒 Security Considerations

Backend APIs are modular and extendable

Can be integrated with authentication systems

Ready for production-grade deployment

🚀 Future Enhancements

User authentication & role-based access

Database integration (PostgreSQL / MongoDB)

Real banking transaction feeds

Advanced fraud pattern learning

Cloud deployment (AWS / Azure)

SOC-style alerting system

🎓 Academic Relevance

This project demonstrates:

Applied Machine Learning

Cybersecurity analytics

Explainable AI

Full-stack development

Real-time monitoring systems

Suitable for:

Major Project

Final Year Project

Capstone Project

Research-oriented submissions

👤 Author

Saheel Yadav
B.Tech – Computer Science Engineering
Specialization: Cybersecurity & AI