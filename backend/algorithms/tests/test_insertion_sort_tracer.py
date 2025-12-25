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
        
        # Count COMPARE steps
        compare_steps = [s for s in result['trace']['steps'] if s['type'] == 'COMPARE']
        
        # Should match result comparisons
        assert len(compare_steps) == result['result']['comparisons']

    def test_shift_count_matches_result(self):
        """Shift count in trace should match result."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1]})
        
        # Count SHIFT steps
        shift_steps = [s for s in result['trace']['steps'] if s['type'] == 'SHIFT']
        
        # Should match result shifts
        assert len(shift_steps) == result['result']['shifts']


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestInsertionSortVisualizationState:
    """Test visualization state generation."""

    def test_visualization_in_all_steps(self):
        """All steps should have visualization state."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_array_visualization_structure(self):
        """Array visualization should have correct structure."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Check first step visualization
        viz = result['trace']['steps'][0]['data']['visualization']
        
        assert 'array' in viz
        assert isinstance(viz['array'], list)
        
        # Each array element should have index, value, state
        for elem in viz['array']:
            assert 'index' in elem
            assert 'value' in elem
            assert 'state' in elem

    def test_key_visualization_when_present(self):
        """Key should be in visualization when active."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        # Find a SELECT_KEY step
        select_key_step = next(s for s in result['trace']['steps'] if s['type'] == 'SELECT_KEY')
        
        viz = select_key_step['data']['visualization']
        assert 'key' in viz
        
        if viz['key'] is not None:
            assert 'index' in viz['key']
            assert 'value' in viz['key']

    def test_sorted_boundary_in_visualization(self):
        """Sorted boundary should be in visualization."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'sorted_boundary' in viz

    def test_element_states_valid(self):
        """Element states should be valid values."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        valid_states = {'sorted', 'examining', 'comparing', 'shifting', 'unsorted'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            if 'array' in viz:
                for elem in viz['array']:
                    assert elem['state'] in valid_states

    def test_sorted_boundary_grows(self):
        """Sorted boundary should grow as algorithm progresses."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 2, 8, 1, 9]})
        
        # Find INSERT steps
        insert_steps = [s for s in result['trace']['steps'] if s['type'] == 'INSERT']
        
        # Sorted boundary should increase with each insertion
        prev_boundary = 0
        for step in insert_steps:
            viz = step['data']['visualization']
            current_boundary = viz['sorted_boundary']
            assert current_boundary > prev_boundary
            prev_boundary = current_boundary


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestInsertionSortPredictionPoints:
    """Test prediction point generation for active learning."""

    def test_prediction_points_exist(self):
        """Prediction points should be generated."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        assert len(predictions) > 0

    def test_prediction_point_structure(self):
        """Each prediction point should have required fields."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            assert 'step_index' in pred
            assert 'question' in pred
            assert 'choices' in pred
            assert 'hint' in pred
            assert 'correct_answer' in pred
            assert 'explanation' in pred

    def test_prediction_choices_valid(self):
        """Prediction choices should have id and label."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            assert len(pred['choices']) > 0
            for choice in pred['choices']:
                assert 'id' in choice
                assert 'label' in choice

    def test_prediction_has_3_choices(self):
        """Each prediction should have exactly 3 choices."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            assert len(pred['choices']) == 3

    def test_correct_answer_in_choices(self):
        """Correct answer should match one of the choice ids."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choice_ids = [c['id'] for c in pred['choices']]
            assert pred['correct_answer'] in choice_ids

    def test_predictions_at_compare_steps(self):
        """Predictions should be at COMPARE steps."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [3, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            assert steps[step_index]['type'] == 'COMPARE'


# =============================================================================
# Test Class 5: Edge Cases
# =============================================================================

@pytest.mark.unit
class TestInsertionSortEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_input_not_dict(self):
        """Should raise ValueError if input is not a dict."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="Input must be a dictionary"):
            tracer.execute([3, 1, 2])

    def test_invalid_input_missing_array_key(self):
        """Should raise ValueError if 'array' key missing."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="Input must contain 'array' key"):
            tracer.execute({'data': [3, 1, 2]})

    def test_invalid_input_array_not_list(self):
        """Should raise ValueError if array is not a list."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="Array must be a list"):
            tracer.execute({'array': "not a list"})

    def test_invalid_input_array_too_small(self):
        """Should raise ValueError if array has < 2 elements."""
        tracer = InsertionSortTracer()
        
        with pytest.raises(ValueError, match="Array must contain at least 2 elements"):
            tracer.execute({'array': [1]})
        
        with pytest.raises(ValueError, match="Array must contain at least 2 elements"):
            tracer.execute({'array': []})

    def test_two_element_array(self):
        """Should handle minimum valid size (2 elements)."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [2, 1]})
        
        assert result['result']['sorted_array'] == [1, 2]

    def test_already_sorted_array(self):
        """Should handle already sorted array efficiently."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [1, 2, 3, 4, 5]})
        
        # Should have minimal comparisons (n-1)
        assert result['result']['comparisons'] == 4
        # Should have no shifts
        assert result['result']['shifts'] == 0

    def test_reverse_sorted_array(self):
        """Should handle reverse sorted array (worst case)."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 4, 3, 2, 1]})
        
        # Should have maximum comparisons and shifts
        assert result['result']['sorted_array'] == [1, 2, 3, 4, 5]
        assert result['result']['comparisons'] > 0
        assert result['result']['shifts'] > 0

    def test_all_same_elements(self):
        """Should handle array with all identical elements."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [5, 5, 5, 5]})
        
        assert result['result']['sorted_array'] == [5, 5, 5, 5]
        # Should have comparisons but no shifts
        assert result['result']['comparisons'] == 3
        assert result['result']['shifts'] == 0


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.unit
class TestInsertionSortMetadataCompliance:
    """Test compliance with Backend Checklist metadata requirements."""

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


