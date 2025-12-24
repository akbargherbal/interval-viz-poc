
"""
Depth-First Search (Iterative) algorithm tracer for educational visualization.

Implements iterative DFS using explicit stack with complete trace generation
for step-by-step visualization and prediction mode.

VERSION: 2.1 - Backend Checklist v2.2 Compliance
- Graph Algorithm Extensions applied
- Frontend Visualization Hints section included
"""

from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer


class DepthFirstSearchTracer(AlgorithmTracer):
    """
    Tracer for Depth-First Search (Iterative) algorithm on graphs.

    Visualization shows:
    - Graph nodes with states (unvisited, examining, visited)
    - Graph edges with states (unexplored, traversed, backtrack)
    - Explicit stack with directional indicators
    - Visited set tracking

    Prediction points ask: "Will this neighbor be visited or skipped?"
    """

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.adjacency = {}
        self.start_node = None
        self.stack = []
        self.visited = set()
        self.current_node = None
        self.traversal_order = []

    def _get_visualization_state(self) -> dict:
        """
        Return current graph state with node/edge states and traversal structures.

        Node states:
        - 'unvisited': Not yet visited
        - 'examining': Currently being processed (top of stack)
        - 'visited': Already processed

        Edge states:
        - 'unexplored': Not yet traversed
        - 'traversed': Used to reach a new node
        - 'backtrack': Returned along this edge
        """
        if not self.nodes:
            return {}

        # Build node visualization
        nodes_viz = []
        for node in self.nodes:
            if node == self.current_node:
                state = 'examining'
            elif node in self.visited:
                state = 'visited'
            else:
                state = 'unvisited'
            
            nodes_viz.append({
                'id': node,
                'state': state
            })

        # Build edge visualization
        edges_viz = []
        for from_node, to_node in self.edges:
            # Determine edge state based on traversal history
            if from_node in self.visited and to_node in self.visited:
                # Both nodes visited - edge was traversed
                state = 'traversed'
            elif from_node in self.visited and to_node not in self.visited:
                # From visited, to unvisited - unexplored
                state = 'unexplored'
            else:
                state = 'unexplored'
            
            edges_viz.append({
                'from': from_node,
                'to': to_node,
                'state': state
            })

        return {
            'nodes': nodes_viz,
            'edges': edges_viz,
            'stack': list(self.stack),  # Copy for immutability
            'visited': sorted(list(self.visited)),  # Sorted for consistent display
            'current_node': self.current_node,
            'traversal_order': list(self.traversal_order)
        }

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from DFS trace.

        Shows complete execution flow with all decision data visible.
        Applies Graph Algorithm Extensions from Backend Checklist v2.2.

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Depth-First Search (Iterative) Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Start Node:** {self.start_node}\n"
        narrative += f"**Graph Size:** {metadata['input_size']} nodes\n"
        narrative += f"**Traversal Order:** {' → '.join(result['traversal_order'])}\n"
        narrative += f"**Nodes Visited:** {result['nodes_visited']}/{len(self.nodes)}\n\n"
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
                narrative += f"**Graph Structure (Adjacency List):**\n"
                for node in sorted(self.adjacency.keys()):
                    neighbors = self.adjacency[node]
                    if neighbors:
                        narrative += f"- {node}: [{', '.join(sorted(neighbors))}]\n"
                    else:
                        narrative += f"- {node}: []\n"
                narrative += "\n"

                narrative += f"**Initial Configuration:**\n"
                narrative += f"- Start node: **{data['start_node']}**\n"
                narrative += f"- Stack: Empty (will push start node)\n"
                narrative += f"- Visited set: Empty\n"
                narrative += f"- Goal: Explore all reachable nodes depth-first\n\n"

            elif step_type == "PUSH_STACK":
                node = data['node']
                reason = data['reason']
                
                narrative += f"**Action:** Push node **{node}** onto stack\n\n"
                narrative += f"**Reason:** {reason}\n\n"
                
                narrative += f"**Stack State:**\n"
                narrative += f"```\n"
                if viz['stack']:
                    narrative += f"[{', '.join(viz['stack'])}] ← {viz['stack'][-1]} on top (processed next)\n"
                narrative += f"```\n\n"
                
                narrative += f"**Visited Set:** {{{', '.join(viz['visited']) if viz['visited'] else 'empty'}}}\n\n"

            elif step_type == "POP_STACK":
                node = data['node']
                
                narrative += f"**Action:** Pop node **{node}** from stack for processing\n\n"
                
                narrative += f"**Stack Before Pop:**\n"
                narrative += f"```\n"
                # Reconstruct stack before pop
                stack_before = viz['stack'] + [node]
                narrative += f"[{', '.join(stack_before)}] ← {node} on top\n"
                narrative += f"```\n\n"
                
                narrative += f"**Stack After Pop:**\n"
                narrative += f"```\n"
                if viz['stack']:
                    narrative += f"[{', '.join(viz['stack'])}] ← {viz['stack'][-1]} on top (processed next)\n"
                else:
                    narrative += f"Empty\n"
                narrative += f"```\n\n"

            elif step_type == "VISIT_NODE":
                node = data['node']
                neighbors = data['neighbors']
                
                narrative += f"**Processing Node:** {node}\n\n"
                
                narrative += f"**Check Visited Status:**\n"
                # Show explicit comparison
                visited_before = sorted(list(set(viz['visited']) - {node}))
                narrative += f"- Visited set before: {{{', '.join(visited_before) if visited_before else 'empty'}}}\n"
                narrative += f"- Is {node} in visited set? **No** ✓\n"
                narrative += f"- Action: Mark {node} as visited\n\n"
                
                narrative += f"**Updated Visited Set:** {{{', '.join(viz['visited'])}}}\n\n"
                
                narrative += f"**Neighbors of {node}:** [{', '.join(sorted(neighbors)) if neighbors else 'none'}]\n\n"
                
                if neighbors:
                    narrative += f"**Neighbor Processing:**\n"
                    narrative += f"We will examine each neighbor to determine if it should be added to the stack.\n\n"

            elif step_type == "SKIP_VISITED":
                node = data['node']
                neighbor = data['neighbor']
                
                narrative += f"**Examining Neighbor:** {neighbor} (from node {node})\n\n"
                
                narrative += f"**Check Visited Status:**\n"
                narrative += f"- Current visited set: {{{', '.join(viz['visited'])}}}\n"
                narrative += f"- Is {neighbor} in visited set? **Yes** ✓\n"
                narrative += f"- Decision: **Skip** {neighbor} (already explored)\n\n"
                
                narrative += f"**Reason:** DFS only visits each node once. Since {neighbor} is already in the visited set, "
                narrative += f"we don't need to explore it again.\n\n"

            elif step_type == "BACKTRACK":
                narrative += f"**Backtracking:**\n\n"
                
                current = data.get('from_node', 'unknown')
                narrative += f"- Finished exploring all neighbors of **{current}**\n"
                narrative += f"- No unvisited neighbors remain\n"
                narrative += f"- Return to previous node in stack (if any)\n\n"
                
                narrative += f"**Stack State:**\n"
                narrative += f"```\n"
                if viz['stack']:
                    narrative += f"[{', '.join(viz['stack'])}] ← {viz['stack'][-1]} on top (processed next)\n"
                else:
                    narrative += f"Empty (traversal complete)\n"
                narrative += f"```\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Traversal Complete:**\n"
        narrative += f"- Nodes visited: **{result['nodes_visited']}** out of {len(self.nodes)}\n"
        narrative += f"- Traversal order: {' → '.join(result['traversal_order'])}\n"
        
        if result['nodes_visited'] < len(self.nodes):
            unvisited = sorted(set(self.nodes) - set(result['traversal_order']))
            narrative += f"- Unreachable nodes: {', '.join(unvisited)}\n"
            narrative += f"  *(Graph is disconnected - these nodes cannot be reached from {self.start_node})*\n"
        else:
            narrative += f"- All nodes reachable from start node {self.start_node}\n"
        
        narrative += f"\n**Algorithm Characteristics:**\n"
        narrative += f"- Time Complexity: O(V + E) where V = vertices, E = edges\n"
        narrative += f"- Space Complexity: O(V) for stack and visited set\n"
        narrative += f"- Traversal Strategy: Depth-first (explore as far as possible before backtracking)\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Stack Contents** (`stack`) - Shows the exploration frontier and backtracking path\n"
        narrative += "- **Visited Set Size** (`visited.length`) - Demonstrates progress through the graph\n"
        narrative += "- **Current Node** (`current_node`) - The active exploration point\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the stack's LIFO behavior** - Use vertical stack visualization with top clearly marked\n"
        narrative += "2. **Emphasize depth-first exploration** - Animate following one path to its end before backtracking\n"
        narrative += "3. **Show visited vs. unvisited distinction** - Use distinct colors for `visited` vs `unvisited` node states\n"
        narrative += "4. **Animate backtracking moments** - When stack pops without new pushes, show return to previous node\n"
        narrative += "5. **Track traversal order** - Display the sequence of visited nodes to show exploration path\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.nodes[*].id\n"
        narrative += "step.data.visualization.nodes[*].state  // 'unvisited' | 'examining' | 'visited'\n"
        narrative += "step.data.visualization.edges[*].from\n"
        narrative += "step.data.visualization.edges[*].to\n"
        narrative += "step.data.visualization.edges[*].state  // 'unexplored' | 'traversed' | 'backtrack'\n"
        narrative += "step.data.visualization.stack  // Array with top at end: [..., top]\n"
        narrative += "step.data.visualization.visited  // Sorted array of visited node IDs\n"
        narrative += "step.data.visualization.current_node  // Currently processing node\n"
        narrative += "step.data.visualization.traversal_order  // Sequence of visited nodes\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "DFS's defining characteristic is its **depth-first exploration strategy** - it follows one path as far as possible before backtracking. "
        narrative += "The most pedagogically important visualization is the **stack's LIFO behavior**: when we push neighbors onto the stack, "
        narrative += "the last one pushed is the first one explored (creating the depth-first pattern). "
        narrative += "Consider using a **vertical stack visualization** with clear directional indicators (arrows pointing to top). "
        narrative += "When backtracking occurs (popping without pushing), animate the 'return' to show we're unwinding the exploration path. "
        narrative += "The contrast between DFS and BFS becomes clear when students see the stack (LIFO) vs. queue (FIFO) - "
        narrative += "emphasize this by showing how the stack's top element determines the next exploration direction. "
        narrative += "For disconnected graphs, clearly show when the stack empties with unvisited nodes remaining, "
        narrative += "demonstrating that DFS only explores the connected component containing the start node.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute DFS algorithm with trace generation.

        Args:
            input_data: dict with keys:
                - 'nodes': List of node identifiers (strings)
                - 'edges': List of [from, to] pairs (undirected)
                - 'start_node': Node to begin traversal

        Returns:
            Standardized trace result with:
                - result: {'traversal_order': List[str], 'nodes_visited': int}
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='graph'

        Raises:
            ValueError: If input is invalid or start_node not in graph
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        
        required_keys = ['nodes', 'edges', 'start_node']
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Input must contain '{key}' key")

        self.nodes = input_data['nodes']
        self.edges = input_data['edges']
        self.start_node = input_data['start_node']

        if not self.nodes:
            raise ValueError("Graph must contain at least one node")
        
        if self.start_node not in self.nodes:
            raise ValueError(f"Start node '{self.start_node}' not in graph nodes")

        # Build adjacency list (undirected graph)
        self.adjacency = {node: [] for node in self.nodes}
        for from_node, to_node in self.edges:
            if from_node not in self.adjacency:
                raise ValueError(f"Edge references unknown node: {from_node}")
            if to_node not in self.adjacency:
                raise ValueError(f"Edge references unknown node: {to_node}")
            
            # Undirected: add both directions
            self.adjacency[from_node].append(to_node)
            self.adjacency[to_node].append(from_node)

        # Initialize traversal state
        self.stack = []
        self.visited = set()
        self.current_node = None
        self.traversal_order = []

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'depth-first-search',
            'display_name': 'Depth-First Search (Iterative)',
            'visualization_type': 'graph',
            'visualization_config': {
                'directed': False,
                'show_stack': True,
                'show_visited': True
            },
            'input_size': len(self.nodes),
            'start_node': self.start_node
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'start_node': self.start_node,
                'graph_size': len(self.nodes),
                'edge_count': len(self.edges)
            },
            f"🔍 Initialize DFS from node {self.start_node}"
        )

        # Push start node onto stack
        self.stack.append(self.start_node)
        self._add_step(
            "PUSH_STACK",
            {
                'node': self.start_node,
                'reason': 'Starting node for traversal'
            },
            f"📥 Push start node {self.start_node} onto stack"
        )

        # DFS loop
        while self.stack:
            # Pop node from stack
            self.current_node = self.stack.pop()
            
            self._add_step(
                "POP_STACK",
                {
                    'node': self.current_node
                },
                f"📤 Pop node {self.current_node} from stack"
            )

            # Check if already visited
            if self.current_node in self.visited:
                # Skip - already processed
                self._add_step(
                    "SKIP_VISITED",
                    {
                        'node': self.current_node,
                        'neighbor': self.current_node
                    },
                    f"⏭️ Skip {self.current_node} (already visited)"
                )
                continue

            # Visit node
            self.visited.add(self.current_node)
            self.traversal_order.append(self.current_node)
            
            neighbors = sorted(self.adjacency[self.current_node])
            
            self._add_step(
                "VISIT_NODE",
                {
                    'node': self.current_node,
                    'neighbors': neighbors,
                    'visit_order': len(self.traversal_order)
                },
                f"✅ Visit node {self.current_node} (neighbor count: {len(neighbors)})"
            )

            # Process neighbors in reverse order (so first neighbor is processed first due to stack LIFO)
            unvisited_neighbors = []
            for neighbor in reversed(neighbors):
                if neighbor in self.visited:
                    # Skip visited neighbor
                    self._add_step(
                        "SKIP_VISITED",
                        {
                            'node': self.current_node,
                            'neighbor': neighbor
                        },
                        f"⏭️ Skip neighbor {neighbor} (already visited)"
                    )
                else:
                    # Push unvisited neighbor
                    unvisited_neighbors.append(neighbor)
                    self.stack.append(neighbor)
                    self._add_step(
                        "PUSH_STACK",
                        {
                            'node': neighbor,
                            'reason': f'Unvisited neighbor of {self.current_node}'
                        },
                        f"📥 Push neighbor {neighbor} onto stack"
                    )

            # If no unvisited neighbors, we're backtracking
            if not unvisited_neighbors and neighbors:
                self._add_step(
                    "BACKTRACK",
                    {
                        'from_node': self.current_node,
                        'all_neighbors_visited': True
                    },
                    f"⬅️ Backtrack from {self.current_node} (all neighbors visited)"
                )

        # Final state
        self.current_node = None
        
        return self._build_trace_result({
            'traversal_order': self.traversal_order,
            'nodes_visited': len(self.visited)
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "When examining a neighbor, will it be visited or skipped?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: When we encounter a neighbor, before decision
            if step.type == "VISIT_NODE" and i + 1 < len(self.trace):
                node = step.data['node']
                neighbors = step.data['neighbors']
                
                if not neighbors:
                    continue
                
                # Look ahead to find first neighbor decision
                for j in range(i + 1, min(i + 10, len(self.trace))):
                    next_step = self.trace[j]
                    
                    if next_step.type in ["SKIP_VISITED", "PUSH_STACK"]:
                        neighbor = next_step.data.get('neighbor') or next_step.data.get('node')
                        
                        if neighbor in neighbors:
                            # Found a neighbor decision
                            correct_answer = "skip" if next_step.type == "SKIP_VISITED" else "visit"
                            
                            predictions.append({
                                'step_index': i,
                                'question': f"Node {node} has neighbor {neighbor}. Will it be visited or skipped?",
                                'choices': [
                                    {'id': 'visit', 'label': f'Visit {neighbor} (push onto stack)'},
                                    {'id': 'skip', 'label': f'Skip {neighbor} (already visited)'}
                                ],
                                'hint': f"Check if {neighbor} is in the visited set",
                                'correct_answer': correct_answer,
                                'explanation': self._get_prediction_explanation(neighbor, correct_answer, step.data['visualization'])
                            })
                            
                            break  # Only one prediction per VISIT_NODE step

        return predictions

    def _get_prediction_explanation(self, neighbor: str, answer: str, viz_state: dict) -> str:
        """Generate explanation for prediction answer."""
        visited = set(viz_state.get('visited', []))
        
        if answer == "skip":
            return f"{neighbor} is already in the visited set {{{', '.join(sorted(visited))}}}, so we skip it to avoid revisiting."
        else:
            return f"{neighbor} is not in the visited set {{{', '.join(sorted(visited))}}}, so we push it onto the stack for future exploration."
