
"""
Breadth-First Search (BFS) algorithm tracer for educational visualization.

Implements BFS graph traversal with complete trace generation for step-by-step
visualization, showing level-order exploration using a queue data structure.

VERSION: 2.1 - Backend Checklist v2.2 Compliance
- Graph topology shown once in Step 0
- Multi-element filtering patterns for neighbor processing
- Traversal structure visibility with queue directional indicators
- Frontend Visualization Hints section included
"""

from typing import Any, List, Dict, Set
from collections import deque
from .base_tracer import AlgorithmTracer


class BreadthFirstSearchTracer(AlgorithmTracer):
    """
    Tracer for Breadth-First Search algorithm on undirected graphs.

    Visualization shows:
    - Graph nodes with states (unvisited, enqueued, visiting, visited)
    - Graph edges with states (unexplored, exploring, traversed)
    - Queue contents with directional indicators (front → back)
    - Level tracking for each node
    - Traversal order sequence

    Prediction points ask: "Which neighbors will be enqueued next?"
    """

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.adjacency = {}
        self.start_node = None
        self.queue = deque()
        self.visited = set()
        self.levels = {}
        self.traversal_order = []
        self.current_node = None

    def _build_adjacency_list(self, nodes: List[str], edges: List[tuple]) -> Dict[str, List[str]]:
        """Build adjacency list from edge list (undirected graph)."""
        adjacency = {node: [] for node in nodes}
        for u, v in edges:
            adjacency[u].append(v)
            adjacency[v].append(u)
        # Sort neighbors for consistent ordering
        for node in adjacency:
            adjacency[node].sort()
        return adjacency

    def _get_visualization_state(self) -> dict:
        """
        Return current graph state with node/edge states and queue visualization.

        Node states:
        - 'unvisited': Not yet discovered
        - 'enqueued': In queue waiting to be processed
        - 'visiting': Currently being processed (dequeued)
        - 'visited': Fully processed (all neighbors explored)

        Edge states:
        - 'unexplored': Not yet traversed
        - 'exploring': Currently examining (from visiting node to neighbor)
        - 'traversed': Already used in traversal
        """
        if not self.nodes:
            return {}

        # Determine node states
        node_states = []
        for node in self.nodes:
            # Priority 1: If in visited set AND is current node, show 'visited' (processing complete)
            if node in self.visited and node == self.current_node:
                state = 'visited'
            # Priority 2: If current but not yet in visited, show 'visiting' (processing ongoing)
            elif node == self.current_node:
                state = 'visiting'
            elif node in self.visited:
                state = 'visited'
            elif node in self.queue:
                state = 'enqueued'
            else:
                state = 'unvisited'
            
            node_states.append({
                'id': node,
                'state': state,
                'level': self.levels.get(node, None)
            })

        # Determine edge states
        edge_states = []
        for u, v in self.edges:
            # Edge is traversed if both nodes are visited
            if u in self.visited and v in self.visited:
                state = 'traversed'
            # Edge is exploring if one node is current and other is being examined
            elif (u == self.current_node or v == self.current_node):
                state = 'exploring'
            else:
                state = 'unexplored'
            
            edge_states.append({
                'from': u,
                'to': v,
                'state': state
            })

        return {
            'nodes': node_states,
            'edges': edge_states,
            'queue': list(self.queue),
            'visited': sorted(list(self.visited)),
            'current_level': self.levels.get(self.current_node, None) if self.current_node else None,
            'traversal_order': self.traversal_order.copy()
        }

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from BFS trace.

        Shows complete execution flow with all decision data visible,
        following graph algorithm extensions for multi-element filtering,
        traversal structure visibility, and explicit neighbor processing.

        Args:
            trace_result: Complete trace result from execute() method

        Returns:
            Markdown-formatted narrative showing step-by-step execution
        """
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header
        narrative = "# Breadth-First Search Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Start Node:** {result['start_node']}\n"
        narrative += f"**Graph Size:** {metadata['input_size']} nodes, {len(self.edges)} edges\n"
        narrative += f"**Traversal Order:** {' → '.join(result['traversal_order'])}\n"
        narrative += f"**Total Nodes Visited:** {len(result['traversal_order'])}\n\n"
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
            if step_type == "INITIAL_STATE":
                narrative += f"**Graph Structure (Adjacency List):**\n\n"
                narrative += "| Node | Neighbors |\n"
                narrative += "|------|----------|\n"
                for node in sorted(self.adjacency.keys()):
                    neighbors = ', '.join(self.adjacency[node]) if self.adjacency[node] else '(none)'
                    narrative += f"| {node} | {neighbors} |\n"
                narrative += "\n"

                narrative += f"**Initial Configuration:**\n"
                narrative += f"- Start node: **{data['start_node']}**\n"
                narrative += f"- Queue: Empty `[]`\n"
                narrative += f"- Visited set: Empty `{{}}`\n"
                narrative += f"- All nodes marked as **unvisited**\n\n"

                narrative += "*BFS explores nodes level by level, visiting all neighbors at distance d before moving to distance d+1.*\n\n"

            elif step_type == "ENQUEUE":
                node = data['node']
                level = data['level']
                queue_after = data['queue_after']

                narrative += f"**Action:** Add node **{node}** to queue\n\n"
                narrative += f"**Level Assignment:**\n"
                narrative += f"- Node **{node}** is at level **{level}** (distance {level} from start)\n\n"

                narrative += f"**Queue State:**\n"
                narrative += f"```\n"
                narrative += f"Front → {queue_after} ← Back\n"
                narrative += f"```\n"
                narrative += f"*Queue now contains **{len(queue_after)}** node(s) waiting to be processed*\n\n"

                if viz.get('nodes'):
                    enqueued_nodes = [n['id'] for n in viz['nodes'] if n['state'] == 'enqueued']
                    if enqueued_nodes:
                        narrative += f"**Enqueued nodes:** {', '.join(enqueued_nodes)}\n\n"

            elif step_type == "DEQUEUE":
                node = data['node']
                level = data['level']
                queue_after = data['queue_after']

                narrative += f"**Action:** Remove node **{node}** from front of queue\n\n"
                narrative += f"**Processing:**\n"
                narrative += f"- Current node: **{node}**\n"
                narrative += f"- Current level: **{level}**\n"
                narrative += f"- Traversal position: #{data['traversal_position']}\n\n"

                narrative += f"**Queue State After Dequeue:**\n"
                narrative += f"```\n"
                if queue_after:
                    narrative += f"Front → {queue_after} ← Back\n"
                else:
                    narrative += f"(empty)\n"
                narrative += f"```\n"
                if queue_after:
                    narrative += f"*Queue now contains **{len(queue_after)}** node(s)*\n\n"
                else:
                    narrative += f"*Queue is now empty*\n\n"

            elif step_type == "VISIT_NODE":
                node = data['node']
                level = data['level']

                narrative += f"**Mark Visited:** Node **{node}** is now fully processed\n\n"
                narrative += f"**Visited Set:**\n"
                narrative += f"```\n"
                narrative += f"{{{', '.join(sorted(viz['visited']))}}}\n"
                narrative += f"```\n"
                narrative += f"*Total visited: **{len(viz['visited'])}** nodes*\n\n"

                narrative += f"**Traversal Progress:**\n"
                narrative += f"```\n"
                narrative += f"{' → '.join(viz['traversal_order'])}\n"
                narrative += f"```\n\n"

            elif step_type == "ENQUEUE_NEIGHBORS":
                current = data['current_node']
                all_neighbors = data['all_neighbors']
                visited_set = data['visited_set']
                already_visited = data['already_visited']
                to_enqueue = data['to_enqueue']
                enqueued_count = data['enqueued_count']

                narrative += f"**Multi-Element Filtering: Process Neighbors of {current}**\n\n"

                # Step 1: Show full collection
                narrative += f"**Step 1 - Full Neighbor List:**\n"
                if all_neighbors:
                    narrative += f"- Node **{current}** has neighbors: **{all_neighbors}**\n\n"
                else:
                    narrative += f"- Node **{current}** has **no neighbors** (isolated or leaf node)\n\n"

                if all_neighbors:
                    # Step 2: Show filter criteria
                    narrative += f"**Step 2 - Filter Criteria:**\n"
                    narrative += f"- Check against visited set: `{{{', '.join(sorted(visited_set))}}}`\n"
                    narrative += f"- Rule: Only enqueue **unvisited** neighbors\n\n"

                    # Step 3: Show explicit comparisons
                    narrative += f"**Step 3 - Explicit Neighbor Checks:**\n"
                    for neighbor in all_neighbors:
                        if neighbor in already_visited:
                            narrative += f"- **{neighbor}**: visited ✓ → skip (already processed)\n"
                        else:
                            narrative += f"- **{neighbor}**: unvisited → enqueue (new discovery)\n"
                    narrative += "\n"

                    # Step 4: Show filtered result
                    narrative += f"**Step 4 - Filtered Result:**\n"
                    if to_enqueue:
                        narrative += f"- Neighbors to enqueue: **{to_enqueue}**\n"
                        narrative += f"- Count: **{enqueued_count}** new node(s) added to queue\n\n"
                    else:
                        narrative += f"- No new neighbors to enqueue (all already visited)\n\n"
                else:
                    narrative += f"*No neighbors to process*\n\n"

                # Show updated queue
                if viz.get('queue'):
                    narrative += f"**Updated Queue:**\n"
                    narrative += f"```\n"
                    narrative += f"Front → {viz['queue']} ← Back\n"
                    narrative += f"```\n\n"

            elif step_type == "COMPLETE":
                total_visited = data['total_visited']
                total_nodes = data['total_nodes']

                narrative += f"**BFS Traversal Complete**\n\n"
                narrative += f"**Final Statistics:**\n"
                narrative += f"- Nodes visited: **{total_visited}** out of **{total_nodes}**\n"
                narrative += f"- Queue state: Empty (all reachable nodes processed)\n\n"

                if total_visited < total_nodes:
                    unvisited = total_nodes - total_visited
                    narrative += f"⚠️ **Note:** {unvisited} node(s) remain unvisited (disconnected component)\n\n"

                narrative += f"**Final Traversal Order:**\n"
                narrative += f"```\n"
                narrative += f"{' → '.join(viz['traversal_order'])}\n"
                narrative += f"```\n\n"

                narrative += f"**Level Distribution:**\n"
                level_counts = {}
                for node_data in viz['nodes']:
                    level = node_data['level']
                    if level is not None:
                        level_counts[level] = level_counts.get(level, 0) + 1
                
                for level in sorted(level_counts.keys()):
                    narrative += f"- Level {level}: {level_counts[level]} node(s)\n"
                narrative += "\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Traversal Result:**\n"
        narrative += f"- Start node: **{result['start_node']}**\n"
        narrative += f"- Nodes visited: **{len(result['traversal_order'])}** out of **{len(self.nodes)}**\n"
        narrative += f"- Traversal order: {' → '.join(result['traversal_order'])}\n\n"

        narrative += f"**Level Assignments:**\n"
        for node in result['traversal_order']:
            level = result['levels'][node]
            narrative += f"- Node **{node}**: Level {level}\n"
        narrative += "\n"

        narrative += f"**Algorithm Properties:**\n"
        narrative += f"- Time Complexity: O(V + E) where V = vertices, E = edges\n"
        narrative += f"- Space Complexity: O(V) for queue and visited set\n"
        narrative += f"- Guarantees: Finds shortest path (in terms of edge count) from start to all reachable nodes\n"
        narrative += f"- Traversal Pattern: Level-order (all nodes at distance d before distance d+1)\n\n"

        # Add Frontend Visualization Hints section (Backend Checklist v2.2)
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Queue Contents** (`queue`) - Shows the frontier of exploration, critical for understanding BFS's level-order nature\n"
        narrative += "- **Current Level** (`current_level`) - Demonstrates how BFS explores all nodes at distance d before moving to d+1\n"
        narrative += "- **Traversal Order** (`traversal_order`) - Shows the sequence of node discovery, proving level-order exploration\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Animate queue operations** - Show enqueue (add to back) and dequeue (remove from front) with clear directional flow\n"
        narrative += "2. **Highlight level boundaries** - Use distinct colors or visual grouping for nodes at the same level\n"
        narrative += "3. **Emphasize the visiting node** - The `visiting` state is the active exploration moment\n"
        narrative += "4. **Show neighbor filtering** - When processing neighbors, visually distinguish already-visited vs. newly-discovered\n"
        narrative += "5. **Track traversal progress** - Display the growing traversal order sequence prominently\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.nodes[*].id\n"
        narrative += "step.data.visualization.nodes[*].state  // 'unvisited' | 'enqueued' | 'visiting' | 'visited'\n"
        narrative += "step.data.visualization.nodes[*].level\n"
        narrative += "step.data.visualization.edges[*].from\n"
        narrative += "step.data.visualization.edges[*].to\n"
        narrative += "step.data.visualization.edges[*].state  // 'unexplored' | 'exploring' | 'traversed'\n"
        narrative += "step.data.visualization.queue  // Array showing front → back order\n"
        narrative += "step.data.visualization.visited  // Set of fully processed nodes\n"
        narrative += "step.data.visualization.current_level\n"
        narrative += "step.data.visualization.traversal_order  // Growing sequence of visited nodes\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "BFS's defining characteristic is **level-order traversal** - it explores all neighbors at distance d before moving to distance d+1. "
        narrative += "The queue is the heart of this behavior: nodes are added to the back (enqueue) and removed from the front (dequeue), creating FIFO ordering. "
        narrative += "Visualize the queue as a **horizontal pipeline** with clear front/back indicators. "
        narrative += "When a node is dequeued and becomes `visiting`, show its neighbors being examined - some will be skipped (already visited), others will be enqueued (new discoveries). "
        narrative += "Use **level-based coloring** or **concentric rings** to show nodes at the same distance from the start. "
        narrative += "The traversal order sequence should be prominently displayed, growing with each VISIT_NODE step. "
        narrative += "For disconnected graphs, clearly indicate when nodes remain unvisited after the queue empties. "
        narrative += "BFS guarantees shortest paths (by edge count), so emphasize how the level assignments represent minimum distances from the start node.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute BFS algorithm with trace generation.

        Args:
            input_data: dict with keys:
                - 'nodes': List of node identifiers (strings)
                - 'edges': List of tuples (u, v) representing undirected edges
                - 'start_node': Node identifier to start traversal from

        Returns:
            Standardized trace result with:
                - result: {
                    'start_node': str,
                    'traversal_order': List[str],
                    'levels': Dict[str, int],
                    'visited_count': int
                  }
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
            raise ValueError(f"Start node '{self.start_node}' not found in graph nodes")

        # Validate edges
        for edge in self.edges:
            if len(edge) != 2:
                raise ValueError(f"Each edge must be a tuple of 2 nodes, got: {edge}")
            u, v = edge
            if u not in self.nodes or v not in self.nodes:
                raise ValueError(f"Edge ({u}, {v}) contains node not in graph")

        # Build adjacency list
        self.adjacency = self._build_adjacency_list(self.nodes, self.edges)

        # Initialize BFS data structures
        self.queue = deque()
        self.visited = set()
        self.levels = {}
        self.traversal_order = []
        self.current_node = None

        # Set metadata for frontend
        self.metadata = {
            'algorithm': 'breadth-first-search',
            'display_name': 'Breadth-First Search',
            'visualization_type': 'graph',
            'visualization_config': {
                'directed': False,
                'show_queue': True,
                'show_levels': True,
                'node_colors': {
                    'unvisited': 'gray',
                    'enqueued': 'yellow',
                    'visiting': 'orange',
                    'visited': 'green'
                },
                'edge_colors': {
                    'unexplored': 'lightgray',
                    'exploring': 'orange',
                    'traversed': 'green'
                }
            },
            'input_size': len(self.nodes),
            'start_node': self.start_node
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {
                'start_node': self.start_node,
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges)
            },
            f"🔍 Initialize BFS from start node {self.start_node}"
        )

        # Enqueue start node at level 0
        self.queue.append(self.start_node)
        self.levels[self.start_node] = 0

        self._add_step(
            "ENQUEUE",
            {
                'node': self.start_node,
                'level': 0,
                'queue_after': list(self.queue)
            },
            f"➕ Enqueue start node {self.start_node} at level 0"
        )

        # BFS main loop
        while self.queue:
            # Dequeue node from front
            self.current_node = self.queue.popleft()
            current_level = self.levels[self.current_node]

            self._add_step(
                "DEQUEUE",
                {
                    'node': self.current_node,
                    'level': current_level,
                    'queue_after': list(self.queue),
                    'traversal_position': len(self.traversal_order) + 1
                },
                f"⬅️ Dequeue node {self.current_node} from front (level {current_level})"
            )

            # Mark as visited and add to traversal order
            self.visited.add(self.current_node)
            self.traversal_order.append(self.current_node)

            self._add_step(
                "VISIT_NODE",
                {
                    'node': self.current_node,
                    'level': current_level,
                    'traversal_position': len(self.traversal_order)
                },
                f"✅ Visit node {self.current_node} (position #{len(self.traversal_order)} in traversal)"
            )

            # Process neighbors
            neighbors = self.adjacency[self.current_node]
            already_visited = [n for n in neighbors if n in self.visited or n in self.queue]
            to_enqueue = [n for n in neighbors if n not in self.visited and n not in self.queue]

            self._add_step(
                "ENQUEUE_NEIGHBORS",
                {
                    'current_node': self.current_node,
                    'all_neighbors': neighbors,
                    'visited_set': sorted(list(self.visited)),
                    'already_visited': already_visited,
                    'to_enqueue': to_enqueue,
                    'enqueued_count': len(to_enqueue)
                },
                f"🔍 Process neighbors of {self.current_node}: {len(to_enqueue)} new, {len(already_visited)} already seen"
            )

            # Enqueue unvisited neighbors
            for neighbor in to_enqueue:
                self.queue.append(neighbor)
                self.levels[neighbor] = current_level + 1

                self._add_step(
                    "ENQUEUE",
                    {
                        'node': neighbor,
                        'level': current_level + 1,
                        'queue_after': list(self.queue)
                    },
                    f"➕ Enqueue neighbor {neighbor} at level {current_level + 1}"
                )

        # Mark completion
        self.current_node = None

        self._add_step(
            "COMPLETE",
            {
                'total_visited': len(self.visited),
                'total_nodes': len(self.nodes)
            },
            f"🏁 BFS complete: visited {len(self.visited)} out of {len(self.nodes)} nodes"
        )

        return self._build_trace_result({
            'start_node': self.start_node,
            'traversal_order': self.traversal_order,
            'levels': self.levels,
            'visited_count': len(self.visited)
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After dequeuing a node, which neighbors will be
        enqueued (unvisited) vs. skipped (already visited)?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: Right after dequeuing, before processing neighbors
            if step.type == "DEQUEUE" and i + 2 < len(self.trace):
                # Look ahead to find ENQUEUE_NEIGHBORS step
                next_step = self.trace[i + 1]  # Should be VISIT_NODE
                neighbors_step = self.trace[i + 2]  # Should be ENQUEUE_NEIGHBORS

                if neighbors_step.type == "ENQUEUE_NEIGHBORS":
                    current = neighbors_step.data['current_node']
                    all_neighbors = neighbors_step.data['all_neighbors']
                    to_enqueue = neighbors_step.data['to_enqueue']

                    if not all_neighbors:
                        continue  # Skip if no neighbors

                    # Create choices (max 3)
                    if len(all_neighbors) <= 3:
                        # Show all neighbors as choices
                        choices = []
                        for neighbor in all_neighbors:
                            if neighbor in to_enqueue:
                                choices.append({
                                    'id': neighbor,
                                    'label': f'{neighbor} (will be enqueued)'
                                })
                            else:
                                choices.append({
                                    'id': neighbor,
                                    'label': f'{neighbor} (already seen)'
                                })
                        
                        correct_answer = ','.join(sorted(to_enqueue)) if to_enqueue else 'none'
                        
                        predictions.append({
                            'step_index': i,
                            'question': f"Node {current} has neighbors {all_neighbors}. Which will be enqueued (unvisited)?",
                            'choices': choices[:3],  # Enforce max 3
                            'hint': f"Check which neighbors are not yet visited or in queue",
                            'correct_answer': correct_answer,
                            'explanation': f"Neighbors {to_enqueue if to_enqueue else 'none'} are unvisited and will be enqueued. Others are already visited or in queue."
                        })
                    else:
                        # Too many neighbors, ask about count instead
                        enqueue_count = len(to_enqueue)
                        choices = [
                            {'id': 'none', 'label': 'None (all already seen)'},
                            {'id': 'some', 'label': f'Some ({enqueue_count} neighbors)'},
                            {'id': 'all', 'label': f'All ({len(all_neighbors)} neighbors)'}
                        ]

                        if enqueue_count == 0:
                            correct_answer = 'none'
                        elif enqueue_count == len(all_neighbors):
                            correct_answer = 'all'
                        else:
                            correct_answer = 'some'

                        predictions.append({
                            'step_index': i,
                            'question': f"Node {current} has {len(all_neighbors)} neighbors. How many will be enqueued?",
                            'choices': choices,
                            'hint': "Count neighbors that are not yet visited or in queue",
                            'correct_answer': correct_answer,
                            'explanation': f"{enqueue_count} out of {len(all_neighbors)} neighbors are unvisited and will be enqueued."
                        })

        return predictions
