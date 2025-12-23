
"""
Longest Increasing Subsequence (Patience Sorting) algorithm tracer.

Implements the O(n log n) patience sorting algorithm to find the length of
the longest strictly increasing subsequence in an array. Uses binary search
to maintain an array of "tails" where tails[i] represents the smallest ending
value of all increasing subsequences of length i+1.

VERSION: 2.0 - Backend Checklist v2.2 Compliance
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer
import bisect


class LongestIncreasingSubsequenceTracer(AlgorithmTracer):
    """
    Tracer for Longest Increasing Subsequence using Patience Sorting.

    Visualization shows:
    - Input array with current element being examined
    - Tails array showing smallest ending values for each subsequence length
    - Binary search process when finding replacement position
    - Final LIS length

    Algorithm maintains tails[i] = smallest ending value of all increasing
    subsequences of length i+1. For each element:
    - If element > last tail: extend (append to tails)
    - Otherwise: binary search to find replacement position
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.tails = []
        self.current_index = None
        self.current_num = None
        self.search_left = None
        self.search_right = None
        self.search_mid = None
        self.replacement_index = None

    def _get_visualization_state(self) -> dict:
        """
        Return current state for visualization.

        Shows:
        - Input array with element states (pending, examining, processed)
        - Tails array with current values
        - Binary search pointers (when searching)
        """
        if not self.array:
            return {}

        viz_state = {
            'array': [
                {
                    'index': i,
                    'value': v,
                    'state': self._get_element_state(i)
                }
                for i, v in enumerate(self.array)
            ],
            'tails': [
                {
                    'index': i,
                    'value': v,
                    'state': self._get_tail_state(i)
                }
                for i, v in enumerate(self.tails)
            ],
            'current_element': {
                'index': self.current_index,
                'value': self.current_num
            } if self.current_index is not None else None,
            'tails_length': len(self.tails)
        }

        # Add binary search pointers if active
        if self.search_left is not None:
            viz_state['binary_search'] = {
                'left': self.search_left,
                'right': self.search_right,
                'mid': self.search_mid
            }

        return viz_state

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element."""
        if self.current_index is None:
            return 'pending'
        if index == self.current_index:
            return 'examining'
        if index < self.current_index:
            return 'processed'
        return 'pending'

    def _get_tail_state(self, index: int) -> str:
        """Determine visual state of tail element."""
        if self.search_mid is not None and index == self.search_mid:
            return 'examining'
        if self.replacement_index is not None and index == self.replacement_index:
            return 'replacing'
        return 'active'

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from LIS trace.

        Shows complete execution with all decision data visible, including
        binary search details and tail array updates.

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Longest Increasing Subsequence (Patience Sorting) Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {self.array}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Result:** LIS Length = **{result['lis_length']}**\n\n"
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
                narrative += "**Algorithm Overview:**\n"
                narrative += "We maintain a `tails` array where `tails[i]` = smallest ending value of all increasing subsequences of length `i+1`.\n\n"
                
                narrative += "**Strategy:**\n"
                narrative += "- If current number > last tail: **extend** (append to tails)\n"
                narrative += "- Otherwise: **replace** using binary search to find position\n\n"

                narrative += "**Initial State:**\n"
                narrative += f"- Input array: `{self.array}`\n"
                narrative += f"- Tails array: `[]` (empty)\n"
                narrative += f"- Array size: {len(self.array)} elements\n\n"

                narrative += "**Input Array Visualization:**\n```\n"
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in viz['array']) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                narrative += "```\n\n"

            elif step_type == "CHECK_ELEMENT":
                current_num = data['current_num']
                current_index = data['current_index']
                tails_before = data['tails_before']
                last_tail = data.get('last_tail')

                narrative += f"**Current Element:** `array[{current_index}] = {current_num}`\n\n"

                narrative += f"**Tails Array Before:** `{tails_before}`\n"
                if tails_before:
                    narrative += f"- Length: {len(tails_before)}\n"
                    narrative += f"- Last tail: `tails[{len(tails_before)-1}] = {last_tail}`\n\n"
                else:
                    narrative += "- Empty (no subsequences yet)\n\n"

                narrative += "**Decision Point:**\n"
                if not tails_before:
                    narrative += f"Tails array is empty → **extend** with first element\n\n"
                else:
                    narrative += f"Compare current number ({current_num}) with last tail ({last_tail}):\n"
                    if current_num > last_tail:
                        narrative += f"- `{current_num} > {last_tail}` ✓\n"
                        narrative += f"- Action: **Extend** (append to tails)\n\n"
                    else:
                        narrative += f"- `{current_num} ≤ {last_tail}` ✓\n"
                        narrative += f"- Action: **Replace** using binary search\n\n"

            elif step_type == "BINARY_SEARCH":
                current_num = data['current_num']
                search_range = data['search_range']
                left = data['left']
                right = data['right']
                mid = data['mid']
                mid_value = data['mid_value']
                comparison = data['comparison']

                narrative += f"**Binary Search in Tails Array:**\n"
                narrative += f"Goal: Find leftmost position where `tails[pos] ≥ {current_num}`\n\n"

                narrative += f"**Search Range:** indices [{left}, {right}]\n"
                narrative += f"**Tails Subset:**\n```\n"
                tails_subset = viz['tails'][left:right+1]
                narrative += "Index: " + " ".join(f"{t['index']:3d}" for t in tails_subset) + "\n"
                narrative += "Value: " + " ".join(f"{t['value']:3d}" for t in tails_subset) + "\n"
                
                # Show pointers
                pointer_line = "       "
                for t in tails_subset:
                    if t['index'] == left and t['index'] == mid:
                        pointer_line += " LM"
                    elif t['index'] == right and t['index'] == mid:
                        pointer_line += " MR"
                    elif t['index'] == left:
                        pointer_line += "  L"
                    elif t['index'] == mid:
                        pointer_line += "  M"
                    elif t['index'] == right:
                        pointer_line += "  R"
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n\n"

                narrative += f"**Mid Calculation:**\n"
                narrative += f"```\n"
                narrative += f"mid = ({left} + {right}) // 2 = {mid}\n"
                narrative += f"```\n\n"

                narrative += f"**Comparison:** `tails[{mid}] ({mid_value}) vs {current_num}`\n"
                narrative += f"- {comparison}\n\n"

            elif step_type == "REPLACE_TAIL":
                current_num = data['current_num']
                replace_index = data['replace_index']
                old_value = data['old_value']
                new_value = data['new_value']
                tails_after = data['tails_after']

                narrative += f"**Replacement Found:**\n"
                narrative += f"Position: `tails[{replace_index}]`\n\n"

                narrative += f"**Update:**\n"
                narrative += f"- Old value: `tails[{replace_index}] = {old_value}`\n"
                narrative += f"- New value: `tails[{replace_index}] = {new_value}`\n\n"

                narrative += f"**Reason:** {new_value} is smaller than {old_value}, making it a better candidate for extending subsequences of length {replace_index + 1}\n\n"

                narrative += f"**Tails Array After:**\n```\n"
                narrative += f"{tails_after}\n"
                narrative += "```\n"
                narrative += f"- Length: {len(tails_after)} (unchanged)\n"
                narrative += f"- Updated position: index {replace_index}\n\n"

            elif step_type == "EXTEND_TAIL":
                current_num = data['current_num']
                new_length = data['new_length']
                tails_after = data['tails_after']

                narrative += f"**Extension:**\n"
                narrative += f"Append `{current_num}` to tails array\n\n"

                narrative += f"**Tails Array After:**\n```\n"
                narrative += f"{tails_after}\n"
                narrative += "```\n"
                narrative += f"- Length: {new_length} (increased by 1)\n"
                narrative += f"- New tail: `tails[{new_length - 1}] = {current_num}`\n\n"

                narrative += f"**Meaning:** We found a strictly increasing subsequence of length **{new_length}** ending with value {current_num}\n\n"

        # Summary
        narrative += "---\n\n## Execution Summary\n\n"
        narrative += f"**Final Result:** Longest Increasing Subsequence Length = **{result['lis_length']}**\n\n"

        narrative += f"**Final Tails Array:** `{result['final_tails']}`\n"
        narrative += f"- Length: {len(result['final_tails'])}\n"
        narrative += f"- Each position represents the smallest ending value for that subsequence length\n\n"

        narrative += f"**Performance:**\n"
        narrative += f"- Array size: {len(self.array)}\n"
        narrative += f"- Total operations: {len(steps) - 1} (excluding initialization)\n"
        narrative += f"- Time Complexity: O(n log n) - each element processed with binary search\n"
        narrative += f"- Space Complexity: O(n) - tails array storage\n\n"

        narrative += "**Algorithm Insight:**\n"
        narrative += "The tails array maintains optimal candidates at each length. "
        narrative += "By keeping the smallest possible ending value for each subsequence length, "
        narrative += "we maximize opportunities for future extensions. "
        narrative += f"The final length of the tails array ({len(result['final_tails'])}) equals the LIS length.\n\n"

        # Add Frontend Visualization Hints section
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Tails Array Length** (`tails_length`) - This IS the LIS length, the primary result\n"
        narrative += "- **Current Element** (`current_element.value`) - Shows which number is being processed\n"
        narrative += "- **Tails Array Contents** (`tails[*].value`) - Shows the optimal candidates at each length\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the tails array growth** - When length increases, this is a key moment (new LIS length found)\n"
        narrative += "2. **Show extend vs replace decisions** - Use distinct visual cues (e.g., green for extend, yellow for replace)\n"
        narrative += "3. **Animate binary search** - When searching for replacement position, show the narrowing search space\n"
        narrative += "4. **Emphasize the current element** - Make it clear which array element is being examined\n"
        narrative += "5. **Show tails overlay on input array** - Help learners see the relationship between input and tails\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.array[*].state  // 'pending' | 'examining' | 'processed'\n"
        narrative += "step.data.visualization.array[*].value\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "step.data.visualization.tails[*].value\n"
        narrative += "step.data.visualization.tails[*].index\n"
        narrative += "step.data.visualization.tails[*].state  // 'active' | 'examining' | 'replacing'\n"
        narrative += "step.data.visualization.tails_length\n"
        narrative += "step.data.visualization.current_element.index\n"
        narrative += "step.data.visualization.current_element.value\n"
        narrative += "step.data.visualization.binary_search.left  // When searching\n"
        narrative += "step.data.visualization.binary_search.mid\n"
        narrative += "step.data.visualization.binary_search.right\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "The patience sorting algorithm's power comes from maintaining **optimal candidates** at each subsequence length. "
        narrative += "The most important visualization is the **tails array** - its length IS the answer, and its contents show why. "
        narrative += "Consider using a **dual-panel view**: input array on top, tails array below with clear length indicator. "
        narrative += "The **extend vs replace decision** is the algorithm's \"brain\" - highlight this moment with visual emphasis. "
        narrative += "When binary searching for replacement position, show the search narrowing (similar to binary search visualization). "
        narrative += "The final state should clearly show: input array (all processed), final tails array, and the LIS length prominently displayed. "
        narrative += "Use the `show_tails_overlay` config to help learners understand which input elements correspond to tail values.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Longest Increasing Subsequence algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers

        Returns:
            Standardized trace result with:
                - result: {'lis_length': int, 'final_tails': List[int]}
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

        self.array = input_data['array']

        if not self.array:
            raise ValueError("Array cannot be empty")

        # Initialize
        self.tails = []
        self.current_index = None
        self.current_num = None
        self.search_left = None
        self.search_right = None
        self.search_mid = None
        self.replacement_index = None

        # Set metadata
        self.metadata = {
            'algorithm': 'longest-increasing-subsequence',
            'display_name': 'Longest Increasing Subsequence (Patience Sorting)',
            'visualization_type': 'array',
            'visualization_config': {
                'show_indices': True,
                'show_tails_overlay': True
            },
            'input_size': len(self.array)
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'array_size': len(self.array),
                'initial_array': self.array.copy()
            },
            "🎯 Initialize: Find length of longest strictly increasing subsequence"
        )

        # Process each element
        for i, num in enumerate(self.array):
            self.current_index = i
            self.current_num = num
            self.search_left = None
            self.search_right = None
            self.search_mid = None
            self.replacement_index = None

            # Record checking this element
            last_tail = self.tails[-1] if self.tails else None
            self._add_step(
                "CHECK_ELEMENT",
                {
                    'current_index': i,
                    'current_num': num,
                    'tails_before': self.tails.copy(),
                    'last_tail': last_tail
                },
                f"📍 Examine array[{i}] = {num}"
            )

            # Decision: extend or replace?
            if not self.tails or num > self.tails[-1]:
                # Extend: append to tails
                self.tails.append(num)
                self._add_step(
                    "EXTEND_TAIL",
                    {
                        'current_num': num,
                        'new_length': len(self.tails),
                        'tails_after': self.tails.copy()
                    },
                    f"➕ Extend: {num} > last tail, append to tails (new length: {len(self.tails)})"
                )
            else:
                # Replace: binary search for position
                # Use bisect_left to find leftmost position where tails[pos] >= num
                self.search_left = 0
                self.search_right = len(self.tails) - 1

                # Manual binary search with trace
                left = 0
                right = len(self.tails) - 1

                while left < right:
                    mid = (left + right) // 2
                    self.search_mid = mid
                    mid_value = self.tails[mid]

                    # Record binary search step
                    comparison = f"tails[{mid}] ({mid_value}) < {num}" if mid_value < num else f"tails[{mid}] ({mid_value}) ≥ {num}"
                    self._add_step(
                        "BINARY_SEARCH",
                        {
                            'current_num': num,
                            'left': left,
                            'right': right,
                            'mid': mid,
                            'mid_value': mid_value,
                            'comparison': comparison,
                            'search_range': f"[{left}, {right}]"
                        },
                        f"🔍 Binary search: mid={mid}, tails[{mid}]={mid_value}"
                    )

                    if self.tails[mid] < num:
                        left = mid + 1
                    else:
                        right = mid

                    self.search_left = left
                    self.search_right = right

                # Found replacement position
                pos = left
                self.replacement_index = pos
                old_value = self.tails[pos]
                self.tails[pos] = num

                self._add_step(
                    "REPLACE_TAIL",
                    {
                        'current_num': num,
                        'replace_index': pos,
                        'old_value': old_value,
                        'new_value': num,
                        'tails_after': self.tails.copy()
                    },
                    f"🔄 Replace: tails[{pos}] = {num} (was {old_value})"
                )

        # Build result
        return self._build_trace_result({
            'lis_length': len(self.tails),
            'final_tails': self.tails.copy()
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After examining current element, will we extend
        the tails array or replace an existing value?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after CHECK_ELEMENT, before decision
            if step.type == "CHECK_ELEMENT" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                current_num = step.data['current_num']
                tails_before = step.data['tails_before']
                last_tail = step.data.get('last_tail')

                # Determine correct answer from next step type
                if next_step.type == "EXTEND_TAIL":
                    correct_answer = "extend"
                elif next_step.type == "BINARY_SEARCH":
                    correct_answer = "replace"
                else:
                    continue  # Skip if unexpected

                # Build question
                if not tails_before:
                    question = f"Tails array is empty. What happens with {current_num}?"
                else:
                    question = f"Current number: {current_num}, Last tail: {last_tail}. What's next?"

                predictions.append({
                    'step_index': i,
                    'question': question,
                    'choices': [
                        {'id': 'extend', 'label': f'Extend (append {current_num} to tails)'},
                        {'id': 'replace', 'label': f'Replace (binary search for position)'},
                        {'id': 'skip', 'label': f'Skip (ignore {current_num})'}
                    ],
                    'hint': f"Compare {current_num} with last tail {last_tail}" if last_tail else "First element always extends",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(current_num, last_tail, correct_answer)
                })

        return predictions

    def _get_prediction_explanation(self, current_num: int, last_tail: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "extend":
            if last_tail is None:
                return f"Tails array is empty, so we extend with the first element {current_num}"
            return f"{current_num} > {last_tail}, so we can extend the subsequence by appending to tails"
        elif answer == "replace":
            return f"{current_num} ≤ {last_tail}, so we use binary search to find a position to replace for a better candidate"
        return ""
