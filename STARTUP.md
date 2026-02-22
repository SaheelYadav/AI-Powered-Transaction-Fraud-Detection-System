# 🚀 Project Startup Guide

## 📋 Quick Start Summary

```bash
# 1. Navigate to project
cd C:\Users\Saheel\Desktop\projects\AI-Powered-Transaction-Fraud-Detection-System-master

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start MLflow (Terminal 1)
mlflow server --host 127.0.0.1 --port 5001

# 4. Start Flask app (Terminal 2)
python app.py

# 5. Open browser
http://127.0.0.1:5000
```

## 🔴 What Happens When You Close Everything?

If you:
- ❌ Close VS Code
- ❌ Close terminals  
- ❌ Restart laptop

👉 **Everything stops:**
- ✅ Flask stops
- ✅ MLflow stops
- ✅ Virtual environment deactivates

## ✅ CORRECT EXECUTION ORDER (VERY IMPORTANT)

### 🟢 STEP 1: Open Project Folder
```bash
cd C:\Users\Saheel\Desktop\projects\AI-Powered-Transaction-Fraud-Detection-System-master
```

### 🟢 STEP 2: Activate Virtual Environment
```bash
venv\Scripts\activate
```

**You should see:**
```
(venv) C:\Users\Saheel\Desktop\projects\AI-Powered-Transaction-Fraud-Detection-System-master>
```

⚠️ **If you don't see (venv) → STOP → it won't work**

### 🟢 STEP 3: Start MLflow Server (MANDATORY)

**Open Terminal 1 and run:**
```bash
mlflow server --host 127.0.0.1 --port 5001
```

**Leave this terminal OPEN.**

**You should see:**
```
[2024-02-22 21:23:45,678] INFO  [MainThread] Listening at http://127.0.0.1:5001
```

👉 **MLflow UI:** http://127.0.0.1:5001

### 🟢 STEP 4: Start Backend / Flask App

**Open Terminal 2 (new terminal, same folder, venv active):**
```bash
python app.py
```

**You should see:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

👉 **Backend + API:** http://127.0.0.1:5000

### 🟢 STEP 5: Open Dashboard

**Open browser:** http://127.0.0.1:5000

## 🔁 EVERY TIME SUMMARY (SHORT VERSION)

1. `cd project_folder`
2. `venv\Scripts\activate`
3. `mlflow server --host 127.0.0.1 --port 5001`
4. `python app.py`
5. `open browser`

## ❌ COMMON MISTAKES (AVOID THESE)

| Mistake | Result | Fix |
|---------|--------|-----|
| Forget MLflow | ConnectionRefusedError | Start MLflow first |
| Forget venv | Module not found | Activate virtual environment |
| Close MLflow terminal | App crashes | Keep MLflow terminal open |
| Run app first | MLflow error | Start MLflow before app |
| Use wrong port | Blank UI | Use correct ports (5000, 5001) |

## 🛠️ Troubleshooting

### Issue: "venv is not recognized"
**Solution:**
```bash
# Check if venv exists
dir venv

# If not, create it
python -m venv venv
```

### Issue: "mlflow command not found"
**Solution:**
```bash
# Install mlflow
pip install mlflow
```

### Issue: "Port already in use"
**Solution:**
```bash
# Kill processes on ports
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# Kill the process (replace PID)
taskkill /PID <PID_NUMBER> /F
```

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# Install requirements
pip install -r requirements.txt
```

## 🐳 Docker Alternative (If Available)

If Docker Desktop is running:

```bash
# Build and run with Docker
docker-compose up --build -d

# Access at:
# http://localhost:5001 (main app)
# http://localhost:5000 (mlflow)
```

## 📱 Quick Access URLs

- **Main Application:** http://127.0.0.1:5000
- **MLflow Dashboard:** http://127.0.0.1:5001
- **API Documentation:** http://127.0.0.1:5000/api

## 🎯 Success Indicators

✅ **MLflow Running:** See "Listening at http://127.0.0.1:5001"  
✅ **Flask Running:** See "Running on http://127.0.0.1:5000"  
✅ **Browser Loads:** Dashboard appears without errors  
✅ **Transactions Show:** Live transaction feed working  

---

**🚀 Follow these steps exactly for successful startup every time!**
