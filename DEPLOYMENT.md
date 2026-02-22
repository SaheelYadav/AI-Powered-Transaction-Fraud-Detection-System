# 🚀 Deployment Guide

This guide will help you deploy your AI-Powered Transaction Fraud Detection System to various platforms.

## 📋 Table of Contents

- [🆓 Free Cloud Deployment](#-free-cloud-deployment)
- [☁️ Paid Cloud Deployment](#️-paid-cloud-deployment)
- [🖥️ Self-Hosted VPS](#️-self-hosted-vps)
- [🔧 Local Production Setup](#-local-production-setup)

## 🆓 Free Cloud Deployment

### Option 1: Railway (Recommended)

**Pros:**
- Free tier available
- Easy GitHub integration
- Automatic SSL
- Support for Docker

**Steps:**
1. **Sign up for Railway**
   ```bash
   # Go to https://railway.app
   # Sign up with GitHub
   ```

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Docker setup

3. **Configure Environment Variables**
   ```
   FLASK_ENV=production
   MLFLOW_TRACKING_URI=http://localhost:5000
   ```

4. **Access your app**
   - Railway will provide a public URL
   - Example: `https://your-app-name.up.railway.app`

### Option 2: Render

**Pros:**
- Free tier for web services
- PostgreSQL free tier
- Automatic deployments

**Steps:**
1. **Sign up**: https://render.com
2. **Connect GitHub repository**
3. **Create Web Service**
   - Choose your repo
   - Set build command: `docker build -t fraud-detection .`
   - Set start command: `docker run -p 5000:5000 fraud-detection`

### Option 3: Vercel

**Pros:**
- Excellent for frontend
- Free tier available
- Great performance

**Steps:**
1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

## ☁️ Paid Cloud Deployment

### Option 1: AWS

#### AWS ECS (Elastic Container Service)

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name fraud-detection
   ```

2. **Build and Push Docker Image**
   ```bash
   # Get login token
   aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com
   
   # Build image
   docker build -t fraud-detection .
   
   # Tag and push
   docker tag fraud-detection:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/fraud-detection:latest
   docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/fraud-detection:latest
   ```

3. **Create ECS Task Definition**
   ```json
   {
     "family": "fraud-detection",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "fraud-detection",
         "image": "<account-id>.dkr.ecr.us-west-2.amazonaws.com/fraud-detection:latest",
         "portMappings": [
           {
             "containerPort": 5000,
             "protocol": "tcp"
           }
         ]
       }
     ]
   }
   ```

#### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - t2.micro (free tier) or t3.small
   - Configure security groups (ports 80, 443, 22)

2. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy Application**
   ```bash
   git clone https://github.com/SaheelYadav/AI-Powered-Transaction-Fraud-Detection-System.git
   cd AI-Powered-Transaction-Fraud-Detection-System
   docker-compose up -d
   ```

### Option 2: Google Cloud Platform

#### Google Cloud Run

1. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Build and Deploy**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/fraud-detection
   gcloud run deploy --image gcr.io/PROJECT-ID/fraud-detection --platform managed
   ```

### Option 3: Microsoft Azure

#### Azure Container Instances

1. **Create Resource Group**
   ```bash
   az group create --name fraud-detection-rg --location eastus
   ```

2. **Deploy Container**
   ```bash
   az container create \
     --resource-group fraud-detection-rg \
     --name fraud-detection \
     --image your-registry/fraud-detection:latest \
     --dns-name-label fraud-detection-unique \
     --ports 5000
   ```

## 🖥️ Self-Hosted VPS

### DigitalOcean Droplet

1. **Create Droplet**
   - Ubuntu 20.04 LTS
   - 2GB RAM, 1 CPU (minimum)
   - Add SSH keys

2. **Setup Server**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Deploy Application**
   ```bash
   git clone https://github.com/SaheelYadav/AI-Powered-Transaction-Fraud-Detection-System.git
   cd AI-Powered-Transaction-Fraud-Detection-System
   docker-compose up -d
   ```

4. **Setup SSL with Let's Encrypt**
   ```bash
   # Install certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Get SSL certificate
   sudo certbot --nginx -d your-domain.com
   ```

## 🔧 Local Production Setup

### Using Docker Compose

1. **Build and Run**
   ```bash
   docker-compose up --build -d
   ```

2. **Access Application**
   - Main App: http://localhost:5001
   - MLflow: http://localhost:5000
   - Nginx (if configured): http://localhost

### Using PM2 (Node.js Process Manager)

1. **Install PM2**
   ```bash
   npm install -g pm2
   ```

2. **Create PM2 Config**
   ```javascript
   // ecosystem.config.js
   module.exports = {
     apps: [{
       name: 'fraud-detection',
       script: 'app.py',
       interpreter: 'python',
       instances: 'max',
       exec_mode: 'cluster',
       env: {
         NODE_ENV: 'production',
         FLASK_ENV: 'production'
       }
     }]
   };
   ```

3. **Start Application**
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

## 🔒 Security Considerations

### Environment Variables
```bash
# Create .env file
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MLFLOW_TRACKING_URI=http://localhost:5000
DATABASE_URL=your-database-url
```

### Firewall Setup
```bash
# Ubuntu UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### SSL Certificate
```bash
# Using Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

## 📊 Monitoring and Logging

### Health Checks
- Application health: `/health`
- Database connectivity
- Model performance metrics

### Logging
```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/fraud-detection.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

## 🚀 Quick Deployment Commands

### Railway (Easiest)
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Deploy on Railway
# Visit railway.app and connect your repo
```

### DigitalOcean (Quick VPS)
```bash
# 1. Create Droplet and SSH into it
ssh root@your-droplet-ip

# 2. One-line deployment
curl -fsSL https://get.docker.com -o get-docker.sh && \
sudo sh get-docker.sh && \
git clone https://github.com/SaheelYadav/AI-Powered-Transaction-Fraud-Detection-System.git && \
cd AI-Powered-Transaction-Fraud-Detection-System && \
docker-compose up -d
```

## 📞 Support

For deployment issues:
- 📧 Email: saheelyadav67@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/SaheelYadav/AI-Powered-Transaction-Fraud-Detection-System/issues)

---

🎉 **Choose the deployment option that best fits your needs and budget!**
