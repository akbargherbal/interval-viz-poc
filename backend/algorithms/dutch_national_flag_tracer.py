
"""
Dutch National Flag (Sort Colors) algorithm tracer for educational visualization.

Implements three-way partitioning to sort an array of 0s, 1s, and 2s in one pass
with complete trace generation for step-by-step visualization and prediction mode.

VERSION: 2.1 - Backend Checklist v2.2 Compliance
- Added Frontend Visualization Hints section to narrative
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class DutchNationalFlagTracer(AlgorithmTracer):
    """
    Tracer for Dutch National Flag (Sort Colors) algorithm.

    Visualization shows:
    - Array elements with color states (red=0, white=1, blue=2)
    - Three pointers (low, mid, high)
    - Three regions: [0s | 1s | 2s]

    Prediction points ask: "What action will we take for this value?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.low = 0
        self.mid = 0
        self.high = 0
        self.swaps = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element colors and pointers.

        Element states:
        - 'examining': Current mid element being processed
        - 'sorted_low': In the 0s region (before low pointer)
        - 'sorted_mid': In the 1s region (between low and mid)
        - 'sorted_high': In the 2s region (after high pointer)
        - 'unsorted': Not yet processed (between mid and high)
        """
        if not self.array:
            return {}

        return {
            'array': [
                {
                    'index': i,
                    'value': v,
                    'state': self._get_element_state(i),
                    'color': self._get_color_for_value(v)
                }
                for i, v in enumerate(self.array)
            ],
            'pointers': {
                'low': self.low,
                'mid': self.mid,
                'high': self.high
            },
            'regions': {
                'zeros': f"[0, {self.low})",
                'ones': f"[{self.low}, {self.mid})",
                'unsorted': f"[{self.mid}, {self.high + 1})",
                'twos': f"({self.high}, {len(self.array)})"
            }
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        if index == self.mid and index <= self.high:
            return 'examining'
        elif index < self.low:
            return 'sorted_low'
        elif index < self.mid:
            return 'sorted_mid'
        elif index > self.high:
            return 'sorted_high'
        else:
            return 'unsorted'

    def _get_color_for_value(self, value: int) -> str:
        """Map value to color name."""
        color_map = {0: 'red', 1: 'white', 2: 'blue'}
        return color_map.get(value, 'gray')

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Dutch National Flag trace.

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
        narrative = "# Dutch National Flag (Sort Colors) Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {result['original_array']}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Goal:** Sort array of 0s (red), 1s (white), and 2s (blue) in one pass\n"
        narrative += f"**Result:** {result['sorted_array']}\n"
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
                narrative += f"- Three pointers initialized:\n"
                narrative += f"  - `low = 0` (boundary for 0s region)\n"
                narrative += f"  - `mid = 0` (current element to examine)\n"
                narrative += f"  - `high = {data['array_size'] - 1}` (boundary for 2s region)\n\n"

                narrative += "**Strategy:**\n"
                narrative += "- Maintain three regions: [0s | 1s | unsorted | 2s]\n"
                narrative += "- Process elements at `mid` pointer:\n"
                narrative += "  - If 0 (red): swap with `low`, advance both `low` and `mid`\n"
                narrative += "  - If 1 (white): already in correct region, advance `mid`\n"
                narrative += "  - If 2 (blue): swap with `high`, decrement `high` (don't advance `mid`)\n\n"

                narrative += "**Array Visualization:**\n```\n"
                narrative += "Index: " + " ".join(f"{i:3d}" for i in range(len(viz['array']))) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                narrative += "Color: " + " ".join(f"{elem['color'][:3]:>3s}" for elem in viz['array']) + "\n"
                narrative += "       " + " ".join("LMH" if i == 0 else "   " for i in range(len(viz['array']))) + "\n"
                narrative += "```\n"
                narrative += f"*All pointers start at position 0 (low=mid) and {len(viz['array'])-1} (high)*\n\n"

            elif step_type == "CHECK_VALUE":
                mid_index = data['mid_index']
                mid_value = data['mid_value']
                low = data['low']
                high = data['high']

                narrative += f"**Current State:**\n"
                narrative += f"- Examining element at index `mid = {mid_index}`\n"
                narrative += f"- Value at mid: `{mid_value}` (color: {self._get_color_for_value(mid_value)})\n"
                narrative += f"- Pointer positions: `low = {low}`, `mid = {mid_index}`, `high = {high}`\n\n"

                narrative += "**Current Array:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                narrative += "Color: " + " ".join(f"{elem['color'][:3]:>3s}" for elem in active_elements) + "\n"

                # Show pointer positions
                pointer_line = "       "
                for elem in active_elements:
                    idx = elem['index']
                    markers = []
                    if idx == low:
                        markers.append('L')
                    if idx == mid_index:
                        markers.append('M')
                    if idx == high:
                        markers.append('H')
                    
                    if markers:
                        pointer_line += "".join(markers).ljust(3)
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n\n"

                narrative += f"**Regions:**\n"
                narrative += f"- 0s (red): indices [0, {low}) - **{low} elements**\n"
                narrative += f"- 1s (white): indices [{low}, {mid_index}) - **{mid_index - low} elements**\n"
                narrative += f"- Unsorted: indices [{mid_index}, {high + 1}) - **{high - mid_index + 1} elements**\n"
                narrative += f"- 2s (blue): indices ({high}, {len(viz['array'])}) - **{len(viz['array']) - high - 1} elements**\n\n"

                narrative += f"**Decision Point:** What to do with value `{mid_value}`?\n\n"

            elif step_type == "SWAP_LOW":
                mid_index = data['mid_index']
                low_index = data['low_index']
                mid_value = data['mid_value']
                low_value = data['low_value']
                new_low = data['new_low']
                new_mid = data['new_mid']

                narrative += f"**Value is 0 (red) - Move to 0s region:**\n\n"

                narrative += f"**Comparison:** `array[mid] = {mid_value}` → This is a 0 (red)\n\n"

                narrative += f"**Action:** Swap with `low` boundary and advance both pointers\n"
                narrative += f"- Swap `array[{mid_index}]` (value: {mid_value}) with `array[{low_index}]` (value: {low_value})\n"
                narrative += f"- Calculation: `low = {low_index} + 1 = {new_low}`\n"
                narrative += f"- Calculation: `mid = {mid_index} + 1 = {new_mid}`\n\n"

                narrative += f"**Swap Details:**\n"
                narrative += f"```\n"
                narrative += f"Before: array[{low_index}] = {low_value}, array[{mid_index}] = {mid_value}\n"
                narrative += f"After:  array[{low_index}] = {mid_value}, array[{mid_index}] = {low_value}\n"
                narrative += f"```\n\n"

                narrative += f"**Reasoning:**\n"
                narrative += f"- The 0 at position {mid_index} belongs in the 0s region\n"
                narrative += f"- Swap it with the element at `low` boundary (position {low_index})\n"
                narrative += f"- Advance `low` to expand the 0s region: {low_index} → {new_low}\n"
                narrative += f"- Advance `mid` because swapped element from `low` is already processed (it's either 0 or 1): {mid_index} → {new_mid}\n\n"

                narrative += "**Updated Array:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                narrative += "Color: " + " ".join(f"{elem['color'][:3]:>3s}" for elem in active_elements) + "\n"

                pointer_line = "       "
                for elem in active_elements:
                    idx = elem['index']
                    markers = []
                    if idx == new_low:
                        markers.append('L')
                    if idx == new_mid:
                        markers.append('M')
                    if idx == viz['pointers']['high']:
                        markers.append('H')
                    
                    if markers:
                        pointer_line += "".join(markers).ljust(3)
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n\n"

            elif step_type == "SWAP_HIGH":
                mid_index = data['mid_index']
                high_index = data['high_index']
                mid_value = data['mid_value']
                high_value = data['high_value']
                new_high = data['new_high']

                narrative += f"**Value is 2 (blue) - Move to 2s region:**\n\n"

                narrative += f"**Comparison:** `array[mid] = {mid_value}` → This is a 2 (blue)\n\n"

                narrative += f"**Action:** Swap with `high` boundary and decrement `high`\n"
                narrative += f"- Swap `array[{mid_index}]` (value: {mid_value}) with `array[{high_index}]` (value: {high_value})\n"
                narrative += f"- Calculation: `high = {high_index} - 1 = {new_high}`\n"
                narrative += f"- Note: `mid` stays at {mid_index} (need to examine swapped element)\n\n"

                narrative += f"**Swap Details:**\n"
                narrative += f"```\n"
                narrative += f"Before: array[{mid_index}] = {mid_value}, array[{high_index}] = {high_value}\n"
                narrative += f"After:  array[{mid_index}] = {high_value}, array[{high_index}] = {mid_value}\n"
                narrative += f"```\n\n"

                narrative += f"**Reasoning:**\n"
                narrative += f"- The 2 at position {mid_index} belongs in the 2s region\n"
                narrative += f"- Swap it with the element at `high` boundary (position {high_index})\n"
                narrative += f"- Decrement `high` to expand the 2s region: {high_index} → {new_high}\n"
                narrative += f"- **Don't advance `mid`** because the element swapped from `high` (value: {high_value}) hasn't been examined yet\n"
                narrative += f"- Next iteration will examine this newly swapped element at position {mid_index}\n\n"

                narrative += "**Updated Array:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                narrative += "Color: " + " ".join(f"{elem['color'][:3]:>3s}" for elem in active_elements) + "\n"

                pointer_line = "       "
                for elem in active_elements:
                    idx = elem['index']
                    markers = []
                    if idx == viz['pointers']['low']:
                        markers.append('L')
                    if idx == mid_index:
                        markers.append('M')
                    if idx == new_high:
                        markers.append('H')
                    
                    if markers:
                        pointer_line += "".join(markers).ljust(3)
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n\n"

            elif step_type == "ADVANCE_MID":
                mid_index = data['mid_index']
                mid_value = data['mid_value']
                new_mid = data['new_mid']

                narrative += f"**Value is 1 (white) - Already in correct region:**\n\n"

                narrative += f"**Comparison:** `array[mid] = {mid_value}` → This is a 1 (white)\n\n"

                narrative += f"**Action:** Simply advance `mid` pointer\n"
                narrative += f"- Calculation: `mid = {mid_index} + 1 = {new_mid}`\n"
                narrative += f"- No swap needed (1s belong between `low` and `mid`)\n\n"

                narrative += f"**Reasoning:**\n"
                narrative += f"- The 1 at position {mid_index} is already in the correct region (1s region)\n"
                narrative += f"- The 1s region is defined as indices [{viz['pointers']['low']}, {mid_index})\n"
                narrative += f"- By advancing `mid`, we expand the 1s region to include this element\n"
                narrative += f"- New 1s region: [{viz['pointers']['low']}, {new_mid})\n\n"

                narrative += "**Updated Array:**\n```\n"
                active_elements = viz['array']
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                narrative += "Color: " + " ".join(f"{elem['color'][:3]:>3s}" for elem in active_elements) + "\n"

                pointer_line = "       "
                for elem in active_elements:
                    idx = elem['index']
                    markers = []
                    if idx == viz['pointers']['low']:
                        markers.append('L')
                    if idx == new_mid:
                        markers.append('M')
                    if idx == viz['pointers']['high']:
                        markers.append('H')
                    
                    if markers:
                        pointer_line += "".join(markers).ljust(3)
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Original Array:** {result['original_array']}\n"
        narrative += f"**Sorted Array:** {result['sorted_array']}\n\n"

        narrative += f"**Final Regions:**\n"
        final_viz = steps[-1]['data']['visualization']
        low_final = final_viz['pointers']['low']
        mid_final = final_viz['pointers']['mid']
        
        narrative += f"- 0s (red): indices [0, {low_final}) → {result['sorted_array'][:low_final]}\n"
        narrative += f"- 1s (white): indices [{low_final}, {mid_final}) → {result['sorted_array'][low_final:mid_final]}\n"
        narrative += f"- 2s (blue): indices [{mid_final}, {len(result['sorted_array'])}) → {result['sorted_array'][mid_final:]}\n\n"

        narrative += f"**Performance:**\n"
        narrative += f"- Total swaps: {result['swaps']}\n"
        narrative += f"- Single pass through array: O(n) time complexity\n"
        narrative += f"- In-place sorting: O(1) space complexity\n"
        narrative += f"- Optimal for three-value sorting problems\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Three Pointer Positions** (`pointers.low`, `pointers.mid`, `pointers.high`) - Core of the algorithm's partitioning strategy\n"
        narrative += "- **Region Boundaries** (`regions.zeros`, `regions.ones`, `regions.twos`) - Visual representation of the three-way partition\n"
        narrative += "- **Swap Count** (`swaps`) - Demonstrates in-place efficiency\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Color-code elements by value** - Use red (0), white (1), blue (2) to match Dutch flag theme\n"
        narrative += "2. **Highlight the three regions** - Use background shading or borders to show [0s | 1s | unsorted | 2s]\n"
        narrative += "3. **Emphasize pointer movements** - Show when `low` and `mid` advance together vs. when only one moves\n"
        narrative += "4. **Animate swaps clearly** - When swapping with `low` or `high`, show the element movement\n"
        narrative += "5. **Show the examining state** - The element at `mid` is the decision point—highlight it distinctly\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.pointers.low\n"
        narrative += "step.data.visualization.pointers.mid\n"
        narrative += "step.data.visualization.pointers.high\n"
        narrative += "step.data.visualization.regions.zeros\n"
        narrative += "step.data.visualization.regions.ones\n"
        narrative += "step.data.visualization.regions.twos\n"
        narrative += "step.data.visualization.array[*].state  // 'examining' | 'sorted_low' | 'sorted_mid' | 'sorted_high' | 'unsorted'\n"
        narrative += "step.data.visualization.array[*].value  // 0, 1, or 2\n"
        narrative += "step.data.visualization.array[*].color  // 'red', 'white', 'blue'\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "The Dutch National Flag algorithm's elegance comes from **maintaining invariants with three pointers**. "
        narrative += "The most pedagogically important visualization is showing how the three regions grow and shrink: "
        narrative += "the 0s region expands from the left, the 2s region expands from the right, and the 1s region grows in the middle. "
        narrative += "The **unsorted region shrinks** as `mid` approaches `high`. "
        narrative += "Consider using **distinct background colors** for each region to make the partitioning crystal clear. "
        narrative += "The key insight to emphasize: when we swap with `low`, we advance `mid` (because we know what came from `low`), "
        narrative += "but when we swap with `high`, we **don't advance `mid`** (because we need to examine what came from `high`). "
        narrative += "This asymmetry is the algorithm's clever trick. "
        narrative += "Use the color theme (red/white/blue) not just for aesthetics but to reinforce the three-way partition concept. "
        narrative += "When the algorithm completes (`mid > high`), show the final sorted array with clear region boundaries to celebrate the one-pass achievement.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Dutch National Flag algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers (must contain only 0, 1, 2)

        Returns:
            Standardized trace result with:
                - result: {'sorted_array': list, 'original_array': list, 'swaps': int}
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='array'

        Raises:
            ValueError: If array contains values other than 0, 1, 2 or input is invalid
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if 'array' not in input_data:
            raise ValueError("Input must contain 'array' key")

        self.array = input_data['array'][:]  # Copy to avoid modifying input
        original_array = input_data['array'][:]

        if not self.array:
            raise ValueError("Array cannot be empty")

        # Validate array contains only 0, 1, 2
        if not all(v in [0, 1, 2] for v in self.array):
            raise ValueError("Array must contain only values 0, 1, and 2")

        # Initialize pointers
        self.low = 0
        self.mid = 0
        self.high = len(self.array) - 1
        self.swaps = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'dutch-national-flag',
            'display_name': 'Sort Colors (Dutch National Flag)',
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'colored_box',
                'show_indices': True,
                'color_map': {
                    '0': 'red',
                    '1': 'white',
                    '2': 'blue'
                },
                'pointer_colors': {
                    'low': 'green',
                    'mid': 'yellow',
                    'high': 'purple'
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
                'low': self.low,
                'mid': self.mid,
                'high': self.high
            },
            f"🎨 Initialize three pointers for sorting {len(self.array)} elements (0s, 1s, 2s)"
        )

        # Dutch National Flag algorithm
        while self.mid <= self.high:
            # Check current value at mid
            current_value = self.array[self.mid]

            self._add_step(
                "CHECK_VALUE",
                {
                    'mid_index': self.mid,
                    'mid_value': current_value,
                    'low': self.low,
                    'high': self.high
                },
                f"🔍 Examine array[{self.mid}] = {current_value} (color: {self._get_color_for_value(current_value)})"
            )

            if current_value == 0:
                # Swap with low and advance both low and mid
                low_value = self.array[self.low]
                self.array[self.low], self.array[self.mid] = self.array[self.mid], self.array[self.low]
                self.swaps += 1

                old_low = self.low
                old_mid = self.mid
                self.low += 1
                self.mid += 1

                self._add_step(
                    "SWAP_LOW",
                    {
                        'mid_index': old_mid,
                        'low_index': old_low,
                        'mid_value': current_value,
                        'low_value': low_value,
                        'new_low': self.low,
                        'new_mid': self.mid,
                        'swaps': self.swaps
                    },
                    f"🔴 Value is 0 (red): swap array[{old_mid}] ↔ array[{old_low}], advance low and mid"
                )

            elif current_value == 2:
                # Swap with high and decrement high (don't advance mid)
                high_value = self.array[self.high]
                self.array[self.mid], self.array[self.high] = self.array[self.high], self.array[self.mid]
                self.swaps += 1

                old_high = self.high
                self.high -= 1

                self._add_step(
                    "SWAP_HIGH",
                    {
                        'mid_index': self.mid,
                        'high_index': old_high,
                        'mid_value': current_value,
                        'high_value': high_value,
                        'new_high': self.high,
                        'swaps': self.swaps
                    },
                    f"🔵 Value is 2 (blue): swap array[{self.mid}] ↔ array[{old_high}], decrement high (mid stays)"
                )

            else:  # current_value == 1
                # Already in correct position, just advance mid
                old_mid = self.mid
                self.mid += 1

                self._add_step(
                    "ADVANCE_MID",
                    {
                        'mid_index': old_mid,
                        'mid_value': current_value,
                        'new_mid': self.mid
                    },
                    f"⚪ Value is 1 (white): already in correct region, advance mid"
                )

        return self._build_trace_result({
            'sorted_array': self.array,
            'original_array': original_array,
            'swaps': self.swaps
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After examining the value at mid, what action
        will the algorithm take?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after checking value, before action
            if step.type == "CHECK_VALUE" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                mid_value = step.data['mid_value']

                # Determine correct answer from next step type
                if next_step.type == "SWAP_LOW":
                    correct_answer = "swap-low"
                elif next_step.type == "SWAP_HIGH":
                    correct_answer = "swap-high"
                elif next_step.type == "ADVANCE_MID":
                    correct_answer = "advance-mid"
                else:
                    continue  # Skip if unexpected step type

                color_name = self._get_color_for_value(mid_value)

                predictions.append({
                    'step_index': i,
                    'question': f"Value at mid is {mid_value} ({color_name}). What action should we take?",
                    'choices': [
                        {'id': 'swap-low', 'label': 'Swap with low, advance both low and mid'},
                        {'id': 'swap-high', 'label': 'Swap with high, decrement high only'},
                        {'id': 'advance-mid', 'label': 'Just advance mid (no swap)'}
                    ],
                    'hint': f"Consider where {mid_value}s belong in the sorted array",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(mid_value, correct_answer)
                })

        return predictions

    def _get_prediction_explanation(self, value: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "swap-low":
            return f"Value {value} (red) belongs in the 0s region at the left. Swap with low boundary and advance both pointers."
        elif answer == "swap-high":
            return f"Value {value} (blue) belongs in the 2s region at the right. Swap with high boundary and decrement high (don't advance mid because we need to examine the swapped element)."
        elif answer == "advance-mid":
            return f"Value {value} (white) is already in the correct region (1s belong between low and mid). Just advance mid to expand the 1s region."
        return ""
