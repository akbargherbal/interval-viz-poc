
"""
Tests for Bubble Sort algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.bubble_sort_tracer import BubbleSortTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestBubbleSortCorrectness:
    """Test algorithm correctness - does it sort correctly?"""

    @pytest.mark.parametrize("input_array,expected_sorted", [
        # Basic cases
        ([5, 2, 8, 1, 9], [1, 2, 5, 8, 9]),
        ([3, 1, 4, 1, 5], [1, 1, 3, 4, 5]),
        ([2, 1], [1, 2]),
        ([1, 2], [1, 2]),  # Already sorted
        
        # Edge cases
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),  # Reverse sorted
        ([1, 1, 1, 1], [1, 1, 1, 1]),  # All same
        ([42, 17], [17, 42]),  # Two elements
        
        # Larger arrays
        ([9, 7, 5, 3, 1, 2, 4, 6, 8], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        
        # With duplicates
        ([5, 2, 8, 2, 9, 5], [2, 2, 5, 5, 8, 9]),
        ([3, 3, 1, 1, 2, 2], [1, 1, 2, 2, 3, 3]),
        
        # Negative numbers
        ([-5, -2, -8, -1], [-8, -5, -2, -1]),
        ([-3, 0, 3, -1, 1], [-3, -1, 0, 1, 3]),
    ])
    def test_bubble_sort_scenarios(self, input_array, expected_sorted):
        """Test bubble sort with various input scenarios."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': input_array})
        
        assert result['result']['sorted_array'] == expected_sorted

    def test_original_array_preserved(self):
        """Original array should be preserved in result."""
        original = [5, 2, 8, 1, 9]
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': original})
        
        assert result['result']['original_array'] == original
        # Verify original wasn't modified
        assert original == [5, 2, 8, 1, 9]

    def test_already_sorted_minimal_work(self):
        """Already sorted array should terminate early with 0 swaps."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [1, 2, 3, 4, 5]})
        
        assert result['result']['sorted_array'] == [1, 2, 3, 4, 5]
        assert result['result']['swaps'] == 0
        assert result['result']['passes'] == 1  # Only one pass needed

    def test_reverse_sorted_maximum_work(self):
        """Reverse sorted array should require maximum swaps."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2, 3, 4, 5]
        # For n=5 reverse sorted: 4+3+2+1 = 10 swaps
        assert result['result']['swaps'] == 10

    def test_comparison_count_reasonable(self):
        """Comparison count should be O(n²) worst case."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        n = 5
        # Worst case: n*(n-1)/2 comparisons
        max_comparisons = n * (n - 1) // 2
        assert result['result']['comparisons'] <= max_comparisons


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestBubbleSortTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'array' in first_step['data']
        assert 'array_size' in first_step['data']

    def test_compare_steps_present(self):
        """COMPARE steps should be present for each comparison."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        # Should have at least one COMPARE step
        assert len(compare_steps) >= 1
        
        # Each should have required data
        for step in compare_steps:
            assert 'index_i' in step['data']
            assert 'index_j' in step['data']
            assert 'value_i' in step['data']
            assert 'value_j' in step['data']
            assert 'comparison' in step['data']

    def test_swap_or_no_swap_follows_compare(self):
        """SWAP or NO_SWAP should follow each COMPARE."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        steps = result['trace']['steps']
        
        for i, step in enumerate(steps):
            if step['type'] == 'COMPARE' and i + 1 < len(steps):
                next_step = steps[i + 1]
                assert next_step['type'] in ['SWAP', 'NO_SWAP']

    def test_swap_step_structure(self):
        """SWAP steps should have correct structure."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        swap_steps = [s for s in result['trace']['steps'] if s['type'] == 'SWAP']
        
        # Should have at least one swap for this input
        assert len(swap_steps) >= 1
        
        for step in swap_steps:
            assert 'index_i' in step['data']
            assert 'index_j' in step['data']
            assert 'value_i' in step['data']
            assert 'value_j' in step['data']

    def test_no_swap_step_structure(self):
        """NO_SWAP steps should have correct structure."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [1, 2, 3]})  # Already sorted
        
        no_swap_steps = [s for s in result['trace']['steps'] if s['type'] == 'NO_SWAP']
        
        # Should have NO_SWAP steps for already sorted array
        assert len(no_swap_steps) >= 1
        
        for step in no_swap_steps:
            assert 'index_i' in step['data']
            assert 'index_j' in step['data']
            assert 'value_i' in step['data']
            assert 'value_j' in step['data']

    def test_pass_complete_steps(self):
        """PASS_COMPLETE steps should be present."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        pass_complete_steps = [s for s in result['trace']['steps'] if s['type'] == 'PASS_COMPLETE']
        
        # Should have at least one pass complete
        assert len(pass_complete_steps) >= 1
        
        for step in pass_complete_steps:
            assert 'pass_number' in step['data']
            assert 'sorted_boundary' in step['data']
            assert 'swaps_in_pass' in step['data']

    def test_pass_numbers_sequential(self):
        """Pass numbers should be sequential starting from 1."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        pass_complete_steps = [s for s in result['trace']['steps'] if s['type'] == 'PASS_COMPLETE']
        
        for i, step in enumerate(pass_complete_steps):
            assert step['data']['pass_number'] == i + 1

    def test_sorted_boundary_decreases(self):
        """Sorted boundary should decrease with each pass."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        pass_complete_steps = [s for s in result['trace']['steps'] if s['type'] == 'PASS_COMPLETE']
        
        previous_boundary = None
        for step in pass_complete_steps:
            boundary = step['data']['sorted_boundary']
            
            if previous_boundary is not None:
                assert boundary < previous_boundary
            
            previous_boundary = boundary

    def test_comparison_count_matches_compare_steps(self):
        """Comparison count should match number of COMPARE steps."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        comparisons = result['result']['comparisons']
        compare_count = len([s for s in result['trace']['steps'] if s['type'] == 'COMPARE'])
        
        assert comparisons == compare_count

    def test_swap_count_matches_swap_steps(self):
        """Swap count should match number of SWAP steps."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        swaps = result['result']['swaps']
        swap_count = len([s for s in result['trace']['steps'] if s['type'] == 'SWAP'])
        
        assert swaps == swap_count

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestBubbleSortVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step (except INITIAL_STATE) should have visualization data."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, and state."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check a COMPARE step
        compare_step = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE'][0]
        viz = compare_step['data']['visualization']
        
        assert 'array' in viz
        assert len(viz['array']) == 3
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element

    def test_element_states_valid(self):
        """Element states should be one of: unsorted, comparing, sorted."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        valid_states = {'unsorted', 'comparing', 'sorted'}
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for element in viz['array']:
                    assert element['state'] in valid_states

    def test_comparing_state_at_indices(self):
        """Elements at comparing_indices should have 'comparing' state."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check COMPARE steps
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        for step in compare_steps:
            viz = step['data']['visualization']
            comparing_indices = viz['comparing_indices']
            
            if comparing_indices is not None:
                i, j = comparing_indices
                assert viz['array'][i]['state'] == 'comparing'
                assert viz['array'][j]['state'] == 'comparing'

    def test_sorted_state_after_boundary(self):
        """Elements at or after sorted_boundary should have 'sorted' state."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check PASS_COMPLETE steps
        pass_steps = [s for s in result['trace']['steps'] if s['type'] == 'PASS_COMPLETE']
        
        for step in pass_steps:
            viz = step['data']['visualization']
            boundary = viz['sorted_boundary']
            
            for element in viz['array']:
                if element['index'] >= boundary:
                    assert element['state'] == 'sorted'

    def test_unsorted_state_before_boundary(self):
        """Elements before sorted_boundary (not comparing) should have 'unsorted' state."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        # Check a PASS_COMPLETE step
        pass_steps = [s for s in result['trace']['steps'] if s['type'] == 'PASS_COMPLETE']
        
        if pass_steps:
            step = pass_steps[0]
            viz = step['data']['visualization']
            boundary = viz['sorted_boundary']
            
            for element in viz['array']:
                if element['index'] < boundary:
                    assert element['state'] == 'unsorted'

    def test_comparing_indices_present(self):
        """comparing_indices should be present in visualization."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        for step in compare_steps:
            viz = step['data']['visualization']
            assert 'comparing_indices' in viz

    def test_sorted_boundary_present(self):
        """sorted_boundary should be present in visualization."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'sorted_boundary' in viz

    def test_current_pass_present(self):
        """current_pass should be present in visualization."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'current_pass' in viz

    def test_running_totals_present(self):
        """Running totals (comparisons, swaps) should be present."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'comparisons' in viz
                assert 'swaps' in viz

    def test_running_totals_increase(self):
        """Running totals should increase or stay same (never decrease)."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        prev_comparisons = 0
        prev_swaps = 0
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                
                assert viz['comparisons'] >= prev_comparisons
                assert viz['swaps'] >= prev_swaps
                
                prev_comparisons = viz['comparisons']
                prev_swaps = viz['swaps']


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestBubbleSortPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_count_matches_comparisons(self):
        """Prediction count should match number of COMPARE steps."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        compare_count = len([s for s in result['trace']['steps'] if s['type'] == 'COMPARE'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == compare_count

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 2 choices with id and label."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 2
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'swap', 'no-swap'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice
                assert isinstance(choice['label'], str)
                assert len(choice['label']) > 0

    def test_correct_answer_valid(self):
        """Correct answer should be one of the two choices."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'swap', 'no-swap'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_step(self):
        """Correct answer should match the actual next step taken."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Get next step
            next_step = steps[step_index + 1]
            
            # Verify answer matches next step type
            if correct_answer == 'swap':
                assert next_step['type'] == 'SWAP'
            elif correct_answer == 'no-swap':
                assert next_step['type'] == 'NO_SWAP'

    def test_prediction_question_mentions_values(self):
        """Question should mention the values being compared."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            # Question should mention comparison or values
            assert 'compare' in question or 'arr[' in question

    def test_prediction_hint_present(self):
        """Each prediction should have a helpful hint."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint']
            assert isinstance(hint, str)
            assert len(hint) > 0

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            explanation = pred['explanation']
            assert isinstance(explanation, str)
            assert len(explanation) > 0


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestBubbleSortEdgeCases:
    """Test edge cases and error handling."""

    def test_single_element_raises_error(self):
        """Single element array should raise ValueError."""
        tracer = BubbleSortTracer()
        
        with pytest.raises(ValueError, match="at least 2 elements"):
            tracer.execute({'array': [42]})

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = BubbleSortTracer()
        
        with pytest.raises(ValueError, match="at least 2 elements"):
            tracer.execute({'array': []})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = BubbleSortTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([3, 1, 2])

    def test_missing_array_key_raises_error(self):
        """Missing 'array' key should raise ValueError."""
        tracer = BubbleSortTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({'data': [3, 1, 2]})

    def test_non_list_array_raises_error(self):
        """Non-list array should raise ValueError."""
        tracer = BubbleSortTracer()
        
        with pytest.raises(ValueError, match="list"):
            tracer.execute({'array': "not a list"})

    def test_non_integer_elements_raise_error(self):
        """Array with non-integer elements should raise ValueError."""
        tracer = BubbleSortTracer()
        
        with pytest.raises(ValueError, match="integers"):
            tracer.execute({'array': [3, 1.5, 2]})

    def test_two_elements_sorted(self):
        """Two element array already sorted."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [1, 2]})
        
        assert result['result']['sorted_array'] == [1, 2]
        assert result['result']['swaps'] == 0

    def test_two_elements_unsorted(self):
        """Two element array needing swap."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2]
        assert result['result']['swaps'] == 1

    def test_all_same_values(self):
        """Array with all same values."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [5, 5, 5, 5]})
        
        assert result['result']['sorted_array'] == [5, 5, 5, 5]
        assert result['result']['swaps'] == 0

    def test_negative_numbers(self):
        """Array with negative numbers should work."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [-3, -1, -5, -2]})
        
        assert result['result']['sorted_array'] == [-5, -3, -2, -1]

    def test_mixed_positive_negative(self):
        """Array with mixed positive and negative numbers."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, -1, 0, -5, 2]})
        
        assert result['result']['sorted_array'] == [-5, -1, 0, 2, 3]

    def test_large_array(self):
        """Test with larger array (10 elements)."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestBubbleSortMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
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
        """algorithm field should be 'bubble-sort'."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['metadata']['algorithm'] == 'bubble-sort'

    def test_display_name_field_correct(self):
        """display_name field should be 'Bubble Sort'."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['metadata']['display_name'] == 'Bubble Sort'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'highlight_sorted_tail' in config
        assert 'state_colors' in config
        
        # Check state colors structure
        state_colors = config['state_colors']
        assert 'unsorted' in state_colors
        assert 'comparing' in state_colors
        assert 'sorted' in state_colors

    def test_input_size_correct(self):
        """input_size should match array length."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2, 5, 4]})
        
        assert result['metadata']['input_size'] == 5

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_metadata_types_correct(self):
        """All metadata fields should have correct types."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        metadata = result['metadata']
        
        assert isinstance(metadata['algorithm'], str)
        assert isinstance(metadata['display_name'], str)
        assert isinstance(metadata['visualization_type'], str)
        assert isinstance(metadata['visualization_config'], dict)
        assert isinstance(metadata['input_size'], int)
        assert isinstance(metadata['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'sorted_array' in result['result']
        assert 'original_array' in result['result']
        assert 'comparisons' in result['result']
        assert 'swaps' in result['result']
        assert 'passes' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestBubbleSortNarrativeGeneration:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generation_executes(self):
        """generate_narrative should execute without errors."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Should not raise exception
        narrative = tracer.generate_narrative(result)
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_has_header(self):
        """Narrative should have a header section."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        narrative = tracer.generate_narrative(result)
        
        assert "# Bubble Sort Execution Narrative" in narrative
        assert "**Algorithm:**" in narrative
        assert "**Input Array:**" in narrative

    def test_narrative_has_steps(self):
        """Narrative should include step-by-step sections."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        narrative = tracer.generate_narrative(result)
        
        assert "## Step 0:" in narrative
        assert "## Step" in narrative

    def test_narrative_has_summary(self):
        """Narrative should have an execution summary."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        narrative = tracer.generate_narrative(result)
        
        assert "## Execution Summary" in narrative
        assert "**Final Result:**" in narrative

    def test_narrative_has_visualization_hints(self):
        """Narrative should include Frontend Visualization Hints section."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        narrative = tracer.generate_narrative(result)
        
        assert "## 🎨 Frontend Visualization Hints" in narrative
        assert "### Primary Metrics to Emphasize" in narrative
        assert "### Visualization Priorities" in narrative
        assert "### Key JSON Paths" in narrative
        assert "### Algorithm-Specific Guidance" in narrative

    def test_narrative_shows_comparisons(self):
        """Narrative should show explicit comparisons."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        narrative = tracer.generate_narrative(result)
        
        # Should show comparison logic
        assert "Compare" in narrative or "compare" in narrative

    def test_narrative_shows_swaps(self):
        """Narrative should describe swap operations."""
        tracer = BubbleSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        narrative = tracer.generate_narrative(result)
        
        # Should mention swaps
        assert "Swap" in narrative or "swap" in narrative
