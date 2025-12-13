"""
Tests for Binary Search algorithm tracer.

Session 28: Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.binary_search import BinarySearchTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestBinarySearchCorrectness:
    """Test algorithm correctness - does it find the right answer?"""

    @pytest.mark.parametrize("array,target,expected_found,expected_index", [
        # Target found - various positions
        ([1, 3, 5, 7, 9], 5, True, 2),           # Middle
        ([1, 3, 5, 7, 9], 1, True, 0),           # First element
        ([1, 3, 5, 7, 9], 9, True, 4),           # Last element
        ([1, 3, 5, 7, 9], 3, True, 1),           # Second element
        ([1, 3, 5, 7, 9], 7, True, 3),           # Fourth element
        ([42], 42, True, 0),                      # Single element found
        ([1, 3], 1, True, 0),                     # Two elements - first
        ([1, 3], 3, True, 1),                     # Two elements - last
        
        # Target not found - various scenarios
        ([1, 3, 5, 7, 9], 4, False, None),       # Between elements
        ([1, 3, 5, 7, 9], 0, False, None),       # Before first
        ([1, 3, 5, 7, 9], 10, False, None),      # After last
        ([1, 3, 5, 7, 9], 2, False, None),       # Between first two
        ([42], 99, False, None),                  # Single element miss
        ([1, 3], 2, False, None),                 # Two elements - between
        ([1, 3], 0, False, None),                 # Two elements - before
        ([1, 3], 4, False, None),                 # Two elements - after
    ])
    def test_binary_search_scenarios(self, array, target, expected_found, expected_index):
        """Test binary search with various input scenarios."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        assert result['result']['found'] == expected_found
        assert result['result']['index'] == expected_index

    def test_large_array_found(self):
        """Test with large array (100 elements) - target found."""
        array = list(range(0, 200, 2))  # [0, 2, 4, ..., 198]
        target = 100
        
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        assert result['result']['found'] is True
        assert result['result']['index'] == 50
        assert array[result['result']['index']] == target

    def test_large_array_not_found(self):
        """Test with large array (100 elements) - target not found."""
        array = list(range(0, 200, 2))  # [0, 2, 4, ..., 198]
        target = 99  # Odd number not in array
        
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        assert result['result']['found'] is False
        assert result['result']['index'] is None

    def test_array_with_duplicates(self):
        """Test with array containing duplicate values (still sorted)."""
        array = [1, 2, 2, 2, 3, 4, 5]
        target = 2
        
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        # Should find ONE of the 2's (any valid index is acceptable)
        assert result['result']['found'] is True
        assert array[result['result']['index']] == target

    def test_comparison_count_reasonable(self):
        """Comparison count should be O(log n)."""
        array = list(range(1, 101, 2))  # 50 elements
        target = 51
        
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        comparisons = result['result']['comparisons']
        
        # For 50 elements, log2(50) ≈ 5.6, so max ~6-7 comparisons
        assert comparisons <= 7


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestBinarySearchTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'target' in first_step['data']
        assert 'array_size' in first_step['data']

    def test_target_found_final_step(self):
        """When target found, last step should be TARGET_FOUND."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'TARGET_FOUND'
        assert last_step['data']['index'] == 2
        assert last_step['data']['value'] == 5

    def test_target_not_found_final_step(self):
        """When target not found, last step should be TARGET_NOT_FOUND."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 4})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'TARGET_NOT_FOUND'
        assert last_step['data']['final_state'] == 'search_space_empty'

    def test_calculate_mid_steps_present(self):
        """CALCULATE_MID steps should be present for each iteration."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 7})
        
        calc_mid_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        # Should have at least one CALCULATE_MID step
        assert len(calc_mid_steps) >= 1
        
        # Each should have required data
        for step in calc_mid_steps:
            assert 'mid_index' in step['data']
            assert 'mid_value' in step['data']
            assert 'left' in step['data']
            assert 'right' in step['data']
            assert 'calculation' in step['data']

    def test_search_direction_steps(self):
        """SEARCH_LEFT or SEARCH_RIGHT should follow CALCULATE_MID (when not found)."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9, 11, 13, 15], 'target': 13})
        
        steps = result['trace']['steps']
        
        for i, step in enumerate(steps):
            if step['type'] == 'CALCULATE_MID' and i + 1 < len(steps):
                next_step = steps[i + 1]
                # Next step should be a decision
                assert next_step['type'] in ['TARGET_FOUND', 'SEARCH_LEFT', 'SEARCH_RIGHT']

    def test_search_left_updates_pointers(self):
        """SEARCH_LEFT step should update right pointer."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 3})
        
        search_left_steps = [s for s in result['trace']['steps'] if s['type'] == 'SEARCH_LEFT']
        
        # There should be at least one SEARCH_LEFT for this case
        if search_left_steps:
            step = search_left_steps[0]
            assert 'old_right' in step['data']
            assert 'new_right' in step['data']
            assert step['data']['new_right'] < step['data']['old_right']

    def test_search_right_updates_pointers(self):
        """SEARCH_RIGHT step should update left pointer."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 7})
        
        search_right_steps = [s for s in result['trace']['steps'] if s['type'] == 'SEARCH_RIGHT']
        
        # There should be at least one SEARCH_RIGHT for this case
        if search_right_steps:
            step = search_right_steps[0]
            assert 'old_left' in step['data']
            assert 'new_left' in step['data']
            assert step['data']['new_left'] > step['data']['old_left']

    def test_comparison_count_matches_iterations(self):
        """Comparison count should match number of CALCULATE_MID steps."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 3})
        
        comparisons = result['result']['comparisons']
        calc_mid_count = len([s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID'])
        
        assert comparisons == calc_mid_count

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestBinarySearchVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step (except INITIAL_STATE) should have visualization data."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, and state."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        # Check a CALCULATE_MID step
        calc_step = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID'][0]
        viz = calc_step['data']['visualization']
        
        assert 'array' in viz
        assert len(viz['array']) == 5
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element

    def test_element_states_valid(self):
        """Element states should be one of: excluded, active_range, examining, found."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        valid_states = {'excluded', 'active_range', 'examining', 'found'}
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for element in viz['array']:
                    assert element['state'] in valid_states

    def test_examining_state_at_mid(self):
        """Element at mid index should have 'examining' state."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        # Check CALCULATE_MID steps
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        for step in calc_steps:
            mid_index = step['data']['mid_index']
            viz = step['data']['visualization']
            
            mid_element = viz['array'][mid_index]
            assert mid_element['state'] == 'examining'

    def test_found_state_when_target_found(self):
        """When target found, element should have 'found' state."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        # Check TARGET_FOUND step
        found_step = [s for s in result['trace']['steps'] if s['type'] == 'TARGET_FOUND'][0]
        viz = found_step['data']['visualization']
        
        found_index = result['result']['index']
        found_element = viz['array'][found_index]
        
        assert found_element['state'] == 'found'
        assert found_element['value'] == 5

    def test_excluded_state_outside_range(self):
        """Elements outside [left, right] should have 'excluded' state."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9, 11, 13, 15], 'target': 13})
        
        # Check a SEARCH_RIGHT step (left moves forward)
        search_steps = [s for s in result['trace']['steps'] if s['type'] == 'SEARCH_RIGHT']
        
        if search_steps:
            # After searching right, left elements should be excluded
            # Check the step AFTER the search decision
            for i, step in enumerate(result['trace']['steps']):
                if step['type'] == 'SEARCH_RIGHT' and i + 1 < len(result['trace']['steps']):
                    next_step = result['trace']['steps'][i + 1]
                    if next_step['type'] == 'CALCULATE_MID':
                        viz = next_step['data']['visualization']
                        left = viz['pointers']['left']
                        
                        # Elements before left should be excluded
                        for element in viz['array']:
                            if element['index'] < left:
                                assert element['state'] == 'excluded'

    def test_active_range_within_bounds(self):
        """Elements within [left, right] should have 'active_range' state (except mid)."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            left = viz['pointers']['left']
            right = viz['pointers']['right']
            mid = viz['pointers']['mid']
            
            for element in viz['array']:
                idx = element['index']
                if left <= idx <= right and idx != mid:
                    # Should be active_range (not examining, not excluded)
                    assert element['state'] == 'active_range'

    def test_pointers_present_and_valid(self):
        """Pointers (left, right, mid, target) should be present and valid."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            pointers = viz['pointers']
            
            assert 'left' in pointers
            assert 'right' in pointers
            assert 'mid' in pointers
            assert 'target' in pointers
            
            # Validate pointer values
            assert 0 <= pointers['left'] <= pointers['right']
            assert pointers['left'] <= pointers['mid'] <= pointers['right']
            assert pointers['target'] == 5

    def test_search_space_size_decreases(self):
        """Search space size should decrease with each iteration."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9, 11, 13, 15], 'target': 13})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        previous_size = None
        for step in calc_steps:
            viz = step['data']['visualization']
            current_size = viz['search_space_size']
            
            assert current_size > 0
            
            if previous_size is not None:
                # Size should decrease or stay same (edge case)
                assert current_size <= previous_size
            
            previous_size = current_size

    def test_search_space_zero_when_complete(self):
        """Search space size should be 0 when search completes (not found)."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 4})
        
        final_step = result['trace']['steps'][-1]
        if 'visualization' in final_step['data']:
            viz = final_step['data']['visualization']
            assert viz['search_space_size'] == 0
    ### jjj
    def test_all_excluded_when_not_found(self):
            """When target not found, all elements should be 'excluded' (except possibly last mid)."""
            tracer = BinarySearchTracer()
            result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 4})
            
            final_step = result['trace']['steps'][-1]
            if 'visualization' in final_step['data']:
                viz = final_step['data']['visualization']
                
                # Most elements should be excluded
                excluded_count = sum(1 for el in viz['array'] if el['state'] == 'excluded')
                assert excluded_count >= len(viz['array']) - 1  # At least all but one
                
                # The last examined mid element might still be 'examining'
                # This is acceptable behavior showing which element was last checked

# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestBinarySearchPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_count_matches_iterations(self):
        """Prediction count should match number of CALCULATE_MID steps."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        calc_mid_count = len([s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == calc_mid_count

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'found', 'search-left', 'search-right'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice
                assert isinstance(choice['label'], str)
                assert len(choice['label']) > 0

    def test_correct_answer_valid(self):
        """Correct answer should be one of the three choices."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'found', 'search-left', 'search-right'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_step(self):
        """Correct answer should match the actual next step taken."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 7})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Get next step
            next_step = steps[step_index + 1]
            
            # Verify answer matches next step type
            if correct_answer == 'found':
                assert next_step['type'] == 'TARGET_FOUND'
            elif correct_answer == 'search-left':
                assert next_step['type'] == 'SEARCH_LEFT'
            elif correct_answer == 'search-right':
                assert next_step['type'] == 'SEARCH_RIGHT'

    def test_prediction_question_mentions_values(self):
        """Question should mention mid_value and target."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            # Question should mention comparison
            assert 'mid' in question or 'compare' in question

    def test_prediction_hint_present(self):
        """Each prediction should have a helpful hint."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint']
            assert isinstance(hint, str)
            assert len(hint) > 0

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            explanation = pred['explanation']
            assert isinstance(explanation, str)
            assert len(explanation) > 0


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestBinarySearchEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'array': [], 'target': 5})

    def test_unsorted_array_raises_error(self):
        """Unsorted array should raise ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="sorted"):
            tracer.execute({'array': [5, 3, 1, 7, 9], 'target': 3})

    def test_descending_array_raises_error(self):
        """Descending sorted array should raise ValueError (ascending required)."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="sorted"):
            tracer.execute({'array': [9, 7, 5, 3, 1], 'target': 5})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([1, 3, 5])

    def test_missing_array_key_raises_error(self):
        """Missing 'array' key should raise ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({'target': 5})

    def test_missing_target_key_raises_error(self):
        """Missing 'target' key should raise ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="target"):
            tracer.execute({'array': [1, 3, 5]})

    def test_single_element_found(self):
        """Single element array - target found."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [42], 'target': 42})
        
        assert result['result']['found'] is True
        assert result['result']['index'] == 0
        assert result['result']['comparisons'] == 1

    def test_single_element_not_found(self):
        """Single element array - target not found."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [42], 'target': 99})
        
        assert result['result']['found'] is False
        assert result['result']['index'] is None
        assert result['result']['comparisons'] == 1

    def test_negative_numbers(self):
        """Array with negative numbers should work."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [-10, -5, -3, 0, 5, 10], 'target': -5})
        
        assert result['result']['found'] is True
        assert result['result']['index'] == 1

    def test_all_same_values(self):
        """Array with all same values (duplicates)."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [5, 5, 5, 5, 5], 'target': 5})
        
        assert result['result']['found'] is True
        # Any index is valid
        assert 0 <= result['result']['index'] <= 4

    def test_target_smaller_than_all(self):
        """Target smaller than all elements."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [10, 20, 30, 40, 50], 'target': 5})
        
        assert result['result']['found'] is False
        assert result['result']['index'] is None

    def test_target_larger_than_all(self):
        """Target larger than all elements."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [10, 20, 30, 40, 50], 'target': 100})
        
        assert result['result']['found'] is False
        assert result['result']['index'] is None


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestBinarySearchMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        metadata = result['metadata']
        
        required_fields = [
            'algorithm',
            'display_name',
            'visualization_type',
            'visualization_config',
            'input_size',
            'target_value',
            'prediction_points'
        ]
        
        for field in required_fields:
            assert field in metadata, f"Missing required field: {field}"

    def test_algorithm_field_correct(self):
        """algorithm field should be 'binary-search'."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        assert result['metadata']['algorithm'] == 'binary-search'

    def test_display_name_field_correct(self):
        """display_name field should be 'Binary Search'."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        assert result['metadata']['display_name'] == 'Binary Search'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'pointer_colors' in config
        
        # Check pointer colors structure
        pointer_colors = config['pointer_colors']
        assert 'left' in pointer_colors
        assert 'right' in pointer_colors
        assert 'mid' in pointer_colors
        assert 'target' in pointer_colors

    def test_input_size_correct(self):
        """input_size should match array length."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        assert result['metadata']['input_size'] == 5

    def test_target_value_correct(self):
        """target_value should match input target."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 42})
        
        assert result['metadata']['target_value'] == 42

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_metadata_types_correct(self):
        """All metadata fields should have correct types."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        metadata = result['metadata']
        
        assert isinstance(metadata['algorithm'], str)
        assert isinstance(metadata['display_name'], str)
        assert isinstance(metadata['visualization_type'], str)
        assert isinstance(metadata['visualization_config'], dict)
        assert isinstance(metadata['input_size'], int)
        assert isinstance(metadata['target_value'], int)
        assert isinstance(metadata['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'found' in result['result']
        assert 'index' in result['result']
        assert 'comparisons' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']