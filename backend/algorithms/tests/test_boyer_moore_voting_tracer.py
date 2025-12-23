
"""
Tests for Boyer-Moore Voting algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.boyer_moore_voting_tracer import BoyerMooreVotingTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestBoyerMooreVotingCorrectness:
    """Test algorithm correctness - does it find the right answer?"""

    def test_clear_majority_found(self):
        """Test with clear majority element."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [3, 3, 4, 2, 3, 3, 3]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 3
        assert result['result']['occurrences'] == 5

    def test_no_majority_exists(self):
        """Test when no majority element exists."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 3, 4]})
        
        assert result['result']['has_majority'] is False
        assert result['result']['majority_element'] is None

    def test_all_same_elements(self):
        """Test when all elements are the same."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [5, 5, 5]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 5
        assert result['result']['occurrences'] == 3

    def test_single_element(self):
        """Test with single element (always majority)."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [42]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 42
        assert result['result']['occurrences'] == 1

    def test_two_elements_same(self):
        """Test with two identical elements."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [7, 7]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 7
        assert result['result']['occurrences'] == 2

    def test_two_elements_different(self):
        """Test with two different elements (no majority)."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2]})
        
        assert result['result']['has_majority'] is False
        assert result['result']['majority_element'] is None

    def test_majority_at_start(self):
        """Test when majority element appears mostly at start."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 1, 2, 3]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 1
        assert result['result']['occurrences'] == 3

    def test_majority_at_end(self):
        """Test when majority element appears mostly at end."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 3, 3, 3]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 3
        assert result['result']['occurrences'] == 3

    def test_majority_scattered(self):
        """Test when majority element is scattered throughout."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1, 3, 1, 4, 1]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 1
        assert result['result']['occurrences'] == 4

    def test_almost_majority(self):
        """Test when element appears exactly n/2 times (not majority)."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2, 2]})
        
        assert result['result']['has_majority'] is False
        assert result['result']['majority_element'] is None

    def test_large_array_with_majority(self):
        """Test with larger array containing majority."""
        array = [1] * 60 + [2] * 40  # 1 appears 60 times out of 100
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 1
        assert result['result']['occurrences'] == 60

    def test_large_array_no_majority(self):
        """Test with larger array without majority."""
        array = [1] * 50 + [2] * 50  # No element appears > 50 times
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': array})
        
        assert result['result']['has_majority'] is False
        assert result['result']['majority_element'] is None

    def test_negative_numbers(self):
        """Test with negative numbers."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [-1, -1, -1, 2, 3]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == -1
        assert result['result']['occurrences'] == 3

    def test_mixed_positive_negative(self):
        """Test with mix of positive and negative numbers."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [-5, 3, -5, 3, -5]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == -5
        assert result['result']['occurrences'] == 3


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestBoyerMooreVotingTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'array_size' in first_step['data']
        assert 'majority_threshold' in first_step['data']

    def test_check_candidate_steps_present(self):
        """CHECK_CANDIDATE steps should be present for each element."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_CANDIDATE']
        
        # Should have one CHECK_CANDIDATE per array element
        assert len(check_steps) == 3

    def test_update_count_steps_present(self):
        """UPDATE_COUNT steps should follow CHECK_CANDIDATE when count > 0."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2]})
        
        update_steps = [s for s in result['trace']['steps'] if s['type'] == 'UPDATE_COUNT']
        
        # Should have UPDATE_COUNT steps
        assert len(update_steps) > 0
        
        for step in update_steps:
            assert 'old_count' in step['data']
            assert 'new_count' in step['data']
            assert 'action' in step['data']
            assert step['data']['action'] in ['increment', 'decrement']

    def test_change_candidate_when_count_zero(self):
        """CHANGE_CANDIDATE should occur when count reaches 0."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 3]})
        
        change_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHANGE_CANDIDATE']
        
        # Should have candidate changes
        assert len(change_steps) > 0
        
        for step in change_steps:
            assert 'old_candidate' in step['data']
            assert 'new_candidate' in step['data']

    def test_phase_transition_present(self):
        """PHASE_TRANSITION should occur between finding and verification."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2]})
        
        phase_steps = [s for s in result['trace']['steps'] if s['type'] == 'PHASE_TRANSITION']
        
        assert len(phase_steps) == 1
        
        step = phase_steps[0]
        assert 'candidate' in step['data']
        assert 'final_count' in step['data']

    def test_verify_candidate_steps_present(self):
        """VERIFY_CANDIDATE steps should be present for each element."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        verify_steps = [s for s in result['trace']['steps'] if s['type'] == 'VERIFY_CANDIDATE']
        
        # Should have one VERIFY_CANDIDATE per array element
        assert len(verify_steps) == 3
        
        for step in verify_steps:
            assert 'matches' in step['data']
            assert 'verification_count' in step['data']

    def test_majority_found_final_step(self):
        """When majority exists, last step should be MAJORITY_FOUND."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 1, 2]})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'MAJORITY_FOUND'
        assert 'candidate' in last_step['data']
        assert 'occurrences' in last_step['data']
        assert 'threshold' in last_step['data']

    def test_no_majority_final_step(self):
        """When no majority, last step should be NO_MAJORITY."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 3]})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'NO_MAJORITY'
        assert 'candidate' in last_step['data']
        assert 'occurrences' in last_step['data']
        assert 'threshold' in last_step['data']

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestBoyerMooreVotingVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step (except INITIAL_STATE) should have visualization data."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_array_elements_structure(self):
        """Array elements should have index, value, and state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        check_step = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_CANDIDATE'][0]
        viz = check_step['data']['visualization']
        
        assert 'array' in viz
        assert len(viz['array']) == 3
        
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element

    def test_element_states_valid(self):
        """Element states should be valid."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        valid_states = {'examining', 'supporting', 'opposing', 'verified', 'rejected', 'neutral'}
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for element in viz['array']:
                    assert element['state'] in valid_states

    def test_examining_state_at_current_index(self):
        """Element at current_index should have 'examining' state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_CANDIDATE']
        
        for step in check_steps:
            viz = step['data']['visualization']
            current_idx = viz['current_index']
            
            if current_idx is not None:
                current_element = viz['array'][current_idx]
                assert current_element['state'] == 'examining'

    def test_candidate_tracked(self):
        """Candidate should be tracked in visualization state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'candidate' in viz

    def test_count_tracked(self):
        """Count should be tracked in visualization state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'count' in viz
                assert isinstance(viz['count'], int)
                assert viz['count'] >= 0

    def test_phase_tracked(self):
        """Phase should be tracked in visualization state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'phase' in viz
                assert viz['phase'] in ['FINDING', 'VERIFYING']

    def test_phase_transition_changes_phase(self):
        """Phase should change from FINDING to VERIFYING."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        steps = result['trace']['steps']
        
        # Find phase transition
        transition_idx = None
        for i, step in enumerate(steps):
            if step['type'] == 'PHASE_TRANSITION':
                transition_idx = i
                break
        
        assert transition_idx is not None
        
        # Check phase before and after transition
        before_step = steps[transition_idx - 1]
        after_step = steps[transition_idx + 1]
        
        if 'visualization' in before_step['data']:
            assert before_step['data']['visualization']['phase'] == 'FINDING'
        
        if 'visualization' in after_step['data']:
            assert after_step['data']['visualization']['phase'] == 'VERIFYING'

    def test_verification_count_tracked(self):
        """Verification count should be tracked during verification phase."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        verify_steps = [s for s in result['trace']['steps'] if s['type'] == 'VERIFY_CANDIDATE']
        
        for step in verify_steps:
            viz = step['data']['visualization']
            assert 'verification_count' in viz
            assert isinstance(viz['verification_count'], int)
            assert viz['verification_count'] >= 0

    def test_verification_count_increases(self):
        """Verification count should increase when matches found."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2]})
        
        verify_steps = [s for s in result['trace']['steps'] if s['type'] == 'VERIFY_CANDIDATE']
        
        previous_count = 0
        for step in verify_steps:
            current_count = step['data']['visualization']['verification_count']
            matches = step['data']['matches']
            
            if matches:
                assert current_count == previous_count + 1
            else:
                assert current_count == previous_count
            
            previous_count = current_count

    def test_supporting_state_during_finding(self):
        """Elements matching candidate should have 'supporting' state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2]})
        
        # Find a step where element matches candidate
        for step in result['trace']['steps']:
            if step['type'] == 'UPDATE_COUNT' and step['data']['action'] == 'increment':
                viz = step['data']['visualization']
                if viz['phase'] == 'FINDING':
                    # Previous elements matching candidate should be 'supporting'
                    candidate = viz['candidate']
                    for elem in viz['array']:
                        if elem['index'] < viz['current_index'] and elem['value'] == candidate:
                            assert elem['state'] == 'supporting'

    def test_opposing_state_during_finding(self):
        """Elements not matching candidate should have 'opposing' state."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        # Find a step where element doesn't match candidate
        for step in result['trace']['steps']:
            if step['type'] == 'UPDATE_COUNT' and step['data']['action'] == 'decrement':
                viz = step['data']['visualization']
                if viz['phase'] == 'FINDING':
                    # Previous elements not matching candidate should be 'opposing'
                    candidate = viz['candidate']
                    for elem in viz['array']:
                        if elem['index'] < viz['current_index'] and elem['value'] != candidate:
                            assert elem['state'] == 'opposing'


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestBoyerMooreVotingPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        # May or may not have predictions depending on array

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_valid(self):
        """Prediction choices should be valid."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) <= 3  # Max 3 choices
            assert len(choices) >= 2  # At least 2 choices
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice

    def test_correct_answer_valid(self):
        """Correct answer should be one of the choice IDs."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            correct_answer = pred['correct_answer']
            choice_ids = {c['id'] for c in pred['choices']}
            assert correct_answer in choice_ids

    def test_phase_transition_prediction(self):
        """Should have prediction at phase transition."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2]})
        
        predictions = result['metadata']['prediction_points']
        
        # Find phase transition step
        phase_transition_idx = None
        for i, step in enumerate(result['trace']['steps']):
            if step['type'] == 'PHASE_TRANSITION':
                phase_transition_idx = i
                break
        
        if phase_transition_idx is not None:
            # Should have a prediction at or near phase transition
            prediction_indices = {p['step_index'] for p in predictions}
            assert phase_transition_idx in prediction_indices


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestBoyerMooreVotingEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_array_raises_error(self):
        """Empty array should raise ValueError."""
        tracer = BoyerMooreVotingTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'array': []})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = BoyerMooreVotingTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([1, 2, 3])

    def test_missing_array_key_raises_error(self):
        """Missing 'array' key should raise ValueError."""
        tracer = BoyerMooreVotingTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({})

    def test_single_element_always_majority(self):
        """Single element is always majority."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [99]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 99

    def test_two_elements_tie(self):
        """Two different elements is a tie (no majority)."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2]})
        
        assert result['result']['has_majority'] is False

    def test_alternating_pattern(self):
        """Alternating pattern with no majority."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1, 2, 1, 2]})
        
        assert result['result']['has_majority'] is False

    def test_majority_by_one(self):
        """Majority by exactly one occurrence."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 1, 2, 2]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 1
        assert result['result']['occurrences'] == 3

    def test_zero_values(self):
        """Array containing zeros."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [0, 0, 1]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 0

    def test_large_numbers(self):
        """Array with large numbers."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1000000, 1000000, 999999]})
        
        assert result['result']['has_majority'] is True
        assert result['result']['majority_element'] == 1000000


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestBoyerMooreVotingMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
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
        """algorithm field should be 'boyer-moore-voting'."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert result['metadata']['algorithm'] == 'boyer-moore-voting'

    def test_display_name_field_correct(self):
        """display_name field should be 'Boyer-Moore Voting'."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert result['metadata']['display_name'] == 'Boyer-Moore Voting'

    def test_visualization_type_correct(self):
        """visualization_type should be 'array'."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert result['metadata']['visualization_type'] == 'array'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'show_candidate' in config

    def test_input_size_correct(self):
        """input_size should match array length."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 3, 4, 5]})
        
        assert result['metadata']['input_size'] == 5

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'has_majority' in result['result']
        assert 'majority_element' in result['result']
        assert 'occurrences' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestBoyerMooreVotingNarrative:
    """Test narrative generation."""

    def test_narrative_generates_without_error(self):
        """Narrative should generate without KeyError."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        # Should not raise KeyError
        narrative = tracer.generate_narrative(result)
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_contains_header(self):
        """Narrative should contain header with algorithm name."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        narrative = tracer.generate_narrative(result)
        assert "Boyer-Moore Voting" in narrative

    def test_narrative_contains_result(self):
        """Narrative should contain final result."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 1, 2]})
        
        narrative = tracer.generate_narrative(result)
        
        if result['result']['has_majority']:
            assert "Majority element" in narrative or "majority" in narrative.lower()
        else:
            assert "No majority" in narrative or "no majority" in narrative.lower()

    def test_narrative_contains_visualization_hints(self):
        """Narrative should contain Frontend Visualization Hints section."""
        tracer = BoyerMooreVotingTracer()
        result = tracer.execute({'array': [1, 2, 1]})
        
        narrative = tracer.generate_narrative(result)
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative
