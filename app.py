import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from quality_predictor import MoldingQualityPredictor
from optimization_engine import OptimizationEngine
import json
from datetime import datetime
import os

st.set_page_config(
    page_title="Injection Molding Quality Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'predictor' not in st.session_state:
    st.session_state.predictor = MoldingQualityPredictor()
    # Load or train models
    if not st.session_state.predictor.load_models():
        with st.spinner("Training AI models... This happens only once"):
            st.session_state.predictor.train_models()

if 'optimizer' not in st.session_state:
    st.session_state.optimizer = OptimizationEngine()

if 'history' not in st.session_state:
    st.session_state.history = []

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .quality-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
    }
    .quality-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
    }
    .suggestion-box {
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style="text-align: center; color: #2c3e50;">
    🏭 Injection Molding Quality Checker
    </h1>
    <p style="text-align: center; color: #7f8c8d; font-size: 18px;">
    AI-Powered Quality Prediction & Optimization System
    </p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Select Page", [
    "📊 Quality Analysis",
    "🎯 Optimization Assistant",
    "📈 History & Reports",
    "ℹ️ About"
])

# ============================================================================
# PAGE: Quality Analysis
# ============================================================================
if page == "📊 Quality Analysis":
    st.markdown("## Input Process Parameters & Geometry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Process Parameters")
        melt_temp = st.slider(
            "Melt Temperature (°C)",
            min_value=180.0, max_value=280.0, value=230.0, step=1.0
        )
        mold_temp = st.slider(
            "Mold Temperature (°C)",
            min_value=20.0, max_value=100.0, value=50.0, step=1.0
        )
        injection_pressure = st.slider(
            "Injection Pressure (MPa)",
            min_value=20.0, max_value=150.0, value=75.0, step=1.0
        )
        holding_pressure = st.slider(
            "Holding Pressure (MPa)",
            min_value=10.0, max_value=100.0, value=65.0, step=1.0
        )
    
    with col2:
        st.subheader("📐 Part Geometry")
        holding_time = st.slider(
            "Holding Time (seconds)",
            min_value=2.0, max_value=60.0, value=15.0, step=0.5
        )
        cooling_time = st.slider(
            "Cooling Time (seconds)",
            min_value=5.0, max_value=120.0, value=35.0, step=1.0
        )
        wall_thickness = st.slider(
            "Wall Thickness (mm)",
            min_value=0.5, max_value=5.0, value=2.5, step=0.1
        )
        part_volume = st.slider(
            "Part Volume (cm³)",
            min_value=10.0, max_value=300.0, value=80.0, step=5.0
        )
        aspect_ratio = st.slider(
            "Aspect Ratio (Length/Width)",
            min_value=0.5, max_value=4.0, value=1.5, step=0.1
        )
    
    # Predict button
    if st.button("🔍 Analyze Quality", use_container_width=True, key="analyze"):
        process_params = {
            'melt_temp': melt_temp,
            'mold_temp': mold_temp,
            'injection_pressure': injection_pressure,
            'holding_pressure': holding_pressure,
            'holding_time': holding_time,
            'cooling_time': cooling_time
        }
        
        geometry_params = {
            'wall_thickness': wall_thickness,
            'part_volume': part_volume,
            'aspect_ratio': aspect_ratio
        }
        
        # Get predictions
        predictions = st.session_state.predictor.predict(process_params, geometry_params)
        
        # Calculate quality score
        quality_data = st.session_state.optimizer.calculate_quality_score(
            predictions['warpage_percent'],
            predictions['sinkage_percent']
        )
        
        # Store in history
        st.session_state.history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'process_params': process_params,
            'geometry_params': geometry_params,
            'predictions': predictions,
            'quality_score': quality_data['overall_quality']
        })
        
        # Display results
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Warpage %",
                f"{predictions['warpage_percent']:.2f}%",
                delta=f"Target: < 5%",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Sinkage %",
                f"{predictions['sinkage_percent']:.2f}%",
                delta=f"Target: < 2%",
                delta_color="inverse"
            )
        
        with col3:
            quality_score = quality_data['overall_quality']
            rating, color = st.session_state.optimizer.get_quality_rating(quality_score)
            
            if quality_data['meets_target']:
                st.markdown(
                    f'<div class="quality-good">Quality Score: {quality_score:.1f}%<br>{rating}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="quality-warning">Quality Score: {quality_score:.1f}%<br>{rating}</div>',
                    unsafe_allow_html=True
                )
        
        # Visualizations
        st.markdown("### 📈 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Quality Score Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=quality_score,
                title={'text': "Overall Quality Score"},
                delta={'reference': 95},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ff6b6b"},
                        {'range': [60, 75], 'color': "#ffa726"},
                        {'range': [75, 85], 'color': "#ffeb3b"},
                        {'range': [85, 95], 'color': "#81c784"},
                        {'range': [95, 100], 'color': "#66bb6a"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 95
                    }
                }
            ))
            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Defect Distribution
            defect_data = {
                'Defect Type': ['Warpage', 'Sinkage'],
                'Percentage': [
                    predictions['warpage_percent'],
                    predictions['sinkage_percent']
                ]
            }
            fig_defect = px.bar(
                defect_data,
                x='Defect Type',
                y='Percentage',
                color='Defect Type',
                title="Quality Defects",
                color_discrete_map={'Warpage': '#667eea', 'Sinkage': '#764ba2'}
            )
            fig_defect.add_hline(
                y=5, line_dash="dash", line_color="red",
                annotation_text="Acceptable Threshold"
            )
            fig_defect.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_defect, use_container_width=True)
        
        # Process parameters radar chart
        st.markdown("### 🎯 Process Parameters vs Optimal Range")
        
        param_names = ['Melt Temp\n(°C)', 'Mold Temp\n(°C)', 'Inj. Pressure\n(MPa)',
                      'Hold Pressure\n(MPa)', 'Hold Time\n(s)', 'Cool Time\n(s)']
        
        current_vals = [
            (melt_temp / 300) * 100,  # Normalize to 0-100
            (mold_temp / 100) * 100,
            (injection_pressure / 150) * 100,
            (holding_pressure / 100) * 100,
            (holding_time / 60) * 100,
            (cooling_time / 120) * 100
        ]
        
        optimal_ranges = [
            ((230 / 300) * 100, (240 / 300) * 100),
            ((50 / 100) * 100, (65 / 100) * 100),
            ((60 / 150) * 100, (90 / 150) * 100),
            ((60 / 100) * 100, (75 / 100) * 100),
            ((12 / 60) * 100, (18 / 60) * 100),
            ((30 / 120) * 100, (45 / 120) * 100)
        ]
        
        optimal_vals = [np.mean(r) for r in optimal_ranges]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=current_vals,
            theta=param_names,
            fill='toself',
            name='Current Settings',
            marker_color='#667eea'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=optimal_vals,
            theta=param_names,
            fill='toself',
            name='Optimal Range',
            marker_color='#38ef7d'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)


