"""
Tests for Container With Most Water algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.container_with_most_water_tracer import ContainerWithMostWaterTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestContainerWithMostWaterCorrectness:
    """Test algorithm correctness - does it find the right maximum area?"""

    @pytest.mark.parametrize("heights,expected_area,expected_left,expected_right", [
        # Basic cases
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49, 1, 8),  # Classic example
        ([1, 1], 1, 0, 1),                         # Minimum size
        ([4, 3, 2, 1, 4], 16, 0, 4),              # Max at boundaries
        ([1, 2, 1], 2, 0, 2),                      # Small array
        
        # Equal heights
        ([5, 5, 5, 5], 15, 0, 3),                 # All equal
        ([3, 3, 3], 6, 0, 2),                      # All equal (3 elements)
        
        # Ascending/Descending
        ([1, 2, 3, 4, 5], 6, 0, 4),               # Ascending
        ([5, 4, 3, 2, 1], 6, 0, 4),               # Descending
        
        # Peak in middle
        ([1, 3, 5, 3, 1], 6, 1, 3),               # Peak in middle (Corrected from 4 to 6)
        ([2, 1, 5, 1, 2], 8, 0, 4),               # Valley pattern
    ])
    def test_container_scenarios(self, heights, expected_area, expected_left, expected_right):
        """Test container with most water with various input scenarios."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': heights})
        
        assert result['result']['max_area'] == expected_area
        # Note: Multiple valid solutions may exist with same area
        # Verify the returned indices produce the expected area
        left_idx = result['result']['left_index']
        right_idx = result['result']['right_index']
        width = right_idx - left_idx
        height = min(heights[left_idx], heights[right_idx])
        calculated_area = width * height
        assert calculated_area == expected_area

    def test_large_array(self):
        """Test with larger array (20 elements)."""
        heights = [1, 8, 6, 2, 5, 4, 8, 3, 7, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 1]
        
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': heights})
        
        # Verify result structure
        assert 'max_area' in result['result']
        assert 'left_index' in result['result']
        assert 'right_index' in result['result']
        assert result['result']['max_area'] > 0

    def test_two_tall_walls_at_ends(self):
        """Test with two tall walls at boundaries."""
        heights = [10, 1, 1, 1, 1, 1, 1, 1, 10]
        
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': heights})
        
        # Should select the two tall walls at ends
        assert result['result']['max_area'] == 80  # width=8, height=10
        assert result['result']['left_index'] == 0
        assert result['result']['right_index'] == 8

    def test_iterations_count(self):
        """Iterations should equal n-1 for array of size n."""
        heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
        
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': heights})
        
        # Should have n-1 iterations (pointers meet after n-1 moves)
        assert result['result']['iterations'] == len(heights) - 1


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestContainerWithMostWaterTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'heights' in first_step['data']
        assert 'left' in first_step['data']
        assert 'right' in first_step['data']

    def test_search_complete_final_step(self):
        """Last step should be SEARCH_COMPLETE."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'SEARCH_COMPLETE'
        assert 'max_area' in last_step['data']
        assert 'max_left' in last_step['data']
        assert 'max_right' in last_step['data']

    def test_calculate_area_steps_present(self):
        """CALCULATE_AREA steps should be present for each iteration."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        calc_area_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_AREA']
        
        # Should have n-1 CALCULATE_AREA steps
        assert len(calc_area_steps) == 4  # 5 elements = 4 iterations
        
        # Each should have required data
        for step in calc_area_steps:
            assert 'left' in step['data']
            assert 'right' in step['data']
            assert 'left_height' in step['data']
            assert 'right_height' in step['data']
            assert 'width' in step['data']
            assert 'height' in step['data']
            assert 'area' in step['data']

    def test_move_steps_follow_calculate(self):
        """MOVE_LEFT or MOVE_RIGHT should follow CALCULATE_AREA (possibly with UPDATE_MAX between)."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        steps = result['trace']['steps']
        
        for i, step in enumerate(steps):
            if step['type'] == 'CALCULATE_AREA' and i + 1 < len(steps):
                # Next step should be UPDATE_MAX or MOVE_LEFT/MOVE_RIGHT
                next_step = steps[i + 1]
                assert next_step['type'] in ['UPDATE_MAX', 'MOVE_LEFT', 'MOVE_RIGHT', 'SEARCH_COMPLETE']

    def test_update_max_when_area_increases(self):
        """UPDATE_MAX should occur when new maximum is found."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5, 4, 8, 3, 7]})
        
        update_max_steps = [s for s in result['trace']['steps'] if s['type'] == 'UPDATE_MAX']
        
        # Should have at least one UPDATE_MAX
        assert len(update_max_steps) > 0
        
        # Each should show old and new max
        for step in update_max_steps:
            assert 'old_max_area' in step['data']
            assert 'new_max_area' in step['data']
            assert step['data']['new_max_area'] > step['data']['old_max_area']

    def test_move_left_updates_pointer(self):
        """MOVE_LEFT step should update left pointer."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        move_left_steps = [s for s in result['trace']['steps'] if s['type'] == 'MOVE_LEFT']
        
        if move_left_steps:
            step = move_left_steps[0]
            assert 'old_left' in step['data']
            assert 'new_left' in step['data']
            assert step['data']['new_left'] == step['data']['old_left'] + 1

    def test_move_right_updates_pointer(self):
        """MOVE_RIGHT step should update right pointer."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [8, 6, 2, 5, 1]})
        
        move_right_steps = [s for s in result['trace']['steps'] if s['type'] == 'MOVE_RIGHT']
        
        if move_right_steps:
            step = move_right_steps[0]
            assert 'old_right' in step['data']
            assert 'new_right' in step['data']
            assert step['data']['new_right'] == step['data']['old_right'] - 1

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestContainerWithMostWaterVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, and state."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        calc_step = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_AREA'][0]
        viz = calc_step['data']['visualization']
        
        assert 'array' in viz
        assert len(viz['array']) == 5
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element

    def test_element_states_valid(self):
        """Element states should be valid."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        valid_states = {'excluded', 'active', 'examining', 'max_container'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for element in viz['array']:
                assert element['state'] in valid_states

    def test_examining_state_at_pointers(self):
        """Elements at left and right pointers should have 'examining' state."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_AREA']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            left = viz['pointers']['left']
            right = viz['pointers']['right']
            
            left_element = viz['array'][left]
            right_element = viz['array'][right]
            
            assert left_element['state'] == 'examining'
            assert right_element['state'] == 'examining'

    def test_max_container_state_in_final_step(self):
        """Final step should mark max container elements."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        final_step = result['trace']['steps'][-1]
        viz = final_step['data']['visualization']
        
        max_container_elements = [e for e in viz['array'] if e['state'] == 'max_container']
        
        # Should have exactly 2 elements marked as max_container
        assert len(max_container_elements) == 2

    def test_pointers_present_and_valid(self):
        """Pointers (left, right) should be present and valid."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_AREA']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            pointers = viz['pointers']
            
            assert 'left' in pointers
            assert 'right' in pointers
            
            # Validate pointer values
            assert 0 <= pointers['left'] < pointers['right'] < len(result['result'])

    def test_current_area_tracked(self):
        """Current area should be tracked in visualization."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_AREA']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            assert 'current_area' in viz
            assert viz['current_area'] >= 0

    def test_max_area_tracked(self):
        """Max area should be tracked in visualization."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'max_area' in viz
            assert viz['max_area'] >= 0

    def test_container_dimensions_present(self):
        """Container width and height should be present."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_AREA']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            assert 'container_width' in viz
            assert 'container_height' in viz


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestContainerWithMostWaterPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'move-left', 'move-right', 'done'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice

    def test_correct_answer_valid(self):
        """Correct answer should be one of the three choices."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'move-left', 'move-right', 'done'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_move(self):
        """Correct answer should match the actual next move taken."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Find next MOVE step
            for i in range(step_index + 1, len(steps)):
                if steps[i]['type'] in ['MOVE_LEFT', 'MOVE_RIGHT']:
                    next_move = steps[i]
                    break
            
            # Verify answer matches next move
            if correct_answer == 'move-left':
                assert next_move['type'] == 'MOVE_LEFT'
            elif correct_answer == 'move-right':
                assert next_move['type'] == 'MOVE_RIGHT'


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestContainerWithMostWaterEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = ContainerWithMostWaterTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'heights': []})

    def test_single_element_raises_error(self):
        """Single element array should raise ValueError."""
        tracer = ContainerWithMostWaterTracer()
        
        with pytest.raises(ValueError, match="at least 2 elements"):
            tracer.execute({'heights': [5]})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = ContainerWithMostWaterTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([1, 8, 6])

    def test_missing_heights_key_raises_error(self):
        """Missing 'heights' key should raise ValueError."""
        tracer = ContainerWithMostWaterTracer()
        
        with pytest.raises(ValueError, match="heights"):
            tracer.execute({'data': [1, 8, 6]})

    def test_negative_height_raises_error(self):
        """Negative heights should raise ValueError."""
        tracer = ContainerWithMostWaterTracer()
        
        with pytest.raises(ValueError, match="positive integers"):
            tracer.execute({'heights': [1, -5, 6]})

    def test_zero_height_raises_error(self):
        """Zero heights should raise ValueError."""
        tracer = ContainerWithMostWaterTracer()
        
        with pytest.raises(ValueError, match="positive integers"):
            tracer.execute({'heights': [1, 0, 6]})

    def test_two_elements_minimum(self):
        """Two elements is minimum valid input."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [5, 3]})
        
        assert result['result']['max_area'] == 3  # width=1, height=3
        assert result['result']['iterations'] == 1

    def test_all_same_heights(self):
        """Array with all same heights."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [5, 5, 5, 5]})
        
        # Max area should be at boundaries: width=3, height=5
        assert result['result']['max_area'] == 15

    def test_large_heights(self):
        """Test with large height values."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [100, 50, 100]})
        
        # Should select the two 100s: width=2, height=100
        assert result['result']['max_area'] == 200


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestContainerWithMostWaterMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6]})
        
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
        """algorithm field should be 'container-with-most-water'."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6]})
        
        assert result['metadata']['algorithm'] == 'container-with-most-water'

    def test_display_name_field_correct(self):
        """display_name field should be 'Container With Most Water'."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6]})
        
        assert result['metadata']['display_name'] == 'Container With Most Water'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6]})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_result_structure_correct(self):
        """Result should have correct structure."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'max_area' in result['result']
        assert 'left_index' in result['result']
        assert 'right_index' in result['result']
        assert 'left_height' in result['result']
        assert 'right_height' in result['result']
        assert 'iterations' in result['result']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestContainerWithMostWaterNarrative:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generation_executes(self):
        """Narrative generation should execute without errors."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        
        # Should not raise KeyError
        narrative = tracer.generate_narrative(result)
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_contains_key_sections(self):
        """Narrative should contain expected sections."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        narrative = tracer.generate_narrative(result)
        
        # Check for key sections
        assert "# Container With Most Water Execution Narrative" in narrative
        assert "## Step 0:" in narrative
        assert "## Execution Summary" in narrative
        assert "🎨 Frontend Visualization Hints" in narrative

    def test_narrative_shows_calculations(self):
        """Narrative should show explicit calculations."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        narrative = tracer.generate_narrative(result)
        
        # Should show area calculations
        assert "Width" in narrative
        assert "Height" in narrative
        assert "Area" in narrative
        assert "×" in narrative or "*" in narrative

    def test_narrative_includes_visualization_hints(self):
        """Narrative should include frontend visualization hints."""
        tracer = ContainerWithMostWaterTracer()
        result = tracer.execute({'heights': [1, 8, 6, 2, 5]})
        narrative = tracer.generate_narrative(result)
        
        # Check for visualization hints section
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics to Emphasize" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative
        assert "Algorithm-Specific Guidance" in narrative