"""
Merge Intervals algorithm tracer for educational visualization.

Implements interval merging with complete trace generation for step-by-step
visualization on a timeline. Sorts intervals by start time, then merges
overlapping intervals by comparing each interval with the last merged interval.

VERSION: 2.2 - Bug Fix: Mutable Reference in Trace Data
- FIXED: Line 395 - Create copy of last_merged to prevent retroactive mutation
- Previous bug: Trace recorded reference to list that was later mutated
- Impact: Step 1 showed post-merge state ([1,6]) instead of pre-merge state ([1,3])
"""

from typing import Any, List, Dict

try:
    from .base_tracer import AlgorithmTracer
except ImportError:
    # For standalone testing
    from algorithms.base_tracer import AlgorithmTracer


class MergeIntervalsTracer(AlgorithmTracer):
    """
    Tracer for Merge Intervals algorithm on timeline data.

    Visualization shows:
    - All intervals with states (pending, examining, merged, new_interval)
    - Call stack showing merge decisions
    - Timeline axis with merged result building progressively

    Prediction points ask: "Will this interval merge with the last one or start new?"
    """

    def __init__(self):
        super().__init__()
        self.intervals = []
        self.sorted_intervals = []
        self.merged = []
        self.current_interval = None
        self.current_index = None

    def _get_visualization_state(self) -> dict:
        """
        Return current timeline state with interval states and call stack.

        Interval states:
        - 'pending': Not yet examined
        - 'examining': Currently being compared
        - 'merged': Merged into existing interval
        - 'new_interval': Added as new interval to result
        """
        if not self.sorted_intervals:
            return {}

        # Build all_intervals with current states
        all_intervals = []
        for i, interval in enumerate(self.sorted_intervals):
            interval_id = i + 1
            start, end = interval

            # Determine state
            if self.current_index is not None and i == self.current_index:
                state = 'examining'
            elif i < (self.current_index if self.current_index is not None else 0):
                # Already processed
                state = 'merged' if self._was_merged(i) else 'new_interval'
            else:
                state = 'pending'

            all_intervals.append({
                'id': interval_id,
                'start': start,
                'end': end,
                'state': state
            })

        # Build call stack state
        call_stack_state = []
        if self.current_interval is not None:
            call_stack_state.append({
                'interval_id': self.current_index + 1,
                'type': 'EXAMINING',
                'interval': self.current_interval
            })

        return {
            'all_intervals': all_intervals,
            'call_stack_state': call_stack_state,
            'merged_count': len(self.merged),
            'pending_count': len(self.sorted_intervals) - (self.current_index + 1 if self.current_index is not None else 0)
        }

    def _was_merged(self, index: int) -> bool:
        """Check if interval at index was merged (not added as new)."""
        # This is a helper for visualization state determination
        # An interval was merged if it's not the first and overlapped with previous
        if index == 0:
            return False
        
        # Check if this interval's end is part of a merged interval
        interval = self.sorted_intervals[index]
        # If merged list has fewer intervals than processed, some were merged
        processed_count = index + 1
        return len(self.merged) < processed_count

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Merge Intervals trace.

        Shows complete execution flow with all decision data visible.
        Updated to include Frontend Visualization Hints (Backend Checklist v2.2).

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        # Extract input size from metadata (set during execute)
        input_size = metadata.get('input_size', 0)
        
        narrative = "# Merge Intervals Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Intervals:** {input_size} intervals\n"
        narrative += f"**Result:** {len(result['merged_intervals'])} merged intervals\n"
        narrative += f"**Merges Performed:** {result['merge_count']}\n\n"
        narrative += "---\n\n"

        # Step-by-step narrative
        for step in steps:
            step_num = step['step']
            step_type = step['type']
            description = step['description']
            data = step['data']

            narrative += f"## Step {step_num}: {description}\n\n"

            # Type-specific details
            if step_type == "SORT_INTERVALS":
                original = data['original_intervals']
                sorted_intervals = data['sorted_intervals']

                narrative += f"**Original Intervals (unsorted):**\n"
                for i, interval in enumerate(original, 1):
                    narrative += f"- Interval {i}: [{interval[0]}, {interval[1]}]\n"
                narrative += "\n"

                narrative += f"**After Sorting by Start Time:**\n"
                for i, interval in enumerate(sorted_intervals, 1):
                    narrative += f"- Interval {i}: [{interval[0]}, {interval[1]}]\n"
                narrative += "\n"

                narrative += "**Why Sort?** Sorting by start time ensures we process intervals in chronological order, "
                narrative += "making it easy to detect overlaps by comparing each interval with the last merged interval.\n\n"

                # Show visualization state
                if 'visualization' in data:
                    viz = data['visualization']
                    narrative += f"**Timeline State:**\n"
                    narrative += f"- Total intervals: {len(sorted_intervals)}\n"
                    narrative += f"- Merged so far: {viz['merged_count']}\n"
                    narrative += f"- Pending: {viz['pending_count']}\n\n"

            elif step_type == "COMPARE_OVERLAP":
                current = data['current_interval']
                last_merged = data['last_merged']
                current_start = current[0]
                last_end = last_merged[1]
                overlaps = data['overlaps']

                narrative += f"**Current Interval:** [{current[0]}, {current[1]}]\n"
                narrative += f"**Last Merged Interval:** [{last_merged[0]}, {last_merged[1]}]\n\n"

                narrative += f"**Overlap Check:**\n"
                narrative += f"```\n"
                narrative += f"Compare current.start ({current_start}) with last_merged.end ({last_end})\n"
                narrative += f"{current_start} <= {last_end}? → {overlaps}\n"
                narrative += f"```\n\n"

                if overlaps:
                    narrative += f"**Decision:** Intervals **overlap** because current starts ({current_start}) "
                    narrative += f"before or when last ends ({last_end})\n"
                    narrative += f"- Action: Merge by extending the last interval's end time\n\n"
                else:
                    narrative += f"**Decision:** Intervals **do not overlap** because current starts ({current_start}) "
                    narrative += f"after last ends ({last_end})\n"
                    narrative += f"- Action: Add current interval as new separate interval\n\n"

                # Show visualization state
                if 'visualization' in data:
                    viz = data['visualization']
                    narrative += f"**Timeline State:**\n"
                    narrative += f"- Merged so far: {viz['merged_count']}\n"
                    narrative += f"- Pending: {viz['pending_count']}\n\n"

            elif step_type == "MERGE":
                current = data['current_interval']
                old_last = data['old_last_merged']
                new_end = data['new_end']
                calculation = data['calculation']

                narrative += f"**Merging Intervals:**\n"
                narrative += f"- Current interval: [{current[0]}, {current[1]}]\n"
                narrative += f"- Last merged (before): [{old_last[0]}, {old_last[1]}]\n\n"

                narrative += f"**End Time Calculation:**\n"
                narrative += f"```\n"
                narrative += f"{calculation}\n"
                narrative += f"```\n\n"

                narrative += f"**Result:**\n"
                narrative += f"- Last merged (after): [{old_last[0]}, {new_end}]\n"
                narrative += f"- The last interval now spans from {old_last[0]} to {new_end}\n\n"

                narrative += f"**Why max()?** We take the maximum of the two end times to ensure the merged interval "
                narrative += f"covers both original intervals completely. If current interval is fully enclosed "
                narrative += f"(ends before last ends), we keep the larger end time.\n\n"

            elif step_type == "ADD_NEW":
                current = data['current_interval']

                narrative += f"**Adding New Interval:**\n"
                narrative += f"- Interval: [{current[0]}, {current[1]}]\n"
                narrative += f"- This interval does not overlap with the last merged interval\n"
                narrative += f"- Added as separate interval to result\n\n"

            narrative += "---\n\n"

        # Execution summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Input:** {input_size} intervals\n"
        narrative += f"**Output:** {len(result['merged_intervals'])} merged intervals\n"
        narrative += f"**Merges Performed:** {result['merge_count']}\n\n"

        narrative += f"**Final Merged Intervals:**\n"
        for i, interval in enumerate(result['merged_intervals'], 1):
            narrative += f"- Interval {i}: [{interval[0]}, {interval[1]}]\n"
        narrative += "\n"

        narrative += f"**Performance:**\n"
        narrative += f"- Time Complexity: O(n log n) - dominated by sorting\n"
        narrative += f"- Space Complexity: O(n) - for storing merged result\n"
        narrative += f"- Merge operations: {result['merge_count']} (out of {input_size - 1} possible)\n\n"

        narrative += "---\n\n"

        # Frontend Visualization Hints
        narrative += "## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Merged Count** (`merged_count`) - Shows progressive building of result\n"
        narrative += "- **Pending Count** (`pending_count`) - Shows remaining work\n"
        narrative += "- **Overlap Comparisons** - The critical decision point (current.start vs last.end)\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Timeline axis** - Show intervals as horizontal bars on a time axis (0-24 hours)\n"
        narrative += "2. **Highlight examining interval** - Use distinct color for `examining` state\n"
        narrative += "3. **Show merge animation** - When intervals merge, animate the extension of last interval's end\n"
        narrative += "4. **Distinguish merged vs new** - Use different colors for `merged` vs `new_interval` states\n"
        narrative += "5. **Call stack visualization** - Show which interval is currently being examined\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.all_intervals[*].id\n"
        narrative += "step.data.visualization.all_intervals[*].start\n"
        narrative += "step.data.visualization.all_intervals[*].end\n"
        narrative += "step.data.visualization.all_intervals[*].state  // 'pending' | 'examining' | 'merged' | 'new_interval'\n"
        narrative += "step.data.visualization.call_stack_state[*].interval_id\n"
        narrative += "step.data.visualization.call_stack_state[*].type\n"
        narrative += "step.data.visualization.merged_count\n"
        narrative += "step.data.visualization.pending_count\n"
        narrative += "step.data.current_interval  // [start, end] being examined\n"
        narrative += "step.data.last_merged  // [start, end] of last merged interval\n"
        narrative += "step.data.overlaps  // boolean - critical decision\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Merge Intervals is fundamentally about **temporal overlap detection**. The most important "
        narrative += "visualization is the **timeline itself** - showing intervals as horizontal bars makes overlaps "
        narrative += "visually obvious. The key pedagogical moment is the **comparison step** (current.start <= last.end) "
        narrative += "- this should be highlighted with visual indicators showing the two values being compared. "
        narrative += "When a merge happens, animate the **extension** of the last interval's end time to show how "
        narrative += "the intervals combine. Use color coding to show the **state progression**: pending (gray) → "
        narrative += "examining (yellow) → merged (green) or new_interval (blue). The call stack visualization helps "
        narrative += "students track which interval is currently being processed. Consider showing a **before/after "
        narrative += "comparison** for merge operations to emphasize the transformation.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute merge intervals algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'intervals': List of [start, end] pairs (integers)

        Returns:
            Standardized trace result with:
                - result: {'merged_intervals': List[[start, end]], 'merge_count': int}
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='timeline'

        Raises:
            ValueError: If input is invalid or intervals violate constraints
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if 'intervals' not in input_data:
            raise ValueError("Input must contain 'intervals' key")

        self.intervals = input_data['intervals']

        if not self.intervals:
            raise ValueError("Intervals list cannot be empty")

        # Validate each interval
        for interval in self.intervals:
            if not isinstance(interval, (list, tuple)) or len(interval) != 2:
                raise ValueError("Each interval must be a list/tuple of [start, end]")
            start, end = interval
            if not isinstance(start, int) or not isinstance(end, int):
                raise ValueError("Interval start and end must be integers")
            if start > end:
                raise ValueError(f"Invalid interval [{start}, {end}]: start must be <= end")

        # Initialize state
        self.sorted_intervals = []
        self.merged = []
        self.current_interval = None
        self.current_index = None
        merge_count = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'merge-intervals',
            'display_name': 'Merge Intervals',
            'visualization_type': 'timeline',
            'visualization_config': {
                'show_merged': True,
                'show_axis': True,
                'axis_range': [0, 24]
            },
            'input_size': len(self.intervals)
        }

        # Step 1: Sort intervals by start time
        self.sorted_intervals = sorted(self.intervals, key=lambda x: x[0])

        self._add_step(
            "SORT_INTERVALS",
            {
                'original_intervals': self.intervals,
                'sorted_intervals': self.sorted_intervals
            },
            f"📊 Sort {len(self.intervals)} intervals by start time"
        )

        # Initialize merged list with first interval
        self.merged = [list(self.sorted_intervals[0])]

        # Step 2: Process each interval
        for i in range(1, len(self.sorted_intervals)):
            self.current_index = i
            self.current_interval = self.sorted_intervals[i]
            current_start, current_end = self.current_interval
            # BUG FIX: Create copy to prevent retroactive mutation in trace data
            last_merged = list(self.merged[-1])
            last_start, last_end = last_merged

            # Check for overlap
            overlaps = current_start <= last_end

            self._add_step(
                "COMPARE_OVERLAP",
                {
                    'current_interval': self.current_interval,
                    'last_merged': last_merged,
                    'overlaps': overlaps,
                    'comparison': f"{current_start} <= {last_end}"
                },
                f"🔍 Compare interval [{current_start}, {current_end}] with last merged [{last_start}, {last_end}]"
            )

            if overlaps:
                # Merge: extend the end of last merged interval
                old_last = list(last_merged)
                new_end = max(last_end, current_end)
                self.merged[-1][1] = new_end
                merge_count += 1

                self._add_step(
                    "MERGE",
                    {
                        'current_interval': self.current_interval,
                        'old_last_merged': old_last,
                        'new_end': new_end,
                        'calculation': f"new_end = max({last_end}, {current_end}) = {new_end}"
                    },
                    f"🔗 Merge: Extend last interval to [{last_start}, {new_end}]"
                )
            else:
                # No overlap: add as new interval
                self.merged.append(list(self.current_interval))

                self._add_step(
                    "ADD_NEW",
                    {
                        'current_interval': self.current_interval
                    },
                    f"➕ Add new interval [{current_start}, {current_end}] (no overlap)"
                )

        # Mark processing complete
        self.current_index = None
        self.current_interval = None

        return self._build_trace_result({
            'merged_intervals': self.merged,
            'merge_count': merge_count
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After comparing current interval with last merged,
        will they merge or will current be added as new interval?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after COMPARE_OVERLAP, before decision
            if step.type == "COMPARE_OVERLAP" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                current = step.data['current_interval']
                last_merged = step.data['last_merged']
                overlaps = step.data['overlaps']

                # Determine correct answer from next step type
                if next_step.type == "MERGE":
                    correct_answer = "merge"
                elif next_step.type == "ADD_NEW":
                    correct_answer = "add-new"
                else:
                    continue  # Skip if unexpected step type

                predictions.append({
                    'step_index': i,
                    'question': f"Interval [{current[0]}, {current[1]}] vs last merged [{last_merged[0]}, {last_merged[1]}]. What happens next?",
                    'choices': [
                        {'id': 'merge', 'label': f'Merge (extend last interval)'},
                        {'id': 'add-new', 'label': f'Add as new interval'},
                        {'id': 'skip', 'label': f'Skip this interval'}
                    ],
                    'hint': f"Compare current.start ({current[0]}) with last_merged.end ({last_merged[1]})",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(current, last_merged, overlaps)
                })

        return predictions

    def _get_prediction_explanation(self, current: List[int], last_merged: List[int], overlaps: bool) -> str:
        """Generate explanation for prediction answer."""
        current_start = current[0]
        last_end = last_merged[1]
        
        if overlaps:
            return (f"Intervals overlap because current.start ({current_start}) <= last_merged.end ({last_end}). "
                    f"We merge by extending the last interval's end time to cover both intervals.")
        else:
            return (f"Intervals do not overlap because current.start ({current_start}) > last_merged.end ({last_end}). "
                    f"We add current as a new separate interval.")