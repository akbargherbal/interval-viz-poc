# backend/algorithms/binary_search.py
"""
Binary Search algorithm tracer for educational visualization.

Implements iterative binary search on a sorted array with complete
trace generation for step-by-step visualization and prediction mode.
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class BinarySearchTracer(AlgorithmTracer):
    """
    Tracer for Binary Search algorithm on sorted arrays.
    
    Visualization shows:
    - Array elements with states (excluded, active_range, examining, found)
    - Pointers (left, right, mid, target)
    - Search space reduction at each step
    
    Prediction points ask: "Will we search left, right, or is target found?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.target = None
        self.left = 0
        self.right = 0
        self.mid = None
        self.found_index = None
        self.search_complete = False

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states and pointers.
        
        Element states:
        - 'examining': Current mid element being compared
        - 'excluded': Outside current search range
        - 'active_range': Within current [left, right] range
        - 'found': Target element (when found)
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
            'pointers': {
                'left': self.left,
                'right': self.right,
                'mid': self.mid,
                'target': self.target
            },
            'search_space_size': self.right - self.left + 1 if not self.search_complete else 0
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        if self.found_index is not None and index == self.found_index:
            return 'found'
        if self.mid is not None and index == self.mid:
            return 'examining'
        if self.search_complete:
            return 'excluded'
        if index < self.left or index > self.right:
            return 'excluded'
        return 'active_range'

    def execute(self, input_data: Any) -> dict:
        """
        Execute binary search algorithm with trace generation.
        
        Args:
            input_data: dict with keys:
                - 'array': List of integers (must be sorted)
                - 'target': Integer to search for
        
        Returns:
            Standardized trace result with:
                - result: {'found': bool, 'index': int or None, 'comparisons': int}
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='array'
        
        Raises:
            ValueError: If array is not sorted or input is invalid
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if 'array' not in input_data or 'target' not in input_data:
            raise ValueError("Input must contain 'array' and 'target' keys")
        
        self.array = input_data['array']
        self.target = input_data['target']
        
        if not self.array:
            raise ValueError("Array cannot be empty")
        
        # Validate array is sorted
        if not all(self.array[i] <= self.array[i+1] for i in range(len(self.array)-1)):
            raise ValueError("Array must be sorted in ascending order")
        
        # Initialize search
        self.left = 0
        self.right = len(self.array) - 1
        self.mid = None
        self.found_index = None
        self.search_complete = False
        comparisons = 0
        
        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'binary-search',
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True,
                'pointer_colors': {
                    'left': 'blue',
                    'right': 'red',
                    'mid': 'yellow',
                    'target': 'green'
                }
            },
            'input_size': len(self.array),
            'target_value': self.target
        }
        
        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'target': self.target,
                'array_size': len(self.array),
                'search_range': f"[{self.left}, {self.right}]"
            },
            f"🔍 Searching for {self.target} in sorted array of {len(self.array)} elements"
        )
        
        # Binary search loop
        while self.left <= self.right:
            # Calculate mid
            self.mid = (self.left + self.right) // 2
            mid_value = self.array[self.mid]
            
            self._add_step(
                "CALCULATE_MID",
                {
                    'mid_index': self.mid,
                    'mid_value': mid_value,
                    'left': self.left,
                    'right': self.right,
                    'calculation': f"mid = ({self.left} + {self.right}) // 2 = {self.mid}"
                },
                f"📍 Calculate middle: index {self.mid} (value = {mid_value})"
            )
            
            # Compare mid with target
            comparisons += 1
            
            if mid_value == self.target:
                # Target found!
                self.found_index = self.mid
                self.search_complete = True
                
                self._add_step(
                    "TARGET_FOUND",
                    {
                        'index': self.mid,
                        'value': mid_value,
                        'comparisons': comparisons
                    },
                    f"✅ Found target {self.target} at index {self.mid} (after {comparisons} comparisons)"
                )
                
                return self._build_trace_result({
                    'found': True,
                    'index': self.mid,
                    'comparisons': comparisons
                })
            
            elif mid_value < self.target:
                # Target is in right half
                self._add_step(
                    "SEARCH_RIGHT",
                    {
                        'comparison': f"{mid_value} < {self.target}",
                        'action': 'eliminate_left_half',
                        'old_left': self.left,
                        'new_left': self.mid + 1,
                        'eliminated_elements': self.mid - self.left + 1
                    },
                    f"➡️ {mid_value} < {self.target}, search right half (eliminate {self.mid - self.left + 1} elements)"
                )
                self.left = self.mid + 1
                
            else:  # mid_value > self.target
                # Target is in left half
                self._add_step(
                    "SEARCH_LEFT",
                    {
                        'comparison': f"{mid_value} > {self.target}",
                        'action': 'eliminate_right_half',
                        'old_right': self.right,
                        'new_right': self.mid - 1,
                        'eliminated_elements': self.right - self.mid + 1
                    },
                    f"⬅️ {mid_value} > {self.target}, search left half (eliminate {self.right - self.mid + 1} elements)"
                )
                self.right = self.mid - 1
        
        # Target not found
        self.search_complete = True
        
        self._add_step(
            "TARGET_NOT_FOUND",
            {
                'comparisons': comparisons,
                'final_state': 'search_space_empty'
            },
            f"❌ Target {self.target} not found in array (after {comparisons} comparisons)"
        )
        
        return self._build_trace_result({
            'found': False,
            'index': None,
            'comparisons': comparisons
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.
        
        Students predict: "After comparing mid with target, will we search
        left, search right, or have we found the target?"
        
        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []
        
        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after calculating mid, before decision
            if step.type == "CALCULATE_MID" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                mid_value = step.data['mid_value']
                
                # Determine correct answer from next step type
                if next_step.type == "TARGET_FOUND":
                    correct_answer = "found"
                elif next_step.type == "SEARCH_LEFT":
                    correct_answer = "search-left"
                elif next_step.type == "SEARCH_RIGHT":
                    correct_answer = "search-right"
                else:
                    continue  # Skip if unexpected step type
                
                predictions.append({
                    'step_index': i,
                    'question': f"Compare mid value ({mid_value}) with target ({self.target}). What's next?",
                    'choices': [
                        {'id': 'found', 'label': f'Found! ({mid_value} == {self.target})'},
                        {'id': 'search-left', 'label': f'Search Left ({mid_value} > {self.target})'},
                        {'id': 'search-right', 'label': f'Search Right ({mid_value} < {self.target})'}
                    ],
                    'hint': f"Compare {mid_value} with {self.target}",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(mid_value, self.target, correct_answer)
                })
        
        return predictions

    def _get_prediction_explanation(self, mid_value: int, target: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "found":
            return f"{mid_value} == {target}, so the target is found at this index!"
        elif answer == "search-left":
            return f"{mid_value} > {target}, so the target must be in the left half (smaller values)"
        elif answer == "search-right":
            return f"{mid_value} < {target}, so the target must be in the right half (larger values)"
        return ""