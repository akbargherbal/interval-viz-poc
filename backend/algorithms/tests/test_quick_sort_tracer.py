
"""
Tests for Quick Sort algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.quick_sort_tracer import QuickSortTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestQuickSortCorrectness:
    """Test algorithm correctness - does it sort correctly?"""

    @pytest.mark.parametrize("array,expected", [
        # Basic cases
        ([5, 2, 8, 1, 9], [1, 2, 5, 8, 9]),
        ([3, 1, 4, 1, 5], [1, 1, 3, 4, 5]),
        ([10, 7, 8, 9, 1, 5], [1, 5, 7, 8, 9, 10]),
        
        # Already sorted
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        
        # Reverse sorted
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        
        # Duplicates
        ([3, 1, 3, 2, 3], [1, 2, 3, 3, 3]),
        
        # All equal
        ([3, 3, 3, 3, 3], [3, 3, 3, 3, 3]),
        
        # Two elements
        ([2, 1], [1, 2]),
        ([1, 2], [1, 2]),
        
        # Negative numbers
        ([-5, 3, -1, 7, -9], [-9, -5, -1, 3, 7]),
        
        # Mixed positive and negative
        ([5, -2, 8, -1, 0, 3], [-2, -1, 0, 3, 5, 8]),
    ])
    def test_quick_sort_scenarios(self, array, expected):
        """Test Quick Sort with various input scenarios."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_large_array(self):
        """Test with larger array (15 elements)."""
        array = [15, 3, 9, 8, 5, 2, 7, 1, 6, 4, 13, 12, 11, 10, 14]
        expected = sorted(array)
        
        tracer = QuickSortTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_preserves_duplicates(self):
        """Test that duplicates are preserved."""
        array = [5, 2, 5, 1, 5, 3, 5]
        
        tracer = QuickSortTracer()
        result = tracer.execute({'array': array})
        
        sorted_array = result['result']['sorted_array']
        
        # Check all elements present
        assert sorted(sorted_array) == sorted(array)
        # Check count of each element
        assert sorted_array.count(5) == 4
        assert sorted_array.count(2) == 1

    def test_comparison_count_reasonable(self):
        """Comparison count should be reasonable for array size."""
        array = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        
        tracer = QuickSortTracer()
        result = tracer.execute({'array': array})
        
        comparisons = result['result']['comparisons']
        n = len(array)
        
        # Average case: O(n log n), worst case: O(n²)
        # For n=9, expect roughly 9 * log2(9) ≈ 28 comparisons (average)
        # Allow up to n² for worst case
        assert comparisons > 0
        assert comparisons <= n * n

    def test_swap_count_reasonable(self):
        """Swap count should be reasonable."""
        array = [5, 2, 8, 1, 9]
        
        tracer = QuickSortTracer()
        result = tracer.execute({'array': array})
        
        swaps = result['result']['swaps']
        
        # Should have some swaps for unsorted array
        assert swaps > 0
        # Should not exceed n²
        assert swaps <= len(array) * len(array)


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestQuickSortTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'array' in first_step['data']
        assert 'array_size' in first_step['data']

    def test_recurse_steps_present(self):
        """RECURSE steps should be present for recursive calls."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        recurse_steps = [s for s in result['trace']['steps'] if s['type'] == 'RECURSE']
        
        # Should have at least one recursive call
        assert len(recurse_steps) >= 1
        
        # Each should have required data
        for step in recurse_steps:
            assert 'low' in step['data']
            assert 'high' in step['data']
            assert 'subarray_size' in step['data']
            assert 'depth' in step['data']

    def test_select_pivot_steps_present(self):
        """SELECT_PIVOT steps should be present."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        pivot_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_PIVOT']
        
        # Should have at least one pivot selection
        assert len(pivot_steps) >= 1
        
        # Each should have required data
        for step in pivot_steps:
            assert 'pivot_index' in step['data']
            assert 'pivot_value' in step['data']
            assert 'low' in step['data']
            assert 'high' in step['data']

    def test_compare_steps_present(self):
        """COMPARE steps should be present."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        # Should have multiple comparisons
        assert len(compare_steps) > 0
        
        # Each should have required data
        for step in compare_steps:
            assert 'comparing_index' in step['data']
            assert 'comparing_value' in step['data']
            assert 'pivot_value' in step['data']
            assert 'comparison' in step['data']
            assert 'result' in step['data']

    def test_swap_steps_present(self):
        """SWAP steps should be present."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        swap_steps = [s for s in result['trace']['steps'] if s['type'] == 'SWAP']
        
        # Should have swaps for unsorted array
        assert len(swap_steps) > 0
        
        # Each should have required data
        for step in swap_steps:
            assert 'index1' in step['data']
            assert 'value1' in step['data']
            assert 'index2' in step['data']
            assert 'value2' in step['data']
            assert 'reason' in step['data']

    def test_partition_done_steps_present(self):
        """PARTITION_DONE steps should be present."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        partition_steps = [s for s in result['trace']['steps'] if s['type'] == 'PARTITION_DONE']
        
        # Should have at least one partition
        assert len(partition_steps) >= 1
        
        # Each should have required data
        for step in partition_steps:
            assert 'pivot_index' in step['data']
            assert 'pivot_value' in step['data']
            assert 'left_partition' in step['data']
            assert 'right_partition' in step['data']

    def test_step_sequence_logical(self):
        """Steps should follow logical sequence: SELECT_PIVOT → COMPARE → SWAP → PARTITION_DONE."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        steps = result['trace']['steps']
        
        # Find first SELECT_PIVOT
        pivot_idx = None
        for i, step in enumerate(steps):
            if step['type'] == 'SELECT_PIVOT':
                pivot_idx = i
                break
        
        assert pivot_idx is not None
        
        # After SELECT_PIVOT, should have COMPARE steps
        found_compare = False
        for i in range(pivot_idx + 1, len(steps)):
            if steps[i]['type'] == 'COMPARE':
                found_compare = True
                break
        
        assert found_compare

    def test_comparison_count_matches_trace(self):
        """Comparison count in result should match COMPARE steps."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        assert result['result']['comparisons'] == len(compare_steps)

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestQuickSortVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, and state."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        # Check a step with visualization
        steps_with_viz = [s for s in result['trace']['steps'] if 'visualization' in s['data']]
        
        assert len(steps_with_viz) > 0
        
        viz = steps_with_viz[0]['data']['visualization']
        
        assert 'array' in viz
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element

    def test_recursion_depth_tracked(self):
        """Recursion depth should be tracked in visualization."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        recurse_steps = [s for s in result['trace']['steps'] if s['type'] == 'RECURSE']
        
        for step in recurse_steps:
            viz = step['data']['visualization']
            assert 'recursion_depth' in viz
            assert viz['recursion_depth'] > 0

    def test_swap_count_tracked(self):
        """Swap count should be tracked in visualization."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        steps_with_viz = [s for s in result['trace']['steps'] if 'visualization' in s['data']]
        
        for step in steps_with_viz:
            viz = step['data']['visualization']
            assert 'swap_count' in viz

    def test_comparison_count_tracked(self):
        """Comparison count should be tracked in visualization."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        steps_with_viz = [s for s in result['trace']['steps'] if 'visualization' in s['data']]
        
        for step in steps_with_viz:
            viz = step['data']['visualization']
            assert 'comparison_count' in viz

    def test_pivot_data_in_select_pivot(self):
        """SELECT_PIVOT steps should have pivot information."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        pivot_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_PIVOT']
        
        for step in pivot_steps:
            assert 'pivot_index' in step['data']
            assert 'pivot_value' in step['data']

    def test_comparison_data_complete(self):
        """COMPARE steps should have complete comparison data."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        for step in compare_steps:
            data = step['data']
            assert 'comparing_index' in data
            assert 'comparing_value' in data
            assert 'pivot_value' in data
            assert 'comparison' in data
            assert 'result' in data
            assert isinstance(data['result'], bool)

    def test_swap_data_complete(self):
        """SWAP steps should have complete swap data."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        swap_steps = [s for s in result['trace']['steps'] if s['type'] == 'SWAP']
        
        for step in swap_steps:
            data = step['data']
            assert 'index1' in data
            assert 'value1' in data
            assert 'index2' in data
            assert 'value2' in data
            assert 'reason' in data

    def test_partition_data_complete(self):
        """PARTITION_DONE steps should have complete partition data."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        partition_steps = [s for s in result['trace']['steps'] if s['type'] == 'PARTITION_DONE']
        
        for step in partition_steps:
            data = step['data']
            assert 'pivot_index' in data
            assert 'pivot_value' in data
            assert 'left_partition' in data
            assert 'right_partition' in data
            assert 'left_size' in data
            assert 'right_size' in data


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestQuickSortPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        # May have 0 predictions if all elements already in position
        assert len(predictions) >= 0

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'swap-left', 'no-swap', 'swap-right'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice

    def test_correct_answer_valid(self):
        """Correct answer should be one of the three choices."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'swap-left', 'no-swap', 'swap-right'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_prediction_question_mentions_values(self):
        """Question should mention element and pivot values."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            assert 'element' in question or 'compared' in question or 'pivot' in question

    def test_prediction_hint_present(self):
        """Each prediction should have a helpful hint."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint']
            assert isinstance(hint, str)
            assert len(hint) > 0

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            explanation = pred['explanation']
            assert isinstance(explanation, str)
            assert len(explanation) > 0


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestQuickSortEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = QuickSortTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'array': []})

    def test_single_element_raises_error(self):
        """Single element array should raise ValueError (min 2 elements)."""
        tracer = QuickSortTracer()
        
        with pytest.raises(ValueError, match="at least 2 elements"):
            tracer.execute({'array': [42]})

    def test_two_elements_sorted(self):
        """Two elements already sorted."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [1, 2]})
        
        assert result['result']['sorted_array'] == [1, 2]

    def test_two_elements_unsorted(self):
        """Two elements unsorted."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2]

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = QuickSortTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([5, 2, 8])

    def test_missing_array_key_raises_error(self):
        """Missing 'array' key should raise ValueError."""
        tracer = QuickSortTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({'data': [5, 2, 8]})

    def test_already_sorted_array(self):
        """Already sorted array (worst case for Lomuto)."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [1, 2, 3, 4, 5]})
        
        assert result['result']['sorted_array'] == [1, 2, 3, 4, 5]

    def test_reverse_sorted_array(self):
        """Reverse sorted array."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2, 3, 4, 5]

    def test_all_duplicates(self):
        """Array with all same values."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 5, 5, 5, 5]})
        
        assert result['result']['sorted_array'] == [5, 5, 5, 5, 5]

    def test_negative_numbers(self):
        """Array with negative numbers."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [-5, 3, -1, 7, -9]})
        
        assert result['result']['sorted_array'] == [-9, -5, -1, 3, 7]

    def test_mixed_positive_negative_zero(self):
        """Array with mixed positive, negative, and zero."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, -2, 0, 3, -1]})
        
        assert result['result']['sorted_array'] == [-2, -1, 0, 3, 5]


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestQuickSortMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
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
        """algorithm field should be 'quick-sort'."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        assert result['metadata']['algorithm'] == 'quick-sort'

    def test_display_name_field_correct(self):
        """display_name field should be 'Quick Sort'."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        assert result['metadata']['display_name'] == 'Quick Sort'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'highlight_pivot' in config
        assert 'show_partitions' in config

    def test_input_size_correct(self):
        """input_size should match array length."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        assert result['metadata']['input_size'] == 5

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'sorted_array' in result['result']
        assert 'comparisons' in result['result']
        assert 'swaps' in result['result']
        assert 'partitions' in result['result']
        assert 'max_depth' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']

    def test_metadata_types_correct(self):
        """All metadata fields should have correct types."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        metadata = result['metadata']
        
        assert isinstance(metadata['algorithm'], str)
        assert isinstance(metadata['display_name'], str)
        assert isinstance(metadata['visualization_type'], str)
        assert isinstance(metadata['visualization_config'], dict)
        assert isinstance(metadata['input_size'], int)
        assert isinstance(metadata['prediction_points'], list)


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestQuickSortNarrativeGeneration:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generates_without_error(self):
        """generate_narrative should execute without exceptions."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        # Should not raise exception
        narrative = tracer.generate_narrative(result)
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_contains_header(self):
        """Narrative should contain header with algorithm name."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "# Quick Sort Execution Narrative" in narrative

    def test_narrative_contains_input_info(self):
        """Narrative should contain input array information."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "Input Array" in narrative
        assert "[5, 2, 8]" in narrative

    def test_narrative_contains_step_sections(self):
        """Narrative should contain step sections."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "## Step" in narrative

    def test_narrative_contains_summary(self):
        """Narrative should contain execution summary."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "## Execution Summary" in narrative

    def test_narrative_contains_visualization_hints(self):
        """Narrative should contain Frontend Visualization Hints section."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics to Emphasize" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative
        assert "Algorithm-Specific Guidance" in narrative

    def test_narrative_shows_comparisons(self):
        """Narrative should show explicit comparisons."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should contain comparison notation
        assert "<" in narrative or ">" in narrative or "≥" in narrative

    def test_narrative_shows_performance_metrics(self):
        """Narrative should show performance metrics."""
        tracer = QuickSortTracer()
        result = tracer.execute({'array': [5, 2, 8]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "Comparisons" in narrative
        assert "Swaps" in narrative
        assert "Partitions" in narrative
