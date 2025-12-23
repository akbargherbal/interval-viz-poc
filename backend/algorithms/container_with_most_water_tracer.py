
"""
Container With Most Water algorithm tracer for educational visualization.

Implements two-pointer technique to find maximum water container area with complete
trace generation for step-by-step visualization and prediction mode.

VERSION: 2.5 - Backend Checklist v2.5 Compliance
- Universal Pedagogical Principles applied
- Frontend Visualization Hints section included
- Result field traceability implemented
- Explicit arithmetic in all calculations
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class ContainerWithMostWaterTracer(AlgorithmTracer):
    """
    Tracer for Container With Most Water algorithm using two-pointer technique.

    Visualization shows:
    - Array elements representing heights with states (active, examining, excluded)
    - Pointers (left, right) showing current container boundaries
    - Current area calculation and maximum area tracking
    - Visual representation of container formed by two heights

    Prediction points ask: "Which pointer should we move next - left or right?"
    """

    def __init__(self):
        super().__init__()
        self.heights = []
        self.left = 0
        self.right = 0
        self.max_area = 0
        self.max_left = None
        self.max_right = None
        self.current_area = 0
        self.search_complete = False

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states and pointers.

        Element states:
        - 'examining': Current left and right elements forming container
        - 'excluded': Elements outside current [left, right] range
        - 'active': Elements within current range but not being examined
        - 'max_container': Elements forming the maximum area container (final state)
        """
        if not self.heights:
            return {}

        return {
            'array': [
                {
                    'index': i,
                    'value': v,
                    'state': self._get_element_state(i)
                }
                for i, v in enumerate(self.heights)
            ],
            'pointers': {
                'left': self.left,
                'right': self.right
            },
            'current_area': self.current_area,
            'max_area': self.max_area,
            'container_width': self.right - self.left if not self.search_complete else (self.max_right - self.max_left if self.max_right is not None else 0),
            'container_height': min(self.heights[self.left], self.heights[self.right]) if not self.search_complete and self.left < len(self.heights) and self.right < len(self.heights) else 0
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        if self.search_complete:
            # After search completes, highlight max container
            if self.max_left is not None and self.max_right is not None:
                if index == self.max_left or index == self.max_right:
                    return 'max_container'
            return 'excluded'
        
        if index == self.left or index == self.right:
            return 'examining'
        if index < self.left or index > self.right:
            return 'excluded'
        return 'active'

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Container With Most Water trace.

        Shows complete execution flow with all decision data visible, explicit
        arithmetic calculations, and result field traceability.

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
        narrative = "# Container With Most Water Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Heights:** {self.heights}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"
        narrative += f"**Maximum Area Found:** {result['max_area']} square units\n"
        narrative += f"**Optimal Container:** indices [{result['left_index']}, {result['right_index']}] "
        narrative += f"with heights [{result['left_height']}, {result['right_height']}]\n"
        narrative += f"**Total Iterations:** {result['iterations']}\n\n"
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
                narrative += f"**Algorithm Setup:**\n"
                narrative += f"- Heights array: {data['heights']}\n"
                narrative += f"- Array size: {data['array_size']} elements\n"
                narrative += f"- Strategy: Two-pointer technique (start at both ends, move inward)\n\n"

                narrative += "**Initial Pointers:**\n"
                narrative += f"- Left pointer: index {data['left']} (height = {data['left_height']})\n"
                narrative += f"- Right pointer: index {data['right']} (height = {data['right_height']})\n\n"

                narrative += "**Tracking Variables:**\n"
                narrative += f"- `max_area`: {data['max_area']} (will track maximum area found)\n"
                narrative += f"- `max_left`: None (will track left index of max container)\n"
                narrative += f"- `max_right`: None (will track right index of max container)\n\n"

                narrative += "**Array Visualization:**\n```\n"
                narrative += "Index:  " + " ".join(f"{elem['index']:3d}" for elem in viz['array']) + "\n"
                narrative += "Height: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                narrative += "        " + " ".join("  ^" if i == 0 or i == len(viz['array'])-1 else "   " for i in range(len(viz['array']))) + "\n"
                narrative += "        " + " ".join("  L" if i == 0 else ("  R" if i == len(viz['array'])-1 else "   ") for i in range(len(viz['array']))) + "\n"
                narrative += "```\n\n"

            elif step_type == "CALCULATE_AREA":
                left_idx = data['left']
                right_idx = data['right']
                left_height = data['left_height']
                right_height = data['right_height']
                width = data['width']
                height = data['height']
                area = data['area']

                narrative += f"**Current Container:**\n"
                narrative += f"- Left boundary: index {left_idx} (height = {left_height})\n"
                narrative += f"- Right boundary: index {right_idx} (height = {right_height})\n\n"

                narrative += f"**Area Calculation:**\n"
                narrative += f"```\n"
                narrative += f"Width = right_index - left_index\n"
                narrative += f"      = {right_idx} - {left_idx}\n"
                narrative += f"      = {width}\n\n"
                narrative += f"Height = min(left_height, right_height)\n"
                narrative += f"       = min({left_height}, {right_height})\n"
                narrative += f"       = {height}\n\n"
                narrative += f"Area = Width × Height\n"
                narrative += f"     = {width} × {height}\n"
                narrative += f"     = {area}\n"
                narrative += f"```\n\n"

                narrative += f"**Explanation:** Container height is limited by the shorter wall ({height}). "
                narrative += f"Water would overflow the shorter side, so we use min({left_height}, {right_height}) = {height}.\n\n"

                narrative += "**Current State:**\n```\n"
                active_elements = [elem for elem in viz['array'] if elem['state'] in ['active', 'examining']]
                narrative += "Index:  " + " ".join(f"{elem['index']:3d}" for elem in active_elements) + "\n"
                narrative += "Height: " + " ".join(f"{elem['value']:3d}" for elem in active_elements) + "\n"
                
                pointer_line = "        "
                for elem in active_elements:
                    if elem['index'] == left_idx:
                        pointer_line += "  L"
                    elif elem['index'] == right_idx:
                        pointer_line += "  R"
                    else:
                        pointer_line += "   "
                narrative += pointer_line + "\n"
                narrative += "```\n"
                narrative += f"*Container width: {viz['container_width']}, height: {viz['container_height']}, area: {viz['current_area']}*\n\n"

            elif step_type == "UPDATE_MAX":
                old_max = data['old_max_area']
                new_max = data['new_max_area']
                left_idx = data['left']
                right_idx = data['right']

                narrative += f"**New Maximum Found!**\n\n"
                narrative += f"**Comparison:** Current area ({new_max}) vs Previous max ({old_max})\n"
                narrative += f"- Compare: {new_max} > {old_max} ✓\n"
                narrative += f"- Decision: Update maximum area\n\n"

                narrative += f"**Updates:**\n"
                narrative += f"- `max_area`: {old_max} → {new_max}\n"
                narrative += f"- `max_left`: updated to {left_idx}\n"
                narrative += f"- `max_right`: updated to {right_idx}\n\n"

                narrative += f"**Tracking Purpose:** These variables (`max_area`, `max_left`, `max_right`) are tracked "
                narrative += f"because the final result needs to return the maximum area and the indices that formed it.\n\n"

            elif step_type == "MOVE_LEFT":
                left_height = data['left_height']
                right_height = data['right_height']
                old_left = data['old_left']
                new_left = data['new_left']

                narrative += f"**Decision: Move Left Pointer**\n\n"
                narrative += f"**Comparison:** Left height ({left_height}) vs Right height ({right_height})\n"
                narrative += f"- Compare: {left_height} < {right_height} ✓\n"
                narrative += f"- Conclusion: Left side is the limiting factor (shorter wall)\n\n"

                narrative += f"**Reasoning:**\n"
                narrative += f"- Current container height is limited by left side ({left_height})\n"
                narrative += f"- Moving right pointer would only decrease width, keeping same height limit\n"
                narrative += f"- Moving left pointer might find a taller wall, potentially increasing area\n\n"

                narrative += f"**Pointer Update:**\n"
                narrative += f"- Left pointer: {old_left} → {new_left}\n"
                narrative += f"- Right pointer: {viz['pointers']['right']} (unchanged)\n\n"

                if viz['pointers']['left'] <= viz['pointers']['right']:
                    remaining = [elem for elem in viz['array'] if elem['state'] in ['active', 'examining']]
                    narrative += f"**Remaining Search Space:**\n```\n"
                    narrative += "Index:  " + " ".join(f"{elem['index']:3d}" for elem in remaining) + "\n"
                    narrative += "Height: " + " ".join(f"{elem['value']:3d}" for elem in remaining) + "\n"
                    narrative += "```\n\n"

            elif step_type == "MOVE_RIGHT":
                left_height = data['left_height']
                right_height = data['right_height']
                old_right = data['old_right']
                new_right = data['new_right']

                narrative += f"**Decision: Move Right Pointer**\n\n"
                narrative += f"**Comparison:** Left height ({left_height}) vs Right height ({right_height})\n"
                narrative += f"- Compare: {right_height} < {left_height} ✓\n"
                narrative += f"- Conclusion: Right side is the limiting factor (shorter wall)\n\n"

                narrative += f"**Reasoning:**\n"
                narrative += f"- Current container height is limited by right side ({right_height})\n"
                narrative += f"- Moving left pointer would only decrease width, keeping same height limit\n"
                narrative += f"- Moving right pointer might find a taller wall, potentially increasing area\n\n"

                narrative += f"**Pointer Update:**\n"
                narrative += f"- Left pointer: {viz['pointers']['left']} (unchanged)\n"
                narrative += f"- Right pointer: {old_right} → {new_right}\n\n"

                if viz['pointers']['left'] <= viz['pointers']['right']:
                    remaining = [elem for elem in viz['array'] if elem['state'] in ['active', 'examining']]
                    narrative += f"**Remaining Search Space:**\n```\n"
                    narrative += "Index:  " + " ".join(f"{elem['index']:3d}" for elem in remaining) + "\n"
                    narrative += "Height: " + " ".join(f"{elem['value']:3d}" for elem in remaining) + "\n"
                    narrative += "```\n\n"

            elif step_type == "SEARCH_COMPLETE":
                max_area = data['max_area']
                max_left = data['max_left']
                max_right = data['max_right']
                iterations = data['iterations']

                narrative += f"**Search Complete**\n\n"
                narrative += f"**Final State:**\n"
                narrative += f"- Pointers have met (left ≥ right)\n"
                narrative += f"- All possible containers have been evaluated\n"
                narrative += f"- Total iterations: {iterations}\n\n"

                narrative += f"**Maximum Container Found:**\n"
                narrative += f"- Indices: [{max_left}, {max_right}]\n"
                narrative += f"- Heights: [{self.heights[max_left]}, {self.heights[max_right]}]\n"
                narrative += f"- Maximum area: **{max_area}** square units\n\n"

                narrative += "**Final Visualization:**\n```\n"
                narrative += "Index:  " + " ".join(f"{elem['index']:3d}" for elem in viz['array']) + "\n"
                narrative += "Height: " + " ".join(f"{elem['value']:3d}" for elem in viz['array']) + "\n"
                
                marker_line = "        "
                for elem in viz['array']:
                    if elem['state'] == 'max_container':
                        marker_line += "  *"
                    else:
                        marker_line += "   "
                narrative += marker_line + "\n"
                narrative += "```\n"
                narrative += "*Elements marked with * form the maximum area container*\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Final Result:**\n"
        narrative += f"- Maximum area: **{result['max_area']}** square units\n"
        narrative += f"- Optimal container: indices [{result['left_index']}, {result['right_index']}]\n"
        narrative += f"- Container dimensions:\n"
        narrative += f"  - Width: {result['right_index'] - result['left_index']}\n"
        narrative += f"  - Height: {min(result['left_height'], result['right_height'])}\n"
        narrative += f"  - Left wall height: {result['left_height']}\n"
        narrative += f"  - Right wall height: {result['right_height']}\n\n"

        narrative += f"**Performance:**\n"
        narrative += f"- Iterations: {result['iterations']}\n"
        narrative += f"- Time Complexity: O(n) - single pass through array\n"
        narrative += f"- Space Complexity: O(1) - only constant extra space\n\n"

        narrative += f"**Algorithm Efficiency:**\n"
        narrative += f"The two-pointer technique evaluates {result['iterations']} containers out of "
        narrative += f"{len(self.heights) * (len(self.heights) - 1) // 2} possible pairs, "
        narrative += f"achieving optimal solution in linear time by always moving the pointer at the shorter height.\n\n"

        # Add Frontend Visualization Hints section (LOCKED requirement)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Current Area** (`current_area`) - Shows area of container being evaluated at each step\n"
        narrative += "- **Max Area** (`max_area`) - Tracks the best solution found so far\n"
        narrative += "- **Container Dimensions** (`container_width`, `container_height`) - Visual representation of current container\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the active container** - Use distinct visual for the two `examining` elements forming current container\n"
        narrative += "2. **Show area calculation visually** - Consider shading/filling the rectangular area between pointers\n"
        narrative += "3. **Emphasize the limiting height** - The shorter of the two walls determines container height\n"
        narrative += "4. **Animate pointer movements** - Show left/right pointer moving inward based on which wall is shorter\n"
        narrative += "5. **Celebrate max updates** - When `max_area` increases, use visual feedback (pulse, color change)\n"
        narrative += "6. **Final state highlight** - Mark the `max_container` elements distinctly in final visualization\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.pointers.left\n"
        narrative += "step.data.visualization.pointers.right\n"
        narrative += "step.data.visualization.current_area\n"
        narrative += "step.data.visualization.max_area\n"
        narrative += "step.data.visualization.container_width\n"
        narrative += "step.data.visualization.container_height\n"
        narrative += "step.data.visualization.array[*].state  // 'examining' | 'active' | 'excluded' | 'max_container'\n"
        narrative += "step.data.visualization.array[*].value  // height at each index\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "step.data.left_height  // height at left pointer\n"
        narrative += "step.data.right_height  // height at right pointer\n"
        narrative += "step.data.area  // calculated area for current container\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "The Container With Most Water problem is fundamentally about **visualizing area maximization**. "
        narrative += "The most pedagogically important aspect is showing WHY we move the pointer at the shorter height: "
        narrative += "moving the taller side can only decrease area (width decreases, height stays limited by shorter side), "
        narrative += "but moving the shorter side might find a taller wall and increase area despite width decrease. "
        narrative += "Consider using a **filled rectangle** or **shaded area** between the two pointers to make the container concept concrete. "
        narrative += "The height should be visually limited by the shorter wall (perhaps with a horizontal line at min height). "
        narrative += "When max_area updates, emphasize this moment - it's a key learning point that the greedy choice (move shorter pointer) "
        narrative += "leads to optimal solution. The final state should clearly show the winning container with both its dimensions and "
        narrative += "why this particular pair of heights produces maximum area.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Container With Most Water algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'heights': List of integers representing wall heights

        Returns:
            Standardized trace result with:
                - result: {
                    'max_area': int,
                    'left_index': int,
                    'right_index': int,
                    'left_height': int,
                    'right_height': int,
                    'iterations': int
                  }
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='array'

        Raises:
            ValueError: If input is invalid
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if 'heights' not in input_data:
            raise ValueError("Input must contain 'heights' key")

        self.heights = input_data['heights']

        if not self.heights:
            raise ValueError("Heights array cannot be empty")
        if len(self.heights) < 2:
            raise ValueError("Heights array must contain at least 2 elements")
        if not all(isinstance(h, int) and h > 0 for h in self.heights):
            raise ValueError("All heights must be positive integers")

        # Initialize search
        self.left = 0
        self.right = len(self.heights) - 1
        self.max_area = 0
        self.max_left = None
        self.max_right = None
        self.current_area = 0
        self.search_complete = False
        iterations = 0

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'container-with-most-water',
            'display_name': 'Container With Most Water',
            'visualization_type': 'array',
            'visualization_config': {
                'element_renderer': 'bar',
                'show_indices': True,
                'highlight_area': True,
                'show_pointers': True,
                'pointer_colors': {
                    'left': 'blue',
                    'right': 'red'
                }
            },
            'input_size': len(self.heights)
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'heights': self.heights,
                'array_size': len(self.heights),
                'left': self.left,
                'right': self.right,
                'left_height': self.heights[self.left],
                'right_height': self.heights[self.right],
                'max_area': self.max_area
            },
            f"🔍 Initialize two pointers at array boundaries: left={self.left}, right={self.right}"
        )

        # Two-pointer algorithm
        while self.left < self.right:
            iterations += 1

            # Calculate current area
            width = self.right - self.left
            height = min(self.heights[self.left], self.heights[self.right])
            self.current_area = width * height

            self._add_step(
                "CALCULATE_AREA",
                {
                    'left': self.left,
                    'right': self.right,
                    'left_height': self.heights[self.left],
                    'right_height': self.heights[self.right],
                    'width': width,
                    'height': height,
                    'area': self.current_area
                },
                f"📏 Calculate area: width={width} × height={height} = {self.current_area}"
            )

            # Update maximum if current area is larger
            if self.current_area > self.max_area:
                old_max = self.max_area
                self.max_area = self.current_area
                self.max_left = self.left
                self.max_right = self.right

                self._add_step(
                    "UPDATE_MAX",
                    {
                        'old_max_area': old_max,
                        'new_max_area': self.max_area,
                        'left': self.left,
                        'right': self.right
                    },
                    f"⬆️ New maximum area found: {self.max_area} (previous: {old_max})"
                )

            # Move pointer at shorter height
            if self.heights[self.left] < self.heights[self.right]:
                old_left = self.left
                self.left += 1

                self._add_step(
                    "MOVE_LEFT",
                    {
                        'left_height': self.heights[old_left],
                        'right_height': self.heights[self.right],
                        'old_left': old_left,
                        'new_left': self.left,
                        'reason': 'left_shorter'
                    },
                    f"➡️ Move left pointer: {old_left} → {self.left} (left height {self.heights[old_left]} < right height {self.heights[self.right]})"
                )
            else:
                old_right = self.right
                self.right -= 1

                self._add_step(
                    "MOVE_RIGHT",
                    {
                        'left_height': self.heights[self.left],
                        'right_height': self.heights[old_right],
                        'old_right': old_right,
                        'new_right': self.right,
                        'reason': 'right_shorter_or_equal'
                    },
                    f"⬅️ Move right pointer: {old_right} → {self.right} (right height {self.heights[old_right]} ≤ left height {self.heights[self.left]})"
                )

        # Search complete
        self.search_complete = True

        self._add_step(
            "SEARCH_COMPLETE",
            {
                'max_area': self.max_area,
                'max_left': self.max_left,
                'max_right': self.max_right,
                'iterations': iterations
            },
            f"✅ Search complete: Maximum area = {self.max_area} at indices [{self.max_left}, {self.max_right}]"
        )

        return self._build_trace_result({
            'max_area': self.max_area,
            'left_index': self.max_left,
            'right_index': self.max_right,
            'left_height': self.heights[self.max_left],
            'right_height': self.heights[self.max_right],
            'iterations': iterations
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After calculating area, which pointer should we move - left or right?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after calculating area, before moving pointer
            if step.type == "CALCULATE_AREA" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]
                
                # Skip if next step is UPDATE_MAX (we want the move step)
                move_step_index = i + 1
                if next_step.type == "UPDATE_MAX" and i + 2 < len(self.trace):
                    move_step_index = i + 2
                    next_step = self.trace[move_step_index]

                if next_step.type in ["MOVE_LEFT", "MOVE_RIGHT"]:
                    left_height = step.data['left_height']
                    right_height = step.data['right_height']
                    left_idx = step.data['left']
                    right_idx = step.data['right']

                    # Determine correct answer from next step type
                    if next_step.type == "MOVE_LEFT":
                        correct_answer = "move-left"
                    else:
                        correct_answer = "move-right"

                    predictions.append({
                        'step_index': i,
                        'question': f"Container at [{left_idx}, {right_idx}] with heights [{left_height}, {right_height}]. Which pointer should move?",
                        'choices': [
                            {'id': 'move-left', 'label': f'Move Left (height {left_height})'},
                            {'id': 'move-right', 'label': f'Move Right (height {right_height})'},
                            {'id': 'done', 'label': 'Search Complete'}
                        ],
                        'hint': f"Move the pointer at the shorter height. Compare {left_height} vs {right_height}",
                        'correct_answer': correct_answer,
                        'explanation': self._get_prediction_explanation(left_height, right_height, correct_answer)
                    })

        return predictions

    def _get_prediction_explanation(self, left_height: int, right_height: int, answer: str) -> str:
        """Generate explanation for prediction answer."""
        if answer == "move-left":
            return (f"Move left pointer because left height ({left_height}) < right height ({right_height}). "
                   f"The shorter wall limits container height, so we move that pointer hoping to find a taller wall.")
        elif answer == "move-right":
            return (f"Move right pointer because right height ({right_height}) ≤ left height ({left_height}). "
                   f"The shorter wall limits container height, so we move that pointer hoping to find a taller wall.")
        return ""