# ============================================================================
# PAGE: Optimization Assistant
# ============================================================================
elif page == "🎯 Optimization Assistant":
    st.markdown("## AI-Powered Optimization Suggestions")
    
    if not st.session_state.history:
        st.info("👉 First analyze a product in the 'Quality Analysis' tab to get optimization suggestions.")
    else:
        # Get the last analysis
        last_analysis = st.session_state.history[-1]
        
        process_params = last_analysis['process_params']
        geometry_params = last_analysis['geometry_params']
        predictions = last_analysis['predictions']
        
        # Get suggestions
        suggestions_data = st.session_state.optimizer.generate_suggestions(
            process_params, geometry_params, predictions
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current Quality Score", f"{last_analysis['quality_score']:.1f}%")
        
        with col2:
            optimized_params = suggestions_data['optimized_parameters']
            # Recalculate with optimized params
            optimized_predictions = st.session_state.predictor.predict(
                optimized_params, geometry_params
            )
            optimized_quality = st.session_state.optimizer.calculate_quality_score(
                optimized_predictions['warpage_percent'],
                optimized_predictions['sinkage_percent']
            )['overall_quality']
            
            st.metric("Potential Optimized Score", f"{optimized_quality:.1f}%",
                     delta=f"+{optimized_quality - last_analysis['quality_score']:.1f}%")
        
        st.markdown("---")
        
        if suggestions_data['suggestion_count'] == 0:
            st.success("✅ Your process parameters are already optimized!")
        else:
            st.markdown(f"### 📋 {suggestions_data['suggestion_count']} Recommendations")
            
            # Sort by priority
            high_priority = [s for s in suggestions_data['suggestions'] if s['priority'] == 'HIGH']
            medium_priority = [s for s in suggestions_data['suggestions'] if s['priority'] == 'MEDIUM']
            
            for priority, suggestions in [('HIGH', high_priority), ('MEDIUM', medium_priority)]:
                if suggestions:
                    if priority == 'HIGH':
                        st.markdown(f"### 🔴 High Priority Adjustments")
                    else:
                        st.markdown(f"### 🟡 Medium Priority Adjustments")
                    
                    for sugg in suggestions:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"""
                                <div class="suggestion-box">
                                    <b>{sugg['parameter']}</b><br>
                                    Issue: {sugg['issue']}<br>
                                    Current: {sugg['current']} → Suggested: {sugg['suggested']}<br>
                                    Impact: {sugg['impact']}
                                </div>
                                """, unsafe_allow_html=True)
                            with col2:
                                if st.button("Apply", key=f"apply_{sugg['parameter']}"):
                                    st.success(f"✅ Applied {sugg['parameter']} change!")
        
        # Comparison Chart
        st.markdown("---")
        st.markdown("### 📊 Current vs Optimized Parameters")
        
        comparison_data = {
            'Parameter': list(process_params.keys()),
            'Current': list(process_params.values()),
            'Optimized': [optimized_params.get(k, v) for k, v in process_params.items()]
        }
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            x=comparison_data['Parameter'],
            y=comparison_data['Current'],
            name='Current',
            marker_color='#667eea'
        ))
        fig_comparison.add_trace(go.Bar(
            x=comparison_data['Parameter'],
            y=comparison_data['Optimized'],
            name='Optimized',
            marker_color='#38ef7d'
        ))
        fig_comparison.update_layout(barmode='group', height=400)
        st.plotly_chart(fig_comparison, use_container_width=True)


