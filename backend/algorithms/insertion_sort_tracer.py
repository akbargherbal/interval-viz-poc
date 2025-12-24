"""
Insertion Sort algorithm tracer for educational visualization.

Implements insertion sort with complete trace generation for step-by-step
visualization and prediction mode. Builds sorted array one element at a time
by inserting each element into its correct position in the sorted portion.

VERSION: 2.1 - Backend Checklist v2.2 Compliance
- Added Frontend Visualization Hints section to narrative
- Follows Universal Pedagogical Principles
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class InsertionSortTracer(AlgorithmTracer):
    """
    Tracer for Insertion Sort algorithm.

    Visualization shows:
    - Array elements with states (sorted, examining, shifting, inserting)
    - Current key being inserted
    - Sorted region growing from left to right
    - Shift operations as elements make room for key

    Prediction points ask: "Will the key be inserted here, or do we shift more?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.current_index = None
        self.key_value = None
        self.compare_index = None
        self.sorted_boundary = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states and key position.

        Element states:
        - 'sorted': In sorted portion (left of current_index)
        - 'examining': Current key being inserted
        - 'comparing': Element being compared with key
        - 'shifting': Element being shifted right
        - 'unsorted': Not yet processed
        """
        if not self.array:
            return {}

        return {
            'array': [
                {
                    'index': i,
                    'value': v,
                    'state': self._get_element_state(i)
                }
                for i, v in enumerate(self.array)
            ],
            'key': {
                'index': self.current_index,
                'value': self.key_value
            } if self.key_value is not None else None,
            'sorted_boundary': self.sorted_boundary,
            'compare_index': self.compare_index
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        if self.current_index is not None and index == self.current_index:
            return 'examining'
        if self.compare_index is not None and index == self.compare_index:
            return 'comparing'
        if index < self.sorted_boundary:
            return 'sorted'
        if self.current_index is not None and index < self.current_index:
            return 'sorted'
        return 'unsorted'

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Insertion Sort trace.

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
        narrative = "# Insertion Sort Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {result['original_array']}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Result:** Sorted array: {result['sorted_array']}\n"
        narrative += f"**Total Comparisons:** {result['comparisons']}\n"
        narrative += f"**Total Shifts:** {result['shifts']}\n\n"
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
            if step_type == "INITIAL_STATE":
                narrative += f"**Initial Configuration:**\n"
                narrative += f"- Array to sort: `{data['array']}`\n"
                narrative += f"- Array size: {data['array_size']} elements\n"
                narrative += f"- First element (index 0) is trivially sorted\n\n"

                narrative += "**Array Visualization:**\n```\n"
                narrative += "Index: " + " ".join(f"{i:3d}" for i in range(len(data['array']))) + "\n"
                narrative += "Value: " + " ".join(f"{v:3d}" for v in data['array']) + "\n"
                narrative += "State: " + "  S" + "   U" * (len(data['array']) - 1) + "\n"
                narrative += "       (S=Sorted, U=Unsorted)\n"
                narrative += "```\n"
                narrative += f"*Sorted region: **1 element** (index 0)*\n\n"

            elif step_type == "SELECT_KEY":
                key_index = data['key_index']
                key_value = data['key_value']
                sorted_count = data['sorted_count']

                narrative += f"**Key Selection:**\n"
                narrative += f"- Select element at index **{key_index}** as key\n"
                narrative += f"- Key value: **{key_value}**\n"
                narrative += f"- Current sorted region: indices [0, {sorted_count - 1}] ({sorted_count} elements)\n\n"

                narrative += f"**Goal:** Insert key ({key_value}) into correct position within sorted region\n\n"

                narrative += "**Current Array State:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"

                state_line = "State: "
                for elem in active_elements:
                    if elem['state'] == 'examining':
                        state_line += "  K"
                    elif elem['state'] == 'sorted':
                        state_line += "  S"
                    else:
                        state_line += "  U"
                narrative += state_line + "\n"
                narrative += "       (K=Key, S=Sorted, U=Unsorted)\n"
                narrative += "```\n\n"

            elif step_type == "COMPARE":
                key_value = data['key_value']
                compare_index = data['compare_index']
                compare_value = data['compare_value']
                comparison = data['comparison']
                decision = data['decision']

                narrative += f"**Comparison:**\n"
                narrative += f"```\n"
                narrative += f"key ({key_value}) < array[{compare_index}] ({compare_value})?\n"
                narrative += f"{key_value} < {compare_value} → {comparison}\n"
                narrative += f"```\n\n"

                if decision == "shift":
                    narrative += f"**Decision:** Key is **smaller** than array[{compare_index}]\n"
                    narrative += f"- Action: Shift array[{compare_index}] ({compare_value}) one position right\n"
                    narrative += f"- Continue comparing with previous elements\n\n"
                else:
                    narrative += f"**Decision:** Key is **not smaller** than array[{compare_index}]\n"
                    narrative += f"- Action: Found correct position for key\n"
                    narrative += f"- Key will be inserted after array[{compare_index}]\n\n"

                narrative += "**Array State After Comparison:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"

                state_line = "State: "
                for elem in active_elements:
                    if elem['state'] == 'examining':
                        state_line += "  K"
                    elif elem['state'] == 'comparing':
                        state_line += "  C"
                    elif elem['state'] == 'sorted':
                        state_line += "  S"
                    else:
                        state_line += "  U"
                narrative += state_line + "\n"
                narrative += "       (K=Key, C=Comparing, S=Sorted, U=Unsorted)\n"
                narrative += "```\n\n"

            elif step_type == "SHIFT":
                from_index = data['from_index']
                to_index = data['to_index']
                value = data['value']
                shifts_so_far = data['shifts_so_far']

                narrative += f"**Shift Operation:**\n"
                narrative += f"- Move array[{from_index}] ({value}) → array[{to_index}]\n"
                narrative += f"- This creates space for the key to be inserted\n"
                narrative += f"- Total shifts so far: {shifts_so_far}\n\n"

                narrative += "**Array State After Shift:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                narrative += "```\n\n"

            elif step_type == "INSERT":
                insert_index = data['insert_index']
                key_value = data['key_value']
                comparisons = data['comparisons']
                shifts = data['shifts']

                narrative += f"**Insertion:**\n"
                narrative += f"- Insert key ({key_value}) at index **{insert_index}**\n"
                narrative += f"- Key is now in correct sorted position\n"
                narrative += f"- Comparisons for this key: {comparisons}\n"
                narrative += f"- Shifts for this key: {shifts}\n\n"

                narrative += "**Array State After Insertion:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"

                state_line = "State: "
                for i, elem in enumerate(active_elements):
                    if i <= insert_index:
                        state_line += "  S"
                    else:
                        state_line += "  U"
                narrative += state_line + "\n"
                narrative += "       (S=Sorted, U=Unsorted)\n"
                narrative += "```\n"
                narrative += f"*Sorted region expanded: **{insert_index + 1} elements***\n\n"

            elif step_type == "COMPLETE":
                total_comparisons = data['total_comparisons']
                total_shifts = data['total_shifts']

                narrative += f"✅ **Sorting Complete!**\n\n"
                narrative += f"**Final Statistics:**\n"
                narrative += f"- Total comparisons: {total_comparisons}\n"
                narrative += f"- Total shifts: {total_shifts}\n"
                narrative += f"- All elements now in sorted order\n\n"

                narrative += "**Final Sorted Array:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                narrative += "State: " + "  S" * len(active_elements) + "\n"
                narrative += "       (All Sorted)\n"
                narrative += "```\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Original Array:** {result['original_array']}\n"
        narrative += f"**Sorted Array:** {result['sorted_array']}\n\n"

        narrative += f"**Performance Metrics:**\n"
        narrative += f"- Total Comparisons: {result['comparisons']}\n"
        narrative += f"- Total Shifts: {result['shifts']}\n"
        narrative += f"- Array Size: {len(result['sorted_array'])} elements\n\n"

        narrative += f"**Complexity Analysis:**\n"
        narrative += f"- Time Complexity: O(n²) worst case, O(n) best case (already sorted)\n"
        narrative += f"- Space Complexity: O(1) (in-place sorting)\n"
        narrative += f"- Stable: Yes (maintains relative order of equal elements)\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"

        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Sorted Boundary** (`sorted_boundary`) - Shows the growing sorted region from left to right\n"
        narrative += "- **Key Value** (`key.value`) - The element currently being inserted into sorted position\n"
        narrative += "- **Comparison Count** (`comparisons`) - Demonstrates how many comparisons needed for each insertion\n\n"

        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the sorted/unsorted boundary** - Use distinct visual separation between sorted (left) and unsorted (right) regions\n"
        narrative += "2. **Emphasize the key element** - The `examining` state is the element being inserted—make it visually prominent\n"
        narrative += "3. **Animate shift operations** - Show elements sliding right to make room for the key (smooth transitions)\n"
        narrative += "4. **Show comparison moments** - When `comparing` state is active, highlight both key and comparison element\n"
        narrative += "5. **Celebrate sorted region growth** - Each successful insertion expands the sorted region by one element\n\n"

        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.key.index\n"
        narrative += "step.data.visualization.key.value\n"
        narrative += "step.data.visualization.sorted_boundary\n"
        narrative += "step.data.visualization.compare_index\n"
        narrative += "step.data.visualization.array[*].state  // 'sorted' | 'examining' | 'comparing' | 'shifting' | 'unsorted'\n"
        narrative += "step.data.visualization.array[*].value\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "step.data.key_value  // Current key being inserted\n"
        narrative += "step.data.compare_value  // Value being compared with key\n"
        narrative += "```\n\n"

        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Insertion sort's pedagogical power comes from its **intuitive card-sorting metaphor**: "
        narrative += "imagine sorting a hand of playing cards by picking up one card at a time and inserting it into the correct position. "
        narrative += "The most important visualization is showing the **growing sorted region** (left side) and how each new element "
        narrative += "finds its place through comparisons and shifts. Use **spatial animation** to show elements sliding right during shifts—this "
        narrative += "makes the 'making room' concept concrete. The comparison moments are critical decision points: highlight both the key "
        narrative += "and the element it's being compared with. Color-code the sorted region distinctly (e.g., green gradient) to show progress. "
        narrative += "When the key finds its position, use a satisfying 'snap into place' animation. The algorithm's efficiency varies dramatically "
        narrative += "based on input: nearly-sorted arrays require few shifts (best case O(n)), while reverse-sorted arrays require maximum shifts "
        narrative += "(worst case O(n²)). Visualize this by showing shift counts per insertion—students will see why insertion sort excels on "
        narrative += "nearly-sorted data but struggles with reverse-sorted input.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute insertion sort algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers to sort

        Returns:
            Standardized trace result with:
                - result: {'sorted_array': list, 'original_array': list, 'comparisons': int, 'shifts': int}
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='array'

        Raises:
            ValueError: If input is invalid
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if 'array' not in input_data:
            raise ValueError("Input must contain 'array' key")

        original_array = input_data['array']

        if not isinstance(original_array, list):
            raise ValueError("Array must be a list")
        if len(original_array) < 2:
            raise ValueError("Array must contain at least 2 elements")

        # Create working copy
        self.array = original_array.copy()
        self.current_index = None
        self.key_value = None
        self.compare_index = None
        self.sorted_boundary = 1  # First element is trivially sorted

        total_comparisons = 0
        total_shifts = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'insertion-sort',
            'display_name': 'Insertion Sort',
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True,
                'highlight_sorted_region': True
            },
            'input_size': len(self.array)
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'array': self.array.copy(),
                'array_size': len(self.array)
            },
            f"🔢 Initial array with {len(self.array)} elements (first element trivially sorted)"
        )

        # Insertion sort algorithm
        for i in range(1, len(self.array)):
            # Select key
            self.current_index = i
            self.key_value = self.array[i]
            key_comparisons = 0
            key_shifts = 0

            self._add_step(
                "SELECT_KEY",
                {
                    'key_index': i,
                    'key_value': self.key_value,
                    'sorted_count': i
                },
                f"📌 Select key: array[{i}] = {self.key_value} (sorted region: {i} elements)"
            )

            # Compare and shift
            j = i - 1
            while j >= 0:
                self.compare_index = j
                compare_value = self.array[j]
                key_comparisons += 1
                total_comparisons += 1

                # Compare key with current element
                if self.key_value < compare_value:
                    # Need to shift
                    self._add_step(
                        "COMPARE",
                        {
                            'key_value': self.key_value,
                            'compare_index': j,
                            'compare_value': compare_value,
                            'comparison': f"{self.key_value} < {compare_value} = True",
                            'decision': 'shift'
                        },
                        f"🔍 Compare: {self.key_value} < {compare_value} → shift right"
                    )

                    # Shift element right
                    self.array[j + 1] = self.array[j]
                    key_shifts += 1
                    total_shifts += 1

                    self._add_step(
                        "SHIFT",
                        {
                            'from_index': j,
                            'to_index': j + 1,
                            'value': compare_value,
                            'shifts_so_far': total_shifts
                        },
                        f"➡️ Shift: array[{j}] ({compare_value}) → array[{j + 1}]"
                    )

                    j -= 1
                else:
                    # Found position
                    self._add_step(
                        "COMPARE",
                        {
                            'key_value': self.key_value,
                            'compare_index': j,
                            'compare_value': compare_value,
                            'comparison': f"{self.key_value} < {compare_value} = False",
                            'decision': 'insert'
                        },
                        f"🔍 Compare: {self.key_value} ≥ {compare_value} → found position"
                    )
                    break

            # Insert key at correct position
            insert_position = j + 1
            self.array[insert_position] = self.key_value

            self.sorted_boundary = i + 1
            
            # Clear compare index before insert step to ensure clean visualization
            self.compare_index = None

            self._add_step(
                "INSERT",
                {
                    'insert_index': insert_position,
                    'key_value': self.key_value,
                    'comparisons': key_comparisons,
                    'shifts': key_shifts
                },
                f"✅ Insert key ({self.key_value}) at index {insert_position} ({key_comparisons} comparisons, {key_shifts} shifts)"
            )

        # Sorting complete
        self.current_index = None
        self.key_value = None
        self.compare_index = None

        self._add_step(
            "COMPLETE",
            {
                'total_comparisons': total_comparisons,
                'total_shifts': total_shifts
            },
            f"🎉 Sorting complete! ({total_comparisons} comparisons, {total_shifts} shifts)"
        )

        return self._build_trace_result({
            'sorted_array': self.array.copy(),
            'original_array': original_array,
            'comparisons': total_comparisons,
            'shifts': total_shifts
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After comparing key with current element, will we
        shift the element right, or insert the key here?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after comparison, before decision
            if step.type == "COMPARE" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                key_value = step.data['key_value']
                compare_value = step.data['compare_value']
                compare_index = step.data['compare_index']

                # Determine correct answer from next step type
                if next_step.type == "SHIFT":
                    correct_answer = "shift"
                elif next_step.type == "INSERT":
                    correct_answer = "insert"
                else:
                    continue  # Skip if unexpected step type

                predictions.append({
                    'step_index': i,
                    'question': f"Key ({key_value}) vs array[{compare_index}] ({compare_value}). What happens next?",
                    'choices': [
                        {'id': 'shift', 'label': f'Shift {compare_value} right (key < {compare_value})'},
                        {'id': 'insert', 'label': f'Insert key here (key ≥ {compare_value})'},
                        {'id': 'continue', 'label': 'Continue without action'}
                    ],
                    'hint': f"Compare {key_value} with {compare_value}",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(key_value, compare_value, correct_answer)
                })

        return predictions

    def _get_prediction_explanation(self, key_value: int, compare_value: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "shift":
            return f"{key_value} < {compare_value}, so we shift {compare_value} right to make room for the key"
        elif answer == "insert":
            return f"{key_value} ≥ {compare_value}, so we've found the correct position—insert key here"
        return ""