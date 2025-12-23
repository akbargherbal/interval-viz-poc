
"""
Tests for Meeting Rooms II algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.meeting_rooms_tracer import MeetingRoomsTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestMeetingRoomsCorrectness:
    """Test algorithm correctness - does it find the right answer?"""

    @pytest.mark.parametrize("intervals,expected_rooms", [
        # Basic cases
        ([[0, 30], [5, 10], [15, 20]], 2),           # Two overlapping groups
        ([[7, 10], [2, 4]], 1),                       # No overlap
        ([[0, 5], [5, 10], [10, 15]], 1),            # Sequential (no overlap)
        ([[0, 5], [0, 5], [0, 5]], 3),               # Maximum overlap (all same)
        
        # Single meeting
        ([[0, 10]], 1),
        
        # Complex overlaps
        ([[0, 30], [5, 10], [15, 20], [25, 35]], 2),
        ([[1, 5], [2, 6], [3, 7], [4, 8]], 4),       # Cascading overlaps
        ([[1, 10], [2, 11], [3, 12], [11, 13]], 3),  # Three overlap, one after
        
        # Edge cases from spec
        ([[0, 5], [5, 10], [10, 15]], 1),            # Sequential meetings
        ([[0, 5], [0, 5], [0, 5]], 3),               # Maximum overlap
    ])
    def test_meeting_rooms_scenarios(self, intervals, expected_rooms):
        """Test meeting rooms with various input scenarios."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assert result['result']['min_rooms'] == expected_rooms

    def test_large_input(self):
        """Test with larger input (10 meetings)."""
        intervals = [
            [0, 10], [5, 15], [10, 20], [15, 25], [20, 30],
            [25, 35], [30, 40], [35, 45], [40, 50], [45, 55]
        ]
        # Overlaps: 0-10 with 5-15, 5-15 with 10-20, etc.
        # Maximum concurrent: 2 rooms
        
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assert result['result']['min_rooms'] == 2

    def test_all_overlapping(self):
        """Test when all meetings overlap completely."""
        intervals = [[0, 100], [0, 100], [0, 100], [0, 100]]
        
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assert result['result']['min_rooms'] == 4

    def test_no_overlaps(self):
        """Test when no meetings overlap."""
        intervals = [[0, 5], [10, 15], [20, 25], [30, 35]]
        
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assert result['result']['min_rooms'] == 1

    def test_room_assignments_valid(self):
        """Room assignments should be valid (all meetings assigned)."""
        intervals = [[0, 30], [5, 10], [15, 20]]
        
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assignments = result['result']['room_assignments']
        
        # All meetings should be assigned
        assert len(assignments) == len(intervals)
        
        # Room numbers should be in valid range
        for room_num in assignments.values():
            assert 1 <= room_num <= result['result']['min_rooms']

    def test_room_assignments_no_conflicts(self):
        """Meetings in same room should not overlap."""
        intervals = [[0, 30], [5, 10], [15, 20], [35, 40]]
        
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': intervals})
        
        assignments = result['result']['room_assignments']
        
        # Group by room
        rooms = {}
        for interval_id, room_num in assignments.items():
            if room_num not in rooms:
                rooms[room_num] = []
            rooms[room_num].append(intervals[interval_id])
        
        # Check no overlaps within each room
        for room_num, room_intervals in rooms.items():
            sorted_intervals = sorted(room_intervals, key=lambda x: x[0])
            for i in range(len(sorted_intervals) - 1):
                end1 = sorted_intervals[i][1]
                start2 = sorted_intervals[i + 1][0]
                assert end1 <= start2, f"Overlap in room {room_num}: {sorted_intervals[i]} and {sorted_intervals[i+1]}"


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestMeetingRoomsTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_sort_start_first_step(self):
        """First step should be SORT_START."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'SORT_START'
        assert 'original_count' in first_step['data']
        assert 'sorted_order' in first_step['data']

    def test_check_earliest_end_steps_present(self):
        """CHECK_EARLIEST_END steps should be present when heap is not empty."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_EARLIEST_END']
        
        # Should have check steps for meetings after the first
        assert len(check_steps) >= 2
        
        for step in check_steps:
            assert 'interval_id' in step['data']
            assert 'interval_start' in step['data']
            assert 'interval_end' in step['data']
            assert 'heap_top' in step['data']

    def test_allocate_room_steps(self):
        """ALLOCATE_ROOM steps should have correct structure."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        allocate_steps = [s for s in result['trace']['steps'] if s['type'] == 'ALLOCATE_ROOM']
        
        for step in allocate_steps:
            assert 'interval_id' in step['data']
            assert 'room_number' in step['data']
            assert 'reused' in step['data']
            
            if step['data']['reused']:
                assert 'old_heap_top' in step['data']

    def test_new_room_steps(self):
        """NEW_ROOM steps should have correct structure."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        new_room_steps = [s for s in result['trace']['steps'] if s['type'] == 'NEW_ROOM']
        
        # Should have at least one NEW_ROOM step
        assert len(new_room_steps) >= 1
        
        for step in new_room_steps:
            assert 'interval_id' in step['data']
            assert 'room_number' in step['data']
            assert 'heap_empty' in step['data']

    def test_update_heap_steps(self):
        """UPDATE_HEAP steps should follow room allocations."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        update_steps = [s for s in result['trace']['steps'] if s['type'] == 'UPDATE_HEAP']
        
        for step in update_steps:
            assert 'interval_id' in step['data']
            assert 'interval_end' in step['data']
            assert 'heap_size' in step['data']

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_trace_duration_recorded(self):
        """Trace should include total duration."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert 'duration' in result['trace']
        assert isinstance(result['trace']['duration'], (int, float))
        assert result['trace']['duration'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestMeetingRoomsVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_all_intervals_structure(self):
        """all_intervals should have id, start, end, state, room."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        # Check a step with visualization
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'all_intervals' in viz
        assert len(viz['all_intervals']) == 2
        
        for interval in viz['all_intervals']:
            assert 'id' in interval
            assert 'start' in interval
            assert 'end' in interval
            assert 'state' in interval
            assert 'room' in interval

    def test_interval_states_valid(self):
        """Interval states should be: pending, examining, scheduled."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        valid_states = {'pending', 'examining', 'scheduled'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for interval in viz['all_intervals']:
                assert interval['state'] in valid_states

    def test_examining_state_for_current_interval(self):
        """Current interval should have 'examining' state."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        # Check CHECK_EARLIEST_END steps
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_EARLIEST_END']
        
        for step in check_steps:
            interval_id = step['data']['interval_id']
            viz = step['data']['visualization']
            
            examining_intervals = [iv for iv in viz['all_intervals'] if iv['state'] == 'examining']
            assert len(examining_intervals) == 1
            assert examining_intervals[0]['id'] == interval_id

    def test_scheduled_state_after_allocation(self):
        """Intervals should have 'scheduled' state after allocation."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        # Check final step
        final_step = result['trace']['steps'][-1]
        viz = final_step['data']['visualization']
        
        scheduled_count = len([iv for iv in viz['all_intervals'] if iv['state'] == 'scheduled'])
        assert scheduled_count == 2  # Both meetings should be scheduled

    def test_heap_state_present(self):
        """heap_state should be present and valid."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'heap_state' in viz
            assert isinstance(viz['heap_state'], list)

    def test_heap_state_sorted(self):
        """heap_state should be sorted (min-heap property)."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            heap = viz['heap_state']
            
            if len(heap) > 1:
                # Check sorted order
                assert heap == sorted(heap)

    def test_room_assignments_present(self):
        """room_assignments should be present in visualization."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'room_assignments' in viz
            assert isinstance(viz['room_assignments'], dict)

    def test_rooms_used_present(self):
        """rooms_used should be present and valid."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'rooms_used' in viz
            assert isinstance(viz['rooms_used'], int)
            assert viz['rooms_used'] >= 0

    def test_rooms_used_increases_correctly(self):
        """rooms_used should increase when new rooms allocated."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        new_room_steps = [s for s in result['trace']['steps'] if s['type'] == 'NEW_ROOM']
        
        previous_rooms = 0
        for step in new_room_steps:
            viz = step['data']['visualization']
            current_rooms = viz['rooms_used']
            assert current_rooms > previous_rooms
            previous_rooms = current_rooms


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestMeetingRoomsPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        assert len(predictions) > 0

    def test_prediction_count_matches_checks(self):
        """Prediction count should match CHECK_EARLIEST_END steps."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        check_count = len([s for s in result['trace']['steps'] if s['type'] == 'CHECK_EARLIEST_END'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == check_count

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        predictions = result['metadata']['prediction_points']
        
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
        
        for pred in predictions:
            for field in required_fields:
                assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_structure(self):
        """Each prediction should have 3 choices with id and label."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choices = pred['choices']
            assert len(choices) == 3
            
            choice_ids = {c['id'] for c in choices}
            assert choice_ids == {'reuse', 'new-room', 'skip'}
            
            for choice in choices:
                assert 'id' in choice
                assert 'label' in choice

    def test_correct_answer_valid(self):
        """Correct answer should be 'reuse' or 'new-room'."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'reuse', 'new-room'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers

    def test_correct_answer_matches_next_step(self):
        """Correct answer should match the actual next step taken."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [35, 40]]})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Get next step
            next_step = steps[step_index + 1]
            
            # Verify answer matches next step type
            if correct_answer == 'reuse':
                assert next_step['type'] == 'ALLOCATE_ROOM'
                assert next_step['data']['reused'] is True
            elif correct_answer == 'new-room':
                assert next_step['type'] == 'NEW_ROOM'

    def test_prediction_question_mentions_times(self):
        """Question should mention start time and heap top."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            question = pred['question'].lower()
            # Question should mention times or comparison
            assert 'start' in question or 'finish' in question or 'meeting' in question

    def test_prediction_hint_present(self):
        """Each prediction should have a helpful hint."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            hint = pred['hint']
            assert isinstance(hint, str)
            assert len(hint) > 0

    def test_prediction_explanation_present(self):
        """Each prediction should have an explanation."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            explanation = pred['explanation']
            assert isinstance(explanation, str)
            assert len(explanation) > 0


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestMeetingRoomsEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_intervals_raises_error(self):
        """Empty intervals list should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'intervals': []})

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([[0, 30], [5, 10]])

    def test_missing_intervals_key_raises_error(self):
        """Missing 'intervals' key should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="intervals"):
            tracer.execute({'data': [[0, 30]]})

    def test_invalid_interval_format_raises_error(self):
        """Invalid interval format should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="must be"):
            tracer.execute({'intervals': [[0, 30], [5]]})  # Missing end

    def test_invalid_interval_values_raises_error(self):
        """Invalid interval values (start >= end) should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="invalid"):
            tracer.execute({'intervals': [[10, 5]]})  # start > end

    def test_equal_start_end_raises_error(self):
        """Equal start and end should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="invalid"):
            tracer.execute({'intervals': [[5, 5]]})

    def test_non_integer_times_raises_error(self):
        """Non-integer times should raise ValueError."""
        tracer = MeetingRoomsTracer()
        
        with pytest.raises(ValueError, match="integers"):
            tracer.execute({'intervals': [[0.5, 10.5]]})

    def test_single_meeting(self):
        """Single meeting should require 1 room."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30]]})
        
        assert result['result']['min_rooms'] == 1

    def test_two_sequential_meetings(self):
        """Two sequential meetings should require 1 room."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 5], [5, 10]]})
        
        assert result['result']['min_rooms'] == 1

    def test_two_overlapping_meetings(self):
        """Two overlapping meetings should require 2 rooms."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 10], [5, 15]]})
        
        assert result['result']['min_rooms'] == 2

    def test_negative_times(self):
        """Negative times should work (valid intervals)."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[-10, -5], [-3, 0]]})
        
        assert result['result']['min_rooms'] == 1

    def test_large_time_values(self):
        """Large time values should work."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[1000000, 2000000], [1500000, 2500000]]})
        
        assert result['result']['min_rooms'] == 2


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestMeetingRoomsMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
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
        """algorithm field should be 'meeting-rooms'."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert result['metadata']['algorithm'] == 'meeting-rooms'

    def test_display_name_field_correct(self):
        """display_name field should be 'Meeting Rooms II'."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert result['metadata']['display_name'] == 'Meeting Rooms II'

    def test_visualization_type_correct(self):
        """visualization_type should be 'timeline'."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert result['metadata']['visualization_type'] == 'timeline'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        config = result['metadata']['visualization_config']
        
        assert 'group_by_room' in config
        assert 'show_heap' in config
        assert config['group_by_room'] is True
        assert config['show_heap'] is True

    def test_input_size_correct(self):
        """input_size should match intervals count."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10], [15, 20]]})
        
        assert result['metadata']['input_size'] == 3

    def test_prediction_points_in_metadata(self):
        """prediction_points should be in metadata."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        assert 'prediction_points' in result['metadata']
        assert isinstance(result['metadata']['prediction_points'], list)

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = MeetingRoomsTracer()
        result = tracer.execute({'intervals': [[0, 30], [5, 10]]})
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'min_rooms' in result['result']
        assert 'room_assignments' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']
