# backend/algorithms/two_pointer.py
"""
Two Pointer algorithm tracer for educational visualization.

Implements the "remove duplicates from a sorted array" pattern using
slow and fast pointers. This demonstrates an in-place array modification
technique.

VERSION: 2.0 - QA Feedback Fix for Temporal Incoherence
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class TwoPointerTracer(AlgorithmTracer):
    """
    Tracer for the Two Pointer pattern (Array Deduplication).

    Visualization shows:
    - Array elements with states (unique, duplicate, pending, stale)
    - Pointers (slow for writing, fast for reading)
    - The count of unique elements found so far.

    Prediction points ask: "When the fast pointer finds a new value,
    should it be kept or skipped?"
    """

    def __init__(self):
        super().__init__()
        self.array: List[int] = []
        self.original_array: List[int] = []
        self.slow: int = 0
        self.fast: int = 1
        self.is_complete: bool = False

    def _get_element_state(self, index: int) -> str:
        """Determine the visual state of an array element."""
        if self.is_complete:
            return 'unique' if index < (self.slow + 1) else 'stale'

        if index <= self.slow:
            return 'unique'
        if index < self.fast:
            return 'duplicate'
        if index == self.fast:
            return 'examining'
        return 'pending'

    def _get_visualization_state(self) -> dict:
        """Return current array state with element states and pointers."""
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
            'pointers': {
                'slow': self.slow,
                'fast': self.fast if self.fast < len(self.array) and not self.is_complete else None,
            },
            'metrics': {
                'unique_count': self.slow + 1
            }
        }

    def execute(self, input_data: Any) -> dict:
        """
        Execute the Two Pointer (deduplication) algorithm with trace generation.
        Refactored to fix temporal incoherence based on QA feedback.
        """
        # 1. Input Validation
        if not isinstance(input_data, dict) or 'array' not in input_data:
            raise ValueError("Input must be a dictionary with an 'array' key.")

        self.original_array = input_data['array']
        self.array = self.original_array.copy()

        if len(self.array) > 1 and not all(self.array[i] <= self.array[i+1] for i in range(len(self.array)-1)):
            raise ValueError("Array must be sorted in ascending order.")

        # 2. Metadata Setup
        self.metadata = {
            'algorithm': 'two-pointer',
            'display_name': 'Two Pointer Pattern',
            'visualization_type': 'array',
            'input_size': len(self.array),
            'visualization_config': { 'pointer_colors': { 'slow': 'blue', 'fast': 'red' } }
        }

        # 3. Edge Case Handling
        if not self.array:
            self._add_step("INITIAL_STATE", {}, "🏁 Array is empty, 0 unique elements.")
            return self._build_trace_result({'unique_count': 0, 'final_array': []})

        if len(self.array) == 1:
            self.is_complete = True
            self.slow = 0
            self._add_step("INITIAL_STATE", {}, "🏁 Array has one element, which is unique.")
            return self._build_trace_result({'unique_count': 1, 'final_array': self.array})

        # 4. Initial State
        self.slow = 0
        self.fast = 1
        self._add_step(
            "INITIAL_STATE",
            {},
            "🚀 Start: slow pointer at index 0, fast pointer at index 1."
        )

        # 5. Main Loop (Refactored Logic)
        while self.fast < len(self.array):
            slow_val = self.array[self.slow]
            fast_val = self.array[self.fast]

            # Step 1: The Decision. This step shows the state BEFORE the action.
            self._add_step(
                "COMPARE",
                {
                    'slow_index': self.slow, 'slow_value': slow_val,
                    'fast_index': self.fast, 'fast_value': fast_val,
                },
                f"⚖️ Compare arr[fast] ({fast_val}) with arr[slow] ({slow_val})."
            )

            # Step 2: The Consequence. This step shows the state AFTER the action.
            if fast_val == slow_val:
                # Duplicate found: Perform action, then add step.
                old_fast = self.fast
                self.fast += 1
                self._add_step(
                    "HANDLE_DUPLICATE",
                    {
                        'comparison': f"{fast_val} == {slow_val}",
                        'action': f"Increment fast pointer from {old_fast} to {self.fast}"
                    },
                    "⏭️ Duplicate found. Moving fast pointer."
                )
            else:
                # New unique element found: Perform all actions, then add step.
                old_slow = self.slow
                old_fast = self.fast
                
                self.slow += 1
                self.array[self.slow] = fast_val
                self.fast += 1

                self._add_step(
                    "HANDLE_UNIQUE",
                    {
                        'comparison': f"{fast_val} != {slow_val}",
                        'source_index': old_fast, 'dest_index': self.slow, 'value': fast_val,
                        'action': f"Increment slow to {self.slow}, copy value, increment fast to {self.fast}"
                    },
                    f"✨ New unique element found. Placed {fast_val} at index {self.slow}."
                )

        # 6. Final State
        self.is_complete = True
        unique_count = self.slow + 1
        final_array = self.array[:unique_count]

        self._add_step(
            "ALGORITHM_COMPLETE",
            { 'unique_count': unique_count, 'final_array_slice': final_array },
            f"✅ Complete! Found {unique_count} unique elements."
        )

        # 7. Return Result
        return self._build_trace_result({
            'unique_count': unique_count,
            'final_array': final_array
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """Identify prediction opportunities at each comparison step."""
        predictions = []
        for i, step in enumerate(self.trace):
            if step.type == "COMPARE" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                compare_data = step.data
                slow_val = compare_data['slow_value']
                fast_val = compare_data['fast_value']

                correct_answer = ""
                # Updated to check for new, consolidated step types
                if next_step.type == "HANDLE_DUPLICATE":
                    correct_answer = "skip"
                elif next_step.type == "HANDLE_UNIQUE":
                    correct_answer = "keep"
                else:
                    continue

                predictions.append({
                    'step_index': i,
                    'question': f"The fast pointer sees value ({fast_val}) and the last unique value is ({slow_val}). What happens next?",
                    'choices': [
                        {'id': 'keep', 'label': 'Keep: New unique element found.'},
                        {'id': 'skip', 'label': 'Skip: Duplicate element found.'}
                    ],
                    'hint': f"Compare {fast_val} and {slow_val}. Are they equal?",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(slow_val, fast_val, correct_answer)
                })
        return predictions

    def _get_prediction_explanation(self, slow_val: int, fast_val: int, answer: str) -> str:
        """Generate a clear explanation for the prediction outcome."""
        if answer == "skip":
            return f"Correct. Since {fast_val} == {slow_val}, it's a duplicate. We only move the fast pointer to check the next element."
        elif answer == "keep":
            return f"Correct. Since {fast_val} != {slow_val}, it's a new unique element. We move the slow pointer, copy the value, and then move the fast pointer."
        return ""

    def _render_array_state(self, viz_data: dict) -> str:
        """Helper to create a text visualization of the array state."""
        array = viz_data['array']
        pointers = viz_data['pointers']
        s = "Index: " + " ".join(f"{elem['index']:<3}" for elem in array) + "\n"
        s += "Value: " + " ".join(f"{elem['value']:<3}" for elem in array) + "\n"
        s += "State: " + " ".join(f"{elem['state'][0].upper():<3}" for elem in array) + "\n"
        pointer_line = "       "
        for i in range(len(array)):
            p_str = ""
            if pointers.get('slow') == i: p_str += "S"
            if pointers.get('fast') == i: p_str += "F"
            pointer_line += f"{p_str:<4}"
        s += pointer_line.rstrip() + "\n"
        return s

    def generate_narrative(self, trace_result: dict) -> str:
        """Generate a human-readable narrative from the Two Pointer trace."""
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        narrative = f"# Two Pointer Pattern: Array Deduplication\n\n"
        narrative += f"**Input Array:** `{self.original_array}`\n"
        narrative += f"**Goal:** Remove duplicates in-place and find the count of unique elements.\n"
        narrative += f"**Result:** Found **{result['unique_count']}** unique elements. Final unique array: `{result['final_array']}`\n\n---\n\n"

        for step in steps:
            step_num, step_type, description, data = step['step'], step['type'], step['description'], step['data']
            viz = data.get('visualization', {})

            narrative += f"## Step {step_num}: {description}\n\n"

            if viz:
                narrative += "**Array State:**\n```\n" + self._render_array_state(viz) + "```\n"
                narrative += f"**Pointers:** slow = `{viz['pointers']['slow']}`, fast = `{viz['pointers'].get('fast', 'None')}`\n"
                narrative += f"**Unique Count so far:** `{viz['metrics']['unique_count']}`\n\n"

            if step_type == "COMPARE":
                narrative += "**Decision Logic:**\n"
                narrative += f"- Compare value at fast pointer (`{data['fast_value']}`) with value at slow pointer (`{data['slow_value']}`).\n"
                is_duplicate = data['fast_value'] == data['slow_value']
                narrative += f"- **Result:** `{data['fast_value']} {'==' if is_duplicate else '!='} {data['slow_value']}` → **{'Duplicate' if is_duplicate else 'Unique'}**\n\n"
            
            elif step_type == "HANDLE_DUPLICATE":
                narrative += "**Action:**\n"
                narrative += "- The values are the same, so this is a duplicate.\n"
                narrative += f"- We increment the `fast` pointer to look at the next element.\n\n"

            elif step_type == "HANDLE_UNIQUE":
                narrative += "**Action:**\n"
                narrative += "- The values are different, so we found a new unique element.\n"
                narrative += f"- The `slow` pointer is moved to index `{data['dest_index']}`.\n"
                narrative += f"- The unique value (`{data['value']}`) is copied to `arr[{data['dest_index']}]`.\n"
                narrative += f"- The `fast` pointer is moved to continue scanning.\n\n"

            elif step_type == "ALGORITHM_COMPLETE":
                narrative += f"The `fast` pointer has reached the end of the array. The algorithm is complete.\n"
                narrative += f"The unique elements are from index 0 to the final `slow` pointer position ({self.slow}).\n\n"
                narrative += f"**Final Unique Array Slice:** `{data['final_array_slice']}`\n"
                narrative += f"**Total Unique Elements:** `{data['unique_count']}`\n\n"

            narrative += "---\n\n"

        return narrative
