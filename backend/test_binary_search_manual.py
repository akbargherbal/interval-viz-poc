#!/usr/bin/env python3
"""
Manual test script for BinarySearchTracer.

Run this to verify the tracer works correctly before adding API endpoints.

Usage:
    cd backend
    python test_binary_search_manual.py
"""

import sys
import json
from algorithms.binary_search import BinarySearchTracer


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_found_target():
    """Test case: Target exists in array."""
    print_section("TEST 1: Target Found (5 in [1,3,5,7,9])")
    
    tracer = BinarySearchTracer()
    result = tracer.execute({
        'array': [1, 3, 5, 7, 9],
        'target': 5
    })
    
    print(f"✓ Result: {result['result']}")
    print(f"✓ Total steps: {result['trace']['total_steps']}")
    print(f"✓ Visualization type: {result['metadata']['visualization_type']}")
    
    # Check structure
    assert result['result']['found'] == True
    assert result['result']['index'] == 2
    assert result['metadata']['visualization_type'] == 'array'
    
    # Check first step has visualization data
    first_step = result['trace']['steps'][0]
    assert 'visualization' in first_step['data']
    assert 'array' in first_step['data']['visualization']
    assert 'pointers' in first_step['data']['visualization']
    
    print("✓ Structure validation passed")
    
    # Check predictions
    predictions = result['metadata']['prediction_points']
    print(f"✓ Prediction points: {len(predictions)}")
    if predictions:
        print(f"  First prediction: {predictions[0]['question']}")
        print(f"  Correct answer: {predictions[0]['correct_answer']}")
    
    return result


def test_not_found_target():
    """Test case: Target doesn't exist in array."""
    print_section("TEST 2: Target Not Found (6 in [1,3,5,7,9])")
    
    tracer = BinarySearchTracer()
    result = tracer.execute({
        'array': [1, 3, 5, 7, 9],
        'target': 6
    })
    
    print(f"✓ Result: {result['result']}")
    print(f"✓ Total steps: {result['trace']['total_steps']}")
    
    assert result['result']['found'] == False
    assert result['result']['index'] == None
    
    print("✓ Structure validation passed")
    return result


def test_edge_cases():
    """Test edge cases."""
    print_section("TEST 3: Edge Cases")
    
    # Single element - found
    print("\n  3a. Single element array (target found)")
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [5], 'target': 5})
    assert result['result']['found'] == True
    assert result['result']['index'] == 0
    print("  ✓ Single element - found")
    
    # Single element - not found
    print("\n  3b. Single element array (target not found)")
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [5], 'target': 3})
    assert result['result']['found'] == False
    print("  ✓ Single element - not found")
    
    # Target at start
    print("\n  3c. Target at start of array")
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [1, 2, 3, 4, 5], 'target': 1})
    assert result['result']['found'] == True
    assert result['result']['index'] == 0
    print("  ✓ Target at start")
    
    # Target at end
    print("\n  3d. Target at end of array")
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [1, 2, 3, 4, 5], 'target': 5})
    assert result['result']['found'] == True
    assert result['result']['index'] == 4
    print("  ✓ Target at end")
    
    print("\n✓ All edge cases passed")


def test_validation_errors():
    """Test input validation."""
    print_section("TEST 4: Input Validation")
    
    tracer = BinarySearchTracer()
    
    # Empty array
    print("\n  4a. Empty array")
    try:
        tracer.execute({'array': [], 'target': 5})
        print("  ✗ Should have raised ValueError")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {e}")
    
    # Unsorted array
    print("\n  4b. Unsorted array")
    try:
        tracer.execute({'array': [5, 1, 3, 2, 4], 'target': 3})
        print("  ✗ Should have raised ValueError")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {e}")
    
    # Missing keys
    print("\n  4c. Missing 'target' key")
    try:
        tracer.execute({'array': [1, 2, 3]})
        print("  ✗ Should have raised ValueError")
        sys.exit(1)
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {e}")
    
    print("\n✓ All validation tests passed")


def inspect_trace_structure(result):
    """Detailed inspection of trace structure."""
    print_section("TRACE STRUCTURE INSPECTION")
    
    print("\n📋 Result Keys:")
    for key in result.keys():
        print(f"  • {key}")
    
    print("\n📋 Metadata:")
    for key, value in result['metadata'].items():
        if key != 'prediction_points':  # Skip large array
            print(f"  • {key}: {value}")
        else:
            print(f"  • {key}: [{len(value)} prediction points]")
    
    print("\n📋 First Step Structure:")
    first_step = result['trace']['steps'][0]
    print(f"  • step: {first_step['step']}")
    print(f"  • type: {first_step['type']}")
    print(f"  • description: {first_step['description']}")
    print(f"  • data keys: {list(first_step['data'].keys())}")
    
    if 'visualization' in first_step['data']:
        viz = first_step['data']['visualization']
        print(f"\n📋 Visualization Data:")
        print(f"  • array: [{len(viz.get('array', []))} elements]")
        print(f"  • pointers: {viz.get('pointers', {})}")
        print(f"  • search_space_size: {viz.get('search_space_size', 'N/A')}")
        
        if viz.get('array'):
            print(f"\n📋 First Array Element:")
            first_elem = viz['array'][0]
            for key, value in first_elem.items():
                print(f"    • {key}: {value}")
    
    print("\n📋 Step Types in Trace:")
    step_types = [step['type'] for step in result['trace']['steps']]
    for i, step_type in enumerate(step_types):
        print(f"  {i}. {step_type}")
    
    print("\n📋 Prediction Points:")
    for i, pred in enumerate(result['metadata']['prediction_points']):
        print(f"\n  Prediction {i+1}:")
        print(f"    • Question: {pred['question']}")
        print(f"    • Choices: {[c['id'] for c in pred['choices']]}")
        print(f"    • Correct: {pred['correct_answer']}")


def export_trace_json(result, filename='binary_search_trace_sample.json'):
    """Export trace to JSON file for inspection."""
    print_section(f"EXPORTING TRACE TO {filename}")
    
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✓ Trace exported to {filename}")
    print(f"✓ File size: {len(json.dumps(result))} bytes")


def main():
    """Run all tests."""
    print("\n" + "🧪" * 35)
    print("  Binary Search Tracer - Manual Test Suite")
    print("🧪" * 35)
    
    try:
        # Run tests
        result1 = test_found_target()
        result2 = test_not_found_target()
        test_edge_cases()
        test_validation_errors()
        
        # Detailed inspection
        inspect_trace_structure(result1)
        
        # Export sample
        export_trace_json(result1)
        
        # Final summary
        print_section("✅ ALL TESTS PASSED")
        print("\n🎉 BinarySearchTracer is working correctly!")
        print("📝 Next steps:")
        print("   1. Review binary_search_trace_sample.json")
        print("   2. Add endpoint to app.py")
        print("   3. Test with frontend")
        print()
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()