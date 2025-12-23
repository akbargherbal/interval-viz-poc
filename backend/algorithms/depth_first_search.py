"""
Depth-First Search (DFS) Algorithm Tracer

Implements graph traversal that explores as far as possible along each branch
before backtracking, using an explicit stack data structure.

Refined for v2.4 Compliance and PE Feedback:
- Unified EXPLORE_NODE steps (Atomicity)
- Explicit neighbor filtering logic
- Consistent stack/visited display
- Disconnected component awareness
- Chronological sub-steps in narrative
- Intermediate stack states visible

Author: Backend Development Team
Date: December 23, 2025
Checklist Version: v2.4
"""

from typing import Any, Dict, List, Set
from .base_tracer import AlgorithmTracer


class DepthFirstSearchTracer(AlgorithmTracer):
    """
    Depth-First Search (DFS) Tracer

    Explores graph by going as deep as possible along each branch before backtracking.
    Uses explicit stack to track traversal path.
    """

    def __init__(self):
        super().__init__()
        self.graph = {}  # Adjacency list representation
        self.nodes = []
        self.start_node = None
        self.visited = set()
        self.visited_list = []  # To maintain order for visualization
        self.stack = []
        self.visit_order = []  # Track order of visits

    def execute(self, input_data: Dict) -> dict:
        """
        Execute DFS algorithm with full trace generation.
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

        # Set required metadata (v2.4 compliance)
        self.metadata = {
            "algorithm": "depth-first-search",
            "display_name": "Depth-First Search",
            "visualization_type": "graph",
            "input_size": len(self.nodes),
            "visualization_config": {
                "directed": False,
                "weighted": False,
                "layout_hints": "hierarchical",
            },
        }

        # Step 0: Show initial graph structure
        self._add_step(
            "INITIAL_STATE",
            {
                "visualization": self._get_visualization_state(),
                "adjacency_list": dict(self.graph),
            },
            f"Initialize DFS with start node '{self.start_node}'",
        )

        # Initialize: Push start node onto stack
        self.stack.append(self.start_node)
        
        self._add_step(
            "INITIALIZATION",
            {
                "visualization": self._get_visualization_state(),
                "action": "push_start",
                "node": self.start_node,
            },
            f"Push start node '{self.start_node}' onto stack",
        )

        # Main DFS loop
        while self.stack:
            # Pop node from stack
            current = self.stack.pop()
            
            # Capture intermediate stack state (after pop, before push)
            stack_after_pop = list(self.stack)

            # Check if already visited
            if current in self.visited:
                self._add_step(
                    "SKIP_VISITED",
                    {
                        "visualization": self._get_visualization_state(),
                        "node": current,
                        "reason": "already_visited",
                        "stack_after_pop": stack_after_pop
                    },
                    f"Pop '{current}' - Already visited, skipping",
                )
                continue

            # Visit node
            self.visited.add(current)
            self.visited_list.append(current)
            self.visit_order.append(current)

            # Process Neighbors
            all_neighbors = self.graph[current]
            filtering_log = []
            unvisited_to_push = []
            
            # Analyze neighbors (Explicit Logic)
            for neighbor in all_neighbors:
                is_visited = neighbor in self.visited
                status = "visited" if is_visited else "unvisited"
                
                if is_visited:
                    action = "skip"
                elif neighbor in self.stack:
                    action = "push (duplicate)"
                    unvisited_to_push.append(neighbor)
                else:
                    action = "push"
                    unvisited_to_push.append(neighbor)
                
                filtering_log.append({
                    "neighbor": neighbor,
                    "status": status,
                    "action": action
                })

            # Push unvisited neighbors onto stack (reverse order for alphabetical traversal)
            pushed_neighbors = []
            for neighbor in reversed(unvisited_to_push):
                self.stack.append(neighbor)
                pushed_neighbors.append(neighbor)

            # Unified Step (Atomicity)
            step_desc = f"Visit '{current}'"
            if pushed_neighbors:
                step_desc += f", push neighbors {pushed_neighbors}"
            else:
                step_desc += " (Backtrack point)"

            self._add_step(
                "EXPLORE_NODE",
                {
                    "visualization": self._get_visualization_state(),
                    "current_node": current,
                    "stack_after_pop": stack_after_pop, # Intermediate state
                    "visit_number": len(self.visit_order),
                    "filtering_log": filtering_log,
                    "pushed_neighbors": pushed_neighbors,
                    "all_neighbors": all_neighbors
                },
                step_desc,
            )

        # Final state
        unreachable = [n for n in self.nodes if n not in self.visited]
        
        self._add_step(
            "ALGORITHM_COMPLETE",
            {
                "visualization": self._get_visualization_state(),
                "stats": {
                    "total": len(self.nodes),
                    "visited": len(self.visited),
                    "unreachable": unreachable
                },
            },
            f"DFS complete - visited {len(self.visited)} nodes",
        )

        # Result: Visit order and statistics
        result = {
            "visit_order": self.visit_order,
            "visited_count": len(self.visited),
            "total_nodes": len(self.nodes),
            "unreachable_nodes": unreachable,
        }

        return self._build_trace_result(result)

    def _get_visualization_state(self) -> dict:
        """
        Generate current visualization state for graph.
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
            "visited_set": list(self.visited_list),  # Ordered list for display
        }

    def _get_node_state(self, node: str) -> str:
        """
        Determine visualization state for a node.
        """
        if node in self.visited:
            return "visited"
        elif node in self.stack:
            return "visiting" # Pending in stack
        else:
            return "unvisited"

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction moments for active learning.
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction: Which neighbor will be visited next?
            if step.type == "EXPLORE_NODE" and step.data.get("pushed_neighbors"):
                pushed = step.data["pushed_neighbors"]
                # Pushed in reverse, so last pushed is top of stack (visited next)
                next_node = pushed[-1]
                
                if len(pushed) >= 2:
                    predictions.append({
                        "step_index": i,
                        "question": "Which node will be visited next?",
                        "choices": [
                            {"id": next_node, "label": f"Node {next_node}"},
                            {"id": pushed[0], "label": f"Node {pushed[0]}"},
                            {"id": "backtrack", "label": "Backtrack"},
                        ][:3],
                        "correct_answer": next_node,
                        "hint": "DFS uses a stack (Last-In-First-Out). The last node pushed is popped first.",
                        "explanation": f"We pushed {pushed}. Since it's a stack (LIFO), {next_node} is at the top and will be visited next."
                    })

        return predictions[:5]

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable markdown narrative following v2.4 graph requirements.
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

        # Show graph structure at Step 0
        lines.append("**Graph Structure (Adjacency List):**\n")
        for node in sorted(self.graph.keys()):
            neighbors = self.graph[node]
            lines.append(f"- {node} → {neighbors}")
        lines.append("")

        # Track if we've defined "Backtrack"
        backtrack_defined = False

        # Step-by-step narrative
        for step in steps:
            step_num = step["step"]
            step_type = step["type"]
            description = step["description"]
            data = step["data"]

            lines.append(f"## Step {step_num}: {description}\n")

            # Show visualization state (Consistent Display)
            if "visualization" in data:
                viz = data["visualization"]
                
                # Stack
                stack_display = viz["stack"] if viz["stack"] else "(empty)"
                lines.append(f"**Stack:** {stack_display}")
                
                # Visited (Ordered)
                visited_display = viz["visited_set"] if viz["visited_set"] else "(none)"
                lines.append(f"**Visited:** {visited_display}")
                lines.append("") # Spacer

            # Step-specific details
            if step_type == "INITIALIZATION":
                lines.append(f"**Action:** Push start node '{data['node']}' onto stack to begin traversal.")

            elif step_type == "EXPLORE_NODE":
                current = data.get("current_node")
                visit_num = data.get("visit_number")
                stack_after_pop = data.get("stack_after_pop", [])
                pushed = data.get("pushed_neighbors", [])
                filtering = data.get("filtering_log", [])
                
                # Sub-step 1: Pop
                lines.append(f"**1. Pop Operation:**")
                lines.append(f"- Pop '{current}' from stack.")
                lines.append(f"- **Intermediate Stack:** {stack_after_pop if stack_after_pop else '(empty)'}")
                lines.append(f"- Mark '{current}' as visited (Visit #{visit_num}).")
                
                # Sub-step 2: Analyze
                lines.append(f"\n**2. Neighbor Analysis:**")
                if filtering:
                    lines.append(f"Check neighbors of '{current}' (in alphabetical order):")
                    for entry in filtering:
                        n = entry['neighbor']
                        status = entry['status']
                        action = entry['action']
                        
                        # Explicit "Skip" language
                        if action == 'push':
                            action_desc = "Push to stack"
                        elif action == 'push (duplicate)':
                            action_desc = "Push to stack (duplicate)"
                        elif action == 'skip':
                            action_desc = "Already visited (do not push)"
                        else:
                            action_desc = action
                            
                        lines.append(f"- Node {n}: {status} → {action_desc}")
                else:
                    lines.append(f"'{current}' has no neighbors.")

                # Sub-step 3: Push
                lines.append(f"\n**3. Stack Update:**")
                if pushed:
                    lines.append(f"- Neighbors to push: {pushed}")
                    lines.append(f"- **Push Order:** Pushed in reverse {pushed} so that {pushed[-1]} is at top.")
                    lines.append(f"- **Result:** Next pop will visit '{pushed[-1]}'.")
                else:
                    lines.append(f"- No neighbors pushed.")
                    if not backtrack_defined:
                        lines.append(f"- **Result:** No unvisited neighbors found. **Backtracking** (returning to previous node).")
                        backtrack_defined = True
                    else:
                        lines.append(f"- **Result:** No unvisited neighbors found. Backtracking.")

            elif step_type == "SKIP_VISITED":
                node = data.get("node")
                stack_after_pop = data.get("stack_after_pop", [])
                lines.append(f"**1. Pop Operation:**")
                lines.append(f"- Pop '{node}' from stack.")
                lines.append(f"- **Intermediate Stack:** {stack_after_pop if stack_after_pop else '(empty)'}")
                lines.append(f"\n**2. Check Visited:**")
                lines.append(f"- '{node}' is already in visited set.")
                lines.append(f"- **Action:** Skip to avoid cycles/redundancy.")

            elif step_type == "ALGORITHM_COMPLETE":
                stats = data.get("stats", {})
                unreachable = stats.get("unreachable", [])
                
                lines.append(f"**Completion:** Stack is empty.")
                if unreachable:
                    lines.append(f"**Note:** Nodes {unreachable} remain unvisited.")
                    lines.append("This indicates the graph has **disconnected components**.")
                    lines.append("DFS only explores the component containing the start node.")

            lines.append("")  # Blank line between steps

        # Final result section
        lines.append("## Final Result\n")
        lines.append(f"**Visit Order:** {result['visit_order']}")
        lines.append(
            f"**Visited Count:** {result['visited_count']} / {result['total_nodes']} nodes"
        )

        if result["unreachable_nodes"]:
            lines.append(f"**Unreachable Nodes:** {result['unreachable_nodes']}")
        else:
            lines.append(
                "**Graph Connectivity:** All nodes reachable from start node ✓"
            )

        lines.append(f"\n**Total Steps:** {trace_result['trace']['total_steps']}")

        # Frontend Visualization Hints
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
        lines.append("- Current node: `step.data.current_node`")
        lines.append("- Visited set: `step.data.visualization.visited_set`")
        lines.append("- Neighbor analysis: `step.data.filtering_log` (for detailed tooltips)\n")

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