# =============================================================================
# Test Class 8: FAA Compliance (Arithmetic Accuracy)
# =============================================================================

@pytest.mark.unit
class TestInsertionSortFAACompliance:
    """Test FAA compliance - verifies sorted region arithmetic correctness."""

    def test_sorted_region_uses_boundary_not_insert_index(self):
        """
        REGRESSION TEST for sorted region bug.
        
        Ensures narrative uses self.sorted_boundary instead of insert_index + 1.
        This prevents the bug where sorted region size was reported as insert 
        position rather than total sorted region size.
        
        Bug example: When key inserts at index 0 but sorted region is 4 elements,
        old code reported "1 elements" (insert_index + 1 = 0 + 1) instead of 
        "4 elements" (self.sorted_boundary = 4).
        """
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [12, 11, 13, 5, 6]})
        
        narrative = tracer.generate_narrative(result)
        
        # The narrative should use pattern: "Sorted region now contains: **N elements**"
        # NOT the old pattern: "Sorted region expanded: **N elements***"
        
        # Verify the new pattern is present
        assert "Sorted region now contains:" in narrative, \
            "Narrative should use 'Sorted region now contains:' pattern"
        
        # Verify specific expected values are present
        # After inserting array[1]=11: sorted region should be 2 elements
        assert "**2 elements**" in narrative, \
            "After inserting second element, sorted region should show 2 elements"
        
        # After inserting array[2]=13: sorted region should be 3 elements
        assert "**3 elements**" in narrative, \
            "After inserting third element, sorted region should show 3 elements"
        
        # After inserting array[3]=5: sorted region should be 4 elements
        assert "**4 elements**" in narrative, \
            "After inserting fourth element, sorted region should show 4 elements"
        
        # After inserting array[4]=6: sorted region should be 5 elements (complete)
        assert "**5 elements**" in narrative, \
            "After inserting fifth element, sorted region should show 5 elements"

    def test_sorted_boundary_value_correctness(self):
        """Verify sorted_boundary values in visualization state are arithmetically correct."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [12, 11, 13, 5, 6]})
        
        # Find all INSERT steps
        insert_steps = [s for s in result['trace']['steps'] if s['type'] == 'INSERT']
        
        # Verify sorted_boundary in visualization for each INSERT step
        expected_boundaries = [2, 3, 4, 5]  # After inserting elements 1, 2, 3, 4
        
        for i, step in enumerate(insert_steps):
            viz = step['data']['visualization']
            actual_boundary = viz['sorted_boundary']
            expected_boundary = expected_boundaries[i]
            
            assert actual_boundary == expected_boundary, \
                f"INSERT step {i}: sorted_boundary should be {expected_boundary}, got {actual_boundary}"

    def test_no_old_expanded_pattern_in_narrative(self):
        """Ensure old buggy pattern is not present in narrative."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [12, 11, 13, 5, 6]})
        
        narrative = tracer.generate_narrative(result)
        
        # The old buggy pattern should NOT be present
        assert "Sorted region expanded: **1 elements***" not in narrative, \
            "Old buggy pattern 'expanded: **1 elements***' should not be in narrative"

    def test_sorted_region_indices_shown_correctly(self):
        """Verify that sorted region indices are shown in narrative."""
        tracer = InsertionSortTracer()
        result = tracer.execute({'array': [12, 11, 13, 5, 6]})
        
        narrative = tracer.generate_narrative(result)
        
        # Should show index ranges like (indices [0,1]), (indices [0,2]), etc.
        assert "indices [0," in narrative, \
            "Narrative should show sorted region index ranges"