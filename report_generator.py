import numpy as np
import json
from datetime import datetime
import os

class QualityReport:
    """Generate comprehensive quality reports"""
    
    @staticmethod
    def generate_report(analysis_data, filename=None):
        """Generate a JSON report from analysis data"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'process_parameters': analysis_data['process_params'],
            'geometry_parameters': analysis_data['geometry_params'],
            'predictions': {
                'warpage_percent': round(analysis_data['predictions']['warpage_percent'], 2),
                'sinkage_percent': round(analysis_data['predictions']['sinkage_percent'], 2)
            },
            'quality_score': round(analysis_data['quality_score'], 1),
            'status': 'PASS' if analysis_data['quality_score'] >= 95 else 'NEEDS IMPROVEMENT'
        }
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
        
        return report
    
    @staticmethod
    def generate_text_report(analysis_data):
        """Generate a human-readable text report"""
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║     INJECTION MOLDING QUALITY ANALYSIS REPORT                ║
╚══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

────────────────────────────────────────────────────────────────
PROCESS PARAMETERS
────────────────────────────────────────────────────────────────
Melt Temperature:        {analysis_data['process_params']['melt_temp']:.1f}°C
Mold Temperature:        {analysis_data['process_params']['mold_temp']:.1f}°C
Injection Pressure:      {analysis_data['process_params']['injection_pressure']:.1f} MPa
Holding Pressure:        {analysis_data['process_params']['holding_pressure']:.1f} MPa
Holding Time:            {analysis_data['process_params']['holding_time']:.1f} seconds
Cooling Time:            {analysis_data['process_params']['cooling_time']:.1f} seconds

────────────────────────────────────────────────────────────────
PART GEOMETRY
────────────────────────────────────────────────────────────────
Wall Thickness:          {analysis_data['geometry_params']['wall_thickness']:.1f} mm
Part Volume:             {analysis_data['geometry_params']['part_volume']:.1f} cm³
Aspect Ratio:            {analysis_data['geometry_params']['aspect_ratio']:.2f}

────────────────────────────────────────────────────────────────
QUALITY PREDICTIONS
────────────────────────────────────────────────────────────────
Warpage:                 {analysis_data['predictions']['warpage_percent']:.2f}% (Target: < 5%)
Sinkage:                 {analysis_data['predictions']['sinkage_percent']:.2f}% (Target: < 2%)
Overall Quality Score:   {analysis_data['quality_score']:.1f}% (Target: ≥ 95%)

Status: {'✅ EXCELLENT - MEETS QUALITY STANDARDS' if analysis_data['quality_score'] >= 95 else '⚠️  NEEDS IMPROVEMENT - REQUIRES OPTIMIZATION'}

════════════════════════════════════════════════════════════════
"""
        return report

if __name__ == "__main__":
    print("Report Generator Ready!")
