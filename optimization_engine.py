import numpy as np
import pandas as pd

class OptimizationEngine:
    """
    Generates optimization suggestions to minimize warpage and sinkage
    Based on injection molding best practices and research
    """
    
    def __init__(self):
        self.optimal_ranges = {
            'melt_temp': (220, 240),      # °C - from research paper
            'mold_temp': (45, 65),        # °C
            'injection_pressure': (40, 90),  # MPa
            'holding_pressure': (50, 75),    # MPa
            'holding_time': (10, 20),     # seconds
            'cooling_time': (25, 45)      # seconds
        }
    
    def generate_suggestions(self, process_params, geometry_params, predictions):
        """
        Generate optimization suggestions based on predictions and parameters
        
        Args:
            process_params (dict): Current process parameters
            geometry_params (dict): Part geometry
            predictions (dict): Warpage and sinkage predictions
            
        Returns:
            dict: Suggestions and optimized parameters
        """
        suggestions = []
        optimized_params = process_params.copy()
        
        warpage = predictions['warpage_percent']
        sinkage = predictions['sinkage_percent']
        
        # Rule 1: Melt Temperature
        if warpage > 3.0:
            if process_params['melt_temp'] > 240:
                suggestions.append({
                    'parameter': 'Melt Temperature',
                    'issue': f'High warpage ({warpage:.2f}%)',
                    'current': f"{process_params['melt_temp']:.1f}°C",
                    'suggested': f"{225:.1f}°C",
                    'impact': 'Reduce by 10-15°C to lower thermal stress',
                    'priority': 'HIGH'
                })
                optimized_params['melt_temp'] = 225
            elif process_params['melt_temp'] < 200:
                suggestions.append({
                    'parameter': 'Melt Temperature',
                    'issue': f'Low fluidity, inadequate fill',
                    'current': f"{process_params['melt_temp']:.1f}°C",
                    'suggested': f"{230:.1f}°C",
                    'impact': 'Increase to improve flow',
                    'priority': 'MEDIUM'
                })
                optimized_params['melt_temp'] = 230
        
        # Rule 2: Mold Temperature
        if sinkage > 4.0:
            if process_params['mold_temp'] < 45:
                suggestions.append({
                    'parameter': 'Mold Temperature',
                    'issue': f'High sinkage ({sinkage:.2f}%)',
                    'current': f"{process_params['mold_temp']:.1f}°C",
                    'suggested': f"{55:.1f}°C",
                    'impact': 'Increase to improve cooling uniformity',
                    'priority': 'HIGH'
                })
                optimized_params['mold_temp'] = 55
        
        # Rule 3: Holding Pressure
        if sinkage > 3.5:
            if process_params['holding_pressure'] < 50:
                suggestions.append({
                    'parameter': 'Holding Pressure',
                    'issue': f'Inadequate packing ({sinkage:.2f}% sinkage)',
                    'current': f"{process_params['holding_pressure']:.1f} MPa",
                    'suggested': f"{65:.1f} MPa",
                    'impact': 'Increase to compensate for material shrinkage',
                    'priority': 'HIGH'
                })
                optimized_params['holding_pressure'] = 65
        
        # Rule 4: Holding Time
        if sinkage > 3.0:
            if process_params['holding_time'] < 10:
                suggestions.append({
                    'parameter': 'Holding Time',
                    'issue': f'Short packing time causes sinkage',
                    'current': f"{process_params['holding_time']:.1f}s",
                    'suggested': f"{15:.1f}s",
                    'impact': 'Extend to ensure proper material packing',
                    'priority': 'MEDIUM'
                })
                optimized_params['holding_time'] = 15
        
        # Rule 5: Cooling Time
        if warpage > 3.5:
            if process_params['cooling_time'] < 30:
                suggestions.append({
                    'parameter': 'Cooling Time',
                    'issue': f'Insufficient cooling causes warpage',
                    'current': f"{process_params['cooling_time']:.1f}s",
                    'suggested': f"{40:.1f}s",
                    'impact': 'Extend to reduce thermal gradients',
                    'priority': 'HIGH'
                })
                optimized_params['cooling_time'] = 40
        
        # Rule 6: Injection Pressure
        if warpage < 2.0 and sinkage > 3.0:
            if process_params['injection_pressure'] < 60:
                suggestions.append({
                    'parameter': 'Injection Pressure',
                    'issue': f'Low fill pressure, high sinkage',
                    'current': f"{process_params['injection_pressure']:.1f} MPa",
                    'suggested': f"{75:.1f} MPa",
                    'impact': 'Increase for better mold filling',
                    'priority': 'MEDIUM'
                })
                optimized_params['injection_pressure'] = 75
        
        # Rule 7: Wall Thickness
        if geometry_params['wall_thickness'] > 3.5:
            suggestions.append({
                'parameter': 'Wall Thickness',
                'issue': 'Thick walls increase cooling time and defects',
                'current': f"{geometry_params['wall_thickness']:.1f}mm",
                'suggested': f"{2.5:.1f}mm (if possible)",
                'impact': 'Reduce wall thickness to improve quality',
                'priority': 'MEDIUM'
            })
        
        return {
            'suggestions': suggestions,
            'optimized_parameters': optimized_params,
            'suggestion_count': len(suggestions)
        }
    
    def calculate_quality_score(self, warpage, sinkage):
        """
        Calculate overall quality score (0-100%)
        
        Warpage contribution: 50%
        Sinkage contribution: 50%
        
        Target values (from research):
        - Optimal warpage: 6.9%
        - Optimal sinkage: 0.99mm
        """
        # Warpage score (0% at 10% warpage, 100% at 0% warpage)
        warpage_score = max(0, 100 - (warpage * 10))
        
        # Sinkage score (0% at 5mm sinkage, 100% at 0% sinkage)
        sinkage_score = max(0, 100 - (sinkage * 20))
        
        # Combined quality score
        quality_score = (warpage_score * 0.5 + sinkage_score * 0.5)
        
        return {
            'overall_quality': quality_score,
            'warpage_score': warpage_score,
            'sinkage_score': sinkage_score,
            'meets_target': quality_score >= 95
        }
    
    def get_quality_rating(self, quality_score):
        """Get quality rating based on score"""
        if quality_score >= 95:
            return "EXCELLENT ⭐⭐⭐⭐⭐", "green"
        elif quality_score >= 85:
            return "GOOD ⭐⭐⭐⭐", "blue"
        elif quality_score >= 75:
            return "ACCEPTABLE ⭐⭐⭐", "yellow"
        elif quality_score >= 60:
            return "NEEDS IMPROVEMENT ⭐⭐", "orange"
        else:
            return "POOR ⭐", "red"

if __name__ == "__main__":
    print("Optimization Engine Ready!")
