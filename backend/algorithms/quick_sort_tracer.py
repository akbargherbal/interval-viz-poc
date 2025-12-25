"""
Quick Sort algorithm tracer for educational visualization.

Implements Quick Sort using Lomuto partition scheme with complete
trace generation for step-by-step visualization and prediction mode.

VERSION: 2.5 - Backend Checklist v2.2 Compliance
- Added Frontend Visualization Hints section to narrative
- Follows Universal Pedagogical Principles
- Shows explicit arithmetic and comparisons
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class QuickSortTracer(AlgorithmTracer):
    """
    Tracer for Quick Sort algorithm using Lomuto partition scheme.

    Visualization shows:
    - Array elements with states (unsorted, pivot, comparing, sorted, partitioned)
    - Partition boundaries (low, high, pivot_index)
    - Swap operations with explicit element movements
    - Recursive call stack depth

    Prediction points ask: "Will this element be swapped with the pivot region?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.original_array = []
        self.recursion_depth = 0
        self.max_depth = 0
        self.swap_count = 0
        self.comparison_count = 0
        self.partition_count = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states and partition boundaries.

        Element states:
        - 'unsorted': Not yet processed
        - 'pivot': Current pivot element
        - 'comparing': Element being compared with pivot
        - 'partitioned': In correct partition (left or right of pivot)
        - 'sorted': In final sorted position
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
            'recursion_depth': self.recursion_depth,
            'swap_count': self.swap_count,
            'comparison_count': self.comparison_count
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        # Default state tracking - will be overridden by step-specific data
        return 'unsorted'

    def _quick_sort_recursive(self, low: int, high: int):
        """
        Recursive Quick Sort implementation with trace generation.

        Args:
            low: Starting index of subarray
            high: Ending index of subarray
        """
        if low < high:
            self.recursion_depth += 1
            self.max_depth = max(self.max_depth, self.recursion_depth)

            # Record recursive call
            self._add_step(
                "RECURSE",
                {
                    'low': low,
                    'high': high,
                    'subarray_size': high - low + 1,
                    'depth': self.recursion_depth,
                    'subarray': self.array[low:high+1]
                },
                f"📞 Recursive call: sort subarray[{low}..{high}] (size: {high - low + 1}, depth: {self.recursion_depth})"
            )

            # Partition the array
            pivot_index = self._partition(low, high)

            # Recursively sort left partition
            self._quick_sort_recursive(low, pivot_index - 1)

            # Recursively sort right partition
            self._quick_sort_recursive(pivot_index + 1, high)

            self.recursion_depth -= 1

    def _partition(self, low: int, high: int) -> int:
        """
        Lomuto partition scheme: pivot is last element.

        Process:
        1. Choose pivot (last element)
        2. Maintain partition index i (elements < pivot go to left of i)
        3. Scan from low to high-1, comparing each with pivot
        4. If element < pivot, swap with element at i, increment i
        5. Finally, swap pivot with element at i (pivot's final position)

        Args:
            low: Starting index
            high: Ending index (pivot position)

        Returns:
            Final pivot index after partitioning
        """
        self.partition_count += 1
        pivot_value = self.array[high]
        pivot_index = high

        self._add_step(
            "SELECT_PIVOT",
            {
                'pivot_index': pivot_index,
                'pivot_value': pivot_value,
                'low': low,
                'high': high,
                'partition_number': self.partition_count
            },
            f"🎯 Select pivot: arr[{pivot_index}] = {pivot_value} (partition #{self.partition_count})"
        )

        # Partition index: elements less than pivot go to left of i
        i = low - 1

        # Scan elements from low to high-1
        for j in range(low, high):
            current_value = self.array[j]
            self.comparison_count += 1

            # Compare current element with pivot
            comparison_result = current_value < pivot_value

            self._add_step(
                "COMPARE",
                {
                    'comparing_index': j,
                    'comparing_value': current_value,
                    'pivot_value': pivot_value,
                    'comparison': f"{current_value} < {pivot_value}",
                    'result': comparison_result,
                    'partition_index': i,
                    'low': low,
                    'high': high
                },
                f"🔍 Compare arr[{j}] = {current_value} with pivot {pivot_value}: {current_value} < {pivot_value} → {comparison_result}"
            )

            if comparison_result:
                # Element is less than pivot, move to left partition
                i += 1

                if i != j:
                    # Capture pre-swap values for accurate reporting
                    value_at_i = self.array[i]
                    value_at_j = self.array[j]
                    
                    # Perform the swap
                    self.array[i], self.array[j] = self.array[j], self.array[i]
                    self.swap_count += 1

                    # Record the swap with PRE-swap values for clarity
                    self._add_step(
                        "SWAP",
                        {
                            'index1': i,
                            'value1': value_at_i,  # Value BEFORE swap
                            'index2': j,
                            'value2': value_at_j,  # Value BEFORE swap
                            'reason': 'move_to_left_partition',
                            'partition_index': i,
                            'low': low,
                            'high': high
                        },
                        f"🔄 Swap arr[{i}] ↔ arr[{j}]: {value_at_i} ↔ {value_at_j} (move {value_at_j} to left partition)"
                    )
                else:
                    # Element already in correct position
                    self._add_step(
                        "SWAP",
                        {
                            'index1': i,
                            'value1': self.array[i],
                            'index2': j,
                            'value2': self.array[j],
                            'reason': 'already_in_position',
                            'partition_index': i,
                            'low': low,
                            'high': high
                        },
                        f"✓ arr[{i}] = {self.array[i]} already in correct position (no swap needed)"
                    )

        # Place pivot in its final sorted position
        final_pivot_index = i + 1

        if final_pivot_index != high:
            # Capture pre-swap values for accurate reporting
            value_at_final_pivot_index = self.array[final_pivot_index]
            value_at_high = self.array[high]  # This is the pivot value
            
            # Perform the swap
            self.array[final_pivot_index], self.array[high] = self.array[high], self.array[final_pivot_index]
            self.swap_count += 1

            # Record the swap with PRE-swap values for clarity
            self._add_step(
                "SWAP",
                {
                    'index1': final_pivot_index,
                    'value1': value_at_final_pivot_index,  # Value BEFORE swap
                    'index2': high,
                    'value2': value_at_high,  # Value BEFORE swap (pivot)
                    'reason': 'place_pivot_final_position',
                    'partition_index': i,
                    'low': low,
                    'high': high
                },
                f"🔄 Place pivot in final position: swap arr[{final_pivot_index}] ↔ arr[{high}]: {value_at_final_pivot_index} ↔ {value_at_high}"
            )
        else:
            self._add_step(
                "SWAP",
                {
                    'index1': final_pivot_index,
                    'value1': self.array[final_pivot_index],
                    'index2': high,
                    'value2': self.array[high],
                    'reason': 'pivot_already_in_position',
                    'partition_index': i,
                    'low': low,
                    'high': high
                },
                f"✓ Pivot arr[{final_pivot_index}] = {self.array[final_pivot_index]} already in final position"
            )

        # Record partition completion
        left_partition = self.array[low:final_pivot_index]
        right_partition = self.array[final_pivot_index+1:high+1]

        self._add_step(
            "PARTITION_DONE",
            {
                'pivot_index': final_pivot_index,
                'pivot_value': self.array[final_pivot_index],
                'left_partition': left_partition,
                'right_partition': right_partition,
                'left_size': len(left_partition),
                'right_size': len(right_partition),
                'low': low,
                'high': high
            },
            f"✅ Partition complete: pivot {self.array[final_pivot_index]} at index {final_pivot_index} | Left: {left_partition} ({len(left_partition)} elements) | Right: {right_partition} ({len(right_partition)} elements)"
        )

        return final_pivot_index

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Quick Sort trace.

        Shows complete execution flow with all decision data visible,
        following Universal Pedagogical Principles and array-specific patterns.

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Quick Sort Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {self.original_array}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Partition Scheme:** Lomuto (pivot = last element)\n\n"

        narrative += f"**Final Result:** {result['sorted_array']}\n"
        narrative += f"**Performance Metrics:**\n"
        narrative += f"- Total Comparisons: {result['comparisons']}\n"
        narrative += f"- Total Swaps: {result['swaps']}\n"
        narrative += f"- Partitions Created: {result['partitions']}\n"
        narrative += f"- Maximum Recursion Depth: {result['max_depth']}\n\n"
        narrative += "---\n\n"

        # Step-by-step narrative
        for step in steps:
            step_num = step['step']
            step_type = step['type']
            description = step['description']
            data = step['data']

            narrative += f"## Step {step_num}: {description}\n\n"

            # Type-specific details
            if step_type == "INITIAL_STATE":
                narrative += f"**Initial Configuration:**\n"
                narrative += f"- Array to sort: `{data['array']}`\n"
                narrative += f"- Array size: {data['array_size']} elements\n"
                narrative += f"- Sorting range: indices [{data['low']}, {data['high']}]\n\n"

                narrative += "**Quick Sort Strategy:**\n"
                narrative += "1. Choose pivot (last element in Lomuto scheme)\n"
                narrative += "2. Partition: move elements < pivot to left, ≥ pivot to right\n"
                narrative += "3. Recursively sort left and right partitions\n"
                narrative += "4. Pivot ends up in its final sorted position after each partition\n\n"

            elif step_type == "RECURSE":
                subarray = data['subarray']
                depth = data['depth']
                size = data['subarray_size']

                narrative += f"**Recursive Call Details:**\n"
                narrative += f"- Subarray range: indices [{data['low']}, {data['high']}]\n"
                narrative += f"- Subarray: `{subarray}`\n"
                narrative += f"- Size: {size} element{'s' if size != 1 else ''}\n"
                narrative += f"- Recursion depth: {depth}\n\n"

                if size == 1:
                    narrative += "*Single element subarray is already sorted (base case).*\n\n"
                elif size == 2:
                    narrative += "*Two-element subarray will be sorted in one partition.*\n\n"

            elif step_type == "SELECT_PIVOT":
                pivot_idx = data['pivot_index']
                pivot_val = data['pivot_value']
                low = data['low']
                high = data['high']

                narrative += f"**Pivot Selection (Lomuto Scheme):**\n"
                narrative += f"- Pivot index: {pivot_idx} (last element of subarray)\n"
                narrative += f"- Pivot value: **{pivot_val}**\n"
                narrative += f"- Subarray range: [{low}, {high}]\n\n"

                narrative += f"**Partitioning Goal:**\n"
                narrative += f"- Move all elements < {pivot_val} to the left\n"
                narrative += f"- Move all elements ≥ {pivot_val} to the right\n"
                narrative += f"- Place pivot in its final sorted position\n\n"

            elif step_type == "COMPARE":
                comparing_idx = data['comparing_index']
                comparing_val = data['comparing_value']
                pivot_val = data['pivot_value']
                result_bool = data['result']
                partition_idx = data['partition_index']

                narrative += f"**Comparison:**\n"
                narrative += f"- Current element: arr[{comparing_idx}] = {comparing_val}\n"
                narrative += f"- Pivot value: {pivot_val}\n"
                narrative += f"- Comparison: `{comparing_val} < {pivot_val}`\n"
                narrative += f"- Result: **{result_bool}**\n\n"

                if result_bool:
                    narrative += f"**Decision:** {comparing_val} < {pivot_val} ✓\n"
                    narrative += f"- Element belongs in **left partition** (values < pivot)\n"
                    narrative += f"- Increment partition index: {partition_idx} → {partition_idx + 1}\n"
                    narrative += f"- Prepare to swap arr[{partition_idx + 1}] with arr[{comparing_idx}]\n\n"
                else:
                    narrative += f"**Decision:** {comparing_val} ≥ {pivot_val}\n"
                    narrative += f"- Element belongs in **right partition** (values ≥ pivot)\n"
                    narrative += f"- Leave in current position (no swap needed)\n"
                    narrative += f"- Partition index remains: {partition_idx}\n\n"

            elif step_type == "SWAP":
                idx1 = data['index1']
                val1 = data['value1']
                idx2 = data['index2']
                val2 = data['value2']
                reason = data['reason']

                narrative += f"**Swap Operation:**\n"
                narrative += f"- Position 1: arr[{idx1}] = {val1}\n"
                narrative += f"- Position 2: arr[{idx2}] = {val2}\n"

                if reason == 'move_to_left_partition':
                    narrative += f"- **Action:** Swap arr[{idx1}] ↔ arr[{idx2}]\n"
                    narrative += f"- **Reason:** Move {val2} to left partition (< pivot)\n"
                    narrative += f"- **Result:** arr[{idx1}] now contains {val2}, arr[{idx2}] now contains {val1}\n\n"
                elif reason == 'already_in_position':
                    narrative += f"- **Action:** No swap needed\n"
                    narrative += f"- **Reason:** Element {val1} already at partition boundary\n\n"
                elif reason == 'place_pivot_final_position':
                    narrative += f"- **Action:** Swap arr[{idx1}] ↔ arr[{idx2}]\n"
                    narrative += f"- **Reason:** Place pivot {val2} in its final sorted position\n"
                    narrative += f"- **Result:** Pivot {val2} now at index {idx1} (all left < {val2}, all right ≥ {val2})\n\n"
                elif reason == 'pivot_already_in_position':
                    narrative += f"- **Action:** No swap needed\n"
                    narrative += f"- **Reason:** Pivot {val1} already in final position\n\n"

            elif step_type == "PARTITION_DONE":
                pivot_idx = data['pivot_index']
                pivot_val = data['pivot_value']
                left_part = data['left_partition']
                right_part = data['right_partition']
                left_size = data['left_size']
                right_size = data['right_size']

                narrative += f"**Partition Summary:**\n"
                narrative += f"- Pivot value: **{pivot_val}** now at index **{pivot_idx}** (final sorted position)\n"
                narrative += f"- Left partition: `{left_part}` ({left_size} element{'s' if left_size != 1 else ''})\n"
                narrative += f"  - All elements < {pivot_val}\n"
                narrative += f"- Right partition: `{right_part}` ({right_size} element{'s' if right_size != 1 else ''})\n"
                narrative += f"  - All elements ≥ {pivot_val}\n\n"

                narrative += f"**Partition Invariant Satisfied:**\n"
                narrative += f"- Every element in left partition < {pivot_val}\n"
                narrative += f"- Pivot {pivot_val} is in its final sorted position\n"
                narrative += f"- Every element in right partition ≥ {pivot_val}\n\n"

                if left_size > 1:
                    narrative += f"*Next: Recursively sort left partition ({left_size} elements)*\n"
                elif left_size == 1:
                    narrative += f"*Left partition has 1 element (already sorted)*\n"
                else:
                    narrative += f"*Left partition is empty*\n"

                if right_size > 1:
                    narrative += f"*Then: Recursively sort right partition ({right_size} elements)*\n\n"
                elif right_size == 1:
                    narrative += f"*Right partition has 1 element (already sorted)*\n\n"
                else:
                    narrative += f"*Right partition is empty*\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Original Array:** {self.original_array}\n"
        narrative += f"**Sorted Array:** {result['sorted_array']}\n\n"

        narrative += f"**Algorithm Performance:**\n"
        narrative += f"- **Comparisons:** {result['comparisons']}\n"
        narrative += f"  - Each element compared with pivot during partitioning\n"
        narrative += f"- **Swaps:** {result['swaps']}\n"
        narrative += f"  - Elements moved to correct partitions\n"
        narrative += f"- **Partitions:** {result['partitions']}\n"
        narrative += f"  - Number of times array was divided\n"
        narrative += f"- **Max Recursion Depth:** {result['max_depth']}\n"
        narrative += f"  - Deepest level of recursive calls\n\n"

        narrative += f"**Complexity Analysis:**\n"
        narrative += f"- **Time Complexity:**\n"
        narrative += f"  - Average case: O(n log n) - balanced partitions\n"
        narrative += f"  - Worst case: O(n²) - unbalanced partitions (already sorted)\n"
        narrative += f"  - Best case: O(n log n) - perfectly balanced partitions\n"
        narrative += f"- **Space Complexity:** O(log n) - recursion stack depth\n\n"

        narrative += f"**Quick Sort Characteristics:**\n"
        narrative += f"- **In-place:** Sorts array without extra space (except recursion stack)\n"
        narrative += f"- **Unstable:** Equal elements may change relative order\n"
        narrative += f"- **Divide-and-conquer:** Recursively partition and sort\n"
        narrative += f"- **Pivot choice matters:** Last element (Lomuto) vs. random/median (better average case)\n\n"

        # Add Frontend Visualization Hints section
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"

        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Partition Progress** - Show how array is divided into left (< pivot) and right (≥ pivot) regions\n"
        narrative += "- **Pivot Position** - Highlight pivot element and its movement to final sorted position\n"
        narrative += "- **Recursion Depth** (`recursion_depth`) - Visualize call stack to show divide-and-conquer strategy\n"
        narrative += "- **Comparison Count** (`comparison_count`) - Track efficiency of partitioning\n\n"

        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight pivot selection** - Use distinct color for pivot element (last element in subarray)\n"
        narrative += "2. **Show partition boundaries** - Visual separator between left partition (< pivot) and right partition (≥ pivot)\n"
        narrative += "3. **Animate swaps** - Show element movements when swapping to left partition or placing pivot\n"
        narrative += "4. **Emphasize sorted positions** - When pivot reaches final position, mark as 'sorted' (won't move again)\n"
        narrative += "5. **Visualize recursion** - Use indentation or tree structure to show recursive calls on subarray ranges\n\n"

        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.pivot_index\n"
        narrative += "step.data.pivot_value\n"
        narrative += "step.data.low                    // Start of current subarray\n"
        narrative += "step.data.high                   // End of current subarray\n"
        narrative += "step.data.partition_index        // Boundary between left/right partitions\n"
        narrative += "step.data.comparing_index        // Element being compared with pivot\n"
        narrative += "step.data.comparing_value\n"
        narrative += "step.data.comparison             // String: 'X < pivot'\n"
        narrative += "step.data.result                 // Boolean: comparison result\n"
        narrative += "step.data.index1, index2         // Swap positions\n"
        narrative += "step.data.value1, value2         // Swap values\n"
        narrative += "step.data.reason                 // Swap reason: 'move_to_left_partition', 'place_pivot_final_position'\n"
        narrative += "step.data.left_partition         // Elements < pivot after partition\n"
        narrative += "step.data.right_partition        // Elements ≥ pivot after partition\n"
        narrative += "step.data.visualization.array[*].state  // 'unsorted', 'pivot', 'comparing', 'partitioned', 'sorted'\n"
        narrative += "step.data.visualization.recursion_depth\n"
        narrative += "step.data.visualization.swap_count\n"
        narrative += "step.data.visualization.comparison_count\n"
        narrative += "```\n\n"

        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Quick Sort's power comes from **in-place partitioning** - rearranging elements without extra space. "
        narrative += "The most pedagogically important visualization is showing the **partition process**: how elements are compared with the pivot and swapped to the correct side. "
        narrative += "Use **color coding** to distinguish:\n"
        narrative += "- **Pivot** (yellow/gold) - The element being used to partition\n"
        narrative += "- **Comparing** (blue) - Element currently being compared with pivot\n"
        narrative += "- **Left partition** (green) - Elements < pivot\n"
        narrative += "- **Right partition** (red) - Elements ≥ pivot\n"
        narrative += "- **Sorted** (gray) - Elements in final position (pivots after partitioning)\n\n"
        narrative += "The **recursion visualization** is critical for understanding divide-and-conquer. "
        narrative += "Show the call stack or use a tree structure where each node represents a subarray being sorted. "
        narrative += "Animate the **recursive descent** (dividing) and **ascent** (combining sorted partitions). "
        narrative += "When a pivot reaches its final position, emphasize that it **never moves again** - this is the key insight that makes Quick Sort work. "
        narrative += "The algorithm's efficiency depends on **balanced partitions** - visualize how pivot choice affects partition sizes.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Quick Sort algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers to sort

        Returns:
            Standardized trace result with:
                - result: {'sorted_array': list, 'comparisons': int, 'swaps': int, 'partitions': int, 'max_depth': int}
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

        self.array = input_data['array'][:]
        self.original_array = input_data['array'][:]

        if not self.array:
            raise ValueError("Array cannot be empty")

        if len(self.array) < 2:
            raise ValueError("Array must have at least 2 elements")

        # Initialize counters
        self.recursion_depth = 0
        self.max_depth = 0
        self.swap_count = 0
        self.comparison_count = 0
        self.partition_count = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'quick-sort',
            'display_name': 'Quick Sort',
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True,
                'highlight_pivot': True,
                'show_partitions': True,
                'partition_colors': {
                    'pivot': 'yellow',
                    'comparing': 'blue',
                    'left_partition': 'green',
                    'right_partition': 'red',
                    'sorted': 'gray'
                }
            },
            'input_size': len(self.array)
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'array': self.array[:],
                'array_size': len(self.array),
                'low': 0,
                'high': len(self.array) - 1
            },
            f"🚀 Starting Quick Sort on array of {len(self.array)} elements"
        )

        # Execute Quick Sort
        self._quick_sort_recursive(0, len(self.array) - 1)

        # Build result
        return self._build_trace_result({
            'sorted_array': self.array,
            'comparisons': self.comparison_count,
            'swaps': self.swap_count,
            'partitions': self.partition_count,
            'max_depth': self.max_depth
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After comparing element with pivot, will it be
        swapped to the left partition (< pivot) or stay in place (≥ pivot)?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after comparison, before swap decision
            if step.type == "COMPARE" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]

                if next_step.type == "SWAP":
                    comparing_val = step.data['comparing_value']
                    pivot_val = step.data['pivot_value']
                    swap_reason = next_step.data['reason']

                    # Determine correct answer from swap reason
                    if swap_reason == 'move_to_left_partition':
                        correct_answer = "swap-left"
                    elif swap_reason == 'already_in_position':
                        correct_answer = "no-swap"
                    else:
                        continue  # Skip pivot placement swaps

                    predictions.append({
                        'step_index': i,
                        'question': f"Element {comparing_val} compared with pivot {pivot_val}. What happens next?",
                        'choices': [
                            {'id': 'swap-left', 'label': f'Swap to left partition ({comparing_val} < {pivot_val})'},
                            {'id': 'no-swap', 'label': f'Stay in place ({comparing_val} ≥ {pivot_val})'},
                            {'id': 'swap-right', 'label': f'Swap to right partition'}
                        ],
                        'hint': f"Compare {comparing_val} with pivot {pivot_val}. Elements < pivot go left.",
                        'correct_answer': correct_answer,
                        'explanation': self._get_prediction_explanation(comparing_val, pivot_val, correct_answer)
                    })

        return predictions

    def _get_prediction_explanation(self, comparing_val: int, pivot_val: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "swap-left":
            return f"{comparing_val} < {pivot_val}, so element moves to left partition (values less than pivot)"
        elif answer == "no-swap":
            return f"{comparing_val} ≥ {pivot_val}, so element stays in place (belongs in right partition)"
        return ""