# ============================================================================
# PAGE: History & Reports
# ============================================================================
elif page == "📈 History & Reports":
    st.markdown("## Analysis History & Reports")
    
    if not st.session_state.history:
        st.info("No analysis records yet. Start by analyzing a product!")
    else:
        # Convert history to DataFrame
        history_data = []
        for record in st.session_state.history:
            history_data.append({
                'Timestamp': record['timestamp'],
                'Warpage %': f"{record['predictions']['warpage_percent']:.2f}%",
                'Sinkage %': f"{record['predictions']['sinkage_percent']:.2f}%",
                'Quality Score': f"{record['quality_score']:.1f}%",
                'Status': '✅ PASS' if record['quality_score'] >= 95 else '⚠️ NEEDS IMPROVEMENT'
            })
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True)
        
        # Quality trend
        st.markdown("### 📈 Quality Trend")
        
        trend_data = {
            'Analysis #': list(range(1, len(st.session_state.history) + 1)),
            'Quality Score': [h['quality_score'] for h in st.session_state.history],
            'Warpage': [h['predictions']['warpage_percent'] for h in st.session_state.history],
            'Sinkage': [h['predictions']['sinkage_percent'] for h in st.session_state.history]
        }
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=trend_data['Analysis #'],
            y=trend_data['Quality Score'],
            mode='lines+markers',
            name='Quality Score',
            marker=dict(size=10),
            line=dict(width=2)
        ))
        fig_trend.add_hline(y=95, line_dash="dash", line_color="green",
                           annotation_text="Target Quality")
        fig_trend.update_layout(height=400, title="Quality Score Trend")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Export option
        st.markdown("---")
        if st.button("📥 Export Report as CSV"):
            csv = df_history.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="quality_report.csv",
                mime="text/csv"
            )


# ============================================================================
# PAGE: About
# ============================================================================
elif page == "ℹ️ About":
    st.markdown("""
    ## About This System
    
    ### 🎯 Purpose
    This AI-powered quality checker helps manufacturers optimize injection molding processes
    to minimize warpage and sinkage defects, ensuring products meet quality standards (>95%).
    
    ### 🧠 Technology
    - **Machine Learning**: Multi-Layer Perceptron (Neural Network) models
    - **Framework**: Scikit-learn & TensorFlow
    - **Prediction Models**: 
      - Warpage prediction model
      - Sinkage prediction model
    
    ### 📊 Input Parameters
    
    **Process Parameters:**
    - Melt Temperature (180-280°C)
    - Mold Temperature (20-100°C)
    - Injection Pressure (20-150 MPa)
    - Holding Pressure (10-100 MPa)
    - Holding Time (2-60 seconds)
    - Cooling Time (5-120 seconds)
    
    **Part Geometry:**
    - Wall Thickness (0.5-5.0 mm)
    - Part Volume (10-300 cm³)
    - Aspect Ratio (0.5-4.0)
    
    ### 📈 Output Metrics
    - **Warpage Percentage**: Deviation from intended shape (%)
    - **Sinkage Percentage**: Material shrinkage (%)
    - **Quality Score**: Overall product quality (0-100%)
    - **Optimization Suggestions**: Actionable recommendations to improve quality
    
    ### 🔬 Research Foundation
    This system is based on research paper:
    **"Multi-Objective Optimization of Injection Molding Process Parameters 
    for Junction Boxes Based on BP Neural Network and NSGA-II Algorithm"**
    
    Reference: DOI: 10.3390/ma18030577
    
    ### 💡 Key Features
    ✅ Real-time quality prediction
    ✅ AI-powered optimization suggestions
    ✅ Historical trend analysis
    ✅ Interactive visualizations
    ✅ Export reports to CSV
    
    ### 📝 Version
    Quality Checker v1.0.0
    Last Updated: February 2026
    """)

# Add footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 12px;">
    <p>🏭 Injection Molding Quality Checker | Powered by AI & Machine Learning</p>
    <p>For inquiries and support, contact the development team.</p>
    </div>
""", unsafe_allow_html=True)
