# Deployment & Integration Guide 🚀

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, Ubuntu 18.04+, macOS 10.14+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for models and dependencies
- **Internet**: For initial dependency installation

### Recommended Setup
- **OS**: Windows Server 2019+, Ubuntu 20.04+
- **Python**: 3.10+
- **RAM**: 16GB
- **CPU**: Multi-core processor
- **Storage**: SSD with 5GB+ space

---

## Local Installation (Development)

### Option 1: Quick Start (Windows)
```bash
cd c:\Users\Jayan\OneDrive\Desktop\quality_checker
run.bat
```

### Option 2: Manual Setup (All Platforms)
```bash
# 1. Navigate to directory
cd c:\Users\Jayan\OneDrive\Desktop\quality_checker

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train models (first time only)
python quality_predictor.py

# 6. Run application
streamlit run app.py
```

---

## Cloud Deployment

### Option 1: Streamlit Cloud (Free & Easiest)

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with GitHub account
   - Click "New app"
   - Select repository and `app.py` as main file
   - Click "Deploy"

3. **Access Application**
   - Your app will be live at: `https://[username]-quality-checker.streamlit.app`

### Option 2: Google Colab (Free)

1. **Upload to Google Drive**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. **Install Dependencies**
   ```python
   !pip install -r requirements.txt
   ```

3. **Run Application**
   ```python
   !streamlit run app.py &
   ```

### Option 3: AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 AMI
   - Instance type: t2.medium or larger
   - Security group: Allow port 8501

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

4. **Access**
   - http://[EC2-Public-IP]:8501

### Option 4: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t quality-checker .
docker run -p 8501:8501 quality-checker
```

---

## Production Deployment Checklist

### Before Going Live
- [ ] Test all features locally
- [ ] Run `test_system.py` and verify all tests pass
- [ ] Review quality predictions with domain experts
- [ ] Validate against historical manufacturing data
- [ ] Set up error logging and monitoring
- [ ] Configure backup procedures
- [ ] Create user documentation
- [ ] Plan for model retraining with real data

### Security Measures
- [ ] Use HTTPS/SSL certificates
- [ ] Implement authentication (if needed)
- [ ] Restrict access to sensitive data
- [ ] Regular security updates
- [ ] Firewall configuration
- [ ] Data encryption at rest and in transit

### Performance Optimization
- [ ] Enable model caching
- [ ] Use production-grade WSGI server (Gunicorn)
- [ ] Configure load balancing
- [ ] Implement CDN for static files
- [ ] Monitor system performance
- [ ] Set up auto-scaling

---

## Integration with Manufacturing Systems

### Option 1: REST API

Create `api.py`:
```python
from fastapi import FastAPI
from quality_predictor import MoldingQualityPredictor

app = FastAPI()
predictor = MoldingQualityPredictor()

@app.post("/predict")
def predict(process_params: dict, geometry_params: dict):
    predictions = predictor.predict(process_params, geometry_params)
    return predictions
```

Run:
```bash
pip install fastapi uvicorn
uvicorn api:app --reload
```

### Option 2: Database Integration

```python
import sqlite3

def save_analysis(analysis_data):
    conn = sqlite3.connect('quality_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analyses 
        (timestamp, melt_temp, mold_temp, warpage, sinkage, quality_score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        analysis_data['timestamp'],
        analysis_data['process_params']['melt_temp'],
        analysis_data['process_params']['mold_temp'],
        analysis_data['predictions']['warpage_percent'],
        analysis_data['predictions']['sinkage_percent'],
        analysis_data['quality_score']
    ))
    conn.commit()
    conn.close()
```

### Option 3: Live Data Feed

```python
import time
from data_source import get_latest_parameters

def continuous_monitoring():
    predictor = MoldingQualityPredictor()
    
    while True:
        # Get live data from manufacturing equipment
        params = get_latest_parameters()
        
        # Make prediction
        predictions = predictor.predict(
            params['process'],
            params['geometry']
        )
        
        # Save results
        save_to_database(predictions)
        
        # Alert if quality drops
        if predictions['quality_score'] < 95:
            send_alert(predictions)
        
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    continuous_monitoring()
```

---

## Model Retraining

### With Real Manufacturing Data

```python
from quality_predictor import MoldingQualityPredictor
import pandas as pd

