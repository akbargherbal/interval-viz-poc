"""
Boyer-Moore Voting algorithm tracer for educational visualization.

Implements the Boyer-Moore majority voting algorithm with two phases:
1. Candidate Phase: Find potential majority element using voting mechanism
2. Verification Phase: Confirm candidate appears > n/2 times

VERSION: 1.0 - Initial implementation with Backend Checklist v2.2 compliance
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class BoyerMooreVotingTracer(AlgorithmTracer):
    """
    Tracer for Boyer-Moore Voting algorithm.

    Visualization shows:
    - Array elements with states (examining, supporting, opposing, verified, rejected)
    - Current candidate and count at each step
    - Phase transitions (candidate finding → verification)

    Prediction points ask: "Will count become 0?" or "Is this the majority element?"
    """

    def __init__(self):
        super().__init__()
        self.array = []
        self.candidate = None
        self.count = 0
        self.current_index = None
        self.phase = None  # 'FINDING' or 'VERIFYING'
        self.verification_count = 0

    def _get_visualization_state(self) -> dict:
        """
        Return current array state with element states, candidate, and count.

        Element states:
        - 'examining': Current element being processed
        - 'supporting': Element that matched candidate (increased count)
        - 'opposing': Element that didn't match candidate (decreased count)
        - 'verified': Element counted during verification phase
        - 'rejected': Element that doesn't match final candidate
        - 'neutral': Not yet processed
        """
        if not self.array:
            return {}

        return {
            "array": [
                {"index": i, "value": v, "state": self._get_element_state(i)}
                for i, v in enumerate(self.array)
            ],
            "candidate": self.candidate,
            "count": self.count,
            "current_index": self.current_index,
            "phase": self.phase,
            "verification_count": self.verification_count,
        }

    def _get_element_state(self, index: int) -> str:
        """Determine visual state of array element at given index."""
        if self.current_index is not None and index == self.current_index:
            return "examining"

        if self.phase == "VERIFYING":
            if self.current_index is not None and index < self.current_index:
                if self.array[index] == self.candidate:
                    return "verified"
                else:
                    return "rejected"
            return "neutral"

        # FINDING phase
        if self.current_index is not None and index < self.current_index:
            if self.array[index] == self.candidate:
                return "supporting"
            else:
                return "opposing"

        return "neutral"

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Boyer-Moore Voting trace.

        Shows complete execution flow with all decision data visible.
        Includes Frontend Visualization Hints (Backend Checklist v2.2).

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result["metadata"]
        steps = trace_result["trace"]["steps"]
        result = trace_result["result"]

        # Header
        narrative = "# Boyer-Moore Voting Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Array:** {self.array}\n"
        narrative += f"**Array Size:** {metadata['input_size']} elements\n"

        if result["has_majority"]:
            narrative += f"**Result:** ✅ Majority element **{result['majority_element']}** found\n"
            narrative += f"**Occurrences:** {result['occurrences']} times (> {len(self.array) // 2} required)\n"
        else:
            narrative += f"**Result:** ❌ No majority element exists\n"

        narrative += "\n---\n\n"

        # Step-by-step narrative
        for step in steps:
            step_num = step["step"]
            step_type = step["type"]
            description = step["description"]
            data = step["data"]
            viz = data["visualization"]

            narrative += f"## Step {step_num}: {description}\n\n"

            # Type-specific details
            if step_type == "INITIAL_STATE":
                narrative += f"**Algorithm Overview:**\n"
                narrative += f"- **Phase 1 (Finding):** Identify potential majority candidate using voting\n"
                narrative += f"- **Phase 2 (Verification):** Confirm candidate appears > n/2 times\n\n"

                narrative += f"**Initial Configuration:**\n"
                narrative += f"- Array size: {data['array_size']} elements\n"
                narrative += f"- Majority threshold: > {data['majority_threshold']} occurrences\n"
                narrative += f"- Starting candidate: `None`\n"
                narrative += f"- Starting count: `0`\n\n"

                narrative += "**Array Visualization:**\n```\n"
                narrative += (
                    "Index: "
                    + " ".join(f"{i:3d}" for i in range(len(self.array)))
                    + "\n"
                )
                narrative += "Value: " + " ".join(f"{v:3d}" for v in self.array) + "\n"
                narrative += "```\n\n"

            elif step_type == "CHECK_CANDIDATE":
                index = data["index"]
                value = data["value"]
                old_count = data["old_count"]

                narrative += f"**Current State:**\n"
                narrative += f"- Examining: array[{index}] = **{value}**\n"
                narrative += f"- Current candidate: `{viz['candidate']}`\n"
                narrative += f"- Current count: `{old_count}`\n\n"

                if old_count == 0:
                    narrative += f"**Decision Logic:**\n"
                    narrative += f"- Count is 0 → No active candidate\n"
                    narrative += f"- Action: Set new candidate to **{value}**\n\n"
                else:
                    narrative += f"**Comparison:**\n"
                    narrative += (
                        f"- Compare: {value} vs candidate ({viz['candidate']})\n"
                    )
                    if value == viz["candidate"]:
                        narrative += f"- Match: {value} == {viz['candidate']} ✓\n"
                        narrative += (
                            f"- Action: This element **supports** the candidate\n\n"
                        )
                    else:
                        narrative += f"- Mismatch: {value} ≠ {viz['candidate']} ✗\n"
                        narrative += (
                            f"- Action: This element **opposes** the candidate\n\n"
                        )

            elif step_type == "UPDATE_COUNT":
                index = data["index"]
                value = data["value"]
                old_count = data["old_count"]
                new_count = data["new_count"]
                action = data["action"]

                narrative += f"**Count Update:**\n"

                if action == "increment":
                    narrative += (
                        f"- Element {value} matches candidate {viz['candidate']}\n"
                    )
                    narrative += (
                        f"- Increment count: {old_count} + 1 = **{new_count}**\n"
                    )
                    narrative += f"- Interpretation: Candidate gains support\n\n"
                elif action == "decrement":
                    narrative += (
                        f"- Element {value} differs from candidate {viz['candidate']}\n"
                    )
                    narrative += (
                        f"- Decrement count: {old_count} - 1 = **{new_count}**\n"
                    )
                    narrative += f"- Interpretation: Opposing vote cancels one supporting vote\n\n"

                narrative += f"**Updated State:**\n"
                narrative += f"- Candidate: `{viz['candidate']}`\n"
                narrative += f"- Count: `{new_count}`\n\n"

                # Show progress through array
                processed = index + 1
                remaining = len(self.array) - processed
                narrative += f"**Progress:** {processed}/{len(self.array)} elements processed ({remaining} remaining)\n\n"

            elif step_type == "CHANGE_CANDIDATE":
                index = data["index"]
                value = data["value"]
                old_candidate = data["old_candidate"]
                new_candidate = data["new_candidate"]

                narrative += f"**Candidate Change Triggered:**\n"
                narrative += (
                    f"- Previous candidate: `{old_candidate}` (count reached 0)\n"
                )
                narrative += f"- New candidate: **{new_candidate}** (current element)\n"
                narrative += f"- Reset count: 0 → **1**\n\n"

                narrative += f"**Why Change?**\n"
                narrative += f'When count reaches 0, the current candidate has been "voted out" by opposing elements. '
                narrative += f"We select the current element as the new candidate and restart counting.\n\n"

            elif step_type == "PHASE_TRANSITION":
                candidate = data["candidate"]
                final_count = data["final_count"]

                narrative += f"**Phase 1 Complete: Candidate Found**\n\n"
                narrative += f"**Candidate Phase Results:**\n"
                narrative += f"- Potential majority element: **{candidate}**\n"
                narrative += f"- Final count: {final_count}\n\n"

                narrative += f"**Why Verification Needed?**\n"
                narrative += f"The voting mechanism guarantees: *if* a majority element exists, it will be the candidate. "
                narrative += f"However, the candidate might NOT be a majority element (e.g., no element appears > n/2 times). "
                narrative += f"We must verify by counting actual occurrences.\n\n"

                narrative += f"**Phase 2: Verification**\n"
                narrative += f"- Count occurrences of candidate {candidate}\n"
                narrative += (
                    f"- Required threshold: > {len(self.array) // 2} occurrences\n\n"
                )

            elif step_type == "VERIFY_CANDIDATE":
                index = data["index"]
                value = data["value"]
                matches = data["matches"]
                verification_count = data["verification_count"]

                narrative += f"**Verification Check:**\n"
                narrative += f"- Examining: array[{index}] = {value}\n"
                narrative += f"- Candidate: {viz['candidate']}\n"
                narrative += f"- Comparison: {value} {'==' if matches else '≠'} {viz['candidate']}\n\n"

                if matches:
                    narrative += f"**Match Found:**\n"
                    narrative += f"- Increment verification count: {verification_count - 1} + 1 = **{verification_count}**\n\n"
                else:
                    narrative += f"**No Match:**\n"
                    narrative += (
                        f"- Verification count unchanged: **{verification_count}**\n\n"
                    )

                # Show progress
                processed = index + 1
                remaining = len(self.array) - processed
                narrative += f"**Progress:** {processed}/{len(self.array)} elements verified ({remaining} remaining)\n\n"

            elif step_type == "MAJORITY_FOUND":
                candidate = data["candidate"]
                occurrences = data["occurrences"]
                threshold = data["threshold"]

                narrative += f"✅ **Majority Element Confirmed!**\n\n"
                narrative += f"**Verification Results:**\n"
                narrative += f"- Candidate: **{candidate}**\n"
                narrative += f"- Actual occurrences: **{occurrences}**\n"
                narrative += f"- Required threshold: > {threshold}\n"
                narrative += f"- Comparison: {occurrences} > {threshold} ✓\n\n"

                narrative += f"**Conclusion:**\n"
                narrative += f"Element **{candidate}** appears in more than half the array positions, "
                narrative += f"making it the majority element.\n\n"

            elif step_type == "NO_MAJORITY":
                candidate = data["candidate"]
                occurrences = data["occurrences"]
                threshold = data["threshold"]

                narrative += f"❌ **No Majority Element**\n\n"
                narrative += f"**Verification Results:**\n"
                narrative += f"- Candidate: {candidate}\n"
                narrative += f"- Actual occurrences: {occurrences}\n"
                narrative += f"- Required threshold: > {threshold}\n"
                narrative += f"- Comparison: {occurrences} ≤ {threshold} ✗\n\n"

                narrative += f"**Conclusion:**\n"
                narrative += f"The candidate {candidate} does not appear in more than half the positions. "
                narrative += f"Therefore, no majority element exists in this array.\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"

        if result["has_majority"]:
            narrative += f"**Final Result:** Majority element **{result['majority_element']}** found\n\n"
            narrative += f"**Statistics:**\n"
            narrative += f"- Array size: {len(self.array)}\n"
            narrative += f"- Majority threshold: > {len(self.array) // 2}\n"
            narrative += f"- Occurrences: {result['occurrences']}\n"
            narrative += f"- Percentage: {(result['occurrences'] / len(self.array) * 100):.1f}%\n\n"
        else:
            narrative += f"**Final Result:** No majority element exists\n\n"
            narrative += f"**Why No Majority?**\n"
            narrative += f"No single element appears in more than {len(self.array) // 2} positions. "
            narrative += f"The array has a distributed element frequency.\n\n"

        narrative += f"**Algorithm Complexity:**\n"
        narrative += (
            f"- Time: O(n) - Two passes through array (finding + verification)\n"
        )
        narrative += f"- Space: O(1) - Only stores candidate and count\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"

        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += (
            "- **Candidate** (`candidate`) - The current potential majority element\n"
        )
        narrative += "- **Count** (`count`) - Voting balance (support vs opposition)\n"
        narrative += "- **Phase** (`phase`) - 'FINDING' vs 'VERIFYING' to show algorithm structure\n"
        narrative += "- **Verification Count** (`verification_count`) - Actual occurrences during Phase 2\n\n"

        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the voting mechanism** - Use distinct colors for `supporting` (green) vs `opposing` (red) states\n"
        narrative += "2. **Emphasize count reaching 0** - This is the critical moment when candidate changes\n"
        narrative += "3. **Show phase transition clearly** - Visual break between finding and verification phases\n"
        narrative += "4. **Animate verification progress** - Show accumulating `verified` elements vs `rejected` elements\n"
        narrative += "5. **Celebrate/reject final result** - Clear visual feedback when majority confirmed or denied\n\n"

        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.candidate\n"
        narrative += "step.data.visualization.count\n"
        narrative += "step.data.visualization.phase  // 'FINDING' | 'VERIFYING'\n"
        narrative += "step.data.visualization.current_index\n"
        narrative += "step.data.visualization.verification_count\n"
        narrative += "step.data.visualization.array[*].state  // 'examining' | 'supporting' | 'opposing' | 'verified' | 'rejected' | 'neutral'\n"
        narrative += "step.data.visualization.array[*].value\n"
        narrative += "step.data.visualization.array[*].index\n"
        narrative += "```\n\n"

        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Boyer-Moore Voting's elegance comes from its **voting metaphor**: each element either supports or opposes the current candidate. "
        narrative += "The most pedagogically important visualization is showing this **balance of power** through the count variable. "
        narrative += 'When count reaches 0, it\'s like a political upset—the candidate is "voted out" and replaced. '
        narrative += "Consider using a **balance scale visual** or **tug-of-war metaphor** where supporting elements pull one way and opposing elements pull the other. "
        narrative += "The phase transition is crucial: Phase 1 finds a *candidate* (not guaranteed majority), Phase 2 *verifies* it. "
        narrative += "Show this distinction clearly—perhaps with different background colors or a visual separator. "
        narrative += "During verification, the accumulating count should feel different from the voting count—it's a simple tally, not a balance. "
        narrative += "The final moment (majority confirmed or denied) should be dramatic, as it reveals whether the clever voting mechanism found a true majority or just a strong candidate.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Boyer-Moore Voting algorithm with trace generation.

        Args:
            input_data: dict with key:
                - 'array': List of integers

        Returns:
            Standardized trace result with:
                - result: {
                    'has_majority': bool,
                    'majority_element': int or None,
                    'occurrences': int
                  }
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='array'

        Raises:
            ValueError: If input is invalid
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if "array" not in input_data:
            raise ValueError("Input must contain 'array' key")

        self.array = input_data["array"]

        if not self.array:
            raise ValueError("Array cannot be empty")

        # Initialize algorithm state
        self.candidate = None
        self.count = 0
        self.current_index = None
        self.phase = "FINDING"
        self.verification_count = 0

        # Set metadata for frontend
        self.metadata = {
            "algorithm": "boyer-moore-voting",
            "display_name": "Boyer-Moore Voting",
            "visualization_type": "array",
            "visualization_config": {
                "element_renderer": "number",
                "show_indices": True,
                "show_candidate": True,
            },
            "input_size": len(self.array),
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {"array_size": len(self.array), "majority_threshold": len(self.array) // 2},
            f"🗳️ Initialize Boyer-Moore Voting for array of {len(self.array)} elements",
        )

        # Phase 1: Find candidate using voting mechanism
        for i, value in enumerate(self.array):
            self.current_index = i
            old_count = self.count

            # Check if we need to set/change candidate
            if self.count == 0:
                # Set new candidate
                old_candidate = self.candidate
                self.candidate = value
                self.count = 1

                if old_candidate is None:
                    # First candidate
                    self._add_step(
                        "CHECK_CANDIDATE",
                        {"index": i, "value": value, "old_count": old_count},
                        f"📍 Examine array[{i}] = {value} (count is 0, set as first candidate)",
                    )

                    self._add_step(
                        "CHANGE_CANDIDATE",
                        {
                            "index": i,
                            "value": value,
                            "old_candidate": old_candidate,
                            "new_candidate": self.candidate,
                        },
                        f"🔄 Set candidate to {value}, count = 1",
                    )
                else:
                    # Candidate change
                    self._add_step(
                        "CHECK_CANDIDATE",
                        {"index": i, "value": value, "old_count": old_count},
                        f"📍 Examine array[{i}] = {value} (count reached 0, candidate change needed)",
                    )

                    self._add_step(
                        "CHANGE_CANDIDATE",
                        {
                            "index": i,
                            "value": value,
                            "old_candidate": old_candidate,
                            "new_candidate": self.candidate,
                        },
                        f"🔄 Change candidate from {old_candidate} to {value}, reset count to 1",
                    )
            else:
                # Check if current element matches candidate
                self._add_step(
                    "CHECK_CANDIDATE",
                    {"index": i, "value": value, "old_count": old_count},
                    f"📍 Examine array[{i}] = {value} (candidate: {self.candidate}, count: {old_count})",
                )

                if value == self.candidate:
                    # Increment count (supporting vote)
                    self.count += 1
                    self._add_step(
                        "UPDATE_COUNT",
                        {
                            "index": i,
                            "value": value,
                            "old_count": old_count,
                            "new_count": self.count,
                            "action": "increment",
                        },
                        f"✅ {value} matches candidate {self.candidate}, increment count: {old_count} → {self.count}",
                    )
                else:
                    # Decrement count (opposing vote)
                    self.count -= 1
                    self._add_step(
                        "UPDATE_COUNT",
                        {
                            "index": i,
                            "value": value,
                            "old_count": old_count,
                            "new_count": self.count,
                            "action": "decrement",
                        },
                        f"❌ {value} differs from candidate {self.candidate}, decrement count: {old_count} → {self.count}",
                    )

        # Phase transition
        self.phase = "VERIFYING"
        self.current_index = None

        self._add_step(
            "PHASE_TRANSITION",
            {"candidate": self.candidate, "final_count": self.count},
            f"🔍 Phase 1 complete. Candidate: {self.candidate}. Begin verification phase.",
        )

        # Phase 2: Verify candidate is actually majority
        self.verification_count = 0

        for i, value in enumerate(self.array):
            self.current_index = i
            matches = value == self.candidate

            if matches:
                self.verification_count += 1

            self._add_step(
                "VERIFY_CANDIDATE",
                {
                    "index": i,
                    "value": value,
                    "matches": matches,
                    "verification_count": self.verification_count,
                },
                f"🔎 Verify array[{i}] = {value} {'==' if matches else '≠'} {self.candidate} (count: {self.verification_count})",
            )

        # Check if candidate is majority
        majority_threshold = len(self.array) // 2
        has_majority = self.verification_count > majority_threshold

        self.current_index = None

        if has_majority:
            self._add_step(
                "MAJORITY_FOUND",
                {
                    "candidate": self.candidate,
                    "occurrences": self.verification_count,
                    "threshold": majority_threshold,
                },
                f"✅ Majority found: {self.candidate} appears {self.verification_count} times (> {majority_threshold})",
            )

            return self._build_trace_result(
                {
                    "has_majority": True,
                    "majority_element": self.candidate,
                    "occurrences": self.verification_count,
                }
            )
        else:
            self._add_step(
                "NO_MAJORITY",
                {
                    "candidate": self.candidate,
                    "occurrences": self.verification_count,
                    "threshold": majority_threshold,
                },
                f"❌ No majority: {self.candidate} appears {self.verification_count} times (≤ {majority_threshold})",
            )

            return self._build_trace_result(
                {
                    "has_majority": False,
                    "majority_element": None,
                    "occurrences": self.verification_count,
                }
            )

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict:
        1. During finding phase: "Will count become 0 after this element?"
        2. At phase transition: "Is the candidate the majority element?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction 1: Before UPDATE_COUNT, predict if count will reach 0
            if step.type == "CHECK_CANDIDATE" and i + 1 < len(self.trace):
                next_step = self.trace[i + 1]

                # Only predict during finding phase (not verification)
                if next_step.type in ["UPDATE_COUNT", "CHANGE_CANDIDATE"]:
                    old_count = step.data["old_count"]
                    value = step.data["value"]
                    candidate = self.trace[i].data["visualization"]["candidate"]

                    # Only ask if count is 1 (interesting case)
                    if old_count == 1 and candidate is not None:
                        if next_step.type == "CHANGE_CANDIDATE":
                            correct_answer = "yes"
                        else:
                            correct_answer = "no"

                        predictions.append(
                            {
                                "step_index": i,
                                "question": f"Current count is 1. Element {value} vs candidate {candidate}. Will count reach 0?",
                                "choices": [
                                    {
                                        "id": "yes",
                                        "label": f"Yes (count → 0, candidate changes)",
                                    },
                                    {"id": "no", "label": f"No (count stays positive)"},
                                ],
                                "hint": f"Compare {value} with candidate {candidate}. If different, count decrements to 0.",
                                "correct_answer": correct_answer,
                                "explanation": self._get_count_zero_explanation(
                                    value, candidate, correct_answer
                                ),
                            }
                        )

            # Prediction 2: At phase transition, predict if candidate is majority
            if step.type == "PHASE_TRANSITION" and i + 1 < len(self.trace):
                candidate = step.data["candidate"]

                # Find the final result
                final_step = self.trace[-1]
                if final_step.type == "MAJORITY_FOUND":
                    correct_answer = "yes"
                else:
                    correct_answer = "no"

                predictions.append(
                    {
                        "step_index": i,
                        "question": f"Candidate {candidate} found. Is it the majority element (appears > {len(self.array) // 2} times)?",
                        "choices": [
                            {"id": "yes", "label": f"Yes (majority confirmed)"},
                            {"id": "no", "label": f"No (not a majority)"},
                        ],
                        "hint": f"The voting mechanism guarantees IF a majority exists, it's the candidate. But does a majority exist?",
                        "correct_answer": correct_answer,
                        "explanation": self._get_majority_explanation(
                            candidate, correct_answer
                        ),
                    }
                )

        return predictions

    def _get_count_zero_explanation(
        self, value: int, candidate: int, answer: str
    ) -> str:
        """Generate explanation for count-reaching-zero prediction."""
        if answer == "yes":
            return f'{value} ≠ {candidate}, so count decrements: 1 - 1 = 0. Candidate is "voted out" and will change.'
        else:
            return f"{value} == {candidate}, so count increments: 1 + 1 = 2. Candidate gains support and remains."

    def _get_majority_explanation(self, candidate: int, answer: str) -> str:
        """Generate explanation for majority verification prediction."""
        if answer == "yes":
            return f"After verification, {candidate} appears {self.verification_count} times, which is > {len(self.array) // 2}. It's the majority element."
        else:
            return f"After verification, {candidate} appears {self.verification_count} times, which is ≤ {len(self.array) // 2}. No majority element exists."
