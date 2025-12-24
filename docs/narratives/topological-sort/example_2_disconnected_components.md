# Topological Sort (Kahn's Algorithm) Execution Narrative

**Algorithm:** Topological Sort (Kahn's Algorithm)
**Graph:** 4 nodes, 2 edges
**Result:** ✅ VALID DAG
**Sorted Order:** A → C → B → D

---

## Step 0: 📊 Calculate in-degrees for all nodes

**Graph Structure (Adjacency List):**
- **A** → ['B']
- **B** → (no outgoing edges)
- **C** → ['D']
- **D** → (no outgoing edges)

**In-Degree Calculation:**

Track how many incoming edges each node has:

| Node | Incoming Edges | In-Degree |
|------|----------------|----------|
| A | (none) | 0 |
| B | A | 1 |
| C | (none) | 0 |
| D | C | 1 |

**Purpose:** Nodes with in-degree 0 have no dependencies and can be processed first.

---

## Step 1: 🎯 Enqueue 2 node(s) with in-degree 0

**Initial Queue Setup:**

Identify nodes with in-degree 0 (no dependencies):

- **A**: in-degree = 0 ✓ → add to queue
- **B**: in-degree = 1 → wait (has dependencies)
- **C**: in-degree = 0 ✓ → add to queue
- **D**: in-degree = 1 → wait (has dependencies)

**Queue State:** ['A', 'C']
*2 node(s) ready to process*

---

## Step 2: ⚙️ Process node A (add to sorted order)

**Dequeue Node:** A

**Queue Before:** ['A', 'C']
**Queue After:** ['C']

**Action:** Add **A** to sorted order
**Sorted Order:** ['A']

**Outgoing Edges from A:**
- A → B

These edges will be "removed" by decrementing neighbor in-degrees.

---

## Step 3: ➖ Decrement in-degree of B: 1 → 0

**Processing Edge:** A → B

**In-Degree Update:**
- Current in-degree of **B**: 1
- Decrement: 1 - 1 = 0
- New in-degree of **B**: 0

**Decision:** in-degree = 0 ✓
- **B** has no remaining dependencies
- Add **B** to queue
- **Queue:** ['C', 'B']

**Current In-Degree Map:**

| Node | In-Degree | Status |
|------|-----------|--------|
| A | 0 | ✓ Sorted |
| B | 0 | Ready |
| C | 0 | Ready |
| D | 1 | Waiting (1 deps) |

---

## Step 4: ⚙️ Process node C (add to sorted order)

**Dequeue Node:** C

**Queue Before:** ['C', 'B']
**Queue After:** ['B']

**Action:** Add **C** to sorted order
**Sorted Order:** ['A', 'C']

**Outgoing Edges from C:**
- C → D

These edges will be "removed" by decrementing neighbor in-degrees.

---

## Step 5: ➖ Decrement in-degree of D: 1 → 0

**Processing Edge:** C → D

**In-Degree Update:**
- Current in-degree of **D**: 1
- Decrement: 1 - 1 = 0
- New in-degree of **D**: 0

**Decision:** in-degree = 0 ✓
- **D** has no remaining dependencies
- Add **D** to queue
- **Queue:** ['B', 'D']

**Current In-Degree Map:**

| Node | In-Degree | Status |
|------|-----------|--------|
| A | 0 | ✓ Sorted |
| B | 0 | Ready |
| C | 0 | ✓ Sorted |
| D | 0 | Ready |

---

## Step 6: ⚙️ Process node B (add to sorted order)

**Dequeue Node:** B

**Queue Before:** ['B', 'D']
**Queue After:** ['D']

**Action:** Add **B** to sorted order
**Sorted Order:** ['A', 'C', 'B']

**Outgoing Edges:** None (leaf node)

---

## Step 7: ⚙️ Process node D (add to sorted order)

**Dequeue Node:** D

**Queue Before:** ['D']
**Queue After:** []

**Action:** Add **D** to sorted order
**Sorted Order:** ['A', 'C', 'B', 'D']

**Outgoing Edges:** None (leaf node)

---

## Execution Summary

**Result:** ✅ **VALID TOPOLOGICAL ORDERING**

**Sorted Order:** A → C → B → D

**Verification:**
- All 4 nodes processed
- No cycles detected
- For every edge (u, v), node u appears before v in sorted order

**Edge Verification:**
- A → B: position 0 < 2 ✓
- C → D: position 1 < 3 ✓

**Algorithm Complexity:**
- Time: O(V + E) where V = 4 nodes, E = 2 edges
- Space: O(V) for in-degree map and queue
- Total steps in trace: 8

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
