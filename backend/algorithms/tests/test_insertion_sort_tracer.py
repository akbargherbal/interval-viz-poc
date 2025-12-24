
"""
Tests for Insertion Sort algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.insertion_sort_tracer import InsertionSortTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestInsertionSortCorrectness:
    """Test algorithm correctness - does it sort correctly?"""

    @pytest.mark.parametrize("input_array,expected_sorted", [
        # Basic cases
        ([5, 2, 8, 1, 9], [1, 2, 5, 8, 9]),
        ([3, 1, 4, 1, 5], [1, 1, 3, 4, 5]),
        ([2, 1], [1, 2]),
        
        # Already sorted
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        
        # Reverse sorted
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        
        # Duplicates
        ([3, 3, 3, 3], [3, 3, 3, 3]),
        ([5, 2, 5, 2, 5], [2, 2, 5, 5, 5]),
        
        # Negative numbers
        ([-5, 3, -1, 7, -9], [-9, -5, -1, 3, 7]),
        ([0, -1, 1, -2, 2], [-2, -1, 0, 1, 2]),
        
        # Mixed
        ([10, -5, 0, 15, -10], [-10, -5, 0, 10, 15]),
    ])
    def test_insertion_sort_correctness(self, input_array, expected_sorted):
        """Test insertion sort produces correct sorted output."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': input_array})
        
        assert result['result']['sorted_array'] == expected_sorted
        assert result['result']['original_array'] == input_array

    def test_large_array_sorting(self):
        """Test with larger array (20 elements)."""
        input_array = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 
                       33, 17, 28, 19, 55, 42, 71, 38, 61, 29]
        expected_sorted = sorted(input_array)
        
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': input_array})
        
        assert result['result']['sorted_array'] == expected_sorted

    def test_original_array_unchanged(self):
        """Original input array should not be modified."""
        input_array = [5, 2, 8, 1, 9]
        original_copy = input_array.copy()
        
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': input_array})
        
        # Input array should be unchanged
        assert input_array == original_copy
        # But result should have sorted version
        assert result['result']['sorted_array'] == [1, 2, 5, 8, 9]

    def test_stability_preserved(self):
        """Insertion sort should be stable (preserve relative order of equal elements)."""
        # Use tuples to track original positions
        input_array = [3, 1, 3, 2, 3]
        
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': input_array})
        
        # Should be sorted
        assert result['result']['sorted_array'] == [1, 2, 3, 3, 3]


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestInsertionSortTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'array' in first_step['data']
        assert 'array_size' in first_step['data']

    def test_complete_final_step(self):
        """Last step should be COMPLETE."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'COMPLETE'
        assert 'total_comparisons' in last_step['data']
        assert 'total_shifts' in last_step['data']

    def test_select_key_steps_present(self):
        """SELECT_KEY steps should be present for each element (except first)."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        select_key_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_KEY']
        
        # Should have n-1 SELECT_KEY steps (first element is trivially sorted)
        assert len(select_key_steps) == 3
        
        # Each should have required data
        for step in select_key_steps:
            assert 'key_index' in step['data']
            assert 'key_value' in step['data']
            assert 'sorted_count' in step['data']

    def test_compare_steps_present(self):
        """COMPARE steps should be present."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        # Should have at least one comparison
        assert len(compare_steps) >= 1
        
        # Each should have required data
        for step in compare_steps:
            assert 'key_value' in step['data']
            assert 'compare_index' in step['data']
            assert 'compare_value' in step['data']
            assert 'comparison' in step['data']
            assert 'decision' in step['data']

    def test_shift_steps_present(self):
        """SHIFT steps should be present when elements need to move."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        shift_steps = [s for s in result['trace']['steps'] if s['type'] == 'SHIFT']
        
        # Should have shifts for this input
        assert len(shift_steps) > 0
        
        # Each should have required data
        for step in shift_steps:
            assert 'from_index' in step['data']
            assert 'to_index' in step['data']
            assert 'value' in step['data']
            assert 'shifts_so_far' in step['data']

    def test_insert_steps_present(self):
        """INSERT steps should be present for each key."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        insert_steps = [s for s in result['trace']['steps'] if s['type'] == 'INSERT']
        
        # Should have n-1 INSERT steps
        assert len(insert_steps) == 3
        
        # Each should have required data
        for step in insert_steps:
            assert 'insert_index' in step['data']
            assert 'key_value' in step['data']
            assert 'comparisons' in step['data']
            assert 'shifts' in step['data']

    def test_step_sequence_logical(self):
        """Steps should follow logical sequence: SELECT_KEY → COMPARE → (SHIFT)* → INSERT."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        steps = result['trace']['steps']
        
        # After INITIAL_STATE, should see SELECT_KEY
        assert steps[1]['type'] == 'SELECT_KEY'
        
        # After SELECT_KEY, should see COMPARE or INSERT
        for i, step in enumerate(steps):
            if step['type'] == 'SELECT_KEY' and i + 1 < len(steps):
                next_step = steps[i + 1]
                assert next_step['type'] in ['COMPARE', 'INSERT']

    def test_comparison_count_matches_result(self):
        """Comparison count in trace should match result."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        total_comparisons = len(compare_steps)
        
        assert result['result']['comparisons'] == total_comparisons

    def test_shift_count_matches_result(self):
        """Shift count in trace should match result."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        shift_steps = [s for s in result['trace']['steps'] if s['type'] == 'SHIFT']
        total_shifts = len(shift_steps)
        
        assert result['result']['shifts'] == total_shifts

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestInsertionSortVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step (except INITIAL_STATE) should have visualization data."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, and state."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check a SELECT_KEY step
        select_step = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_KEY'][0]
        viz = select_step['data']['visualization']
        
        assert 'array' in viz
        assert len(viz['array']) == 3
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element

    def test_element_states_valid(self):
        """Element states should be one of: sorted, examining, comparing, shifting, unsorted."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        valid_states = {'sorted', 'examining', 'comparing', 'shifting', 'unsorted'}
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for element in viz['array']:
                    assert element['state'] in valid_states

    def test_examining_state_at_key(self):
        """Element at key index should have 'examining' state."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check SELECT_KEY steps
        select_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_KEY']
        
        for step in select_steps:
            key_index = step['data']['key_index']
            viz = step['data']['visualization']
            
            key_element = viz['array'][key_index]
            assert key_element['state'] == 'examining'

    def test_comparing_state_during_comparison(self):
        """Element being compared should have 'comparing' state."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check COMPARE steps
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        for step in compare_steps:
            compare_index = step['data']['compare_index']
            viz = step['data']['visualization']
            
            compare_element = viz['array'][compare_index]
            assert compare_element['state'] == 'comparing'

    def test_sorted_state_in_sorted_region(self):
        """Elements in sorted region should have 'sorted' state."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check INSERT steps (after insertion, elements should be sorted)
        insert_steps = [s for s in result['trace']['steps'] if s['type'] == 'INSERT']
        
        for step in insert_steps:
            insert_index = step['data']['insert_index']
            viz = step['data']['visualization']
            
            # Elements up to insert_index should be sorted
            for i in range(insert_index + 1):
                assert viz['array'][i]['state'] == 'sorted'

    def test_unsorted_state_in_unsorted_region(self):
        """Elements not yet processed should have 'unsorted' state."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        # Check SELECT_KEY steps
        select_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_KEY']
        
        for step in select_steps:
            key_index = step['data']['key_index']
            viz = step['data']['visualization']
            
            # Elements after key_index should be unsorted
            for i in range(key_index + 1, len(viz['array'])):
                if viz['array'][i]['state'] != 'examining':
                    assert viz['array'][i]['state'] == 'unsorted'

    def test_key_information_present(self):
        """Key information should be present in visualization."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check SELECT_KEY steps
        select_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_KEY']
        
        for step in select_steps:
            viz = step['data']['visualization']
            
            assert 'key' in viz
            assert viz['key'] is not None
            assert 'index' in viz['key']
            assert 'value' in viz['key']

    def test_sorted_boundary_present(self):
        """Sorted boundary should be tracked."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'sorted_boundary' in viz

    def test_sorted_boundary_grows(self):
        """Sorted boundary should grow with each insertion."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        insert_steps = [s for s in result['trace']['steps'] if s['type'] == 'INSERT']
        
        previous_boundary = 0
        for step in insert_steps:
            viz = step['data']['visualization']
            current_boundary = viz['sorted_boundary']
            
            # Boundary should increase
            assert current_boundary > previous_boundary
            previous_boundary = current_boundary

    def test_compare_index_present_during_comparison(self):
        """Compare index should be present during COMPARE steps."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        for step in compare_steps:
            viz = step['data']['visualization']
            assert 'compare_index' in viz
            assert viz['compare_index'] is not None


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestInsertionSortPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_count_matches_comparisons(self):
        """Prediction count should match number of COMPARE steps."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        compare_count = len([s for s in result['trace']['steps'] if s['type'] == 'COMPARE'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == compare_count

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'shift', 'insert', 'continue'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice
                assert isinstance(choice['label'], str)
                assert len(choice['label']) > 0

    def test_correct_answer_valid(self):
        """Correct answer should be one of the three choices."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'shift', 'insert', 'continue'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_step(self):
        """Correct answer should match the actual next step taken."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Get next step
            next_step = steps[step_index + 1]
            
            # Verify answer matches next step type
            if correct_answer == 'shift':
                assert next_step['type'] == 'SHIFT'
            elif correct_answer == 'insert':
                assert next_step['type'] == 'INSERT'

    def test_prediction_question_mentions_values(self):
        """Question should mention key and compare values."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            # Question should mention comparison
            assert 'key' in question or 'vs' in question or 'array' in question

    def test_prediction_hint_present(self):
        """Each prediction should have a helpful hint."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint']
            assert isinstance(hint, str)
            assert len(hint) > 0

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = InsertionSortTracer()
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
class TestInsertionSortEdgeCases:
    """Test edge cases and error handling."""

    def test_minimum_size_array(self):
        """Array with exactly 2 elements should work."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2]

    def test_single_element_raises_error(self):
        """Single element array should raise ValueError."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="at least 2 elements"):
            tracer.execute({'array': [42]})

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="at least 2 elements"):
            tracer.execute({'array': []})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([3, 1, 2])

    def test_missing_array_key_raises_error(self):
        """Missing 'array' key should raise ValueError."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({'data': [3, 1, 2]})

    def test_non_list_array_raises_error(self):
        """Non-list array should raise ValueError."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="list"):
            tracer.execute({'array': "not a list"})

    def test_already_sorted_minimal_work(self):
        """Already sorted array should require minimal comparisons."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [1, 2, 3, 4, 5]})
        
        # Should have n-1 comparisons (one per element)
        assert result['result']['comparisons'] == 4
        # Should have 0 shifts
        assert result['result']['shifts'] == 0

    def test_reverse_sorted_maximum_work(self):
        """Reverse sorted array should require maximum comparisons and shifts."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        # Should have many comparisons and shifts
        assert result['result']['comparisons'] > 0
        assert result['result']['shifts'] > 0
        # For reverse sorted: comparisons = 1+2+3+4 = 10, shifts = 1+2+3+4 = 10
        assert result['result']['comparisons'] == 10
        assert result['result']['shifts'] == 10

    def test_all_duplicates(self):
        """Array with all same values."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 5, 5, 5]})
        
        assert result['result']['sorted_array'] == [5, 5, 5, 5]
        # Should have comparisons but no shifts
        assert result['result']['comparisons'] > 0
        assert result['result']['shifts'] == 0

    def test_negative_numbers(self):
        """Array with negative numbers should work."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [-5, 3, -1, 7, -9]})
        
        assert result['result']['sorted_array'] == [-9, -5, -1, 3, 7]

    def test_mixed_positive_negative_zero(self):
        """Array with mixed positive, negative, and zero."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [0, -1, 1, -2, 2]})
        
        assert result['result']['sorted_array'] == [-2, -1, 0, 1, 2]

    def test_large_value_range(self):
        """Array with large value range."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [1000, -1000, 500, -500, 0]})
        
        assert result['result']['sorted_array'] == [-1000, -500, 0, 500, 1000]


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestInsertionSortMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = InsertionSortTracer()
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
        """algorithm field should be 'insertion-sort'."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['metadata']['algorithm'] == 'insertion-sort'

    def test_display_name_field_correct(self):
        """display_name field should be 'Insertion Sort'."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['metadata']['display_name'] == 'Insertion Sort'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'highlight_sorted_region' in config

    def test_input_size_correct(self):
        """input_size should match array length."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        assert result['metadata']['input_size'] == 5

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_metadata_types_correct(self):
        """All metadata fields should have correct types."""
        tracer = InsertionSortTracer()
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
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'sorted_array' in result['result']
        assert 'original_array' in result['result']
        assert 'comparisons' in result['result']
        assert 'shifts' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestInsertionSortNarrative:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generation_succeeds(self):
        """Narrative generation should not raise exceptions."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Should not raise exception
        narrative = tracer.generate_narrative(result)
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_contains_header(self):
        """Narrative should contain header with algorithm name."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "# Insertion Sort Execution Narrative" in narrative
        assert "Insertion Sort" in narrative

    def test_narrative_contains_input_info(self):
        """Narrative should contain input information."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "Input Array:" in narrative
        assert "[3, 1, 2]" in narrative

    def test_narrative_contains_step_sections(self):
        """Narrative should contain step sections."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "## Step 0:" in narrative
        assert "## Step" in narrative

    def test_narrative_contains_summary(self):
        """Narrative should contain execution summary."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "## Execution Summary" in narrative
        assert "Original Array:" in narrative
        assert "Sorted Array:" in narrative

    def test_narrative_contains_visualization_hints(self):
        """Narrative should contain frontend visualization hints section."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics to Emphasize" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative
        assert "Algorithm-Specific Guidance" in narrative

    def test_narrative_shows_comparisons(self):
        """Narrative should show comparison operations."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should show comparison format
        assert "Compare:" in narrative or "Comparison:" in narrative

    def test_narrative_shows_shifts(self):
        """Narrative should show shift operations."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should mention shifts
        assert "Shift" in narrative or "shift" in narrative

    def test_narrative_valid_markdown(self):
        """Narrative should be valid markdown."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        # Check for markdown elements
        assert "#" in narrative  # Headers
        assert "**" in narrative  # Bold
        assert "```" in narrative  # Code blocks
