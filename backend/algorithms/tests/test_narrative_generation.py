# backend/algorithms/tests/test_narrative_generation.py
"""
Comprehensive test suite for narrative generation feature (v2.0).

Tests both algorithm implementations (Binary Search, Interval Coverage)
and validates that narratives meet BACKEND_CHECKLIST.md v2.0 requirements.

Test Categories:
1. Narrative Structure - Headers, sections, formatting
2. Data Completeness - All decision data visible
3. Temporal Coherence - Step N logically leads to step N+1
4. Decision Transparency - Comparisons show actual values
5. Error Handling - Missing data causes loud failures
6. Integration - Multiple examples, edge cases
"""

import pytest
from algorithms.binary_search import BinarySearchTracer
from algorithms.interval_coverage import IntervalCoverageTracer


class TestBinarySearchNarratives:
    """Test narrative generation for Binary Search algorithm."""

    @pytest.fixture
    def basic_search_found(self):
        """Fixture: Basic search where target is found."""
        return {
            'array': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            'target': 7
        }

    @pytest.fixture
    def basic_search_not_found(self):
        """Fixture: Basic search where target is not found."""
        return {
            'array': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            'target': 8
        }

    @pytest.fixture
    def single_element_found(self):
        """Fixture: Single element array, target found."""
        return {
            'array': [42],
            'target': 42
        }

    @pytest.fixture
    def single_element_not_found(self):
        """Fixture: Single element array, target not found."""
        return {
            'array': [42],
            'target': 99
        }

    # ===== Structure Tests =====

    def test_narrative_has_required_headers(self, basic_search_found):
        """Narrative must have standard header sections."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Required headers
        assert "# Binary Search Execution Narrative" in narrative
        assert "**Algorithm:**" in narrative
        assert "**Input Array:**" in narrative
        assert "**Target Value:**" in narrative
        assert "**Result:**" in narrative
        assert "## Execution Summary" in narrative

    def test_narrative_has_step_headers(self, basic_search_found):
        """Each step must have its own header."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should have "## Step N:" headers
        assert "## Step 0:" in narrative
        assert "## Step 1:" in narrative

        # Count step headers - should match trace length
        step_count = narrative.count("## Step ")
        assert step_count == len(trace['trace']['steps'])

    def test_narrative_separates_steps_with_dividers(self, basic_search_found):
        """Steps should be separated by dividers for readability."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should have --- dividers between steps
        divider_count = narrative.count("---")
        # Should have at least N-1 dividers for N steps (excluding header divider)
        assert divider_count >= len(trace['trace']['steps'])

    # ===== Data Completeness Tests =====

    def test_narrative_shows_all_pointer_values(self, basic_search_found):
        """All pointer positions must be visible in narrative."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # For any CALCULATE_MID step, should show left, right, mid
        if any(s['type'] == 'CALCULATE_MID' for s in trace['trace']['steps']):
            assert "Left pointer:" in narrative
            assert "Right pointer:" in narrative
            assert "Mid pointer:" in narrative

    def test_narrative_shows_comparison_values(self, basic_search_found):
        """Comparisons must show actual values being compared."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Extract comparison steps
        comparison_steps = [
            s for s in trace['trace']['steps']
            if s['type'] in ['SEARCH_LEFT', 'SEARCH_RIGHT', 'TARGET_FOUND']
        ]

        for step in comparison_steps:
            # Should show "X < Y" or "X > Y" or "X == Y" format
            # This validates that actual values are visible, not just variable names
            data = step['data']
            if 'comparison' in data:
                comparison_text = data['comparison']
                # Should be in format "number <op> number"
                assert any(op in comparison_text for op in ['<', '>', '=='])

    def test_narrative_shows_search_space_size(self, basic_search_found):
        """Each step should show current search space size."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should mention search space size
        assert "Search space:" in narrative or "search space" in narrative.lower()
        assert "elements" in narrative

    def test_narrative_shows_eliminated_count(self, basic_search_found):
        """When eliminating half, should show how many elements removed."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Look for SEARCH_LEFT or SEARCH_RIGHT steps
        if any(s['type'] in ['SEARCH_LEFT', 'SEARCH_RIGHT'] for s in trace['trace']['steps']):
            assert "Eliminate" in narrative or "eliminate" in narrative
            assert "elements" in narrative

    # ===== Temporal Coherence Tests =====

    def test_narrative_steps_are_sequential(self, basic_search_found):
        """Step numbers should be sequential (0, 1, 2, ...)."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Extract step numbers from narrative
        import re
        step_numbers = re.findall(r'## Step (\d+):', narrative)
        step_numbers = [int(n) for n in step_numbers]

        # Should be [0, 1, 2, 3, ...]
        assert step_numbers == list(range(len(step_numbers)))

    def test_narrative_explains_state_transitions(self, basic_search_found):
        """When state changes, narrative should explain why."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # For decision steps, should explain the decision
        decision_steps = [
            s for s in trace['trace']['steps']
            if s['type'] in ['SEARCH_LEFT', 'SEARCH_RIGHT']
        ]

        for step in decision_steps:
            step_num = step['step']
            # Find this step in narrative
            step_section = narrative.split(f"## Step {step_num}:")[1].split("---")[0]

            # Should contain decision explanation
            assert "Decision:" in step_section or "decision" in step_section.lower()
            assert any(word in step_section.lower() for word in ['because', 'must', 'so'])

    # ===== Decision Transparency Tests =====

    def test_narrative_shows_why_search_left(self, basic_search_found):
        """When searching left, should explain why (mid > target)."""
        # Modify input to force a search left scenario
        tracer = BinarySearchTracer()
        input_data = {'array': [1, 3, 5, 7, 9], 'target': 3}
        trace = tracer.execute(input_data)
        narrative = tracer.generate_narrative(trace)

        # Should have at least one SEARCH_LEFT step
        if any(s['type'] == 'SEARCH_LEFT' for s in trace['trace']['steps']):
            assert "greater than" in narrative.lower()
            assert "left" in narrative.lower()

    def test_narrative_shows_why_search_right(self, basic_search_found):
        """When searching right, should explain why (mid < target)."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should have at least one SEARCH_RIGHT step
        if any(s['type'] == 'SEARCH_RIGHT' for s in trace['trace']['steps']):
            assert "less than" in narrative.lower()
            assert "right" in narrative.lower()

    def test_narrative_shows_why_target_found(self, basic_search_found):
        """When target found, should show the matching comparison."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should have TARGET_FOUND step
        assert any(s['type'] == 'TARGET_FOUND' for s in trace['trace']['steps'])

        # Should show match
        assert "Match Found" in narrative or "Found" in narrative
        assert "==" in narrative

    # ===== Edge Case Tests =====

    def test_narrative_handles_single_element_found(self, single_element_found):
        """Narrative works for single-element array with target found."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(single_element_found)
        narrative = tracer.generate_narrative(trace)

        # Should complete without errors
        assert narrative is not None
        assert len(narrative) > 0
        assert "## Step 0:" in narrative
        assert "Found" in narrative or "found" in narrative

    def test_narrative_handles_single_element_not_found(self, single_element_not_found):
        """Narrative works for single-element array with target not found."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(single_element_not_found)
        narrative = tracer.generate_narrative(trace)

        # Should complete without errors
        assert narrative is not None
        assert len(narrative) > 0
        assert "not found" in narrative.lower()

    def test_narrative_handles_target_not_found(self, basic_search_not_found):
        """Narrative explains when target is not in array."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_not_found)
        narrative = tracer.generate_narrative(trace)

        # Should have TARGET_NOT_FOUND step
        assert any(s['type'] == 'TARGET_NOT_FOUND' for s in trace['trace']['steps'])

        # Should explain the failure
        assert "not found" in narrative.lower()
        assert "does not exist" in narrative.lower() or "not in array" in narrative.lower()

    # ===== Performance Metrics Tests =====

    def test_narrative_shows_comparison_count(self, basic_search_found):
        """Narrative must show total comparisons made."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should mention comparisons
        assert "comparison" in narrative.lower()
        # Should show a number
        assert "Comparisons:" in narrative

    def test_narrative_shows_complexity(self, basic_search_found):
        """Narrative should mention time complexity."""
        tracer = BinarySearchTracer()
        trace = tracer.execute(basic_search_found)
        narrative = tracer.generate_narrative(trace)

        # Should mention O(log n)
        assert "O(log n)" in narrative or "log n" in narrative

    # ===== Consistency Tests =====

    def test_narrative_consistent_across_runs(self, basic_search_found):
        """Same input should produce identical narrative."""
        tracer1 = BinarySearchTracer()
        trace1 = tracer1.execute(basic_search_found)
        narrative1 = tracer1.generate_narrative(trace1)

        tracer2 = BinarySearchTracer()
        trace2 = tracer2.execute(basic_search_found)
        narrative2 = tracer2.generate_narrative(trace2)

        assert narrative1 == narrative2


class TestIntervalCoverageNarratives:
    """Test narrative generation for Interval Coverage algorithm."""

    @pytest.fixture
    def basic_intervals(self):
        """Fixture: Basic 4-interval example."""
        return {
            'intervals': [
                {'id': 1, 'start': 540, 'end': 660, 'color': 'blue'},
                {'id': 2, 'start': 600, 'end': 720, 'color': 'green'},
                {'id': 3, 'start': 660, 'end': 840, 'color': 'yellow'},
                {'id': 4, 'start': 900, 'end': 1020, 'color': 'red'}
            ]
        }

    @pytest.fixture
    def no_overlap(self):
        """Fixture: Non-overlapping intervals (all kept)."""
        return {
            'intervals': [
                {'id': 1, 'start': 0, 'end': 100, 'color': 'blue'},
                {'id': 2, 'start': 200, 'end': 300, 'color': 'green'},
                {'id': 3, 'start': 400, 'end': 500, 'color': 'yellow'}
            ]
        }

    @pytest.fixture
    def full_coverage(self):
        """Fixture: One interval covers all others."""
        return {
            'intervals': [
                {'id': 1, 'start': 0, 'end': 1000, 'color': 'blue'},
                {'id': 2, 'start': 100, 'end': 200, 'color': 'green'},
                {'id': 3, 'start': 300, 'end': 400, 'color': 'yellow'}
            ]
        }

    # ===== Structure Tests =====

    def test_narrative_has_required_headers(self, basic_intervals):
        """Narrative must have standard header sections."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Required headers
        assert "# Interval Coverage Execution Narrative" in narrative
        assert "**Algorithm:**" in narrative
        assert "**Input Size:**" in narrative
        assert "**Output Size:**" in narrative
        assert "## Execution Summary" in narrative

    def test_narrative_shows_input_intervals(self, basic_intervals):
        """Narrative must list all input intervals."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should list all intervals with their ranges
        assert "**Input Intervals:**" in narrative
        for interval in basic_intervals['intervals']:
            assert f"Interval {interval['id']}" in narrative

    def test_narrative_shows_final_result(self, basic_intervals):
        """Narrative must show which intervals were kept."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        assert "**Final Result:**" in narrative
        assert "KEPT" in narrative

    # ===== Recursive Structure Tests =====

    def test_narrative_shows_recursion_depth(self, basic_intervals):
        """Narrative should indicate recursion depth."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should mention depth or recursive calls
        assert "depth" in narrative.lower() or "recursive call" in narrative.lower()

    def test_narrative_indents_recursive_calls(self, basic_intervals):
        """Recursive calls should be visually indented."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Look for indented headers (two spaces per depth level)
        # Depth 1 calls should have "  ## Step"
        if "Depth 1" in narrative or "depth 1" in narrative:
            assert "  ## Step" in narrative

    def test_narrative_shows_return_statements(self, basic_intervals):
        """Narrative should show returns from recursive calls."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should have return indicators
        assert "Return" in narrative or "↩️" in narrative

    # ===== Data Completeness Tests =====

    def test_narrative_shows_max_end_values(self, basic_intervals):
        """All max_end values must be visible in narrative."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should show max_end tracking
        assert "max_end" in narrative
        # Should show initial state (infinity symbol or "no coverage")
        assert "-∞" in narrative or "no coverage" in narrative.lower()

    def test_narrative_shows_comparison_data(self, basic_intervals):
        """Comparisons must show actual values."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # For any EXAMINING_INTERVAL step, should show interval.end and max_end
        examining_steps = [
            s for s in trace['trace']['steps']
            if s['type'] == 'EXAMINING_INTERVAL'
        ]

        for step in examining_steps:
            step_num = step['step']
            # Find this step in narrative
            if f"## Step {step_num}:" in narrative:
                step_section = narrative.split(f"## Step {step_num}:")[1].split("---")[0]

                # Should show both values being compared
                assert "Interval end:" in step_section
                assert "max_end:" in step_section

    def test_narrative_shows_sorting_explanation(self, basic_intervals):
        """Narrative should explain sorting strategy."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should explain why we sort this way
        assert "Sorting" in narrative or "sort" in narrative.lower()
        assert "start" in narrative.lower()
        # Should explain the strategy
        assert "Why" in narrative or "strategy" in narrative.lower()

    # ===== Decision Transparency Tests =====

    def test_narrative_shows_keep_decisions(self, basic_intervals):
        """When keeping interval, should show why."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should have DECISION_MADE steps with "keep"
        keep_steps = [
            s for s in trace['trace']['steps']
            if s['type'] == 'DECISION_MADE' and s['data'].get('decision') == 'keep'
        ]

        if keep_steps:
            assert "KEEP" in narrative
            assert "extends" in narrative.lower() or "extend" in narrative.lower()

    def test_narrative_shows_covered_decisions(self, basic_intervals):
        """When interval is covered, should show why."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should have DECISION_MADE steps with "covered"
        covered_steps = [
            s for s in trace['trace']['steps']
            if s['type'] == 'DECISION_MADE' and s['data'].get('decision') == 'covered'
        ]

        if covered_steps:
            assert "COVERED" in narrative
            assert "covered" in narrative.lower()

    def test_narrative_shows_max_end_updates(self, basic_intervals):
        """When max_end updates, should show old and new values."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should have MAX_END_UPDATE steps
        update_steps = [
            s for s in trace['trace']['steps']
            if s['type'] == 'MAX_END_UPDATE'
        ]

        for step in update_steps:
            step_num = step['step']
            if f"## Step {step_num}:" in narrative:
                step_section = narrative.split(f"## Step {step_num}:")[1].split("---")[0]

                # Should show "from X → Y"
                assert "Previous" in step_section or "old" in step_section.lower()
                assert "New" in step_section or "updated" in step_section.lower()
                assert "→" in step_section or "->" in step_section

    # ===== Edge Case Tests =====

    def test_narrative_handles_no_overlap(self, no_overlap):
        """Narrative works when all intervals are kept."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(no_overlap)
        narrative = tracer.generate_narrative(trace)

        # Should complete without errors
        assert narrative is not None
        assert len(narrative) > 0

        # All intervals should be kept
        result = trace['result']
        assert len(result) == len(no_overlap['intervals'])

    def test_narrative_handles_full_coverage(self, full_coverage):
        """Narrative works when one interval covers all others."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(full_coverage)
        narrative = tracer.generate_narrative(trace)

        # Should complete without errors
        assert narrative is not None
        assert len(narrative) > 0

        # Only one interval should be kept
        result = trace['result']
        assert len(result) == 1

    def test_narrative_handles_empty_intervals(self):
        """Narrative works with empty interval list."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute({'intervals': []})
        narrative = tracer.generate_narrative(trace)

        # Should complete without errors
        assert narrative is not None
        assert "0 intervals" in narrative or "no intervals" in narrative.lower()

    # ===== Performance Metrics Tests =====

    def test_narrative_shows_reduction_stats(self, basic_intervals):
        """Narrative should show how many intervals were removed."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should show input/output/removed counts
        assert "Input:" in narrative or "Total intervals" in narrative
        assert "Output:" in narrative or "Intervals kept:" in narrative
        assert "removed" in narrative.lower() or "Removed:" in narrative

    def test_narrative_shows_complexity(self, basic_intervals):
        """Narrative should mention time/space complexity."""
        tracer = IntervalCoverageTracer()
        trace = tracer.execute(basic_intervals)
        narrative = tracer.generate_narrative(trace)

        # Should mention O(n log n)
        assert "O(n log n)" in narrative or "complexity" in narrative.lower()

    # ===== Consistency Tests =====

    def test_narrative_consistent_across_runs(self, basic_intervals):
        """Same input should produce identical narrative."""
        tracer1 = IntervalCoverageTracer()
        trace1 = tracer1.execute(basic_intervals)
        narrative1 = tracer1.generate_narrative(trace1)

        tracer2 = IntervalCoverageTracer()
        trace2 = tracer2.execute(basic_intervals)
        narrative2 = tracer2.generate_narrative(trace2)

        assert narrative1 == narrative2


class TestNarrativeErrorHandling:
    """Test that narratives fail loudly when data is incomplete."""

    def test_narrative_requires_visualization_data(self):
        """Narrative should fail if visualization data is missing."""
        # This test validates that if trace is somehow corrupted,
        # narrative generation catches it with KeyError

        tracer = BinarySearchTracer()
        input_data = {'array': [1, 3, 5], 'target': 3}
        trace = tracer.execute(input_data)

        # Corrupt the trace by removing visualization data
        for step in trace['trace']['steps']:
            if 'visualization' in step['data']:
                del step['data']['visualization']

        # Narrative generation should fail with KeyError
        with pytest.raises(KeyError):
            tracer.generate_narrative(trace)

    def test_base_tracer_raises_not_implemented(self):
        """Base tracer should raise NotImplementedError."""
        from algorithms.base_tracer import AlgorithmTracer

        # Since generate_narrative is abstract, we can't instantiate without it
        # Instead, test that the error message is helpful when calling base implementation
        
        class MinimalImplementation(AlgorithmTracer):
            def execute(self, input_data):
                return {}

            def get_prediction_points(self):
                return []
            
            # Implement with a call to super() to test the error message
            def generate_narrative(self, trace_result: dict) -> str:
                return super().generate_narrative(trace_result)

        tracer = MinimalImplementation()
        with pytest.raises(NotImplementedError) as exc_info:
            tracer.generate_narrative({})

        # Should have helpful error message
        assert "must implement generate_narrative" in str(exc_info.value)
        assert "BACKEND_CHECKLIST.md" in str(exc_info.value)


class TestNarrativeQuality:
    """High-level quality tests for narratives."""

    def test_narrative_is_self_contained(self):
        """Narrative should be understandable without code/JSON."""
        tracer = BinarySearchTracer()
        input_data = {'array': [1, 3, 5, 7, 9], 'target': 5}
        trace = tracer.execute(input_data)
        narrative = tracer.generate_narrative(trace)

        # Should not have undefined variable references
        # If narrative says "compare with X", X's value should be shown

        # Check that comparisons are complete (no "compare with mid" without showing mid value)
        lines = narrative.split('\n')
        for i, line in enumerate(lines):
            if 'compare' in line.lower() and 'with' in line.lower():
                # Look in surrounding lines for actual values
                context = '\n'.join(lines[max(0, i-5):min(len(lines), i+5)])
                # Should have numbers or specific values
                assert any(char.isdigit() for char in context), \
                    f"Comparison at line {i} lacks actual values: {line}"

    def test_narrative_minimum_length(self):
        """Narrative should be substantive (not just a stub)."""
        tracer = BinarySearchTracer()
        input_data = {'array': [1, 3, 5, 7, 9], 'target': 5}
        trace = tracer.execute(input_data)
        narrative = tracer.generate_narrative(trace)

        # Should be at least 500 characters for even simple cases
        assert len(narrative) >= 500, "Narrative too short - likely missing details"

        # Should have multiple sections
        assert narrative.count('##') >= 3, "Narrative lacks sufficient structure"

    def test_narrative_explains_strategy(self):
        """Narrative should explain the algorithm strategy, not just mechanics."""
        tracer = IntervalCoverageTracer()
        input_data = {
            'intervals': [
                {'id': 1, 'start': 0, 'end': 100, 'color': 'blue'},
                {'id': 2, 'start': 50, 'end': 150, 'color': 'green'}
            ]
        }
        trace = tracer.execute(input_data)
        narrative = tracer.generate_narrative(trace)

        # Should mention strategy/why
        assert any(word in narrative.lower() for word in ['strategy', 'why', 'because', 'insight'])

        # Should explain sorting rationale
        assert "left-to-right" in narrative.lower() or "process" in narrative.lower()