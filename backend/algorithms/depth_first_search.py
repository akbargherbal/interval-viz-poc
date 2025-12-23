"""
Depth-First Search (DFS) Algorithm Tracer

Implements graph traversal that explores as far as possible along each branch
before backtracking, using an explicit stack data structure.

Author: Backend Development Team
Date: December 23, 2025
Checklist Version: v2.3
"""

from typing import Any, Dict, List, Set
from .base_tracer import AlgorithmTracer


class DepthFirstSearchTracer(AlgorithmTracer):
    """
    Depth-First Search (DFS) Tracer
    
    Explores graph by going as deep as possible along each branch before backtracking.
    Uses explicit stack to track traversal path.
    
    Compliance: BACKEND_CHECKLIST.md v2.3
    """
    
    def __init__(self):
        super().__init__()
        self.graph = {}  # Adjacency list representation
        self.nodes = []
        self.start_node = None
        self.visited = set()
        self.stack = []
        self.visit_order = []  # Track order of visits


    def execute(self, input_data: Dict) -> dict:
        """
        Execute DFS algorithm with full trace generation.

        Args:
            input_data: {
                'nodes': List[str] - Node identifiers
                'edges': List[Tuple[str, str]] - Edge pairs (undirected)
                'start_node': str - Starting node for traversal
            }

        Returns:
            Standardized trace result with graph visualization data
        """
        # Validate input
        self.nodes = input_data.get("nodes", [])
        edges = input_data.get("edges", [])
        self.start_node = input_data.get("start_node")

        if not self.nodes:
            raise ValueError("Nodes list cannot be empty")
        if not self.start_node:
            raise ValueError("Start node must be specified")
        if self.start_node not in self.nodes:
            raise ValueError(f"Start node '{self.start_node}' not in nodes list")

        # Build adjacency list (undirected graph)
        self.graph = {node: [] for node in self.nodes}
        for u, v in edges:
            if u not in self.graph or v not in self.graph:
                raise ValueError(f"Edge ({u}, {v}) contains unknown node")
            self.graph[u].append(v)
            self.graph[v].append(u)  # Undirected

        # Sort adjacency lists for deterministic traversal
        for node in self.graph:
            self.graph[node].sort()

        # Set required metadata (v2.3 compliance)
        self.metadata = {
            "algorithm": "depth-first-search",
            "display_name": "Depth-First Search",
            "visualization_type": "graph",
            "input_size": len(self.nodes),
            "visualization_config": {"directed": False, "weighted": False},
        }

        # Step 0: Show initial graph structure
        self._add_step(
            "INITIAL_STATE",
            {
                "visualization": self._get_visualization_state(),
                "adjacency_list": dict(self.graph),
            },
            f"Starting DFS from node {self.start_node}",
        )

        # Initialize: Push start node onto stack
        self.stack.append(self.start_node)
        self._add_step(
            "PUSH_STACK",
            {
                "visualization": self._get_visualization_state(),
                "pushed_node": self.start_node,
            },
            f"Push start node '{self.start_node}' onto stack",
        )

        # Main DFS loop
        while self.stack:
            # Pop node from stack
            current = self.stack.pop()

            # Check if already visited
            if current in self.visited:
                self._add_step(
                    "SKIP_VISITED",
                    {
                        "visualization": self._get_visualization_state(),
                        "skipped_node": current,
                    },
                    f"Node '{current}' already visited, skip",
                )
                continue

            # Visit node
            self.visited.add(current)
            self.visit_order.append(current)

            self._add_step(
                "VISIT_NODE",
                {
                    "visualization": self._get_visualization_state(),
                    "current_node": current,
                    "visit_number": len(self.visit_order),
                },
                f"Visit node '{current}' (#{len(self.visit_order)})",
            )

            # Get unvisited neighbors
            neighbors = self.graph[current]
            unvisited_neighbors = [n for n in neighbors if n not in self.visited]

            if unvisited_neighbors:
                # Push unvisited neighbors onto stack (reverse order for proper traversal)
                for neighbor in reversed(unvisited_neighbors):
                    if neighbor not in self.stack:  # Avoid duplicates
                        self.stack.append(neighbor)

                self._add_step(
                    "PUSH_NEIGHBORS",
                    {
                        "visualization": self._get_visualization_state(),
                        "from_node": current,
                        "pushed_neighbors": unvisited_neighbors,
                    },
                    f"Push unvisited neighbors {unvisited_neighbors} from '{current}' onto stack",
                )
            else:
                # No unvisited neighbors - backtracking will happen on next iteration
                self._add_step(
                    "BACKTRACK",
                    {
                        "visualization": self._get_visualization_state(),
                        "from_node": current,
                    },
                    f"No unvisited neighbors from '{current}', backtrack",
                )

        # Final state
        self._add_step(
            "ALGORITHM_COMPLETE",
            {
                "visualization": self._get_visualization_state(),
                "final_visit_order": self.visit_order,
            },
            f"DFS complete - visited {len(self.visited)} nodes",
        )

        # Result: Visit order and statistics
        result = {
            "visit_order": self.visit_order,
            "visited_count": len(self.visited),
            "total_nodes": len(self.nodes),
            "unreachable_nodes": [n for n in self.nodes if n not in self.visited],
        }

        return self._build_trace_result(result)

    def _get_visualization_state(self) -> dict:
        """
        Generate current visualization state for graph.

        Complies with v2.3 Graph Algorithms requirements:
        - graph.nodes (with id, label, state)
        - graph.edges (with from, to)
        - stack (traversal structure)
        - visited_set (algorithm-specific state)
        """
        return {
            "graph": {
                "nodes": [
                    {"id": node, "label": node, "state": self._get_node_state(node)}
                    for node in self.nodes
                ],
                "edges": [
                    {"from": u, "to": v}
                    for u in self.graph
                    for v in self.graph[u]
                    if u < v  # Avoid duplicate edges in undirected graph
                ],
            },
            "stack": list(self.stack),  # Current stack state
            "visited_set": list(self.visited),  # Nodes visited so far
        }

    def _get_node_state(self, node: str) -> str:
        """
        Determine visualization state for a node.

        States:
        - 'visiting': Currently on top of stack (next to be processed)
        - 'visited': Already visited
        - 'unvisited': Not yet visited
        """
        if node in self.visited:
            return "visited"
        elif self.stack and self.stack[-1] == node:
            return "visiting"
        else:
            return "unvisited"

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction moments for active learning.

        Critical: Maximum 3 choices per question (v2.3 requirement)
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction: Which neighbor will be visited next?
            if step.type == "PUSH_NEIGHBORS" and "pushed_neighbors" in step.data:
                neighbors = step.data["pushed_neighbors"]

                if len(neighbors) >= 2:
                    # Create prediction question
                    # Note: Neighbors are pushed in reverse, so first in list is popped first
                    predictions.append(
                        {
                            "step_index": i,
                            "question": "Which neighbor will be visited next?",
                            "choices": [
                                {"id": neighbors[0], "label": f"Node {neighbors[0]}"},
                                {"id": neighbors[1], "label": f"Node {neighbors[1]}"},
                                {"id": "backtrack", "label": "Backtrack"},
                            ][
                                :3
                            ],  # Hard limit: 3 choices
                            "correct_answer": neighbors[
                                0
                            ],  # First in list (popped first due to LIFO)
                            "hint": "DFS uses a stack (Last-In-First-Out)",
                            "explanation": f"The neighbors are pushed in reverse order. '{neighbors[0]}' is popped first (LIFO), so it will be visited next.",
                        }
                    )

        return predictions[:5]  # Limit to ~5 prediction points

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable markdown narrative following v2.3 graph requirements.

        Requirements:
        - Graph structure shown at Step 0 using markdown lists
        - Stack contents visible at each step
        - Multi-variable state (visited set) tracked
        - Conditional logic explained with decision tree format
        - No ASCII art for topology
        - Adjacency overhead minimized after Step 0
        """
        steps = trace_result["trace"]["steps"]
        result = trace_result["result"]

        # Build narrative
        lines = []
        lines.append("# Depth-First Search (DFS) Execution Narrative\n")

        # Input summary
        lines.append("## Input Summary\n")
        lines.append(f"**Start Node:** {self.start_node}")
        lines.append(f"**Total Nodes:** {len(self.nodes)}")
        lines.append(
            f"**Total Edges:** {len([e for u in self.graph for e in self.graph[u]]) // 2}\n"
        )

        # Show graph structure at Step 0 (v2.3 requirement: markdown lists, not ASCII art)
        lines.append("**Graph Structure (Adjacency List):**\n")
        for node in sorted(self.graph.keys()):
            neighbors = self.graph[node]
            lines.append(f"- {node} → {neighbors}")
        lines.append("")

        # Step-by-step narrative
        for step in steps:
            step_num = step["step"]
            step_type = step["type"]
            description = step["description"]
            data = step["data"]

            lines.append(f"## Step {step_num}: {description}\n")

            # Show visualization state
            if "visualization" in data:
                viz = data["visualization"]

                # Show stack state (v2.3 requirement: traversal structure visible)
                if "stack" in viz:
                    stack_display = viz["stack"] if viz["stack"] else "(empty)"
                    lines.append(f"**Stack:** {stack_display}")

                # Show visited set (v2.3 requirement: algorithm-specific state)
                if "visited_set" in viz:
                    visited_display = (
                        viz["visited_set"] if viz["visited_set"] else "(none)"
                    )
                    lines.append(f"**Visited:** {visited_display}")

            # Step-specific details with complete decision data
            if step_type == "VISIT_NODE":
                current = data.get("current_node")
                visit_num = data.get("visit_number")
                lines.append(
                    f"\n**Action:** Mark '{current}' as visited (visit #{visit_num})"
                )
                lines.append(f"**Decision:** Add '{current}' to visited set")

            elif step_type == "PUSH_NEIGHBORS":
                from_node = data.get("from_node")
                pushed = data.get("pushed_neighbors", [])
                lines.append(f"\n**From Node:** '{from_node}'")
                lines.append(f"**Neighbors:** {pushed}")
                lines.append(
                    f"**Decision:** Push {len(pushed)} unvisited neighbor(s) onto stack"
                )
                lines.append(
                    f"**Order:** {pushed} (pushed in reverse for alphabetical traversal)"
                )

            elif step_type == "SKIP_VISITED":
                skipped = data.get("skipped_node")
                lines.append(f"\n**Condition:** IF '{skipped}' in visited set")
                lines.append(f"**Result:** TRUE → Skip '{skipped}'")
                lines.append(f"**Rationale:** Avoid revisiting nodes")

            elif step_type == "BACKTRACK":
                from_node = data.get("from_node")
                lines.append(
                    f"\n**Condition:** IF '{from_node}' has unvisited neighbors"
                )
                lines.append(f"**Result:** FALSE → No unvisited neighbors")
                lines.append(f"**Action:** Backtrack (pop next node from stack)")

            elif step_type == "PUSH_STACK":
                pushed = data.get("pushed_node")
                lines.append(f"\n**Action:** Initialize stack with start node")
                lines.append(f"**Stack becomes:** ['{pushed}']")

            lines.append("")  # Blank line between steps

        # Final result section
        lines.append("## Final Result\n")
        lines.append(f"**Visit Order:** {result['visit_order']}")
        lines.append(
            f"**Visited Count:** {result['visited_count']} / {result['total_nodes']} nodes"
        )

        if result["unreachable_nodes"]:
            lines.append(f"**Unreachable Nodes:** {result['unreachable_nodes']}")
            lines.append("*(These nodes are not connected to the start node)*")
        else:
            lines.append(
                "**Graph Connectivity:** All nodes reachable from start node ✓"
            )

        lines.append(f"\n**Total Steps:** {trace_result['trace']['total_steps']}")

        # Frontend Visualization Hints (v2.3 requirement)
        lines.append("\n---\n")
        lines.append("## 🎨 Frontend Visualization Hints\n")

        lines.append("### Primary Metrics to Emphasize\n")
        lines.append("- Current node being visited (top of stack)")
        lines.append("- Stack contents (showing exploration path)")
        lines.append("- Visited vs unvisited nodes count")
        lines.append("- Visit order numbering (1, 2, 3...)\n")

        lines.append("### Visualization Priorities\n")
        lines.append(
            "1. **Topology context** - Use force-directed or hierarchical layout"
        )
        lines.append("2. **Traversal order** - Number nodes as visited (1, 2, 3...)")
        lines.append(
            "3. **Active structure** - Show stack as vertical sidebar with LIFO animations"
        )
        lines.append(
            "4. **State transitions** - Node color changes (unvisited→visiting→visited)"
        )
        lines.append(
            "5. **Backtracking visualization** - Highlight when popping from stack with no unvisited neighbors\n"
        )

        lines.append("### Key JSON Paths\n")
        lines.append("- Node states: `step.data.visualization.graph.nodes[*].state`")
        lines.append("- Stack contents: `step.data.visualization.stack`")
        lines.append("- Current node: Infer from stack top or `step.data.current_node`")
        lines.append("- Visited set: `step.data.visualization.visited_set`")
        lines.append("- Visit order: `step.data.visit_number` at VISIT_NODE steps\n")

        lines.append("### Algorithm-Specific Guidance\n")
        lines.append(
            'DFS is about exploring "as deep as possible" before backtracking. '
        )
        lines.append("Emphasize the stack's role in remembering where to return. ")
        lines.append(
            "The moment of backtracking (stack pop with no unvisited neighbors) is crucial to highlight. "
        )
        lines.append(
            'Consider animating the "dive deep" vs "climb back up" phases distinctly.\n'
        )

        return "\n".join(lines)


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Basic 5-node graph
    tracer = DepthFirstSearchTracer()

    input_data = {
        "nodes": ["A", "B", "C", "D", "E"],
        "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")],
        "start_node": "A",
    }

    result = tracer.execute(input_data)

    print("=" * 60)
    print("TRACE RESULT")
    print("=" * 60)
    print(f"Visit Order: {result['result']['visit_order']}")
    print(f"Total Steps: {result['trace']['total_steps']}")
    print(
        f"Visited: {result['result']['visited_count']} / {result['result']['total_nodes']}"
    )

    print("\n" + "=" * 60)
    print("NARRATIVE")
    print("=" * 60)
    narrative = tracer.generate_narrative(result)
    print(narrative)

    print("\n" + "=" * 60)
    print("PREDICTION POINTS")
    print("=" * 60)
    predictions = tracer.get_prediction_points()
    print(f"Generated {len(predictions)} prediction points")
    for i, pred in enumerate(predictions, 1):
        print(f"\nPrediction {i}:")
        print(f"  Step: {pred['step_index']}")
        print(f"  Question: {pred['question']}")
        print(f"  Choices: {[c['label'] for c in pred['choices']]}")
        print(f"  Answer: {pred['correct_answer']}")
