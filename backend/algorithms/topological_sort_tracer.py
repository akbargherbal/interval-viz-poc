
"""
Topological Sort (Kahn's Algorithm) tracer for educational visualization.

Implements Kahn's algorithm for topological ordering of a Directed Acyclic Graph (DAG)
with complete trace generation for step-by-step visualization and prediction mode.

Algorithm: BFS-based approach using in-degree tracking
- Calculate in-degrees for all nodes
- Enqueue nodes with in-degree 0
- Process queue: remove node, decrement neighbor in-degrees
- Detect cycles if nodes remain unprocessed

VERSION: 1.0 - Initial implementation with Backend Checklist v2.2 compliance
"""

from typing import Any, List, Dict, Set
from collections import deque, defaultdict
from .base_tracer import AlgorithmTracer


class TopologicalSortTracer(AlgorithmTracer):
    """
    Tracer for Topological Sort using Kahn's Algorithm.

    Visualization shows:
    - Graph nodes with states (unprocessed, ready, processing, sorted)
    - Directed edges with states (active, traversed)
    - In-degree map tracking
    - Queue state (nodes ready to process)
    - Sorted order construction

    Prediction points ask: "Which node(s) will be added to queue next?"
    """

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.adjacency_list = {}
        self.indegree_map = {}
        self.queue = deque()
        self.sorted_order = []
        self.processed_nodes = set()
        self.current_node = None

    def _get_visualization_state(self) -> dict:
        """
        Return current graph state with node/edge states and algorithm structures.

        Node states:
        - 'unprocessed': Not yet ready (in-degree > 0)
        - 'ready': In queue (in-degree = 0, not yet processed)
        - 'processing': Currently being processed
        - 'sorted': Added to sorted order

        Edge states:
        - 'active': Edge from unprocessed/ready node
        - 'traversed': Edge from sorted node
        """
        if not self.nodes:
            return {}

        return {
            'nodes': [
                {
                    'id': node,
                    'state': self._get_node_state(node),
                    'indegree': self.indegree_map.get(node, 0)
                }
                for node in self.nodes
            ],
            'edges': [
                {
                    'from': edge[0],
                    'to': edge[1],
                    'state': self._get_edge_state(edge)
                }
                for edge in self.edges
            ],
            'indegree_map': dict(self.indegree_map),
            'queue': list(self.queue),
            'sorted_order': list(self.sorted_order),
            'nodes_processed': len(self.processed_nodes)
        }

    def _get_node_state(self, node: str) -> str:
        """Determine visual state of node."""
        if node in self.processed_nodes:
            return 'sorted'
        if node == self.current_node:
            return 'processing'
        if node in self.queue:
            return 'ready'
        return 'unprocessed'

    def _get_edge_state(self, edge: tuple) -> str:
        """Determine visual state of edge."""
        from_node = edge[0]
        if from_node in self.processed_nodes:
            return 'traversed'
        return 'active'

    def generate_narrative(self, trace_result: dict) -> str:
        """
        Generate human-readable narrative from Topological Sort trace.

        Shows complete execution flow with all decision data visible.
        Includes Frontend Visualization Hints (Backend Checklist v2.2).

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
        narrative = "# Topological Sort (Kahn's Algorithm) Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Graph:** {len(self.nodes)} nodes, {len(self.edges)} edges\n"
        narrative += f"**Result:** {'✅ VALID DAG' if not result['has_cycle'] else '❌ CYCLE DETECTED'}\n"
        
        if not result['has_cycle']:
            narrative += f"**Sorted Order:** {' → '.join(result['sorted_order'])}\n"
        else:
            narrative += f"**Nodes Processed:** {result['nodes_processed']} of {len(self.nodes)}\n"
        
        narrative += "\n---\n\n"

        # Step-by-step narrative
        for step in steps:
            step_num = step['step']
            step_type = step['type']
            description = step['description']
            data = step['data']
            viz = data['visualization']

            narrative += f"## Step {step_num}: {description}\n\n"

            # Type-specific details
            if step_type == "CALC_INDEGREES":
                narrative += "**Graph Structure (Adjacency List):**\n"
                for node in sorted(self.nodes):
                    neighbors = self.adjacency_list.get(node, [])
                    if neighbors:
                        narrative += f"- **{node}** → {neighbors}\n"
                    else:
                        narrative += f"- **{node}** → (no outgoing edges)\n"
                narrative += "\n"

                narrative += "**In-Degree Calculation:**\n\n"
                narrative += "Track how many incoming edges each node has:\n\n"
                
                narrative += "| Node | Incoming Edges | In-Degree |\n"
                narrative += "|------|----------------|----------|\n"
                
                for node in sorted(self.nodes):
                    indegree = viz['indegree_map'][node]
                    incoming = [edge[0] for edge in self.edges if edge[1] == node]
                    if incoming:
                        narrative += f"| {node} | {', '.join(incoming)} | {indegree} |\n"
                    else:
                        narrative += f"| {node} | (none) | {indegree} |\n"
                
                narrative += "\n"
                narrative += "**Purpose:** Nodes with in-degree 0 have no dependencies and can be processed first.\n\n"

            elif step_type == "ENQUEUE_ZERO_INDEGREE":
                initial_nodes = data['nodes_enqueued']
                
                narrative += "**Initial Queue Setup:**\n\n"
                narrative += "Identify nodes with in-degree 0 (no dependencies):\n\n"
                
                for node in sorted(self.nodes):
                    indegree = viz['indegree_map'][node]
                    if indegree == 0:
                        narrative += f"- **{node}**: in-degree = 0 ✓ → add to queue\n"
                    else:
                        narrative += f"- **{node}**: in-degree = {indegree} → wait (has dependencies)\n"
                
                narrative += f"\n**Queue State:** {viz['queue']}\n"
                narrative += f"*{len(initial_nodes)} node(s) ready to process*\n\n"

            elif step_type == "PROCESS_NODE":
                node = data['node']
                neighbors = data['neighbors']
                
                narrative += f"**Dequeue Node:** {node}\n\n"
                narrative += f"**Queue Before:** {data['queue_before']}\n"
                narrative += f"**Queue After:** {viz['queue']}\n\n"
                
                narrative += f"**Action:** Add **{node}** to sorted order\n"
                narrative += f"**Sorted Order:** {viz['sorted_order']}\n\n"
                
                if neighbors:
                    narrative += f"**Outgoing Edges from {node}:**\n"
                    for neighbor in neighbors:
                        narrative += f"- {node} → {neighbor}\n"
                    narrative += f"\nThese edges will be \"removed\" by decrementing neighbor in-degrees.\n\n"
                else:
                    narrative += f"**Outgoing Edges:** None (leaf node)\n\n"

            elif step_type == "DECREMENT_NEIGHBOR":
                node = data['current_node']
                neighbor = data['neighbor']
                old_indegree = data['old_indegree']
                new_indegree = data['new_indegree']
                
                narrative += f"**Processing Edge:** {node} → {neighbor}\n\n"
                narrative += f"**In-Degree Update:**\n"
                narrative += f"- Current in-degree of **{neighbor}**: {old_indegree}\n"
                narrative += f"- Decrement: {old_indegree} - 1 = {new_indegree}\n"
                narrative += f"- New in-degree of **{neighbor}**: {new_indegree}\n\n"
                
                if new_indegree == 0:
                    narrative += f"**Decision:** in-degree = 0 ✓\n"
                    narrative += f"- **{neighbor}** has no remaining dependencies\n"
                    narrative += f"- Add **{neighbor}** to queue\n"
                    narrative += f"- **Queue:** {viz['queue']}\n\n"
                else:
                    narrative += f"**Decision:** in-degree = {new_indegree} (still has dependencies)\n"
                    narrative += f"- **{neighbor}** not ready yet\n"
                    narrative += f"- **Queue:** {viz['queue']} (unchanged)\n\n"
                
                narrative += "**Current In-Degree Map:**\n\n"
                narrative += "| Node | In-Degree | Status |\n"
                narrative += "|------|-----------|--------|\n"
                for n in sorted(self.nodes):
                    ind = viz['indegree_map'][n]
                    if n in viz['sorted_order']:
                        status = "✓ Sorted"
                    elif ind == 0:
                        status = "Ready"
                    else:
                        status = f"Waiting ({ind} deps)"
                    narrative += f"| {n} | {ind} | {status} |\n"
                narrative += "\n"

            elif step_type == "DETECT_CYCLE":
                nodes_processed = data['nodes_processed']
                total_nodes = data['total_nodes']
                remaining = data['remaining_nodes']
                
                narrative += "🚨 **Cycle Detection Triggered**\n\n"
                narrative += f"**Analysis:**\n"
                narrative += f"- Total nodes in graph: {total_nodes}\n"
                narrative += f"- Nodes successfully processed: {nodes_processed}\n"
                narrative += f"- Nodes remaining: {total_nodes - nodes_processed}\n\n"
                
                narrative += f"**Remaining Nodes:** {remaining}\n\n"
                
                narrative += "**In-Degrees of Remaining Nodes:**\n\n"
                narrative += "| Node | In-Degree | Explanation |\n"
                narrative += "|------|-----------|-------------|\n"
                for node in remaining:
                    indegree = viz['indegree_map'][node]
                    narrative += f"| {node} | {indegree} | Still has dependencies |\n"
                narrative += "\n"
                
                narrative += "**Conclusion:**\n"
                narrative += "- Queue is empty (no nodes with in-degree 0)\n"
                narrative += "- Remaining nodes all have in-degree > 0\n"
                narrative += "- This indicates a **cycle** in the graph\n"
                narrative += "- Topological ordering is **impossible** for graphs with cycles\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        
        if result['has_cycle']:
            narrative += "**Result:** ❌ **CYCLE DETECTED**\n\n"
            narrative += f"The graph contains a cycle, making topological ordering impossible.\n"
            narrative += f"- Nodes processed: {result['nodes_processed']} of {len(self.nodes)}\n"
            narrative += f"- Algorithm terminated early due to cycle detection\n\n"
            narrative += "**Why Cycles Prevent Topological Ordering:**\n"
            narrative += "A topological order requires that for every edge A → B, node A appears before B in the ordering. "
            narrative += "In a cycle (e.g., A → B → C → A), this is impossible because A must come before B, "
            narrative += "B before C, and C before A—a logical contradiction.\n\n"
        else:
            narrative += "**Result:** ✅ **VALID TOPOLOGICAL ORDERING**\n\n"
            narrative += f"**Sorted Order:** {' → '.join(result['sorted_order'])}\n\n"
            narrative += f"**Verification:**\n"
            narrative += f"- All {len(self.nodes)} nodes processed\n"
            narrative += f"- No cycles detected\n"
            narrative += f"- For every edge (u, v), node u appears before v in sorted order\n\n"
            
            narrative += "**Edge Verification:**\n"
            for edge in self.edges:
                from_node, to_node = edge
                from_idx = result['sorted_order'].index(from_node)
                to_idx = result['sorted_order'].index(to_node)
                narrative += f"- {from_node} → {to_node}: position {from_idx} < {to_idx} ✓\n"
            narrative += "\n"
        
        narrative += "**Algorithm Complexity:**\n"
        narrative += f"- Time: O(V + E) where V = {len(self.nodes)} nodes, E = {len(self.edges)} edges\n"
        narrative += f"- Space: O(V) for in-degree map and queue\n"
        narrative += f"- Total steps in trace: {len(steps)}\n\n"

        # Frontend Visualization Hints
        narrative += "---\n\n## 🎨 Frontend Visualization Hints\n\n"
        
        narrative += "### Primary Metrics to Emphasize\n\n"
        narrative += "- **Queue State** (`queue`) - Shows which nodes are ready to process (in-degree = 0)\n"
        narrative += "- **In-Degree Map** (`indegree_map`) - Tracks dependencies for each node\n"
        narrative += "- **Sorted Order** (`sorted_order`) - Progressive construction of topological ordering\n"
        narrative += "- **Nodes Processed** (`nodes_processed`) - Progress indicator and cycle detection metric\n\n"
        
        narrative += "### Visualization Priorities\n\n"
        narrative += "1. **Highlight the queue** - Use distinct visual treatment for nodes in `ready` state\n"
        narrative += "2. **Show in-degree changes** - Animate decrement operations when edges are \"removed\"\n"
        narrative += "3. **Build sorted order progressively** - Show nodes moving from graph to sorted list\n"
        narrative += "4. **Emphasize zero in-degree moments** - When a node's in-degree reaches 0, it's a key decision point\n"
        narrative += "5. **Cycle detection visual** - If `has_cycle` is true, highlight remaining nodes with non-zero in-degrees\n\n"
        
        narrative += "### Key JSON Paths\n\n"
        narrative += "```\n"
        narrative += "step.data.visualization.nodes[*].id\n"
        narrative += "step.data.visualization.nodes[*].state  // 'unprocessed' | 'ready' | 'processing' | 'sorted'\n"
        narrative += "step.data.visualization.nodes[*].indegree\n"
        narrative += "step.data.visualization.edges[*].from\n"
        narrative += "step.data.visualization.edges[*].to\n"
        narrative += "step.data.visualization.edges[*].state  // 'active' | 'traversed'\n"
        narrative += "step.data.visualization.indegree_map\n"
        narrative += "step.data.visualization.queue\n"
        narrative += "step.data.visualization.sorted_order\n"
        narrative += "step.data.visualization.nodes_processed\n"
        narrative += "```\n\n"
        
        narrative += "### Algorithm-Specific Guidance\n\n"
        narrative += "Kahn's algorithm is fundamentally about **dependency resolution**. The most important visualization "
        narrative += "is showing how in-degrees decrease as dependencies are satisfied. Consider using a **two-panel layout**: "
        narrative += "the graph on the left with in-degree labels on each node, and the sorted order building on the right. "
        narrative += "The queue is the \"ready list\"—nodes waiting to be processed. When a node is dequeued, show it moving "
        narrative += "from the graph to the sorted order list. The in-degree decrement operations are the heart of the algorithm: "
        narrative += "visualize these as edges \"dissolving\" or fading out. For cycle detection, the key insight is that the "
        narrative += "queue becomes empty while nodes remain—highlight these stuck nodes with their non-zero in-degrees to show "
        narrative += "why they can't be processed. The final sorted order should clearly show the dependency flow: every edge "
        narrative += "points from left to right in the ordering.\n"

        return narrative

    def execute(self, input_data: Any) -> dict:
        """
        Execute Topological Sort (Kahn's Algorithm) with trace generation.

        Args:
            input_data: dict with keys:
                - 'nodes': List[str] - Node identifiers
                - 'edges': List[Tuple[str, str]] - Directed edges (from, to)

        Returns:
            Standardized trace result with:
                - result: {
                    'sorted_order': List[str],
                    'has_cycle': bool,
                    'nodes_processed': int
                  }
                - trace: Complete step-by-step execution
                - metadata: Includes visualization_type='graph'

        Raises:
            ValueError: If input is invalid or nodes exceed max_nodes constraint
        """
        # Validate input
        if not isinstance(input_data, dict):
            raise ValueError("Input must be a dictionary")
        if 'nodes' not in input_data or 'edges' not in input_data:
            raise ValueError("Input must contain 'nodes' and 'edges' keys")

        self.nodes = input_data['nodes']
        self.edges = input_data['edges']

        if not self.nodes:
            raise ValueError("Nodes list cannot be empty")
        
        if len(self.nodes) > 10:
            raise ValueError("Maximum 10 nodes allowed")

        # Validate edges reference valid nodes
        node_set = set(self.nodes)
        for edge in self.edges:
            if len(edge) != 2:
                raise ValueError(f"Invalid edge format: {edge}")
            from_node, to_node = edge
            if from_node not in node_set:
                raise ValueError(f"Edge references unknown node: {from_node}")
            if to_node not in node_set:
                raise ValueError(f"Edge references unknown node: {to_node}")

        # Initialize data structures
        self.adjacency_list = defaultdict(list)
        self.indegree_map = {node: 0 for node in self.nodes}
        self.queue = deque()
        self.sorted_order = []
        self.processed_nodes = set()
        self.current_node = None

        # Build adjacency list
        for from_node, to_node in self.edges:
            self.adjacency_list[from_node].append(to_node)

        # Set metadata
        self.metadata = {
            'algorithm': 'topological-sort',
            'display_name': 'Topological Sort (Kahn\'s Algorithm)',
            'visualization_type': 'graph',
            'visualization_config': {
                'directed': True,
                'show_indegrees': True,
                'show_queue': True
            },
            'input_size': len(self.nodes),
            'edge_count': len(self.edges)
        }

        # Step 1: Calculate in-degrees
        for from_node, to_node in self.edges:
            self.indegree_map[to_node] += 1

        self._add_step(
            "CALC_INDEGREES",
            {
                'indegree_calculation': dict(self.indegree_map)
            },
            "📊 Calculate in-degrees for all nodes"
        )

        # Step 2: Enqueue all nodes with in-degree 0
        initial_zero_indegree = []
        for node in self.nodes:
            if self.indegree_map[node] == 0:
                self.queue.append(node)
                initial_zero_indegree.append(node)

        self._add_step(
            "ENQUEUE_ZERO_INDEGREE",
            {
                'nodes_enqueued': initial_zero_indegree,
                'queue_size': len(self.queue)
            },
            f"🎯 Enqueue {len(initial_zero_indegree)} node(s) with in-degree 0"
        )

        # Step 3: Process queue (BFS)
        while self.queue:
            # Dequeue node
            queue_before = list(self.queue)
            self.current_node = self.queue.popleft()
            node = self.current_node
            
            # Add to sorted order
            self.sorted_order.append(node)
            self.processed_nodes.add(node)
            
            neighbors = self.adjacency_list.get(node, [])
            
            self._add_step(
                "PROCESS_NODE",
                {
                    'node': node,
                    'neighbors': neighbors,
                    'queue_before': queue_before,
                    'position_in_order': len(self.sorted_order)
                },
                f"⚙️ Process node {node} (add to sorted order)"
            )

            # Process neighbors: decrement in-degrees
            for neighbor in neighbors:
                old_indegree = self.indegree_map[neighbor]
                self.indegree_map[neighbor] -= 1
                new_indegree = self.indegree_map[neighbor]
                
                # If in-degree becomes 0, enqueue
                if new_indegree == 0:
                    self.queue.append(neighbor)
                
                self._add_step(
                    "DECREMENT_NEIGHBOR",
                    {
                        'current_node': node,
                        'neighbor': neighbor,
                        'old_indegree': old_indegree,
                        'new_indegree': new_indegree,
                        'enqueued': new_indegree == 0
                    },
                    f"➖ Decrement in-degree of {neighbor}: {old_indegree} → {new_indegree}"
                )

            self.current_node = None

        # Step 4: Check for cycle
        has_cycle = len(self.sorted_order) < len(self.nodes)
        
        if has_cycle:
            remaining_nodes = [n for n in self.nodes if n not in self.processed_nodes]
            
            self._add_step(
                "DETECT_CYCLE",
                {
                    'nodes_processed': len(self.sorted_order),
                    'total_nodes': len(self.nodes),
                    'remaining_nodes': remaining_nodes,
                    'has_cycle': True
                },
                f"🚨 Cycle detected: {len(remaining_nodes)} node(s) unprocessed"
            )

        return self._build_trace_result({
            'sorted_order': self.sorted_order,
            'has_cycle': has_cycle,
            'nodes_processed': len(self.sorted_order)
        })

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction opportunities for active learning.

        Students predict: "After processing a node and decrementing neighbor in-degrees,
        which node(s) will be added to the queue next?"

        Returns:
            List of prediction points with question, choices, and correct answer
        """
        predictions = []

        for i, step in enumerate(self.trace):
            # Prediction opportunity: After PROCESS_NODE, before DECREMENT_NEIGHBOR
            if step.type == "PROCESS_NODE" and i + 1 < len(self.trace):
                node = step.data['node']
                neighbors = step.data['neighbors']
                
                if not neighbors:
                    continue  # No neighbors to decrement, skip prediction
                
                # Look ahead to find which neighbors get enqueued
                enqueued_neighbors = []
                j = i + 1
                while j < len(self.trace) and self.trace[j].type == "DECREMENT_NEIGHBOR":
                    if self.trace[j].data.get('enqueued', False):
                        enqueued_neighbors.append(self.trace[j].data['neighbor'])
                    j += 1
                
                # Build choices (max 3)
                choices = []
                
                # Choice 1: Correct answer
                if enqueued_neighbors:
                    correct_label = ', '.join(enqueued_neighbors)
                    choices.append({
                        'id': 'correct',
                        'label': f"{correct_label}"
                    })
                    correct_answer = 'correct'
                else:
                    choices.append({
                        'id': 'none',
                        'label': "None (all neighbors still have dependencies)"
                    })
                    correct_answer = 'none'
                
                # Choice 2: All neighbors
                if len(neighbors) > 1 and len(enqueued_neighbors) != len(neighbors):
                    choices.append({
                        'id': 'all',
                        'label': f"All neighbors: {', '.join(neighbors)}"
                    })
                
                # Choice 3: Wrong subset or none
                if enqueued_neighbors and len(neighbors) > len(enqueued_neighbors):
                    wrong_neighbors = [n for n in neighbors if n not in enqueued_neighbors]
                    if wrong_neighbors:
                        choices.append({
                            'id': 'wrong',
                            'label': f"{wrong_neighbors[0]}"
                        })
                elif not enqueued_neighbors and neighbors:
                    choices.append({
                        'id': 'wrong',
                        'label': f"{neighbors[0]}"
                    })
                
                # Ensure exactly 3 choices (pad if needed)
                while len(choices) < 3:
                    choices.append({
                        'id': f'filler_{len(choices)}',
                        'label': "No additional nodes"
                    })
                
                # Limit to 3 choices
                choices = choices[:3]
                
                predictions.append({
                    'step_index': i,
                    'question': f"After processing node {node}, which neighbor(s) will become ready (in-degree = 0)?",
                    'choices': choices,
                    'hint': f"Check which neighbors of {node} will have in-degree decremented to 0",
                    'correct_answer': correct_answer,
                    'explanation': self._get_prediction_explanation(node, neighbors, enqueued_neighbors)
                })

        return predictions

    def _get_prediction_explanation(self, node: str, neighbors: List[str], enqueued: List[str]) -> str:
        """Generate explanation for prediction answer."""
        if not enqueued:
            return f"After processing {node}, all neighbors still have in-degree > 0, so none are ready yet."
        elif len(enqueued) == 1:
            return f"After processing {node}, neighbor {enqueued[0]} reaches in-degree 0 and becomes ready."
        else:
            return f"After processing {node}, neighbors {', '.join(enqueued)} all reach in-degree 0 and become ready."
