
"""
Tests for Dutch National Flag (Sort Colors) algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.dutch_national_flag_tracer import DutchNationalFlagTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestDutchNationalFlagCorrectness:
    """Test algorithm correctness - does it sort correctly?"""

    @pytest.mark.parametrize("array,expected", [
        # Basic cases
        ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
        ([2, 0, 1], [0, 1, 2]),
        ([0, 1, 2], [0, 1, 2]),  # Already sorted
        ([2, 1, 0], [0, 1, 2]),  # Reverse sorted
        
        # All same color
        ([0, 0, 0, 0], [0, 0, 0, 0]),
        ([1, 1, 1, 1], [1, 1, 1, 1]),
        ([2, 2, 2, 2], [2, 2, 2, 2]),
        
        # Single element
        ([0], [0]),
        ([1], [1]),
        ([2], [2]),
        
        # Two elements
        ([1, 0], [0, 1]),
        ([2, 0], [0, 2]),
        ([2, 1], [1, 2]),
        ([0, 1], [0, 1]),
        ([0, 2], [0, 2]),
        ([1, 2], [1, 2]),
        
        # Complex cases
        ([1, 2, 0, 1, 2, 0, 1, 2, 0], [0, 0, 0, 1, 1, 1, 2, 2, 2]),
        ([2, 2, 0, 0, 1, 1], [0, 0, 1, 1, 2, 2]),
        ([0, 2, 1, 0, 2, 1], [0, 0, 1, 1, 2, 2]),
    ])
    def test_sort_colors_scenarios(self, array, expected):
        """Test Dutch National Flag with various input scenarios."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_original_array_preserved(self):
        """Original array should be preserved in result."""
        original = [2, 0, 1, 2, 1, 0]
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': original})
        
        assert result['result']['original_array'] == original
        # Verify input wasn't modified
        assert original == [2, 0, 1, 2, 1, 0]

    def test_swap_count_reasonable(self):
        """Swap count should be reasonable (at most n swaps)."""
        array = [2, 0, 1, 2, 1, 0]
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        swaps = result['result']['swaps']
        
        # Should not exceed array length
        assert swaps <= len(array)
        assert swaps >= 0

    def test_large_array(self):
        """Test with larger array."""
        array = [2, 0, 1] * 5  # 15 elements
        expected = [0] * 5 + [1] * 5 + [2] * 5
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_mostly_zeros(self):
        """Array with mostly 0s."""
        array = [0, 0, 0, 0, 1, 2]
        expected = [0, 0, 0, 0, 1, 2]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_mostly_twos(self):
        """Array with mostly 2s."""
        array = [0, 1, 2, 2, 2, 2]
        expected = [0, 1, 2, 2, 2, 2]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_no_ones(self):
        """Array with no 1s."""
        array = [2, 0, 2, 0, 2, 0]
        expected = [0, 0, 0, 2, 2, 2]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_no_zeros(self):
        """Array with no 0s."""
        array = [2, 1, 2, 1, 2, 1]
        expected = [1, 1, 1, 2, 2, 2]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_no_twos(self):
        """Array with no 2s."""
        array = [1, 0, 1, 0, 1, 0]
        expected = [0, 0, 0, 1, 1, 1]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestDutchNationalFlagTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'array' in first_step['data']
        assert 'array_size' in first_step['data']
        assert 'low' in first_step['data']
        assert 'mid' in first_step['data']
        assert 'high' in first_step['data']

    def test_check_value_steps_present(self):
        """CHECK_VALUE steps should be present for each iteration."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE']
        
        # Should have at least one CHECK_VALUE step
        assert len(check_steps) >= 1
        
        # Each should have required data
        for step in check_steps:
            assert 'mid_index' in step['data']
            assert 'mid_value' in step['data']
            assert 'low' in step['data']
            assert 'high' in step['data']

    def test_action_follows_check(self):
        """An action step should follow each CHECK_VALUE."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        steps = result['trace']['steps']
        
        for i, step in enumerate(steps):
            if step['type'] == 'CHECK_VALUE' and i + 1 < len(steps):
                next_step = steps[i + 1]
                # Next step should be an action
                assert next_step['type'] in ['SWAP_LOW', 'SWAP_HIGH', 'ADVANCE_MID']

    def test_swap_low_updates_pointers(self):
        """SWAP_LOW step should update both low and mid."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [0, 1, 2]})
        
        swap_low_steps = [s for s in result['trace']['steps'] if s['type'] == 'SWAP_LOW']
        
        if swap_low_steps:
            step = swap_low_steps[0]
            assert 'low_index' in step['data']
            assert 'mid_index' in step['data']
            assert 'new_low' in step['data']
            assert 'new_mid' in step['data']
            assert step['data']['new_low'] == step['data']['low_index'] + 1
            assert step['data']['new_mid'] == step['data']['mid_index'] + 1

    def test_swap_high_updates_pointer(self):
        """SWAP_HIGH step should update high only."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 1, 0]})
        
        swap_high_steps = [s for s in result['trace']['steps'] if s['type'] == 'SWAP_HIGH']
        
        if swap_high_steps:
            step = swap_high_steps[0]
            assert 'high_index' in step['data']
            assert 'new_high' in step['data']
            assert step['data']['new_high'] == step['data']['high_index'] - 1

    def test_advance_mid_updates_pointer(self):
        """ADVANCE_MID step should update mid only."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [1, 0, 2]})
        
        advance_steps = [s for s in result['trace']['steps'] if s['type'] == 'ADVANCE_MID']
        
        if advance_steps:
            step = advance_steps[0]
            assert 'mid_index' in step['data']
            assert 'new_mid' in step['data']
            assert step['data']['new_mid'] == step['data']['mid_index'] + 1

    def test_swap_count_increments(self):
        """Swap count should increment with each swap."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        swap_steps = [s for s in result['trace']['steps'] 
                      if s['type'] in ['SWAP_LOW', 'SWAP_HIGH']]
        
        # Each swap step should have swaps field
        for step in swap_steps:
            assert 'swaps' in step['data']
            assert step['data']['swaps'] > 0

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestDutchNationalFlagVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step (except INITIAL_STATE) should have visualization data."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, state, and color."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        # Check a CHECK_VALUE step
        check_step = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE'][0]
        viz = check_step['data']['visualization']
        
        assert 'array' in viz
        assert len(viz['array']) == 3
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element
            assert 'color' in element

    def test_element_states_valid(self):
        """Element states should be valid."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        valid_states = {'examining', 'sorted_low', 'sorted_mid', 'sorted_high', 'unsorted'}
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for element in viz['array']:
                    assert element['state'] in valid_states

    def test_element_colors_correct(self):
        """Element colors should match values (0=red, 1=white, 2=blue)."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        color_map = {0: 'red', 1: 'white', 2: 'blue'}
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for element in viz['array']:
                    expected_color = color_map[element['value']]
                    assert element['color'] == expected_color

    def test_examining_state_at_mid(self):
        """Element at mid index should have 'examining' state."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        # Check CHECK_VALUE steps
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE']
        
        for step in check_steps:
            mid_index = step['data']['mid_index']
            viz = step['data']['visualization']
            
            mid_element = viz['array'][mid_index]
            assert mid_element['state'] == 'examining'

    def test_pointers_present_and_valid(self):
        """Pointers (low, mid, high) should be present and valid."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE']
        
        for step in check_steps:
            viz = step['data']['visualization']
            pointers = viz['pointers']
            
            assert 'low' in pointers
            assert 'mid' in pointers
            assert 'high' in pointers
            
            # Validate pointer values
            assert 0 <= pointers['low'] <= len(result['result']['sorted_array'])
            assert 0 <= pointers['mid'] <= len(result['result']['sorted_array'])
            assert -1 <= pointers['high'] < len(result['result']['sorted_array'])

    def test_regions_present(self):
        """Regions should be present in visualization."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE']
        
        for step in check_steps:
            viz = step['data']['visualization']
            
            assert 'regions' in viz
            assert 'zeros' in viz['regions']
            assert 'ones' in viz['regions']
            assert 'unsorted' in viz['regions']
            assert 'twos' in viz['regions']

    def test_sorted_regions_grow(self):
        """Sorted regions should grow as algorithm progresses."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1, 2, 0, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE']
        
        # Track region sizes
        for i in range(len(check_steps) - 1):
            current_viz = check_steps[i]['data']['visualization']
            next_viz = check_steps[i + 1]['data']['visualization']
            
            current_low = current_viz['pointers']['low']
            next_low = next_viz['pointers']['low']
            
            current_high = current_viz['pointers']['high']
            next_high = next_viz['pointers']['high']
            
            # Low should stay same or increase
            assert next_low >= current_low
            # High should stay same or decrease
            assert next_high <= current_high

    def test_unsorted_region_shrinks(self):
        """Unsorted region should shrink as algorithm progresses."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1, 2, 0, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE']
        
        previous_size = None
        for step in check_steps:
            viz = step['data']['visualization']
            mid = viz['pointers']['mid']
            high = viz['pointers']['high']
            
            current_size = high - mid + 1
            
            if previous_size is not None:
                # Unsorted region should shrink or stay same
                assert current_size <= previous_size
            
            previous_size = current_size


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestDutchNationalFlagPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_count_matches_checks(self):
        """Prediction count should match number of CHECK_VALUE steps."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        check_count = len([s for s in result['trace']['steps'] if s['type'] == 'CHECK_VALUE'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == check_count

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'swap-low', 'swap-high', 'advance-mid'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice
                assert isinstance(choice['label'], str)
                assert len(choice['label']) > 0

    def test_correct_answer_valid(self):
        """Correct answer should be one of the three choices."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'swap-low', 'swap-high', 'advance-mid'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_step(self):
        """Correct answer should match the actual next step taken."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Get next step
            next_step = steps[step_index + 1]
            
            # Verify answer matches next step type
            if correct_answer == 'swap-low':
                assert next_step['type'] == 'SWAP_LOW'
            elif correct_answer == 'swap-high':
                assert next_step['type'] == 'SWAP_HIGH'
            elif correct_answer == 'advance-mid':
                assert next_step['type'] == 'ADVANCE_MID'

    def test_prediction_question_mentions_value(self):
        """Question should mention the value being examined."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            # Question should mention value or color
            assert 'value' in question or 'red' in question or 'white' in question or 'blue' in question

    def test_prediction_hint_present(self):
        """Each prediction should have a helpful hint."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint']
            assert isinstance(hint, str)
            assert len(hint) > 0

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            explanation = pred['explanation']
            assert isinstance(explanation, str)
            assert len(explanation) > 0


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestDutchNationalFlagEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = DutchNationalFlagTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'array': []})

    def test_invalid_values_raise_error(self):
        """Array with values other than 0, 1, 2 should raise ValueError."""
        tracer = DutchNationalFlagTracer()
        
        with pytest.raises(ValueError, match="only values 0, 1, and 2"):
            tracer.execute({'array': [0, 1, 3]})

    def test_negative_values_raise_error(self):
        """Array with negative values should raise ValueError."""
        tracer = DutchNationalFlagTracer()
        
        with pytest.raises(ValueError, match="only values 0, 1, and 2"):
            tracer.execute({'array': [0, 1, -1]})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = DutchNationalFlagTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([2, 0, 1])

    def test_missing_array_key_raises_error(self):
        """Missing 'array' key should raise ValueError."""
        tracer = DutchNationalFlagTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({'data': [2, 0, 1]})

    def test_single_element_each_color(self):
        """Single element of each color."""
        for value in [0, 1, 2]:
            tracer = DutchNationalFlagTracer()
            result = tracer.execute({'array': [value]})
            
            assert result['result']['sorted_array'] == [value]

    def test_all_zeros(self):
        """Array with all 0s."""
        array = [0, 0, 0, 0, 0]
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == array

    def test_all_ones(self):
        """Array with all 1s."""
        array = [1, 1, 1, 1, 1]
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == array

    def test_all_twos(self):
        """Array with all 2s."""
        array = [2, 2, 2, 2, 2]
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == array

    def test_alternating_pattern(self):
        """Alternating pattern."""
        array = [0, 2, 0, 2, 0, 2]
        expected = [0, 0, 0, 2, 2, 2]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected

    def test_reverse_sorted(self):
        """Completely reverse sorted."""
        array = [2, 2, 2, 1, 1, 1, 0, 0, 0]
        expected = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['sorted_array'] == expected


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestDutchNationalFlagMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
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
        """algorithm field should be 'dutch-national-flag'."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert result['metadata']['algorithm'] == 'dutch-national-flag'

    def test_display_name_field_correct(self):
        """display_name field should be 'Sort Colors (Dutch National Flag)'."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert result['metadata']['display_name'] == 'Sort Colors (Dutch National Flag)'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'color_map' in config
        assert 'pointer_colors' in config
        
        # Check color map structure
        color_map = config['color_map']
        assert '0' in color_map
        assert '1' in color_map
        assert '2' in color_map
        assert color_map['0'] == 'red'
        assert color_map['1'] == 'white'
        assert color_map['2'] == 'blue'
        
        # Check pointer colors structure
        pointer_colors = config['pointer_colors']
        assert 'low' in pointer_colors
        assert 'mid' in pointer_colors
        assert 'high' in pointer_colors

    def test_input_size_correct(self):
        """input_size should match array length."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1, 2, 0]})
        
        assert result['metadata']['input_size'] == 5

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_metadata_types_correct(self):
        """All metadata fields should have correct types."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        metadata = result['metadata']
        
        assert isinstance(metadata['algorithm'], str)
        assert isinstance(metadata['display_name'], str)
        assert isinstance(metadata['visualization_type'], str)
        assert isinstance(metadata['visualization_config'], dict)
        assert isinstance(metadata['input_size'], int)
        assert isinstance(metadata['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'sorted_array' in result['result']
        assert 'original_array' in result['result']
        assert 'swaps' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestDutchNationalFlagNarrativeGeneration:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generates_without_error(self):
        """Narrative generation should not raise exceptions."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        # Should not raise KeyError or other exceptions
        narrative = tracer.generate_narrative(result)
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_includes_header(self):
        """Narrative should include header with algorithm name."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "Dutch National Flag" in narrative
        assert "Sort Colors" in narrative

    def test_narrative_includes_input_output(self):
        """Narrative should show input and output arrays."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "[2, 0, 1]" in narrative
        assert "[0, 1, 2]" in narrative

    def test_narrative_includes_step_sections(self):
        """Narrative should have step sections."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "## Step 0:" in narrative
        assert "## Step 1:" in narrative

    def test_narrative_includes_visualization_hints(self):
        """Narrative should include Frontend Visualization Hints section."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        narrative = tracer.generate_narrative(result)
        
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics to Emphasize" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative
        assert "Algorithm-Specific Guidance" in narrative

    def test_narrative_shows_pointer_movements(self):
        """Narrative should explain pointer movements."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should mention pointers
        assert "low" in narrative.lower()
        assert "mid" in narrative.lower()
        assert "high" in narrative.lower()

    def test_narrative_explains_swap_decisions(self):
        """Narrative should explain why swaps occur."""
        tracer = DutchNationalFlagTracer()
        result = tracer.execute({'array': [2, 0, 1]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should explain swap reasoning
        assert "swap" in narrative.lower() or "Swap" in narrative
