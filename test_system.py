#!/usr/bin/env python3
"""
Test script for Injection Molding Quality Checker
Tests all components and validates functionality
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Checking Required Libraries")
    print("="*60)
    
    required_modules = [
        'streamlit',
        'pandas',
        'numpy',
        'sklearn',
        'matplotlib',
        'plotly',
        'tensorflow',
        'joblib'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {', '.join(missing_modules)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required libraries are installed!")
    return True

def test_quality_predictor():
    """Test the quality predictor module"""
    print("\n" + "="*60)
    print("TEST 2: Quality Predictor Module")
    print("="*60)
    
    try:
        from quality_predictor import MoldingQualityPredictor
        print("✅ Successfully imported MoldingQualityPredictor")
        
        # Create predictor instance
        predictor = MoldingQualityPredictor()
        print("✅ Created predictor instance")
        
        # Train models
        print("\n🧠 Training models (this may take 30-60 seconds)...")
        predictor.train_models()
        print("✅ Models trained successfully")
        
        # Test prediction
        process_params = {
            'melt_temp': 230,
            'mold_temp': 50,
            'part_temp': 60,
            'injection_pressure': 75,
            'holding_pressure': 65,
            'holding_time': 15,
            'cooling_time': 35
        }
        
        geometry_params = {
            'wall_thickness': 2.5,
            'part_volume': 80,
            'aspect_ratio': 1.5,
            'time_to_fill': 8
        }
        
        predictions = predictor.predict(process_params, geometry_params)
        print("\n✅ Made predictions successfully")
        print(f"   Warpage: {predictions['warpage_percent']:.2f}%")
        print(f"   Sinkage: {predictions['sinkage_percent']:.2f}%")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_optimization_engine():
    """Test the optimization engine module"""
    print("\n" + "="*60)
    print("TEST 3: Optimization Engine")
    print("="*60)
    
    try:
        from optimization_engine import OptimizationEngine
        print("✅ Successfully imported OptimizationEngine")
        
        # Create engine instance
        optimizer = OptimizationEngine()
        print("✅ Created optimizer instance")
        
        # Test quality score calculation
        quality_data = optimizer.calculate_quality_score(
            warpage=6.9,
            sinkage=0.99
        )
        print(f"\n✅ Calculated quality score: {quality_data['overall_quality']:.1f}%")
        print(f"   Meets target (>95%): {quality_data['meets_target']}")
        
        # Test rating
        rating, color = optimizer.get_quality_rating(quality_data['overall_quality'])
        print(f"   Rating: {rating}")
        
        # Test suggestions
        process_params = {
            'melt_temp': 245,
            'mold_temp': 40,
            'injection_pressure': 60,
            'holding_pressure': 55,
            'holding_time': 8,
            'cooling_time': 25
        }
        
        geometry_params = {
            'wall_thickness': 3.5,
            'part_volume': 100,
            'aspect_ratio': 2.0
        }
        
        predictions = {'warpage_percent': 8.5, 'sinkage_percent': 4.2}
        
        suggestions = optimizer.generate_suggestions(
            process_params, geometry_params, predictions
        )
        
        print(f"\n✅ Generated {suggestions['suggestion_count']} optimization suggestions")
        if suggestions['suggestion_count'] > 0:
            print("   Suggestions:")
            for i, sugg in enumerate(suggestions['suggestions'][:3], 1):
                print(f"   {i}. {sugg['parameter']}: {sugg['issue']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_report_generator():
    """Test the report generator module"""
    print("\n" + "="*60)
    print("TEST 4: Report Generator")
    print("="*60)
    
    try:
        from report_generator import QualityReport
        print("✅ Successfully imported QualityReport")
        
        # Create test data
        test_analysis = {
            'process_params': {
                'melt_temp': 230,
                'mold_temp': 50,
                'part_temp': 60,
                'injection_pressure': 75,
                'holding_pressure': 65,
                'holding_time': 15,
                'cooling_time': 35
            },
            'geometry_params': {
                'wall_thickness': 2.5,
                'part_volume': 80,
                'aspect_ratio': 1.5,
                'time_to_fill': 8
            },
            'predictions': {
                'warpage_percent': 6.9,
                'sinkage_percent': 0.99
            },
            'quality_score': 95.5
        }
        
        # Generate text report
        text_report = QualityReport.generate_text_report(test_analysis)
        print("✅ Generated text report successfully")
        print("\nSample Report Output:")
        print(text_report[:300] + "...\n")
        
        # Generate JSON report
        json_report = QualityReport.generate_report(test_analysis)
        print("✅ Generated JSON report successfully")
        print(f"   Quality Score: {json_report['quality_score']}%")
        print(f"   Status: {json_report['status']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_configuration():
    """Test configuration file"""
    print("\n" + "="*60)
    print("TEST 5: Configuration")
    print("="*60)
    
    try:
        import json
        
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        print("✅ Successfully loaded config.json")
        print(f"   App: {config['app_name']} v{config['version']}")
        print(f"   Optimal Melt Temp: {config['process_parameters']['melt_temperature']['optimal_range']}")
        print(f"   Quality Target Score: {config['quality_targets']['overall_quality_score']['target']}%")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  INJECTION MOLDING QUALITY CHECKER - TEST SUITE".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Quality Predictor", test_quality_predictor),
        ("Optimization Engine", test_optimization_engine),
        ("Report Generator", test_report_generator),
        ("Configuration", test_configuration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Application is ready to use.")
        print("\nTo start the application, run:")
        print("  Windows: run.bat")
        print("  Linux/Mac: ./run.sh")
        print("  Or: streamlit run app.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        print("Install dependencies with: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
