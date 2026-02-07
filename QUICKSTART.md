# Quick Start Guide 🚀

## Installation (5 Minutes)

### Step 1: Install Python Dependencies
```bash
cd c:\Users\Jayan\OneDrive\Desktop\quality_checker
pip install -r requirements.txt
```

### Step 2: Run the Application
**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
streamlit run app.py
```

The application will automatically open at: `http://localhost:8501`

---

## Using the Quality Checker

### Step 1: Enter Process Parameters
1. Go to **"📊 Quality Analysis"** tab
2. Adjust the sliders for:
   - Melt Temperature
   - Mold Temperature
   - Injection Pressure
   - Holding Pressure
   - Holding Time
   - Cooling Time

### Step 2: Enter Part Geometry
3. Adjust the sliders for:
   - Wall Thickness
   - Part Volume
   - Aspect Ratio

### Step 3: Analyze Quality
4. Click **"🔍 Analyze Quality"** button
5. View the predictions and visualizations

### Step 4: Get Optimization Suggestions
1. Go to **"🎯 Optimization Assistant"** tab
2. View AI-powered recommendations
3. See impact of suggested changes

### Step 5: Export Reports
1. Go to **"📈 History & Reports"** tab
2. Click **"📥 Export Report as CSV"** to download data

---

## Example: Optimized Parameters

Based on the research paper, here are optimal parameters for junction boxes:

**Input Values:**
- Melt Temperature: 230°C
- Mold Temperature: 51°C
- Injection Pressure: 49 MPa
- Holding Pressure: 69 MPa
- Holding Time: 15.5 seconds
- Cooling Time: 35 seconds
- Wall Thickness: 2.5 mm
- Part Volume: 80 cm³
- Aspect Ratio: 1.5

**Expected Output:**
- Warpage: ~6.9% ✅
- Sinkage: ~0.99% ✅
- Quality Score: ~95%+ ✅

---

## Interpretation Guide

### Quality Score Meanings

| Score | Rating | Status | Action |
|-------|--------|--------|--------|
| 95-100 | ⭐⭐⭐⭐⭐ | EXCELLENT | Product ready to ship |
| 85-95 | ⭐⭐⭐⭐ | GOOD | Minor adjustments available |
| 75-85 | ⭐⭐⭐ | ACCEPTABLE | Monitor and optimize |
| 60-75 | ⭐⭐ | NEEDS IMPROVEMENT | Apply optimization suggestions |
| <60 | ⭐ | POOR | Major changes required |

### Warpage Reduction Tips
- ✅ Lower melt temperature (each 10°C decrease helps)
- ✅ Increase cooling time by 5-10 seconds
- ✅ Ensure uniform mold temperature distribution
- ✅ Reduce part wall thickness if possible
- ✅ Check cooling system efficiency

### Sinkage Reduction Tips
- ✅ Increase holding pressure by 10-15 MPa
- ✅ Extend holding time by 2-5 seconds
- ✅ Increase mold temperature for uniform cooling
- ✅ Review and optimize wall thickness
- ✅ Ensure proper gate location

---

## Advanced Tips

### 1. Iterative Optimization
- Make small changes (5-10% adjustments)
- Reanalyze after each change
- Track improvements in History tab
- Note which changes have most impact

### 2. Understanding Defects
**Warpage** = Product bends or twists (thermal stress)
**Sinkage** = Dimples or depressions (insufficient packing)

### 3. Material Considerations
Different materials need different parameters:
- **PP (Polypropylene)**: Lower temps, quick cooling
- **ABS**: Moderate temps, careful cooling
- **PC (Polycarbonate)**: Higher temps, slow cooling
- **PET**: Medium temps, controlled cooling

### 4. Design Guidelines
- Uniform wall thickness (±10%)
- Avoid sharp corners (use 1-2mm radii)
- Proper gate design and location
- Adequate cooling channels
- Proper ejector pin placement

---

## Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Problem: "Port 8501 already in use"
**Solution:** Use different port
```bash
streamlit run app.py --server.port 8502
```

### Problem: Models take too long to train
**Solution:** Reduce training samples in `quality_predictor.py`:
```python
self.generate_training_data(samples=300)  # Changed from 500
```

### Problem: Application is slow
**Solution:** 
- Close other applications
- Clear browser cache
- Restart Streamlit

---

## Integration with Actual Data

To integrate with real manufacturing data:

1. **Modify training data** in `quality_predictor.py`:
```python
def generate_training_data(self):
    # Replace synthetic data with real measurements
    # Load from CSV or database
    df = pd.read_csv('manufacturing_data.csv')
    X = df[['melt_temp', 'mold_temp', ...]]
    y_warpage = df['measured_warpage']
    return X, y_warpage, y_sinkage
```

2. **Connect to database**:
```python
import sqlite3
conn = sqlite3.connect('quality_data.db')
# Query historical data
```

3. **Real-time updates**:
```python
# Refresh predictions with latest measurements
def update_predictions_realtime():
    # Connect to manufacturing equipment
    # Get live sensor data
    # Make real-time predictions
```

---

## Key Features Summary

✅ **Input**: Process parameters + Part geometry
✅ **Processing**: Neural network AI prediction
✅ **Output**: Warpage %, Sinkage %, Quality Score
✅ **Suggestions**: Rule-based optimization recommendations
✅ **Quality Gate**: Ensure >95% quality standard
✅ **Reporting**: Export and track history
✅ **Dashboard**: Interactive visualizations

---

## Next Steps

1. ✅ Install and run the application
2. ✅ Test with example parameters
3. ✅ Understand quality metrics
4. ✅ Apply optimization suggestions
5. ✅ Track improvements over time
6. ✅ Integrate with real manufacturing data

---

## Support Resources

- 📖 Read full [README.md](README.md)
- 🔧 Check [config.json](config.json) for parameters
- 📊 View [Research Paper](https://doi.org/10.3390/ma18030577)
- 💻 Review source code comments

---

**Ready to improve your injection molding quality? Start the application now!** 🏭✨
