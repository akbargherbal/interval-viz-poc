
"""
Kadane's Algorithm tracer for educational visualization.

Implements Kadane's Algorithm to find the maximum sum contiguous subarray
using dynamic programming with complete trace generation for step-by-step
visualization and prediction mode.

VERSION: 2.1 - Backend Checklist v2.2 Compliance
- Added Frontend Visualization Hints section to narrative
- Follows Universal Pedagogical Principles
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class KadanesAlgorithmTracer(AlgorithmTracer):
    """
    Tracer for Kadane's Algorithm on integer arrays.

    Visualization shows:
    - Array elements with states (examining, in_current_subarray, in_max_subarray)
    - Current sum tracking (running sum at each position)
    - Maximum sum found so far
    - Subarray boundaries (start/end indices)

    Prediction points ask: "Will we add this element to current sum or reset?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.current_sum = 0
        self.max_sum = float('-inf')
        self.current_start = 0
        self.current_end = 0
        self.max_start = 0
        self.max_end = 0
        self.current_index = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states and subarray tracking.

        Element states:
        - 'examining': Current element being processed
        - 'in_current_subarray': Part of current running subarray
        - 'in_max_subarray': Part of the maximum sum subarray found so far
        - 'excluded': Not part of any tracked subarray
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
            'current_sum': self.current_sum,
            'max_sum': self.max_sum if self.max_sum != float('-inf') else None,
            'current_subarray': {
                'start': self.current_start,
                'end': self.current_end
            },
            'max_subarray': {
                'start': self.max_start,
                'end': self.max_end
            }
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        if index == self.current_index:
            return 'examining'
        if self.max_start <= index <= self.max_end:
            return 'in_max_subarray'
        if self.current_start <= index <= self.current_end and index < self.current_index:
            return 'in_current_subarray'
        return 'excluded'

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Kadane's Algorithm trace.

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
        narrative = "# Kadane's Algorithm Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {self.array}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Maximum Sum Found:** {result['max_sum']}\n"
        narrative += f"**Maximum Subarray:** indices [{result['subarray']['start']}, {result['subarray']['end']}] = {result['subarray']['values']}\n\n"
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
            if step_type == "ITERATE":
                index = data['index']
                value = data['value']
                decision = data['decision']
                old_current = data['old_current_sum']
                new_current = data['new_current_sum']
                calculation = data['calculation']

                narrative += f"**Current Element:** index {index}, value = **{value}**\n\n"

                narrative += f"**Decision Logic:**\n"
                narrative += f"```\n{calculation}\n```\n\n"

                if decision == "add_to_current":
                    narrative += f"**Decision:** Add to current sum (extending subarray)\n"
                    narrative += f"- Previous current_sum: {old_current}\n"
                    narrative += f"- Add current element: {old_current} + {value} = {new_current}\n"
                    narrative += f"- Comparison: max({value}, {old_current} + {value}) = max({value}, {new_current}) = {new_current}\n"
                    narrative += f"- Result: {new_current} ≥ {value}, so **extend** the current subarray\n\n"

                    narrative += f"**Current Subarray:**\n"
                    narrative += f"- Range: indices [{viz['current_subarray']['start']}, {viz['current_subarray']['end']}]\n"
                    narrative += f"- Sum: {viz['current_sum']}\n\n"

                elif decision == "reset_to_current":
                    narrative += f"**Decision:** Reset to current element (start new subarray)\n"
                    narrative += f"- Previous current_sum: {old_current}\n"
                    narrative += f"- Current element: {value}\n"
                    narrative += f"- Comparison: max({value}, {old_current} + {value}) = max({value}, {old_current + value}) = {new_current}\n"
                    narrative += f"- Result: {value} > {old_current + value}, so **start fresh** from this element\n\n"

                    narrative += f"**New Subarray Started:**\n"
                    narrative += f"- Range: index [{viz['current_subarray']['start']}, {viz['current_subarray']['end']}]\n"
                    narrative += f"- Sum: {viz['current_sum']}\n\n"

                # Show array visualization
                narrative += "**Array State:**\n```\n"
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in viz['array']) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                
                # Show current position
                pointer_line = "       "
                for elem in viz['array']:
                    if elem['index'] == index:
                        pointer_line += "  ^"
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n\n"

            elif step_type == "UPDATE_MAX":
                old_max = data['old_max_sum']
                new_max = data['new_max_sum']
                comparison = data['comparison']
                subarray_start = data['subarray_start']
                subarray_end = data['subarray_end']

                narrative += f"**Maximum Sum Update:**\n\n"
                narrative += f"**Comparison:** `{comparison}`\n"
                narrative += f"- Current sum: {new_max}\n"
                narrative += f"- Previous max: {old_max if old_max != float('-inf') else 'None (first update)'}\n"
                narrative += f"- Result: {new_max} > {old_max if old_max != float('-inf') else '-∞'} ✓\n\n"

                narrative += f"**New Maximum Found:**\n"
                narrative += f"- Max sum: **{new_max}**\n"
                narrative += f"- Subarray range: indices [{subarray_start}, {subarray_end}]\n"
                
                # Show subarray values
                subarray_values = self.array[subarray_start:subarray_end + 1]
                narrative += f"- Subarray values: {subarray_values}\n"
                narrative += f"- Verification: sum({subarray_values}) = {sum(subarray_values)} = {new_max} ✓\n\n"

                # Show array with max subarray highlighted
                narrative += "**Array with Maximum Subarray:**\n```\n"
                narrative += "Index: " + " ".join(f"{elem['index']:3d}" for elem in viz['array']) + "\n"
                narrative += "Value: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                
                # Show max subarray markers
                marker_line = "       "
                for elem in viz['array']:
                    if subarray_start <= elem['index'] <= subarray_end:
                        marker_line += " [M]" if elem['index'] == subarray_start else (" M]" if elem['index'] == subarray_end else "  M")
                    else:
                        marker_line += "   "
                narrative += marker_line + "\n"
                narrative += "```\n"
                narrative += "*M = Maximum subarray*\n\n"

            elif step_type == "ADD_TO_CURRENT":
                index = data['index']
                value = data['value']
                old_sum = data['old_sum']
                new_sum = data['new_sum']

                narrative += f"**Extending Current Subarray:**\n\n"
                narrative += f"**Calculation:**\n"
                narrative += f"- Previous sum: {old_sum}\n"
                narrative += f"- Current element: {value}\n"
                narrative += f"- New sum: {old_sum} + {value} = {new_sum}\n\n"

                narrative += f"**Current Subarray:**\n"
                narrative += f"- Range: indices [{viz['current_subarray']['start']}, {viz['current_subarray']['end']}]\n"
                narrative += f"- Sum: {viz['current_sum']}\n\n"

            elif step_type == "RESET_CURRENT":
                index = data['index']
                value = data['value']
                reason = data['reason']

                narrative += f"**Starting New Subarray:**\n\n"
                narrative += f"**Reason:** {reason}\n"
                narrative += f"- New subarray starts at index {index}\n"
                narrative += f"- Initial value: {value}\n"
                narrative += f"- Current sum reset to: {value}\n\n"

                narrative += f"**Current Subarray:**\n"
                narrative += f"- Range: index [{viz['current_subarray']['start']}, {viz['current_subarray']['end']}]\n"
                narrative += f"- Sum: {viz['current_sum']}\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Final Result:**\n"
        narrative += f"- Maximum sum: **{result['max_sum']}**\n"
        narrative += f"- Subarray indices: [{result['subarray']['start']}, {result['subarray']['end']}]\n"
        narrative += f"- Subarray values: {result['subarray']['values']}\n"
        narrative += f"- Verification: sum({result['subarray']['values']}) = {sum(result['subarray']['values'])} = {result['max_sum']} ✓\n\n"

        narrative += f"**Algorithm Efficiency:**\n"
        narrative += f"- Elements processed: {len(self.array)}\n"
        narrative += f"- Time Complexity: O(n) - single pass through array\n"
        narrative += f"- Space Complexity: O(1) - constant extra space\n\n"

        narrative += f"**Key Insight:**\n"
        narrative += f"At each position, we decide: extend the current subarray (if it helps) or start fresh (if previous sum is negative). "
        narrative += f"This greedy choice at each step guarantees finding the global maximum.\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Current Sum** (`current_sum`) - Shows the running sum of the current subarray being considered\n"
        narrative += "- **Max Sum** (`max_sum`) - The best sum found so far (goal metric)\n"
        narrative += "- **Decision Logic** - The comparison `max(num, current + num)` is the heart of the algorithm\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the decision moment** - When processing each element, emphasize the choice: extend vs. reset\n"
        narrative += "2. **Show subarray evolution** - Use distinct colors for `in_current_subarray` (candidate) vs `in_max_subarray` (best so far)\n"
        narrative += "3. **Animate sum updates** - When current_sum changes, show the arithmetic visually (old + new = result)\n"
        narrative += "4. **Celebrate max updates** - When max_sum improves, use visual feedback (pulse, color change, trophy icon)\n"
        narrative += "5. **Show the examining element** - The current element being processed should stand out clearly\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.current_sum\n"
        narrative += "step.data.visualization.max_sum\n"
        narrative += "step.data.visualization.current_subarray.start\n"
        narrative += "step.data.visualization.current_subarray.end\n"
        narrative += "step.data.visualization.max_subarray.start\n"
        narrative += "step.data.visualization.max_subarray.end\n"
        narrative += "step.data.visualization.array[*].state  // 'examining' | 'in_current_subarray' | 'in_max_subarray' | 'excluded'\n"
        narrative += "step.data.visualization.array[*].value\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "step.data.decision  // 'add_to_current' | 'reset_to_current' (for ITERATE steps)\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Kadane's Algorithm is elegant because it makes a **local greedy decision** at each element that leads to the **global optimal solution**. "
        narrative += "The most pedagogically important moment is the decision: \"Should I extend my current subarray or start fresh?\" "
        narrative += "Visualize this as a **fork in the road** at each element. "
        narrative += "When the algorithm resets (starts a new subarray), show the old subarray fading away and a new one beginning. "
        narrative += "When max_sum updates, emphasize that we've found a **new champion** - this is a milestone moment. "
        narrative += "Consider using a **dual-track visualization**: one track showing the current candidate subarray (dynamic, changes frequently) "
        narrative += "and another showing the best subarray found so far (stable, only updates when beaten). "
        narrative += "The contrast between these two tracks helps students understand the algorithm's strategy: "
        narrative += "constantly exploring new possibilities while remembering the best one encountered.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Kadane's Algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers (can contain negative numbers)

        Returns:
            Standardized trace result with:
                - result: {
                    'max_sum': int,
                    'subarray': {
                        'start': int,
                        'end': int,
                        'values': List[int]
                    }
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

        self.array = input_data['array']

        if not self.array:
            raise ValueError("Array cannot be empty")

        if not all(isinstance(x, int) for x in self.array):
            raise ValueError("Array must contain only integers")

        # Initialize algorithm state
        self.current_sum = self.array[0]
        self.max_sum = self.array[0]
        self.current_start = 0
        self.current_end = 0
        self.max_start = 0
        self.max_end = 0
        self.current_index = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'kadanes-algorithm',
            'display_name': "Kadane's Algorithm",
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True,
                'highlight_subarray': True,
                'show_current_sum': True
            },
            'input_size': len(self.array)
        }

        # Initial state - first element
        self._add_step(
            "ITERATE",
            {
                'index': 0,
                'value': self.array[0],
                'decision': 'initialize',
                'old_current_sum': 0,
                'new_current_sum': self.array[0],
                'calculation': f"Initialize: current_sum = {self.array[0]}, max_sum = {self.array[0]}"
            },
            f"🔍 Initialize with first element: {self.array[0]}"
        )

        # Record initial max
        self._add_step(
            "UPDATE_MAX",
            {
                'old_max_sum': float('-inf'),
                'new_max_sum': self.array[0],
                'comparison': f"{self.array[0]} > -∞",
                'subarray_start': 0,
                'subarray_end': 0
            },
            f"📊 Initial maximum: {self.array[0]} at index [0, 0]"
        )

        # Process remaining elements
        for i in range(1, len(self.array)):
            self.current_index = i
            num = self.array[i]

            # Calculate: max(num, current_sum + num)
            extend_sum = self.current_sum + num
            old_current = self.current_sum

            if num > extend_sum:
                # Reset: starting fresh is better
                decision = "reset_to_current"
                self.current_sum = num
                self.current_start = i
                self.current_end = i

                self._add_step(
                    "ITERATE",
                    {
                        'index': i,
                        'value': num,
                        'decision': decision,
                        'old_current_sum': old_current,
                        'new_current_sum': self.current_sum,
                        'calculation': f"max({num}, {old_current} + {num}) = max({num}, {extend_sum}) = {self.current_sum}"
                    },
                    f"🔄 Reset: Start new subarray at index {i} (value = {num})"
                )

            else:
                # Extend: adding to current is better or equal
                decision = "add_to_current"
                self.current_sum = extend_sum
                self.current_end = i

                self._add_step(
                    "ITERATE",
                    {
                        'index': i,
                        'value': num,
                        'decision': decision,
                        'old_current_sum': old_current,
                        'new_current_sum': self.current_sum,
                        'calculation': f"max({num}, {old_current} + {num}) = max({num}, {extend_sum}) = {self.current_sum}"
                    },
                    f"➕ Extend: Add {num} to current subarray (sum = {self.current_sum})"
                )

            # Check if we found a new maximum
            if self.current_sum > self.max_sum:
                old_max = self.max_sum
                self.max_sum = self.current_sum
                self.max_start = self.current_start
                self.max_end = self.current_end

                self._add_step(
                    "UPDATE_MAX",
                    {
                        'old_max_sum': old_max,
                        'new_max_sum': self.max_sum,
                        'comparison': f"{self.current_sum} > {old_max}",
                        'subarray_start': self.max_start,
                        'subarray_end': self.max_end
                    },
                    f"🎯 New maximum found: {self.max_sum} at indices [{self.max_start}, {self.max_end}]"
                )

        # Build result
        result = {
            'max_sum': self.max_sum,
            'subarray': {
                'start': self.max_start,
                'end': self.max_end,
                'values': self.array[self.max_start:self.max_end + 1]
            }
        }

        return self._build_trace_result(result)

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After seeing the current element, will we add it
        to the current subarray or start a new subarray?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: At ITERATE steps (except first initialization)
            if step.type == "ITERATE" and step.data.get('decision') != 'initialize':
                index = step.data['index']
                value = step.data['value']
                old_current = step.data['old_current_sum']
                decision = step.data['decision']

                # Determine correct answer
                if decision == "add_to_current":
                    correct_answer = "extend"
                elif decision == "reset_to_current":
                    correct_answer = "reset"
                else:
                    continue

                predictions.append({
                    'step_index': i - 1,  # Predict before this step
                    'question': f"Element at index {index} is {value}. Current sum is {old_current}. What should we do?",
                    'choices': [
                        {'id': 'extend', 'label': f'Extend subarray (add {value} to current sum)'},
                        {'id': 'reset', 'label': f'Start new subarray (reset to {value})'},
                        {'id': 'skip', 'label': f'Skip this element'}
                    ],
                    'hint': f"Compare {value} with {old_current} + {value}. Which is larger?",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(value, old_current, correct_answer)
                })

        return predictions

    def _get_prediction_explanation(self, value: int, old_current: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        extend_sum = old_current + value
        
        if answer == "extend":
            return (f"Extending is correct: {old_current} + {value} = {extend_sum}. "
                   f"Since {extend_sum} ≥ {value}, adding to the current subarray gives a better or equal sum.")
        elif answer == "reset":
            return (f"Resetting is correct: {old_current} + {value} = {extend_sum}. "
                   f"Since {value} > {extend_sum}, starting fresh from this element gives a better sum.")
        return ""
