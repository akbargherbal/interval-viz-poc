#!/usr/bin/env python3
"""
Demonstration script showing how narrative generator catches the max_end bug.

This script:
1. Generates a trace using the current (buggy) backend
2. Attempts to generate narrative
3. Shows the exact error that exposes the missing max_end
4. Shows how fixing the backend makes the narrative work

Run this from the backend/ directory:
    python test_narrative_bug.py
"""

import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from algorithms.interval_coverage import IntervalCoverageTracer
from narrative_generator_poc import generate_narrative, NarrativeGenerationError


def test_current_implementation():
    """Test current implementation - will fail due to missing max_end."""
    
    print("=" * 70)
    print("TEST 1: Current Implementation (Missing max_end)")
    print("=" * 70)
    
    tracer = IntervalCoverageTracer()
    
    # Use the original example from the problem
    test_input = {
        "intervals": [
            {"id": 1, "start": 540, "end": 660, "color": "blue"},
            {"id": 2, "start": 600, "end": 720, "color": "green"},
            {"id": 3, "start": 540, "end": 720, "color": "amber"},
            {"id": 4, "start": 900, "end": 960, "color": "purple"}
        ]
    }
    
    print("\nGenerating trace...")
    result = tracer.execute(test_input)
    
    # Save trace for inspection
    trace_file = Path("/tmp/trace_with_bug.json")
    with open(trace_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"✓ Trace saved to: {trace_file}")
    
    # Try to generate narrative
    print("\nAttempting to generate narrative...")
    try:
        narrative = generate_narrative(result)
        print("❌ UNEXPECTED: Narrative generated without error!")
        print("This means max_end is present (bug is fixed)")
    except NarrativeGenerationError as e:
        print("\n✅ EXPECTED FAILURE: Narrative generation exposed the bug!")
        print("\n" + str(e))
        return True
    
    return False


def show_bug_in_json():
    """Show the exact location of the bug in the JSON."""
    
    print("\n" + "=" * 70)
    print("JSON INSPECTION: Where is max_end missing?")
    print("=" * 70)
    
    tracer = IntervalCoverageTracer()
    test_input = {
        "intervals": [
            {"id": 1, "start": 540, "end": 660, "color": "blue"},
            {"id": 2, "start": 600, "end": 720, "color": "green"}
        ]
    }
    
    result = tracer.execute(test_input)
    
    # Find first EXAMINING_INTERVAL step
    for step in result['trace']['steps']:
        if step['type'] == 'EXAMINING_INTERVAL':
            print(f"\nStep {step['step']}: EXAMINING_INTERVAL")
            print(f"Description: {step['description']}")
            print("\nVisualization data:")
            viz = step['data']['visualization']
            
            print(f"  - all_intervals: ✓ Present ({len(viz['all_intervals'])} intervals)")
            print(f"  - call_stack_state: ✓ Present ({len(viz['call_stack_state'])} frames)")
            
            # Check for max_end
            if 'max_end' in viz:
                print(f"  - max_end: ✓ Present (value: {viz['max_end']})")
            else:
                print(f"  - max_end: ❌ MISSING")
                print("\n💡 This is the bug! Frontend needs max_end to render the")
                print("   timeline indicator, but it's not in visualization state.")
            
            break


def show_fix():
    """Show what the fix looks like."""
    
    print("\n" + "=" * 70)
    print("THE FIX: Add max_end to _get_visualization_state()")
    print("=" * 70)
    
    print("""
File: backend/algorithms/interval_coverage.py
Method: _get_visualization_state() (lines ~90-98)

CURRENT CODE (BUGGY):
    def _get_visualization_state(self) -> dict:
        return {
            'all_intervals': self._get_all_intervals_with_state(),
            'call_stack_state': self._get_call_stack_state()
            # ❌ MISSING: 'max_end' is not included here
        }

FIXED CODE:
    def __init__(self):
        super().__init__()
        self.call_stack = []
        self.next_call_id = 0
        self.original_intervals = []
        self.interval_states = {}
        self.current_max_end = float('-inf')  # ✅ ADD THIS LINE

    def _get_visualization_state(self) -> dict:
        return {
            'all_intervals': self._get_all_intervals_with_state(),
            'call_stack_state': self._get_call_stack_state(),
            'max_end': self._serialize_value(self.current_max_end)  # ✅ ADD THIS LINE
        }

    def _filter_recursive(self, intervals, max_end):
        self.current_max_end = max_end  # ✅ ADD THIS at start of method
        
        # ... existing code ...
        
        if not is_covered:
            new_max_end = max(max_end, current.end)
            self.current_max_end = new_max_end  # ✅ UPDATE before recursive call
            # ... existing code ...
""")


def main():
    """Run the demonstration."""
    
    print("\n" + "=" * 70)
    print("NARRATIVE-DRIVEN BUG DETECTION DEMONSTRATION")
    print("=" * 70)
    print("\nThis script demonstrates how the narrative generator catches")
    print("the missing max_end bug before frontend integration.\n")
    
    # Test 1: Show the bug
    bug_found = test_current_implementation()
    
    if bug_found:
        # Test 2: Inspect the JSON
        show_bug_in_json()
        
        # Test 3: Show the fix
        show_fix()
        
        print("\n" + "=" * 70)
        print("CONCLUSION")
        print("=" * 70)
        print("\n✅ The narrative generator successfully detected incomplete")
        print("   visualization state BEFORE frontend integration!")
        print("\n📝 Key Insight:")
        print("   If you cannot write 'We compare interval.end with max_end={value}'")
        print("   then the frontend cannot render 'max_end line at position {value}'")
        print("\n💡 This validates the proposal: Narrative-driven quality gate")
        print("   catches backend incompleteness early in the workflow.")
        
    else:
        print("\n" + "=" * 70)
        print("⚠️  Bug not found - max_end is already present!")
        print("=" * 70)
        print("\nThis means the backend has been fixed.")
        print("The narrative generator is working as a validation tool.")


if __name__ == "__main__":
    main()
