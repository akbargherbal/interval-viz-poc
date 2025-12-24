# Topological Sort (Kahn's Algorithm) Execution Narrative

**Algorithm:** Topological Sort (Kahn's Algorithm)
**Graph:** 3 nodes, 3 edges
**Result:** ❌ CYCLE DETECTED
**Nodes Processed:** 0 of 3

---

## Step 0: 📊 Calculate in-degrees for all nodes

**Graph Structure (Adjacency List):**
- **A** → ['B']
- **B** → ['C']
- **C** → ['A']

**In-Degree Calculation:**

Track how many incoming edges each node has:

| Node | Incoming Edges | In-Degree |
|------|----------------|----------|
| A | C | 1 |
| B | A | 1 |
| C | B | 1 |

**Purpose:** Nodes with in-degree 0 have no dependencies and can be processed first.

---

## Step 1: 🎯 Enqueue 0 node(s) with in-degree 0

**Initial Queue Setup:**

Identify nodes with in-degree 0 (no dependencies):

- **A**: in-degree = 1 → wait (has dependencies)
- **B**: in-degree = 1 → wait (has dependencies)
- **C**: in-degree = 1 → wait (has dependencies)

**Queue State:** []
*0 node(s) ready to process*

---

## Step 2: 🚨 Cycle detected: 3 node(s) unprocessed

🚨 **Cycle Detection Triggered**

**Analysis:**
- Total nodes in graph: 3
- Nodes successfully processed: 0
- Nodes remaining: 3

**Remaining Nodes:** ['A', 'B', 'C']

**In-Degrees of Remaining Nodes:**

| Node | In-Degree | Explanation |
|------|-----------|-------------|
| A | 1 | Still has dependencies |
| B | 1 | Still has dependencies |
| C | 1 | Still has dependencies |

**Conclusion:**
- Queue is empty (no nodes with in-degree 0)
- Remaining nodes all have in-degree > 0
- This indicates a **cycle** in the graph
- Topological ordering is **impossible** for graphs with cycles

---

## Execution Summary

**Result:** ❌ **CYCLE DETECTED**

The graph contains a cycle, making topological ordering impossible.
- Nodes processed: 0 of 3
- Algorithm terminated early due to cycle detection

**Why Cycles Prevent Topological Ordering:**
A topological order requires that for every edge A → B, node A appears before B in the ordering. In a cycle (e.g., A → B → C → A), this is impossible because A must come before B, B before C, and C before A—a logical contradiction.

**Algorithm Complexity:**
- Time: O(V + E) where V = 3 nodes, E = 3 edges
- Space: O(V) for in-degree map and queue
- Total steps in trace: 3

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Queue State** (`queue`) - Shows which nodes are ready to process (in-degree = 0)
- **In-Degree Map** (`indegree_map`) - Tracks dependencies for each node
- **Sorted Order** (`sorted_order`) - Progressive construction of topological ordering
- **Nodes Processed** (`nodes_processed`) - Progress indicator and cycle detection metric

### Visualization Priorities

1. **Highlight the queue** - Use distinct visual treatment for nodes in `ready` state
2. **Show in-degree changes** - Animate decrement operations when edges are "removed"
3. **Build sorted order progressively** - Show nodes moving from graph to sorted list
4. **Emphasize zero in-degree moments** - When a node's in-degree reaches 0, it's a key decision point
5. **Cycle detection visual** - If `has_cycle` is true, highlight remaining nodes with non-zero in-degrees

### Key JSON Paths

```
step.data.visualization.nodes[*].id
step.data.visualization.nodes[*].state  // 'unprocessed' | 'ready' | 'processing' | 'sorted'
step.data.visualization.nodes[*].indegree
step.data.visualization.edges[*].from
step.data.visualization.edges[*].to
step.data.visualization.edges[*].state  // 'active' | 'traversed'
step.data.visualization.indegree_map
step.data.visualization.queue
step.data.visualization.sorted_order
step.data.visualization.nodes_processed
```

### Algorithm-Specific Guidance

Kahn's algorithm is fundamentally about **dependency resolution**. The most important visualization is showing how in-degrees decrease as dependencies are satisfied. Consider using a **two-panel layout**: the graph on the left with in-degree labels on each node, and the sorted order building on the right. The queue is the "ready list"—nodes waiting to be processed. When a node is dequeued, show it moving from the graph to the sorted order list. The in-degree decrement operations are the heart of the algorithm: visualize these as edges "dissolving" or fading out. For cycle detection, the key insight is that the queue becomes empty while nodes remain—highlight these stuck nodes with their non-zero in-degrees to show why they can't be processed. The final sorted order should clearly show the dependency flow: every edge points from left to right in the ordering.