# Load real data
df = pd.read_csv('manufacturing_measurements.csv')

# Create predictor
predictor = MoldingQualityPredictor()

# Prepare data
X = df[[
    'melt_temp', 'mold_temp', 'injection_pressure',
    'holding_pressure', 'holding_time', 'cooling_time',
    'wall_thickness', 'part_volume', 'aspect_ratio'
]].values

y_warpage = df['measured_warpage'].values
y_sinkage = df['measured_sinkage'].values

# Scale and train
X_scaled = predictor.scaler.fit_transform(X)
predictor.warpage_model.fit(X_scaled, y_warpage)
predictor.sinkage_model.fit(X_scaled, y_sinkage)

# Save updated models
predictor.save_models()
print("✅ Models retrained with real data!")
```

### Automated Retraining

```python
# Schedule retraining weekly
from apscheduler.schedulers.background import BackgroundScheduler

def retrain_models():
    predictor = MoldingQualityPredictor()
    df = pd.read_csv('manufacturing_measurements.csv')
    # ... retraining code ...
    print("Models retrained successfully")

scheduler = BackgroundScheduler()
scheduler.add_job(func=retrain_models, trigger="cron", day_of_week="mon", hour=2)
scheduler.start()
```

---

## Monitoring & Maintenance

### Logging Setup

```python
import logging

logging.basicConfig(
    filename='quality_checker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def make_prediction(process_params, geometry_params):
    try:
        predictions = predictor.predict(process_params, geometry_params)
        logger.info(f"Prediction successful: {predictions}")
        return predictions
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise
```

### Health Check Endpoint

```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": predictor.warpage_model is not None,
        "timestamp": datetime.now()
    }
```

### Performance Metrics

```python
import time

def track_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"{func.__name__} took {elapsed_time:.3f} seconds")
        return result
    return wrapper

@track_performance
def predict(process_params, geometry_params):
    return predictor.predict(process_params, geometry_params)
```

---

## Troubleshooting Deployment Issues

### Issue: "Module not found" error
**Solution**:
```bash
pip install -r requirements.txt --upgrade
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: Port 8501 already in use
**Solution**:
```bash
streamlit run app.py --server.port 8502
# Or kill process on port 8501:
# Windows: netstat -ano | findstr :8501
# Linux: lsof -ti:8501 | xargs kill -9
```

### Issue: High memory usage
**Solution**:
- Reduce batch size in predictions
- Clear cache regularly
- Use garbage collection: `import gc; gc.collect()`

### Issue: Model file corruption
**Solution**:
```python
# Delete corrupted models
import os
os.remove('models/warpage_model.pkl')
os.remove('models/sinkage_model.pkl')

# Retrain
predictor.train_models()
```

---

## Scaling Considerations

### For 100+ Users
- Use load balancer (nginx)
- Redis for session caching
- Database instead of file storage
- CDN for static assets

### For 1000+ Users
- Kubernetes orchestration
- Microservices architecture
- Distributed model inference
- Advanced caching strategy

### For Real-time Operations
- WebSocket connections
- Message queues (Kafka, RabbitMQ)
- Stream processing (Spark, Flink)
- Real-time database (InfluxDB)

---

## Support & Documentation

- 📖 Full documentation: [README.md](README.md)
- ⚡ Quick start guide: [QUICKSTART.md](QUICKSTART.md)
- 🔧 Configuration: [config.json](config.json)
- 🧪 Test system: `python test_system.py`

---

## Version Updates

### Updating Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Checking for Updates
```bash
pip list --outdated
```

### Updating Specific Package
```bash
pip install streamlit --upgrade
```

---

**Ready to deploy? Follow the Quick Start or choose your deployment option above!** 🚀

For production deployment, consult with your DevOps team and follow your organization's deployment procedures.
