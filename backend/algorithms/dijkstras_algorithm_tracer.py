"""
Dijkstra's Algorithm tracer for educational visualization.

Implements Dijkstra's shortest path algorithm using a min-heap priority queue
with complete trace generation for step-by-step visualization and prediction mode.

VERSION: 2.5 - Backend Checklist v2.5 Compliance
- Graph algorithm extensions applied
- Frontend Visualization Hints section included
- Result field traceability implemented
"""

from typing import Any, List, Dict, Set, Tuple
import heapq
from .base_tracer import AlgorithmTracer


class DijkstrasAlgorithmTracer(AlgorithmTracer):
    """
    Tracer for Dijkstra's shortest path algorithm on weighted graphs.

    Visualization shows:
    - Graph nodes with states (unvisited, examining, visited)
    - Graph edges with states (unexplored, examining, relaxed)
    - Priority queue contents with (distance, node) pairs
    - Distance map tracking shortest known distances
    - Previous map for path reconstruction

    Prediction points ask: "Which node will be selected next from priority queue?"
    """

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.adjacency = {}  # node -> [(neighbor, weight), ...]
        self.start_node = None
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.priority_queue = []
        self.current_node = None

    def _build_adjacency_list(self, nodes: List[str], edges: List[Tuple[str, str, int]]):
        """Build adjacency list from edge list."""
        self.adjacency = {node: [] for node in nodes}
        for u, v, weight in edges:
            self.adjacency[u].append((v, weight))
            self.adjacency[v].append((u, weight))  # Undirected graph

    def _get_visualization_state(self) -> dict:
        """
        Return current graph state with nodes, edges, and algorithm structures.

        Node states:
        - 'unvisited': Not yet processed
        - 'examining': Currently being processed
        - 'visited': Fully processed

        Edge states:
        - 'unexplored': Not yet considered
        - 'examining': Currently being evaluated for relaxation
        - 'relaxed': Used to update a distance
        """
        if not self.nodes:
            return {}

        # Build node visualization
        nodes_viz = []
        for node in self.nodes:
            state = 'visited' if node in self.visited else ('examining' if node == self.current_node else 'unvisited')
            nodes_viz.append({
                'id': node,
                'state': state,
                'distance': self.distances.get(node, float('inf')),
                'previous': self.previous.get(node, None)
            })

        # Build edge visualization
        edges_viz = []
        for u, v, weight in self.edges:
            # Edge is relaxed if it's part of the shortest path tree
            state = 'unexplored'
            if u in self.visited and v in self.visited:
                # Check if this edge is in the shortest path tree
                if self.previous.get(v) == u or self.previous.get(u) == v:
                    state = 'relaxed'
                else:
                    state = 'unexplored'
            elif self.current_node in [u, v]:
                state = 'examining'
            
            edges_viz.append({
                'from': u,
                'to': v,
                'weight': weight,
                'state': state
            })

        # Priority queue visualization (show as list of (distance, node) pairs)
        pq_viz = [{'distance': dist, 'node': node} for dist, node in sorted(self.priority_queue)]

        return {
            'nodes': nodes_viz,
            'edges': edges_viz,
            'priority_queue': pq_viz,
            'distance_map': {node: self._serialize_value(dist) for node, dist in self.distances.items()},
            'previous_map': dict(self.previous),
            'visited_set': list(self.visited),
            'current_node': self.current_node
        }

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Dijkstra's Algorithm trace.

        Shows complete execution flow with all decision data visible.
        Includes Frontend Visualization Hints (Backend Checklist v2.5).

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Dijkstra's Algorithm Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Start Node:** {self.start_node}\n"
        narrative += f"**Graph Size:** {metadata['input_size']} nodes\n"
        narrative += f"**Total Steps:** {len(steps)}\n\n"
        narrative += "---\n\n"

        # Step-by-step narrative
        for step in steps:
            step_num = step['step']
            step_type = step['type']
            description = step['description']
            data = step['data']
            viz = data.get('visualization', {})

            narrative += f"## Step {step_num}: {description}\n\n"

            # Type-specific details
            if step_type == "INIT_DISTANCES":
                narrative += "**Purpose:** Initialize distance tracking for shortest path computation.\n\n"
                
                narrative += "**Graph Structure (Adjacency List):**\n"
                for node in sorted(self.adjacency.keys()):
                    neighbors = self.adjacency[node]
                    if neighbors:
                        neighbor_str = ", ".join([f"{n} (weight: {w})" for n, w in sorted(neighbors)])
                        narrative += f"- **{node}**: [{neighbor_str}]\n"
                    else:
                        narrative += f"- **{node}**: [no neighbors]\n"
                narrative += "\n"

                narrative += "**Initial Distances:**\n"
                narrative += f"- Start node **{data['start_node']}**: distance = **0** (starting point)\n"
                narrative += f"- All other nodes: distance = **∞** (unreachable until proven otherwise)\n\n"

                narrative += "**Initial Priority Queue:**\n"
                narrative += f"- Insert ({data['start_node']}, 0) - start node with distance 0\n"
                narrative += f"- Queue state: `[(0, '{data['start_node']}')]` ← (0, '{data['start_node']}') has highest priority (smallest distance)\n\n"

                narrative += "**Tracking Structures:**\n"
                narrative += f"- **Distance map** (`distances`): Tracks shortest known distance to each node\n"
                narrative += f"- **Previous map** (`previous`): Tracks previous node in shortest path (for path reconstruction)\n"
                narrative += f"- **Visited set**: Tracks nodes with finalized shortest distances\n\n"

            elif step_type == "SELECT_MIN_DIST":
                node = data['selected_node']
                dist = data['distance']
                pq_before = data['pq_before_pop']

                narrative += "**Priority Queue Selection:**\n"
                narrative += f"Queue before pop: `{pq_before}`\n"
                narrative += f"- Extract minimum: **(distance: {dist}, node: '{node}')**\n"
                narrative += f"- This node has the smallest unfinalized distance\n\n"

                narrative += "**Decision:** Process node **{node}** with distance **{dist}**\n"
                narrative += f"- Mark **{node}** as visited (distance is now finalized)\n"
                narrative += f"- Explore all neighbors of **{node}** to potentially improve their distances\n\n"

                if viz.get('visited_set'):
                    narrative += f"**Visited Set:** {{{', '.join(sorted(viz['visited_set']))}}}\n\n"

            elif step_type == "VISIT_NODE":
                node = data['node']
                dist = data['distance']
                neighbors = data['neighbors']

                narrative += f"**Current Node:** **{node}** (distance from start: **{dist}**)\n\n"

                narrative += "**Neighbors to Check:**\n"
                if neighbors:
                    narrative += f"Node **{node}** has neighbors: **{neighbors}**\n"
                    narrative += f"- Will attempt to relax edges to each unvisited neighbor\n"
                    narrative += f"- Edge relaxation: Check if path through **{node}** is shorter than current known distance\n\n"
                else:
                    narrative += f"Node **{node}** has **no neighbors** - nothing to explore\n\n"

            elif step_type == "CHECK_NEIGHBOR":
                current = data['current_node']
                neighbor = data['neighbor']
                edge_weight = data['edge_weight']
                neighbor_visited = data['neighbor_visited']

                narrative += f"**Examining Edge:** **{current}** → **{neighbor}** (weight: **{edge_weight}**)\n\n"

                if neighbor_visited:
                    narrative += f"**Filter Check:** Is **{neighbor}** visited?\n"
                    narrative += f"- **{neighbor}** ∈ visited set ✓\n"
                    narrative += f"- **Decision:** Skip (already has finalized shortest distance)\n\n"
                else:
                    narrative += f"**Filter Check:** Is **{neighbor}** visited?\n"
                    narrative += f"- **{neighbor}** ∉ visited set ✓\n"
                    narrative += f"- **Decision:** Proceed to edge relaxation\n\n"

            elif step_type == "RELAX_EDGE":
                current = data['current_node']
                neighbor = data['neighbor']
                edge_weight = data['edge_weight']
                current_dist = data['current_distance']
                neighbor_old_dist = data['neighbor_old_distance']
                new_dist = data['new_distance']
                improved = data['improved']

                narrative += f"**Edge Relaxation:** Attempt to improve distance to **{neighbor}**\n\n"

                narrative += "**Calculation:**\n"
                narrative += f"- Current distance to **{current}**: **{current_dist}**\n"
                narrative += f"- Edge weight **{current}** → **{neighbor}**: **{edge_weight}**\n"
                narrative += f"- Potential new distance: {current_dist} + {edge_weight} = **{new_dist}**\n\n"

                narrative += "**Comparison:**\n"
                old_dist_str = "∞" if neighbor_old_dist == float('inf') else str(neighbor_old_dist)
                narrative += f"- Current distance to **{neighbor}**: **{old_dist_str}**\n"
                narrative += f"- Compare: {new_dist} < {old_dist_str}?\n\n"

                if improved:
                    narrative += f"**Result:** {new_dist} < {old_dist_str} ✓ (shorter path found)\n\n"
                    narrative += "**Actions Taken:**\n"
                    narrative += f"1. Update `distances[{neighbor}]` = **{new_dist}** (was {old_dist_str})\n"
                    narrative += f"2. Update `previous[{neighbor}]` = **'{current}'** (track path)\n"
                    narrative += f"3. Insert ({new_dist}, '{neighbor}') into priority queue\n\n"
                else:
                    narrative += f"**Result:** {new_dist} ≥ {old_dist_str} ✗ (no improvement)\n\n"
                    narrative += "**Action:** Keep existing distance (no update needed)\n\n"

            elif step_type == "UPDATE_DISTANCE":
                neighbor = data['neighbor']
                old_dist = data['old_distance']
                new_dist = data['new_distance']
                via_node = data['via_node']

                old_dist_str = "∞" if old_dist == float('inf') else str(old_dist)
                narrative += f"**Distance Update Confirmed:**\n"
                narrative += f"- Node: **{neighbor}**\n"
                narrative += f"- Old distance: **{old_dist_str}**\n"
                narrative += f"- New distance: **{new_dist}** (via **{via_node}**)\n"
                narrative += f"- Path tracking: `previous[{neighbor}]` = **'{via_node}'**\n\n"

                # Show current distance map state
                if viz.get('distance_map'):
                    narrative += "**Current Distance Map:**\n\n"
                    narrative += "| Node | Distance | Previous |\n"
                    narrative += "|------|----------|----------|\n"
                    for node in sorted(viz['distance_map'].keys()):
                        dist_val = viz['distance_map'][node]
                        dist_str = "∞" if dist_val is None else str(dist_val)
                        prev_val = viz['previous_map'].get(node, 'null')
                        visited_marker = " ✓" if node in viz.get('visited_set', []) else ""
                        narrative += f"| {node}{visited_marker} | {dist_str} | {prev_val} |\n"
                    narrative += "\n"

            narrative += "---\n\n"

        # Final Result Summary
        narrative += "## Final Result\n\n"
        
        narrative += "**Shortest Distances from Start Node:**\n\n"
        narrative += "| Node | Distance | Path |\n"
        narrative += "|------|----------|------|\n"
        
        for node in sorted(result['distances'].keys()):
            dist = result['distances'][node]
            dist_str = "∞" if dist is None else str(dist)
            path = result['paths'].get(node, [])
            path_str = " → ".join(path) if path else "unreachable"
            narrative += f"| {node} | {dist_str} | {path_str} |\n"
        
        narrative += "\n"

        narrative += "**Algorithm Completion:**\n"
        narrative += f"- All reachable nodes have finalized shortest distances\n"
        narrative += f"- Unreachable nodes remain at distance ∞\n"
        narrative += f"- Paths can be reconstructed using `previous` map\n\n"

        narrative += "**Complexity Analysis:**\n"
        narrative += f"- Time Complexity: O((V + E) log V) with binary heap\n"
        narrative += f"  - V = {len(self.nodes)} nodes, E = {len(self.edges)} edges\n"
        narrative += f"- Space Complexity: O(V) for distance/previous maps and priority queue\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.5)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Priority Queue State** (`priority_queue`) - Shows which nodes are candidates for processing, ordered by distance\n"
        narrative += "- **Distance Map** (`distance_map`) - Real-time view of shortest known distances evolving\n"
        narrative += "- **Current Node** (`current_node`) - The node being processed in this step\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the greedy selection** - When a node is popped from priority queue, emphasize this is the 'closest unvisited node'\n"
        narrative += "2. **Animate edge relaxation** - Show the comparison (new_distance < old_distance) visually with the actual numbers\n"
        narrative += "3. **Show distance improvements** - When a distance updates, use color transitions or animations to show the change\n"
        narrative += "4. **Visualize the shortest path tree** - Edges in the `previous` map form the tree - highlight these differently\n"
        narrative += "5. **Priority queue as sorted list** - Display queue contents sorted by distance to show why certain nodes are selected\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.nodes[*].id\n"
        narrative += "step.data.visualization.nodes[*].state  // 'unvisited' | 'examining' | 'visited'\n"
        narrative += "step.data.visualization.nodes[*].distance\n"
        narrative += "step.data.visualization.nodes[*].previous\n"
        narrative += "step.data.visualization.edges[*].from\n"
        narrative += "step.data.visualization.edges[*].to\n"
        narrative += "step.data.visualization.edges[*].weight\n"
        narrative += "step.data.visualization.edges[*].state  // 'unexplored' | 'examining' | 'relaxed'\n"
        narrative += "step.data.visualization.priority_queue[*].distance\n"
        narrative += "step.data.visualization.priority_queue[*].node\n"
        narrative += "step.data.visualization.distance_map\n"
        narrative += "step.data.visualization.previous_map\n"
        narrative += "step.data.visualization.visited_set\n"
        narrative += "step.data.visualization.current_node\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Dijkstra's algorithm is fundamentally about **greedy selection** and **edge relaxation**. "
        narrative += "The most important visualization moments are: (1) **Priority queue pop** - show why this node has the smallest distance, "
        narrative += "(2) **Edge relaxation comparison** - display the arithmetic (current_dist + edge_weight vs old_dist) with actual values, "
        narrative += "(3) **Distance map updates** - animate the change from old to new distance. "
        narrative += "The priority queue should be visualized as a **sorted list** (not a tree) to make the 'minimum distance' selection obvious. "
        narrative += "Use a **table view** for the distance/previous maps to show all nodes at once - this helps learners see the global state. "
        narrative += "When an edge is relaxed successfully, highlight both the edge AND the distance update simultaneously. "
        narrative += "The final shortest path tree (edges in `previous` map) should be visually distinct - consider using a different color or thickness. "
        narrative += "For unreachable nodes (distance = ∞), use a clear visual indicator like a grayed-out state or a special symbol.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Dijkstra's algorithm with trace generation.

        Args:
            input_data: dict with keys:
                - 'nodes': List[str] - Node identifiers
                - 'edges': List[Tuple[str, str, int]] - (u, v, weight) tuples
                - 'start_node': str - Starting node for shortest paths

        Returns:
            Standardized trace result with:
                - result: {'distances': dict, 'paths': dict}
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='graph'

        Raises:
            ValueError: If input is invalid or start_node not in nodes
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
            raise ValueError("Nodes list cannot be empty")
        
        if self.start_node not in self.nodes:
            raise ValueError(f"Start node '{self.start_node}' not in nodes list")

        # Validate non-negative weights
        for u, v, weight in self.edges:
            if weight < 0:
                raise ValueError(f"Negative weight {weight} on edge ({u}, {v}). Dijkstra's algorithm requires non-negative weights.")

        # Build adjacency list
        self._build_adjacency_list(self.nodes, self.edges)

        # Initialize algorithm state
        self.distances = {node: float('inf') for node in self.nodes}
        self.distances[self.start_node] = 0
        self.previous = {}
        self.visited = set()
        self.priority_queue = [(0, self.start_node)]
        self.current_node = None

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'dijkstras-algorithm',
            'display_name': "Dijkstra's Algorithm",
            'visualization_type': 'graph',
            'visualization_config': {
                'directed': False,
                'weighted': True,
                'show_priority_queue': True,
                'show_distances': True
            },
            'input_size': len(self.nodes),
            'start_node': self.start_node
        }

        # Step 0: Initialize distances
        self._add_step(
            "INIT_DISTANCES",
            {
                'start_node': self.start_node,
                'initial_distances': {node: self._serialize_value(dist) for node, dist in self.distances.items()},
                'initial_pq': [(0, self.start_node)]
            },
            f"🎯 Initialize: Set distance to start node '{self.start_node}' = 0, all others = ∞"
        )

        # Main algorithm loop
        while self.priority_queue:
            # Select node with minimum distance
            current_dist, current_node = heapq.heappop(self.priority_queue)

            # Skip if already visited (duplicate in queue)
            if current_node in self.visited:
                continue

            self.current_node = current_node

            # Mark as visited BEFORE recording step so visualization state is correct
            self.visited.add(current_node)

            # Record selection
            pq_snapshot = list(self.priority_queue)
            self._add_step(
                "SELECT_MIN_DIST",
                {
                    'selected_node': current_node,
                    'distance': current_dist,
                    'pq_before_pop': [(d, n) for d, n in [(current_dist, current_node)] + pq_snapshot]
                },
                f"📍 Select node '{current_node}' with minimum distance {current_dist} from priority queue"
            )

            # Get neighbors
            neighbors = [n for n, w in self.adjacency[current_node]]

            self._add_step(
                "VISIT_NODE",
                {
                    'node': current_node,
                    'distance': current_dist,
                    'neighbors': neighbors
                },
                f"🔍 Visit node '{current_node}' (distance: {current_dist}) - checking {len(neighbors)} neighbor(s)"
            )

            # Process each neighbor
            for neighbor, edge_weight in self.adjacency[current_node]:
                # Check if neighbor already visited
                neighbor_visited = neighbor in self.visited

                self._add_step(
                    "CHECK_NEIGHBOR",
                    {
                        'current_node': current_node,
                        'neighbor': neighbor,
                        'edge_weight': edge_weight,
                        'neighbor_visited': neighbor_visited
                    },
                    f"🔗 Check edge '{current_node}' → '{neighbor}' (weight: {edge_weight})"
                )

                if neighbor_visited:
                    continue

                # Calculate new distance through current node
                new_distance = current_dist + edge_weight
                old_distance = self.distances[neighbor]

                # Edge relaxation
                improved = new_distance < old_distance

                self._add_step(
                    "RELAX_EDGE",
                    {
                        'current_node': current_node,
                        'neighbor': neighbor,
                        'edge_weight': edge_weight,
                        'current_distance': current_dist,
                        'neighbor_old_distance': self._serialize_value(old_distance),
                        'new_distance': new_distance,
                        'improved': improved
                    },
                    f"⚖️ Relax edge: {current_dist} + {edge_weight} = {new_distance} vs current {self._serialize_value(old_distance)}"
                )

                if improved:
                    # Update distance and previous
                    self.distances[neighbor] = new_distance
                    self.previous[neighbor] = current_node
                    heapq.heappush(self.priority_queue, (new_distance, neighbor))

                    self._add_step(
                        "UPDATE_DISTANCE",
                        {
                            'neighbor': neighbor,
                            'old_distance': self._serialize_value(old_distance),
                            'new_distance': new_distance,
                            'via_node': current_node
                        },
                        f"✅ Update: distance['{neighbor}'] = {new_distance} (via '{current_node}')"
                    )

        # Build result with paths
        paths = {}
        for node in self.nodes:
            if self.distances[node] != float('inf'):
                # Reconstruct path
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = self.previous.get(current)
                path.reverse()
                paths[node] = path
            else:
                paths[node] = []

        return self._build_trace_result({
            'distances': {node: self._serialize_value(dist) for node, dist in self.distances.items()},
            'paths': paths
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "Which node will be selected next from the priority queue?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Before SELECT_MIN_DIST step
            if step.type == "SELECT_MIN_DIST" and i > 0:
                # Get previous step to see what nodes are available
                prev_step = self.trace[i - 1]
                
                # Get the node that was actually selected
                selected_node = step.data['selected_node']
                selected_dist = step.data['distance']
                
                # Get priority queue state before selection
                pq_before = step.data.get('pq_before_pop', [])
                
                # Create choices from top 3 nodes in priority queue (or fewer if less available)
                choices = []
                seen_nodes = set()
                
                for dist, node in sorted(pq_before)[:3]:
                    if node not in seen_nodes:
                        choices.append({
                            'id': node,
                            'label': f"Node '{node}' (distance: {dist})"
                        })
                        seen_nodes.add(node)
                
                # Only create prediction if we have multiple choices
                if len(choices) >= 2:
                    predictions.append({
                        'step_index': i - 1,  # Predict before the selection step
                        'question': f"Which node will be selected next from the priority queue?",
                        'choices': choices[:3],  # Max 3 choices
                        'hint': "The node with the smallest distance is always selected next",
                        'correct_answer': selected_node,
                        'explanation': f"Node '{selected_node}' has the smallest distance ({selected_dist}) in the priority queue, so it is selected by the greedy strategy."
                    })

        return predictions