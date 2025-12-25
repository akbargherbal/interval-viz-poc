"""
Bubble Sort algorithm tracer for educational visualization.

Implements bubble sort with complete trace generation for step-by-step
visualization and prediction mode. Shows comparison-swap logic and
progressive sorting from right to left.

VERSION: 2.2 - Backend Checklist v2.2 Compliance
- Universal Pedagogical Principles applied
- Frontend Visualization Hints section included
- Result field traceability implemented
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class BubbleSortTracer(AlgorithmTracer):
    """
    Tracer for Bubble Sort algorithm on integer arrays.

    Visualization shows:
    - Array elements with states (unsorted, comparing, swapped, sorted)
    - Current comparison pair indices
    - Sorted tail boundary (grows from right to left)
    - Pass-by-pass progress

    Prediction points ask: "Will these two elements be swapped?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.n = 0
        self.sorted_boundary = None  # Index where sorted tail begins
        self.current_pass = 0
        self.comparing_indices = None  # (i, i+1) tuple
        self.total_comparisons = 0
        self.total_swaps = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states and comparison pointers.

        Element states:
        - 'sorted': In the sorted tail (index >= sorted_boundary)
        - 'comparing': Currently being compared (at comparing_indices)
        - 'unsorted': Not yet sorted, not currently comparing
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
            'comparing_indices': self.comparing_indices,
            'sorted_boundary': self.sorted_boundary,
            'current_pass': self.current_pass,
            'comparisons': self.total_comparisons,
            'swaps': self.total_swaps
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        # Sorted tail (from sorted_boundary to end)
        if self.sorted_boundary is not None and index >= self.sorted_boundary:
            return 'sorted'
        
        # Currently comparing
        if self.comparing_indices is not None:
            if index in self.comparing_indices:
                return 'comparing'
        
        # Default: unsorted
        return 'unsorted'

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Bubble Sort trace.

        Shows complete execution flow with all decision data visible.
        Follows Universal Pedagogical Principles and Backend Checklist v2.2.

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Bubble Sort Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {result['original_array']}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Result:** Sorted array: {result['sorted_array']}\n"
        narrative += f"**Total Comparisons:** {result['comparisons']}\n"
        narrative += f"**Total Swaps:** {result['swaps']}\n\n"
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
                narrative += f"- Strategy: Bubble largest elements to the right through adjacent comparisons\n\n"

                narrative += "**Array Visualization:**\n```\n"
                narrative += "Index: " + " ".join(f"{i:3d}" for i in range(len(viz['array']))) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                narrative += "State: " + " ".join("  U" for _ in viz['array']) + "  (U = Unsorted)\n"
                narrative += "```\n\n"

                narrative += "**Algorithm Overview:**\n"
                narrative += "Bubble Sort works by repeatedly comparing adjacent elements and swapping them if they're in the wrong order. "
                narrative += "Each complete pass through the array \"bubbles\" the largest unsorted element to its correct position at the end. "
                narrative += "The sorted region grows from right to left.\n\n"

            elif step_type == "PASS_COMPLETE":
                pass_num = data['pass_number']
                sorted_boundary = data['sorted_boundary']
                swaps_in_pass = data['swaps_in_pass']

                narrative += f"**Pass {pass_num} Summary:**\n"
                narrative += f"- Swaps performed: {swaps_in_pass}\n"
                narrative += f"- Sorted boundary: index {sorted_boundary} (elements from {sorted_boundary} to end are now sorted)\n"
                narrative += f"- Total comparisons so far: {viz['comparisons']}\n"
                narrative += f"- Total swaps so far: {viz['swaps']}\n\n"

                if swaps_in_pass == 0:
                    narrative += "🎯 **Early Termination Triggered!**\n"
                    narrative += "No swaps occurred in this pass, meaning the array is already sorted. "
                    narrative += "We can stop early instead of continuing unnecessary passes.\n\n"

                narrative += "**Current Array State:**\n```\n"
                narrative += "Index: " + " ".join(f"{i:3d}" for i in range(len(viz['array']))) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                
                # Show state markers
                state_line = "State: "
                for elem in viz['array']:
                    if elem['state'] == 'sorted':
                        state_line += "  S"
                    else:
                        state_line += "  U"
                narrative += state_line + "  (S = Sorted, U = Unsorted)\n"
                narrative += "```\n\n"

            elif step_type == "COMPARE":
                i = data['index_i']
                j = data['index_j']
                val_i = data['value_i']
                val_j = data['value_j']
                comparison = data['comparison']

                narrative += f"**Comparison:**\n"
                narrative += f"- Position {i}: value = {val_i}\n"
                narrative += f"- Position {j}: value = {val_j}\n"
                narrative += f"- Check: `{comparison}`\n\n"

                narrative += f"**Decision Logic:**\n"
                narrative += f"Compare arr[{i}] ({val_i}) with arr[{j}] ({val_j}):\n"
                narrative += f"- IF {val_i} > {val_j}: Swap (wrong order, larger value should be on right)\n"
                narrative += f"- ELSE: No swap (correct order, continue)\n\n"

                narrative += "**Current Comparison Visualization:**\n```\n"
                # Show complete array to maintain arithmetic consistency
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in viz['array']) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                
                # Show comparison pointers
                pointer_line = "       "
                for elem in viz['array']:
                    if elem['index'] == i:
                        pointer_line += "  ^"
                    elif elem['index'] == j:
                        pointer_line += "  ^"
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                
                label_line = "       "
                for elem in viz['array']:
                    if elem['index'] == i:
                        label_line += "  L"
                    elif elem['index'] == j:
                        label_line += "  R"
                    else:
                        label_line += "   "
                narrative += label_line + "  (L = Left, R = Right in comparison)\n"
                narrative += "```\n\n"

            elif step_type == "SWAP":
                i = data['index_i']
                j = data['index_j']
                val_i = data['value_i']
                val_j = data['value_j']

                narrative += f"**Swap Performed:**\n"
                narrative += f"- Positions: {i} ↔ {j}\n"
                narrative += f"- Values: {val_i} ↔ {val_j}\n"
                narrative += f"- Reason: {val_i} > {val_j} (larger value moves right)\n\n"

                narrative += f"**Array Transformation:**\n"
                narrative += f"- Before swap: arr[{i}] = {val_i}, arr[{j}] = {val_j}\n"
                narrative += f"- After swap: arr[{i}] = {val_j}, arr[{j}] = {val_i}\n"
                narrative += f"- Total swaps: {viz['swaps']}\n\n"

                narrative += "**Updated Array:**\n```\n"
                narrative += "Index: " + " ".join(f"{i:3d}" for i in range(len(viz['array']))) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                narrative += "```\n\n"

            elif step_type == "NO_SWAP":
                i = data['index_i']
                j = data['index_j']
                val_i = data['value_i']
                val_j = data['value_j']

                narrative += f"**No Swap Needed:**\n"
                narrative += f"- Positions: {i}, {j}\n"
                narrative += f"- Values: {val_i}, {val_j}\n"
                narrative += f"- Reason: {val_i} ≤ {val_j} (already in correct order)\n\n"

                narrative += f"**Decision:**\n"
                narrative += f"Since arr[{i}] ({val_i}) ≤ arr[{j}] ({val_j}), these elements are already in the correct relative order. "
                narrative += f"No swap is needed. Continue to next pair.\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Final Result:** {result['sorted_array']}\n\n"
        
        narrative += f"**Performance Metrics:**\n"
        narrative += f"- Total comparisons: {result['comparisons']}\n"
        narrative += f"- Total swaps: {result['swaps']}\n"
        narrative += f"- Passes completed: {result['passes']}\n"
        narrative += f"- Array size: {len(result['sorted_array'])} elements\n\n"

        narrative += f"**Complexity Analysis:**\n"
        narrative += f"- Time Complexity: O(n²) worst/average case, O(n) best case (already sorted)\n"
        narrative += f"- Space Complexity: O(1) (in-place sorting)\n"
        narrative += f"- Stability: Stable (equal elements maintain relative order)\n\n"

        narrative += f"**Algorithm Behavior:**\n"
        if result['swaps'] == 0:
            narrative += f"The array was already sorted! Early termination saved unnecessary comparisons.\n"
        else:
            narrative += f"The algorithm performed {result['swaps']} swaps across {result['passes']} passes to sort the array. "
            narrative += f"Each pass bubbled the largest unsorted element to its correct position at the end.\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "\n---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Sorted Boundary** (`sorted_boundary`) - Shows the growing sorted region from right to left\n"
        narrative += "- **Comparison Count** (`comparisons`) - Demonstrates O(n²) behavior in real-time\n"
        narrative += "- **Swap Count** (`swaps`) - Shows actual work being done (0 swaps = already sorted)\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the sorted tail** - Use distinct color for `sorted` state elements (right side of array)\n"
        narrative += "2. **Animate comparisons** - The `comparing` state shows the active pair being evaluated\n"
        narrative += "3. **Emphasize swaps** - When elements swap, use smooth animation to show the exchange\n"
        narrative += "4. **Show pass completion** - Visual indicator when sorted_boundary moves left (one more element sorted)\n"
        narrative += "5. **Celebrate early termination** - If a pass has 0 swaps, highlight that optimization kicked in\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.comparing_indices  // [i, i+1] tuple or null\n"
        narrative += "step.data.visualization.sorted_boundary    // Index where sorted region begins\n"
        narrative += "step.data.visualization.current_pass       // Which pass through array (1-indexed)\n"
        narrative += "step.data.visualization.comparisons        // Running total of comparisons\n"
        narrative += "step.data.visualization.swaps              // Running total of swaps\n"
        narrative += "step.data.visualization.array[*].state     // 'unsorted' | 'comparing' | 'sorted'\n"
        narrative += "step.data.visualization.array[*].value\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Bubble Sort's defining characteristic is the **growing sorted region from right to left**. "
        narrative += "This is pedagogically crucial - students should see that each pass guarantees one more element "
        narrative += "is in its final sorted position. The `sorted_boundary` moving leftward is the visual proof of progress. "
        narrative += "The comparison pairs (`comparing_indices`) should be highlighted as they march left-to-right through "
        narrative += "the unsorted region. When a swap occurs, animate it clearly - this is the \"bubble\" action that gives "
        narrative += "the algorithm its name. The early termination optimization (when `swaps_in_pass = 0`) is a key teaching "
        narrative += "moment - show that the algorithm is smart enough to detect when work is done. Consider using a "
        narrative += "**color gradient** for the sorted tail to emphasize the progressive nature of the sort.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute bubble sort algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers to sort

        Returns:
            Standardized trace result with:
                - result: {
                    'sorted_array': List[int],
                    'original_array': List[int],
                    'comparisons': int,
                    'swaps': int,
                    'passes': int
                  }
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
        if not all(isinstance(x, int) for x in original_array):
            raise ValueError("Array must contain only integers")

        # Initialize
        self.array = original_array.copy()  # Work on a copy
        self.n = len(self.array)
        self.sorted_boundary = self.n  # Initially, no elements are sorted
        self.current_pass = 0
        self.comparing_indices = None
        self.total_comparisons = 0
        self.total_swaps = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'bubble-sort',
            'display_name': 'Bubble Sort',
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True,
                'highlight_sorted_tail': True,
                'state_colors': {
                    'unsorted': 'gray',
                    'comparing': 'yellow',
                    'sorted': 'green'
                }
            },
            'input_size': self.n
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'array': self.array.copy(),
                'array_size': self.n
            },
            f"🔢 Starting Bubble Sort on array of {self.n} elements"
        )

        # Bubble sort algorithm with optimization
        for pass_num in range(self.n - 1):
            self.current_pass = pass_num + 1
            swaps_in_pass = 0
            
            # One pass through the unsorted portion
            for i in range(self.n - 1 - pass_num):
                j = i + 1
                self.comparing_indices = (i, j)
                
                # Compare adjacent elements
                self.total_comparisons += 1
                
                self._add_step(
                    "COMPARE",
                    {
                        'index_i': i,
                        'index_j': j,
                        'value_i': self.array[i],
                        'value_j': self.array[j],
                        'comparison': f"{self.array[i]} > {self.array[j]}"
                    },
                    f"🔍 Compare arr[{i}] ({self.array[i]}) with arr[{j}] ({self.array[j]})"
                )
                
                # Swap if out of order
                if self.array[i] > self.array[j]:
                    # Record values before swap
                    val_i = self.array[i]
                    val_j = self.array[j]
                    
                    # Perform swap
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    self.total_swaps += 1
                    swaps_in_pass += 1
                    
                    self._add_step(
                        "SWAP",
                        {
                            'index_i': i,
                            'index_j': j,
                            'value_i': val_i,
                            'value_j': val_j
                        },
                        f"🔄 Swap arr[{i}] ({val_i}) ↔ arr[{j}] ({val_j})"
                    )
                else:
                    self._add_step(
                        "NO_SWAP",
                        {
                            'index_i': i,
                            'index_j': j,
                            'value_i': self.array[i],
                            'value_j': self.array[j]
                        },
                        f"✓ No swap needed: {self.array[i]} ≤ {self.array[j]}"
                    )
            
            # Pass complete - update sorted boundary
            self.sorted_boundary = self.n - 1 - pass_num
            self.comparing_indices = None
            
            self._add_step(
                "PASS_COMPLETE",
                {
                    'pass_number': self.current_pass,
                    'sorted_boundary': self.sorted_boundary,
                    'swaps_in_pass': swaps_in_pass
                },
                f"✅ Pass {self.current_pass} complete: {swaps_in_pass} swaps, sorted boundary at index {self.sorted_boundary}"
            )
            
            # Early termination optimization
            if swaps_in_pass == 0:
                # Array is already sorted
                break

        return self._build_trace_result({
            'sorted_array': self.array.copy(),
            'original_array': original_array,
            'comparisons': self.total_comparisons,
            'swaps': self.total_swaps,
            'passes': self.current_pass
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After comparing these two adjacent elements,
        will they be swapped or not?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after COMPARE, before decision
            if step.type == "COMPARE" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                
                val_i = step.data['value_i']
                val_j = step.data['value_j']
                idx_i = step.data['index_i']
                idx_j = step.data['index_j']
                
                # Determine correct answer from next step type
                if next_step.type == "SWAP":
                    correct_answer = "swap"
                elif next_step.type == "NO_SWAP":
                    correct_answer = "no-swap"
                else:
                    continue  # Skip if unexpected step type

                predictions.append({
                    'step_index': i,
                    'question': f"Compare arr[{idx_i}] = {val_i} with arr[{idx_j}] = {val_j}. Will they be swapped?",
                    'choices': [
                        {'id': 'swap', 'label': f'Yes, swap ({val_i} > {val_j})'},
                        {'id': 'no-swap', 'label': f'No, keep order ({val_i} ≤ {val_j})'}
                    ],
                    'hint': f"Bubble sort swaps if left element > right element",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(val_i, val_j, correct_answer)
                })

        return predictions

    def _get_prediction_explanation(self, val_i: int, val_j: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "swap":
            return f"{val_i} > {val_j}, so they are out of order. Swap to move the larger value ({val_i}) to the right."
        elif answer == "no-swap":
            return f"{val_i} ≤ {val_j}, so they are already in correct order. No swap needed."
        return ""