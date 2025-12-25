"""
Meeting Rooms II algorithm tracer for educational visualization.

Implements minimum conference rooms calculation using min-heap of end times
with complete trace generation for step-by-step visualization and prediction mode.

Algorithm: Sort meetings by start time, use min-heap to track earliest ending meeting.
When a new meeting starts, check if earliest ending meeting has finished (heap top).
If finished, reuse that room (pop heap). Otherwise, allocate new room.
Heap size at any point = number of rooms needed.

VERSION: 2.2 - FAA COMPLIANCE FIX + INPUT VALIDATION
- CRITICAL FIX: Heap now stores (end_time, room_id) tuples instead of just end_time
- Room assignments now traceable and temporally exclusive
- Fixes FAA audit failures: room assignment contradictions eliminated
- Added comprehensive input validation (fail loudly on invalid input)
"""

from typing import Any, List, Dict
import heapq
from .base_tracer import AlgorithmTracer


class MeetingRoomsTracer(AlgorithmTracer):
    """
    Tracer for Meeting Rooms II algorithm using min-heap scheduling.

    Visualization shows:
    - Timeline of all meetings grouped by assigned room
    - Min-heap state showing earliest ending meetings WITH room tracking
    - Current meeting being processed
    - Room allocation decisions

    Prediction points ask: "Will we reuse a room or allocate a new one?"
    """

    def __init__(self):
        super().__init__()
        self.intervals = []
        self.sorted_intervals = []
        self.heap = []  # Now stores (end_time, room_id) tuples
        self.room_assignments = {}  # interval_id -> room_number
        self.current_interval_id = None
        self.rooms_used = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current timeline state with intervals and heap.

        Returns timeline visualization with:
        - all_intervals: All meetings with states (pending, examining, scheduled)
        - heap_state: Current min-heap of end times (extracted from tuples)
        - room_assignments: Which room each meeting is in
        - rooms_used: Total rooms allocated so far
        """
        if not self.intervals:
            return {}

        # Build interval visualization
        all_intervals = []
        for i, interval in enumerate(self.intervals):
            state = 'pending'
            if i in self.room_assignments:
                state = 'scheduled'
            elif self.current_interval_id == i:
                state = 'examining'
            
            all_intervals.append({
                'id': i,
                'start': interval[0],
                'end': interval[1],
                'state': state,
                'room': self.room_assignments.get(i, None)
            })

        # Extract end times from heap for visualization
        # Heap contains (end_time, room_id) tuples, but frontend expects just end times
        heap_end_times = sorted([end_time for end_time, _ in self.heap]) if self.heap else []

        return {
            'all_intervals': all_intervals,
            'heap_state': heap_end_times,
            'room_assignments': dict(self.room_assignments),
            'rooms_used': self.rooms_used
        }

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Meeting Rooms II trace.

        Shows complete execution flow with all decision data visible.
        Follows Universal Principles: explicit comparisons, result traceability,
        no redundant state display, defined terms.

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution

        Raises:
            KeyError: If required visualization data is missing
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Meeting Rooms II Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input:** {len(self.intervals)} meetings\n"
        narrative += f"**Result:** Minimum **{result['min_rooms']}** conference rooms required\n"
        narrative += f"**Total Steps:** {len(steps)}\n\n"
        narrative += "---\n\n"

        # Step-by-step narrative
        for step in steps:
            step_num = step['step']
            step_type = step['type']
            description = step['description']
            data = step['data']
            viz = data['visualization']

            narrative += f"## Step {step_num}: {description}\n\n"

            # Type-specific details
            if step_type == "SORT_START":
                narrative += "**Initial Meetings (Unsorted):**\n\n"
                narrative += "| Meeting ID | Start Time | End Time |\n"
                narrative += "|------------|------------|----------|\n"
                for interval in viz['all_intervals']:
                    narrative += f"| {interval['id']} | {interval['start']} | {interval['end']} |\n"
                narrative += "\n"

                narrative += "**Sorting Strategy:**\n"
                narrative += "- Sort meetings by **start time** (ascending order)\n"
                narrative += "- Process meetings in chronological order of when they begin\n"
                narrative += "- This ensures we handle earliest meetings first\n\n"

                narrative += "**Sorted Meetings:**\n\n"
                sorted_meetings = sorted(viz['all_intervals'], key=lambda x: x['start'])
                narrative += "| Meeting ID | Start Time | End Time |\n"
                narrative += "|------------|------------|----------|\n"
                for interval in sorted_meetings:
                    narrative += f"| {interval['id']} | {interval['start']} | {interval['end']} |\n"
                narrative += "\n"

                narrative += "**Data Structures Initialized:**\n"
                narrative += "- **Min-Heap:** Empty (will track earliest ending meetings)\n"
                narrative += "- **Room Assignments:** Empty (will map meetings to rooms)\n"
                narrative += "- **Rooms Used:** 0\n\n"

            elif step_type == "CHECK_EARLIEST_END":
                interval_id = data['interval_id']
                interval_start = data['interval_start']
                interval_end = data['interval_end']
                heap_top = data['heap_top']

                narrative += f"**Current Meeting:** ID {interval_id} [{interval_start}, {interval_end}]\n\n"

                narrative += "**Heap State (Earliest Ending Meetings):**\n"
                if viz['heap_state']:
                    narrative += f"- Heap: {viz['heap_state']}\n"
                    narrative += f"- Top of heap (earliest end time): **{heap_top}**\n\n"
                else:
                    narrative += "- Heap: Empty (no meetings scheduled yet)\n\n"

                narrative += "**Decision Logic:**\n"
                narrative += f"Compare meeting start time ({interval_start}) with earliest end time ({heap_top}):\n\n"

                if interval_start >= heap_top:
                    narrative += f"**Comparison:** {interval_start} ≥ {heap_top} ✓\n\n"
                    narrative += "**Outcome:** Meeting starts **after or when** earliest meeting ends\n"
                    narrative += "- The room from the earliest ending meeting is now **free**\n"
                    narrative += "- We can **reuse** that room (no new room needed)\n"
                    narrative += f"- Action: Remove {heap_top} from heap, reuse its room\n\n"
                else:
                    narrative += f"**Comparison:** {interval_start} < {heap_top} ✗\n\n"
                    narrative += "**Outcome:** Meeting starts **before** earliest meeting ends\n"
                    narrative += "- All currently scheduled meetings are still ongoing\n"
                    narrative += "- No rooms are free yet\n"
                    narrative += "- Action: Must **allocate a new room**\n\n"

            elif step_type == "ALLOCATE_ROOM":
                interval_id = data['interval_id']
                interval_start = data['interval_start']
                interval_end = data['interval_end']
                room_number = data['room_number']
                reused = data.get('reused', False)

                if reused:
                    old_heap_top = data['old_heap_top']
                    freed_room = data['freed_room']  # NEW: Which room was freed
                    
                    narrative += f"**Meeting:** ID {interval_id} [{interval_start}, {interval_end}]\n"
                    narrative += f"**Assigned to:** Room {room_number}\n\n"
                    
                    narrative += "**Room Reuse:**\n"
                    narrative += f"- Heap popped: end time {old_heap_top} (Room {freed_room})\n"
                    narrative += f"- Previous meeting in Room {room_number} ended at {old_heap_top}\n"
                    narrative += f"- Current meeting starts at {interval_start}\n"
                    narrative += f"- Gap: {interval_start - old_heap_top} time units\n"
                    narrative += f"- **Room {room_number}** is now free and reused\n\n"
                else:
                    narrative += f"**Meeting:** ID {interval_id} [{interval_start}, {interval_end}]\n"
                    narrative += f"**Decision:** Allocate **new Room {room_number}**\n\n"

                    heap_top_val = data.get('heap_top')
                    heap_empty = data.get('heap_empty', False)
                    
                    if heap_empty:
                        narrative += "**Reason:**\n"
                        narrative += "- Heap is empty (first meeting being scheduled)\n"
                        narrative += "- Must allocate first room\n\n"
                    else:
                        narrative += "**Reason:**\n"
                        narrative += f"- Meeting starts at {interval_start}\n"
                        narrative += f"- Earliest ending meeting finishes at {heap_top_val}\n"
                        narrative += f"- Comparison: {interval_start} < {heap_top_val}\n"
                        narrative += "- All rooms are occupied, need new room\n\n"

                    narrative += f"**Rooms Used:** {viz['rooms_used']}\n\n"

            elif step_type == "UPDATE_HEAP":
                interval_end = data['interval_end']
                heap_size = data['heap_size']

                narrative += f"**Heap Operation:** Add end time {interval_end} to min-heap\n\n"
                narrative += "**Purpose of Heap:**\n"
                narrative += "- Heap tracks end times of all currently scheduled meetings\n"
                narrative += "- Top of heap = earliest ending meeting\n"
                narrative += "- Heap size = number of rooms currently in use\n\n"

                narrative += f"**Updated Heap:** {viz['heap_state']}\n"
                narrative += f"**Heap Size:** {heap_size} rooms in use\n\n"

            elif step_type == "FINAL_RESULT":
                min_rooms = result['min_rooms']
                room_assignments = result['room_assignments']

                narrative += f"**Minimum Rooms Required:** {min_rooms}\n\n"

                narrative += "**Final Room Assignments:**\n\n"
                
                # Group meetings by room
                rooms_dict = {}
                for interval_id, room in room_assignments.items():
                    if room not in rooms_dict:
                        rooms_dict[room] = []
                    # Get interval details
                    interval = self.intervals[interval_id]
                    rooms_dict[room].append({
                        'id': interval_id,
                        'start': interval[0],
                        'end': interval[1]
                    })

                # Display each room's timeline
                for room in sorted(rooms_dict.keys()):
                    narrative += f"**Room {room}:**\n"
                    meetings = sorted(rooms_dict[room], key=lambda x: x['start'])
                    for meeting in meetings:
                        narrative += f"- Meeting {meeting['id']}: [{meeting['start']}, {meeting['end']}]\n"
                    narrative += "\n"

                narrative += "**Algorithm Efficiency:**\n"
                narrative += f"- Time Complexity: O(n log n) where n = {len(self.intervals)}\n"
                narrative += "  - Sorting: O(n log n)\n"
                narrative += "  - Heap operations: O(n log n) for n insertions/deletions\n"
                narrative += "- Space Complexity: O(n) for heap storage\n"
                narrative += "- Optimal Solution: Uses minimum possible rooms (greedy algorithm)\n\n"

                narrative += "**Key Insight:**\n"
                narrative += "The heap size at any point represents the number of rooms in use. The maximum heap size throughout execution equals the minimum rooms needed. By always reusing the earliest-ending room when possible, we ensure optimal room utilization.\n\n"

            narrative += "---\n\n"

        # Frontend Visualization Hints
        narrative += "## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Rooms Used** (`rooms_used`) - The core result metric, shows minimum rooms needed\n"
        narrative += "- **Heap Size** (`heap_state.length`) - Real-time indicator of concurrent meetings\n"
        narrative += "- **Current Meeting** (`current_interval_id`) - Which meeting is being scheduled\n\n"

        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Timeline grouping by room** - Show meetings stacked vertically by room assignment\n"
        narrative += "2. **Heap visualization** - Display min-heap as a priority queue showing earliest end times\n"
        narrative += "3. **Reuse vs. new room decisions** - Highlight when a room is reused (green) vs. new allocation (blue)\n"
        narrative += "4. **Temporal overlap** - Emphasize when meetings overlap (why new rooms are needed)\n"
        narrative += "5. **Animate heap operations** - Show pop (reuse) and push (schedule) operations clearly\n\n"

        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.all_intervals[*].id\n"
        narrative += "step.data.visualization.all_intervals[*].start\n"
        narrative += "step.data.visualization.all_intervals[*].end\n"
        narrative += "step.data.visualization.all_intervals[*].state  // 'pending' | 'examining' | 'scheduled'\n"
        narrative += "step.data.visualization.all_intervals[*].room   // null or room number\n"
        narrative += "step.data.visualization.heap_state              // array of end times (sorted)\n"
        narrative += "step.data.visualization.room_assignments        // map of interval_id -> room_number\n"
        narrative += "step.data.visualization.rooms_used              // total rooms allocated\n"
        narrative += "step.data.interval_id                           // current meeting being processed\n"
        narrative += "step.data.heap_top                              // earliest end time (for comparisons)\n"
        narrative += "step.data.freed_room                            // room that was just freed (reuse steps)\n"
        narrative += "```\n\n"

        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Meeting Rooms II is fundamentally about **resource allocation over time**. The most pedagogically powerful visualization is a **Gantt chart / timeline** showing meetings grouped by room. Students should see:\n\n"
        narrative += "1. **Why overlaps force new rooms** - When meeting A hasn't ended but meeting B starts\n"
        narrative += "2. **How the heap enables reuse** - The earliest-ending meeting's room becomes available first\n"
        narrative += "3. **The greedy optimality** - Always reusing the earliest-free room minimizes total rooms\n\n"
        narrative += "Consider using **color coding**: pending meetings (gray), examining (yellow), scheduled (green/blue). Animate the **heap pop operation** when reusing a room - show the end time being removed and the room becoming available. The heap visualization should be **synchronized with the timeline** - when heap size grows, show new room allocation; when heap size shrinks, show room reuse. This dual visualization (timeline + heap) makes the algorithm's logic transparent.\n\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Meeting Rooms II algorithm with complete trace generation.

        Args:
            input_data: Dictionary with 'intervals' key containing list of [start, end] pairs

        Returns:
            Complete trace result with steps, metadata, and final result
            
        Raises:
            ValueError: If input validation fails
        """
        # Validation 1: Input must be a dictionary
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary with 'intervals' key")
        
        # Validation 2: 'intervals' key must be present
        if 'intervals' not in input_data:
            raise ValueError("Input dictionary must contain 'intervals' key")
        
        # Validation 3: Intervals list cannot be empty
        self.intervals = input_data.get('intervals', [])
        if not self.intervals:
            raise ValueError("Intervals list cannot be empty")
        
        # Validation 4: Each interval must be a list/tuple with exactly 2 elements
        for i, interval in enumerate(self.intervals):
            if not isinstance(interval, (list, tuple)) or len(interval) != 2:
                raise ValueError(f"Each interval must be a list or tuple of [start, end]. Invalid at index {i}")
        
        # Validation 5: Start and end must be integers
        for i, interval in enumerate(self.intervals):
            start, end = interval
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError(f"Interval times must be integers. Invalid at index {i}: [{start}, {end}]")
        
        # Validation 6: Start must be less than end (no zero-duration or negative-duration meetings)
        for i, interval in enumerate(self.intervals):
            start, end = interval
            if start >= end:
                raise ValueError(f"invalid interval at index {i}: start ({start}) must be less than end ({end})")

        self.metadata = {
            'algorithm': 'meeting-rooms',
            'display_name': 'Meeting Rooms II',
            'visualization_type': 'timeline',
            'visualization_config': {
                'group_by_room': True,
                'show_heap': True,
                'time_axis': 'horizontal',
                'room_axis': 'vertical'
            },
            'input_size': len(self.intervals)
        }

        # Step 0: Sort by start time
        self.sorted_intervals = sorted(enumerate(self.intervals), key=lambda x: x[1][0])
        
        self._add_step(
            "SORT_START",
            {
                'original_count': len(self.intervals),
                'sorted_order': [idx for idx, _ in self.sorted_intervals]
            },
            f"📋 Sort {len(self.intervals)} meetings by start time"
        )

        # Process each meeting in sorted order
        for interval_id, interval in self.sorted_intervals:
            start, end = interval
            self.current_interval_id = interval_id

            # Check if we can reuse a room
            if self.heap:
                # Heap now contains (end_time, room_id) tuples
                earliest_end, earliest_room = self.heap[0]
                
                self._add_step(
                    "CHECK_EARLIEST_END",
                    {
                        'interval_id': interval_id,
                        'interval_start': start,
                        'interval_end': end,
                        'heap_top': earliest_end
                    },
                    f"🔍 Check if meeting {interval_id} [{start}, {end}] can reuse a room"
                )

                if start >= earliest_end:
                    # Reuse room - pop the earliest ending meeting
                    old_end, freed_room = heapq.heappop(self.heap)
                    
                    # CRITICAL FIX: Assign to the SPECIFIC room that was freed
                    room_number = freed_room
                    
                    self.room_assignments[interval_id] = room_number
                    heapq.heappush(self.heap, (end, room_number))
                    
                    self._add_step(
                        "ALLOCATE_ROOM",
                        {
                            'interval_id': interval_id,
                            'interval_start': start,
                            'interval_end': end,
                            'room_number': room_number,
                            'reused': True,
                            'old_heap_top': old_end,
                            'freed_room': freed_room  # NEW: Track which room was freed
                        },
                        f"♻️ Reuse room {room_number} for meeting {interval_id} (previous meeting ended at {old_end})"
                    )
                else:
                    # Need new room
                    self.rooms_used += 1
                    room_number = self.rooms_used
                    self.room_assignments[interval_id] = room_number
                    heapq.heappush(self.heap, (end, room_number))
                    
                    self._add_step(
                        "NEW_ROOM",
                        {
                            'interval_id': interval_id,
                            'interval_start': start,
                            'interval_end': end,
                            'room_number': room_number,
                            'heap_top': earliest_end,
                            'heap_empty': False
                        },
                        f"🆕 Allocate new room {room_number} for meeting {interval_id} (all rooms occupied)"
                    )
                    
                    self._add_step(
                        "UPDATE_HEAP",
                        {
                            'interval_id': interval_id,
                            'interval_end': end,
                            'heap_size': len(self.heap)
                        },
                        f"📊 Add end time {end} to heap (heap size: {len(self.heap)})"
                    )
            else:
                # First meeting - allocate first room
                self.rooms_used += 1
                room_number = self.rooms_used
                self.room_assignments[interval_id] = room_number
                heapq.heappush(self.heap, (end, room_number))
                
                self._add_step(
                    "NEW_ROOM",
                    {
                        'interval_id': interval_id,
                        'interval_start': start,
                        'interval_end': end,
                        'room_number': room_number,
                        'heap_empty': True
                    },
                    f"🆕 Allocate first room {room_number} for meeting {interval_id}"
                )
                
                self._add_step(
                    "UPDATE_HEAP",
                    {
                        'interval_id': interval_id,
                        'interval_end': end,
                        'heap_size': len(self.heap)
                    },
                    f"📊 Initialize heap with end time {end}"
                )

        self.current_interval_id = None

        return self._build_trace_result({
            'min_rooms': self.rooms_used,
            'room_assignments': dict(self.room_assignments)
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After checking the heap, will we reuse a room or allocate a new one?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after checking earliest end, before decision
            if step.type == "CHECK_EARLIEST_END" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                interval_start = step.data['interval_start']
                heap_top = step.data['heap_top']
                interval_id = step.data['interval_id']

                # Determine correct answer from next step type
                if next_step.type == "ALLOCATE_ROOM" and next_step.data.get('reused', False):
                    correct_answer = "reuse"
                elif next_step.type == "NEW_ROOM":
                    correct_answer = "new-room"
                else:
                    continue  # Skip if unexpected step type

                predictions.append({
                    'step_index': i,
                    'question': f"Meeting {interval_id} starts at {interval_start}. Earliest ending meeting finishes at {heap_top}. What happens next?",
                    'choices': [
                        {'id': 'reuse', 'label': f'Reuse a room (start ≥ earliest end)'},
                        {'id': 'new-room', 'label': f'Allocate new room (start < earliest end)'},
                        {'id': 'skip', 'label': 'Skip this meeting'}
                    ],
                    'hint': f"Compare start time ({interval_start}) with earliest end time ({heap_top})",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(interval_start, heap_top, correct_answer)
                })

        return predictions

    def _get_prediction_explanation(self, start: int, heap_top: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "reuse":
            return f"{start} ≥ {heap_top}, so the earliest meeting has finished. We can reuse its room."
        elif answer == "new-room":
            return f"{start} < {heap_top}, so the earliest meeting is still ongoing. All rooms are occupied, need a new room."
        return ""