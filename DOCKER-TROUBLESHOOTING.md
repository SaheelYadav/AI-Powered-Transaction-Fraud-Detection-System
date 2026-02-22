# 🐳 Docker Troubleshooting Guide

## 🔴 Common Docker Issues on Windows

### Issue: "error during connect: Head 'http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping'"

**This means Docker Desktop is NOT running.**

## ✅ SOLUTIONS

### Solution 1: Start Docker Desktop (Recommended)

1. **Press Windows Key** + **R**
2. Type: `Docker Desktop`
3. **Press Enter**
4. **Wait for Docker to start** (Docker whale icon in system tray)
5. **Try Docker commands again**

### Solution 2: Check Docker Status

```powershell
# Check if Docker is running
docker version
docker info
```

### Solution 3: Restart Docker Desktop

1. **Right-click Docker icon** in system tray
2. **Click "Restart"**
3. **Wait for restart to complete**

### Solution 4: Reinstall Docker Desktop

If nothing works:
1. **Uninstall Docker Desktop**
2. **Download latest version** from https://www.docker.com/products/docker-desktop
3. **Reinstall and restart**

## 🚀 Docker Alternative Commands (When Docker is Working)

### Quick Test
```bash
# Test Docker is working
docker run hello-world

# Build your application
docker build -t fraud-detection .

# Run your application
docker run -p 5000:5000 fraud-detection
```

### Using Docker Compose
```bash
# Start all services
docker-compose up --build -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔄 Alternative: Run Without Docker

If Docker keeps failing, use the manual method:

### Option 1: Batch File (Easy)
```bash
# Double-click this file:
start-project.bat
```

### Option 2: PowerShell (Advanced)
```powershell
# Run in PowerShell:
.\start-project.ps1
```

### Option 3: Manual Steps
```bash
# 1. Navigate to project
cd C:\Users\Saheel\Desktop\projects\AI-Powered-Transaction-Fraud-Detection-System-master

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start MLflow (Terminal 1)
mlflow server --host 127.0.0.1 --port 5001

# 4. Start Flask (Terminal 2)
python app.py

# 5. Open browser
http://127.0.0.1:5000
```

## 📋 Docker vs Manual Comparison

| Feature | Docker | Manual |
|---------|---------|--------|
| **Setup Time** | 5 minutes | 2 minutes |
| **Port Conflicts** | Possible | Possible |
| **Dependencies** | Automatic | Manual |
| **Troubleshooting** | Complex | Simple |
| **Windows Support** | Needs Docker Desktop | Works natively |
| **Development** | Good | Better |

## 🎯 Recommendation for Windows Users

**Use Manual Method** because:
- ✅ No Docker Desktop dependency
- ✅ Faster startup
- ✅ Easier debugging
- ✅ Better Windows integration

## 📞 If Docker Still Doesn't Work

1. **Use the batch file**: `start-project.bat`
2. **Or follow manual steps** in STARTUP.md
3. **Contact support**: saheelyadav67@gmail.com

---

**🚀 Choose the method that works best for your system!**
