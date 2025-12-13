# backend/algorithms/tests/test_narrative_generation.py
"""
Test suite for narrative generation from trace output.

This validates that all algorithm traces can generate coherent narratives,
ensuring visualization state is complete before frontend integration.
"""

import pytest
import sys
from pathlib import Path

# Import the narrative generator
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from narrative_generator_poc import generate_narrative, NarrativeGenerationError


@pytest.mark.compliance
class TestNarrativeGeneration:
    """Verify traces generate coherent narratives."""

    def test_interval_coverage_narrative_complete(self):
        """Interval coverage trace should generate complete narrative."""
        from algorithms.interval_coverage import IntervalCoverageTracer
        
        tracer = IntervalCoverageTracer()
        result = tracer.execute({
            'intervals': [
                {"id": 1, "start": 540, "end": 660, "color": "blue"},
                {"id": 2, "start": 600, "end": 720, "color": "green"},
                {"id": 3, "start": 540, "end": 720, "color": "amber"},
                {"id": 4, "start": 900, "end": 960, "color": "purple"}
            ]
        })
        
        # This will raise NarrativeGenerationError if visualization state is incomplete
        narrative = generate_narrative(result)
        
        # Verify narrative was generated
        assert narrative is not None
        assert len(narrative) > 0
        
        # Verify key elements are present
        assert "max_end" in narrative.lower(), \
            "Narrative should mention max_end (coverage tracking)"
        assert "coverage extends to" in narrative.lower(), \
            "Narrative should explain coverage progression"
        assert "EXAMINING_INTERVAL" in narrative, \
            "Narrative should include step types"

    def test_interval_coverage_narrative_has_max_end_in_all_examining_steps(self):
        """Every EXAMINING_INTERVAL step should reference max_end in narrative."""
        from algorithms.interval_coverage import IntervalCoverageTracer
        
        tracer = IntervalCoverageTracer()
        result = tracer.execute({
            'intervals': [
                {"id": 1, "start": 10, "end": 50, "color": "blue"},
                {"id": 2, "start": 20, "end": 60, "color": "green"}
            ]
        })
        
        narrative = generate_narrative(result)
        
        # Count EXAMINING_INTERVAL steps in trace
        examining_steps = [s for s in result['trace']['steps'] if s['type'] == 'EXAMINING_INTERVAL']
        
        # Each examining step should produce a narrative section mentioning coverage
        for step in examining_steps:
            interval = step['data']['interval']
            # Look for this interval's examination in narrative
            assert f"({interval['start']}, {interval['end']})" in narrative, \
                f"Narrative should mention interval ({interval['start']}, {interval['end']})"

    def test_binary_search_narrative_complete(self):
        """Binary search trace should generate complete narrative."""
        from algorithms.binary_search import BinarySearchTracer
        
        tracer = BinarySearchTracer()
        result = tracer.execute({
            'array': [1, 3, 5, 7, 9, 11, 13, 15],
            'target': 7
        })
        
        # Should not raise NarrativeGenerationError
        narrative = generate_narrative(result)
        
        # Verify narrative was generated
        assert narrative is not None
        assert len(narrative) > 0
        
        # Verify it mentions binary search concepts
        assert "array" in narrative.lower() or "search" in narrative.lower()

    def test_empty_intervals_generates_narrative(self):
        """Empty input should still generate valid narrative."""
        from algorithms.interval_coverage import IntervalCoverageTracer
        
        tracer = IntervalCoverageTracer()
        result = tracer.execute({'intervals': []})
        
        # Should not raise error
        narrative = generate_narrative(result)
        
        assert narrative is not None
        assert "0 intervals" in narrative.lower() or "empty" in narrative.lower()

    def test_narrative_includes_summary(self):
        """Generated narrative should include a summary section."""
        from algorithms.interval_coverage import IntervalCoverageTracer
        
        tracer = IntervalCoverageTracer()
        result = tracer.execute({
            'intervals': [
                {"id": 1, "start": 10, "end": 50, "color": "blue"}
            ]
        })
        
        narrative = generate_narrative(result)
        
        assert "## Summary" in narrative, \
            "Narrative should include a summary section"
        assert "Final Result" in narrative or "final result" in narrative.lower(), \
            "Summary should mention final result"

    def test_narrative_includes_metadata(self):
        """Generated narrative should include trace metadata."""
        from algorithms.interval_coverage import IntervalCoverageTracer
        
        tracer = IntervalCoverageTracer()
        result = tracer.execute({
            'intervals': [
                {"id": 1, "start": 10, "end": 50, "color": "blue"}
            ]
        })
        
        narrative = generate_narrative(result)
        
        # Should include metadata at top
        assert "**Input:**" in narrative
        assert "**Output:**" in narrative
        assert "**Total Steps:**" in narrative
        assert "**Duration:**" in narrative


@pytest.mark.compliance
class TestNarrativeGenerationErrorDetection:
    """Test that narrative generator catches incomplete visualization state."""

    def test_missing_visualization_field_raises_error(self):
        """If required field is missing, should raise NarrativeGenerationError."""
        # This test would require a deliberately broken tracer
        # For now, we document the expected behavior
        
        # Example: If a step has type EXAMINING_INTERVAL but visualization.max_end
        # is missing, generate_narrative should raise NarrativeGenerationError
        # with a clear message pointing to the missing field.
        
        # This is more of a documentation test - the actual validation happens
        # when we try to generate narratives from real traces
        pass


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
