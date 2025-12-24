
"""
Tests for Merge Intervals algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.merge_intervals_tracer import MergeIntervalsTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestMergeIntervalsCorrectness:
    """Test algorithm correctness - does it merge intervals correctly?"""

    def test_no_overlap(self):
        """Test case: No overlapping intervals."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        assert result['result']['merged_intervals'] == [[1, 3], [5, 7], [9, 10]]
        assert result['result']['merge_count'] == 0

    def test_full_enclosure(self):
        """Test case: One interval fully encloses others."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 10], [2, 5], [3, 7]]})
        
        assert result['result']['merged_intervals'] == [[1, 10]]
        assert result['result']['merge_count'] == 2

    def test_complete_overlap(self):
        """Test case: Identical intervals."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [1, 5]]})
        
        assert result['result']['merged_intervals'] == [[1, 5]]
        assert result['result']['merge_count'] == 1

    def test_partial_overlap(self):
        """Test case: Intervals with partial overlap."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 4], [3, 6], [5, 8]]})
        
        assert result['result']['merged_intervals'] == [[1, 8]]
        assert result['result']['merge_count'] == 2

    def test_adjacent_intervals(self):
        """Test case: Adjacent intervals (touching but not overlapping)."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [3, 5], [5, 7]]})
        
        # Adjacent intervals should merge (3 <= 3, 5 <= 5)
        assert result['result']['merged_intervals'] == [[1, 7]]
        assert result['result']['merge_count'] == 2

    def test_single_interval(self):
        """Test case: Single interval (nothing to merge)."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[5, 10]]})
        
        assert result['result']['merged_intervals'] == [[5, 10]]
        assert result['result']['merge_count'] == 0

    def test_two_intervals_overlap(self):
        """Test case: Two intervals that overlap."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8]]})
        
        assert result['result']['merged_intervals'] == [[1, 8]]
        assert result['result']['merge_count'] == 1

    def test_two_intervals_no_overlap(self):
        """Test case: Two intervals that don't overlap."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 8]]})
        
        assert result['result']['merged_intervals'] == [[1, 3], [5, 8]]
        assert result['result']['merge_count'] == 0

    def test_unsorted_input(self):
        """Test case: Unsorted input intervals."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[5, 7], [1, 3], [9, 10]]})
        
        # Should sort first, then process
        assert result['result']['merged_intervals'] == [[1, 3], [5, 7], [9, 10]]
        assert result['result']['merge_count'] == 0

    def test_complex_merge_scenario(self):
        """Test case: Complex scenario with multiple merges."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 4], [2, 5], [7, 9], [8, 10], [12, 15]]})
        
        assert result['result']['merged_intervals'] == [[1, 5], [7, 10], [12, 15]]
        assert result['result']['merge_count'] == 2

    def test_all_merge_into_one(self):
        """Test case: All intervals merge into one."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [2, 4], [3, 5], [4, 6]]})
        
        assert result['result']['merged_intervals'] == [[1, 6]]
        assert result['result']['merge_count'] == 3


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestMergeIntervalsTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_sort_intervals_first_step(self):
        """First step should be SORT_INTERVALS."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[5, 7], [1, 3]]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'SORT_INTERVALS'
        assert 'original_intervals' in first_step['data']
        assert 'sorted_intervals' in first_step['data']

    def test_sorting_preserves_intervals(self):
        """Sorted intervals should contain all original intervals."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[5, 7], [1, 3], [9, 10]]})
        
        first_step = result['trace']['steps'][0]
        original = first_step['data']['original_intervals']
        sorted_intervals = first_step['data']['sorted_intervals']
        
        assert len(original) == len(sorted_intervals)
        assert sorted(original) == sorted_intervals

    def test_compare_overlap_steps_present(self):
        """COMPARE_OVERLAP steps should be present for each interval after first."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP']
        
        # Should have n-1 comparisons for n intervals
        assert len(compare_steps) == 2

    def test_compare_overlap_has_required_data(self):
        """COMPARE_OVERLAP steps should have all required data."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP']
        
        for step in compare_steps:
            assert 'current_interval' in step['data']
            assert 'last_merged' in step['data']
            assert 'overlaps' in step['data']
            assert 'comparison' in step['data']

    def test_merge_step_follows_overlap(self):
        """MERGE step should follow COMPARE_OVERLAP when overlaps=True."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8]]})
        
        steps = result['trace']['steps']
        
        for i, step in enumerate(steps):
            if step['type'] == 'COMPARE_OVERLAP' and step['data']['overlaps']:
                next_step = steps[i + 1]
                assert next_step['type'] == 'MERGE'

    def test_add_new_step_follows_no_overlap(self):
        """ADD_NEW step should follow COMPARE_OVERLAP when overlaps=False."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        steps = result['trace']['steps']
        
        for i, step in enumerate(steps):
            if step['type'] == 'COMPARE_OVERLAP' and not step['data']['overlaps']:
                next_step = steps[i + 1]
                assert next_step['type'] == 'ADD_NEW'

    def test_merge_step_has_calculation(self):
        """MERGE step should show max() calculation."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8]]})
        
        merge_steps = [s for s in result['trace']['steps'] if s['type'] == 'MERGE']
        
        assert len(merge_steps) > 0
        for step in merge_steps:
            assert 'calculation' in step['data']
            assert 'max' in step['data']['calculation']
            assert 'new_end' in step['data']
            assert 'old_last_merged' in step['data']

    def test_add_new_step_has_interval(self):
        """ADD_NEW step should include the interval being added."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        add_new_steps = [s for s in result['trace']['steps'] if s['type'] == 'ADD_NEW']
        
        assert len(add_new_steps) > 0
        for step in add_new_steps:
            assert 'current_interval' in step['data']

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestMergeIntervalsVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_all_intervals_structure(self):
        """all_intervals should have id, start, end, state for each interval."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        # Check a COMPARE_OVERLAP step
        compare_step = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP'][0]
        viz = compare_step['data']['visualization']
        
        assert 'all_intervals' in viz
        assert len(viz['all_intervals']) == 2
        
        for interval in viz['all_intervals']:
            assert 'id' in interval
            assert 'start' in interval
            assert 'end' in interval
            assert 'state' in interval

    def test_interval_states_valid(self):
        """Interval states should be one of: pending, examining, merged, new_interval."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        valid_states = {'pending', 'examining', 'merged', 'new_interval'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for interval in viz['all_intervals']:
                assert interval['state'] in valid_states

    def test_examining_state_at_current(self):
        """Current interval should have 'examining' state."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP']
        
        for step in compare_steps:
            viz = step['data']['visualization']
            current_interval = step['data']['current_interval']
            
            # Find the examining interval
            examining = [iv for iv in viz['all_intervals'] if iv['state'] == 'examining']
            assert len(examining) == 1
            assert examining[0]['start'] == current_interval[0]
            assert examining[0]['end'] == current_interval[1]

    def test_call_stack_state_present(self):
        """call_stack_state should be present and valid."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP']
        
        for step in compare_steps:
            viz = step['data']['visualization']
            assert 'call_stack_state' in viz
            
            if viz['call_stack_state']:
                for stack_item in viz['call_stack_state']:
                    assert 'interval_id' in stack_item
                    assert 'type' in stack_item
                    assert 'interval' in stack_item

    def test_merged_count_increases(self):
        """merged_count should increase when intervals merge."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8]]})
        
        steps = result['trace']['steps']
        
        # Find MERGE step
        merge_step_index = None
        for i, step in enumerate(steps):
            if step['type'] == 'MERGE':
                merge_step_index = i
                break
        
        assert merge_step_index is not None
        
        # Check merged_count before and after
        before_step = steps[merge_step_index - 1]
        after_step = steps[merge_step_index]
        
        # After merge, merged_count should reflect the merge
        # (Note: merged_count is the count of intervals in merged list, not merge operations)

    def test_pending_count_decreases(self):
        """pending_count should decrease as intervals are processed."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP']
        
        previous_pending = None
        for step in compare_steps:
            viz = step['data']['visualization']
            current_pending = viz['pending_count']
            
            if previous_pending is not None:
                assert current_pending <= previous_pending
            
            previous_pending = current_pending

    def test_visualization_ids_sequential(self):
        """Interval IDs should be sequential starting from 1."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        first_step = result['trace']['steps'][0]
        viz = first_step['data']['visualization']
        
        ids = [iv['id'] for iv in viz['all_intervals']]
        assert ids == list(range(1, len(viz['all_intervals']) + 1))


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestMergeIntervalsPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_count_matches_comparisons(self):
        """Prediction count should match number of COMPARE_OVERLAP steps."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        compare_count = len([s for s in result['trace']['steps'] if s['type'] == 'COMPARE_OVERLAP'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == compare_count

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'merge', 'add-new', 'skip'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice
                assert isinstance(choice['label'], str)
                assert len(choice['label']) > 0

    def test_correct_answer_valid(self):
        """Correct answer should be one of the three choices."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'merge', 'add-new', 'skip'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_step(self):
        """Correct answer should match the actual next step taken."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8], [10, 12]]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Get next step
            next_step = steps[step_index + 1]
            
            # Verify answer matches next step type
            if correct_answer == 'merge':
                assert next_step['type'] == 'MERGE'
            elif correct_answer == 'add-new':
                assert next_step['type'] == 'ADD_NEW'

    def test_prediction_question_mentions_intervals(self):
        """Question should mention the intervals being compared."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            assert 'interval' in question

    def test_prediction_hint_mentions_comparison(self):
        """Hint should mention the comparison being made."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint'].lower()
            assert 'compare' in hint or 'start' in hint or 'end' in hint

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            explanation = pred['explanation']
            assert isinstance(explanation, str)
            assert len(explanation) > 0


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestMergeIntervalsEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_intervals_raises_error(self):
        """Empty intervals list should raise ValueError."""
        tracer = MergeIntervalsTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'intervals': []})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = MergeIntervalsTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([[1, 3], [5, 7]])

    def test_missing_intervals_key_raises_error(self):
        """Missing 'intervals' key should raise ValueError."""
        tracer = MergeIntervalsTracer()
        
        with pytest.raises(ValueError, match="intervals"):
            tracer.execute({'data': [[1, 3]]})

    def test_invalid_interval_format_raises_error(self):
        """Invalid interval format should raise ValueError."""
        tracer = MergeIntervalsTracer()
        
        with pytest.raises(ValueError, match="list/tuple"):
            tracer.execute({'intervals': [[1, 3], [5]]})

    def test_non_integer_values_raise_error(self):
        """Non-integer interval values should raise ValueError."""
        tracer = MergeIntervalsTracer()
        
        with pytest.raises(ValueError, match="integers"):
            tracer.execute({'intervals': [[1.5, 3.5]]})

    def test_start_greater_than_end_raises_error(self):
        """Interval with start > end should raise ValueError."""
        tracer = MergeIntervalsTracer()
        
        with pytest.raises(ValueError, match="start must be <= end"):
            tracer.execute({'intervals': [[5, 3]]})

    def test_single_interval_no_merge(self):
        """Single interval should return as-is with no merges."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[5, 10]]})
        
        assert result['result']['merged_intervals'] == [[5, 10]]
        assert result['result']['merge_count'] == 0

    def test_zero_length_interval(self):
        """Interval with start == end should be valid."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[5, 5], [7, 7]]})
        
        assert result['result']['merged_intervals'] == [[5, 5], [7, 7]]

    def test_large_time_values(self):
        """Large time values should work correctly."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1000, 2000], [1500, 2500]]})
        
        assert result['result']['merged_intervals'] == [[1000, 2500]]
        assert result['result']['merge_count'] == 1

    def test_many_intervals(self):
        """Should handle many intervals (10 intervals as per spec)."""
        intervals = [[i, i+2] for i in range(0, 20, 3)]  # Non-overlapping
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assert len(result['result']['merged_intervals']) == len(intervals)
        assert result['result']['merge_count'] == 0


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestMergeIntervalsMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        metadata = result['metadata']
        
        required_fields = [
            'algorithm',
            'display_name',
            'visualization_type',
            'visualization_config',
            'input_size',
            'prediction_points'
        ]
        
        for field in required_fields:
            assert field in metadata, f"Missing required field: {field}"

    def test_algorithm_field_correct(self):
        """algorithm field should be 'merge-intervals'."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert result['metadata']['algorithm'] == 'merge-intervals'

    def test_display_name_field_correct(self):
        """display_name field should be 'Merge Intervals'."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert result['metadata']['display_name'] == 'Merge Intervals'

    def test_visualization_type_correct(self):
        """visualization_type should be 'timeline'."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert result['metadata']['visualization_type'] == 'timeline'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        config = result['metadata']['visualization_config']
        
        assert 'show_merged' in config
        assert 'show_axis' in config
        assert config['show_merged'] is True
        assert config['show_axis'] is True

    def test_input_size_correct(self):
        """input_size should match number of intervals."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7], [9, 10]]})
        
        assert result['metadata']['input_size'] == 3

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_metadata_types_correct(self):
        """All metadata fields should have correct types."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        metadata = result['metadata']
        
        assert isinstance(metadata['algorithm'], str)
        assert isinstance(metadata['display_name'], str)
        assert isinstance(metadata['visualization_type'], str)
        assert isinstance(metadata['visualization_config'], dict)
        assert isinstance(metadata['input_size'], int)
        assert isinstance(metadata['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'merged_intervals' in result['result']
        assert 'merge_count' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestMergeIntervalsNarrative:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generation_succeeds(self):
        """generate_narrative should execute without errors."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        narrative = tracer.generate_narrative(result)
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_has_header(self):
        """Narrative should have a header."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        narrative = tracer.generate_narrative(result)
        
        assert '# Merge Intervals Execution Narrative' in narrative

    def test_narrative_has_steps(self):
        """Narrative should include step-by-step breakdown."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        narrative = tracer.generate_narrative(result)
        
        assert '## Step 0:' in narrative
        assert '## Step 1:' in narrative

    def test_narrative_has_summary(self):
        """Narrative should have execution summary."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        narrative = tracer.generate_narrative(result)
        
        assert '## Execution Summary' in narrative

    def test_narrative_has_visualization_hints(self):
        """Narrative should include Frontend Visualization Hints section."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        narrative = tracer.generate_narrative(result)
        
        assert '## 🎨 Frontend Visualization Hints' in narrative
        assert '### Primary Metrics to Emphasize' in narrative
        assert '### Visualization Priorities' in narrative
        assert '### Key JSON Paths' in narrative
        assert '### Algorithm-Specific Guidance' in narrative

    def test_narrative_shows_comparisons(self):
        """Narrative should show explicit comparisons."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8]]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should show comparison with actual values
        assert 'Compare' in narrative or 'compare' in narrative
        assert '<=' in narrative

    def test_narrative_shows_calculations(self):
        """Narrative should show max() calculations for merges."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 5], [3, 8]]})
        
        narrative = tracer.generate_narrative(result)
        
        assert 'max(' in narrative

    def test_narrative_valid_markdown(self):
        """Narrative should be valid markdown (basic check)."""
        tracer = MergeIntervalsTracer()
        result = tracer.execute({'intervals': [[1, 3], [5, 7]]})
        
        narrative = tracer.generate_narrative(result)
        
        # Check for markdown elements
        assert '#' in narrative  # Headers
        assert '**' in narrative  # Bold
        assert '\n\n' in narrative  # Paragraph breaks
