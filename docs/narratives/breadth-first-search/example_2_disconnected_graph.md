# Breadth-First Search Execution Narrative

**Algorithm:** Breadth-First Search
**Start Node:** A
**Graph Size:** 4 nodes, 2 edges
**Traversal Order:** A → B
**Total Nodes Visited:** 2

---

## Step 0: 🔍 Initialize BFS from start node A

**Graph Structure (Adjacency List):**

| Node | Neighbors |
|------|----------|
| A | B |
| B | A |
| C | D |
| D | C |

**Initial Configuration:**
- Start node: **A**
- Queue: Empty `[]`
- Visited set: Empty `{}`
- All nodes marked as **unvisited**

*BFS explores nodes level by level, visiting all neighbors at distance d before moving to distance d+1.*

---

## Step 1: ➕ Enqueue start node A at level 0

**Action:** Add node **A** to queue

**Level Assignment:**
- Node **A** is at level **0** (distance 0 from start)

**Queue State:**
```
Front → ['A'] ← Back
```
*Queue now contains **1** node(s) waiting to be processed*

**Enqueued nodes:** A

---

## Step 2: ⬅️ Dequeue node A from front (level 0)

**Action:** Remove node **A** from front of queue

**Processing:**
- Current node: **A**
- Current level: **0**
- Traversal position: #1

**Queue State After Dequeue:**
```
(empty)
```
*Queue is now empty*

---

## Step 3: ✅ Visit node A (position #1 in traversal)

**Mark Visited:** Node **A** is now fully processed

**Visited Set:**
```
{A}
```
*Total visited: **1** nodes*

**Traversal Progress:**
```
A
```

---

## Step 4: 🔍 Process neighbors of A: 1 new, 0 already seen

**Multi-Element Filtering: Process Neighbors of A**

**Step 1 - Full Neighbor List:**
- Node **A** has neighbors: **['B']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **B**: unvisited → enqueue (new discovery)

**Step 4 - Filtered Result:**
- Neighbors to enqueue: **['B']**
- Count: **1** new node(s) added to queue

---

## Step 5: ➕ Enqueue neighbor B at level 1

**Action:** Add node **B** to queue

**Level Assignment:**
- Node **B** is at level **1** (distance 1 from start)

**Queue State:**
```
Front → ['B'] ← Back
```
*Queue now contains **1** node(s) waiting to be processed*

**Enqueued nodes:** B

---

## Step 6: ⬅️ Dequeue node B from front (level 1)

**Action:** Remove node **B** from front of queue

**Processing:**
- Current node: **B**
- Current level: **1**
- Traversal position: #2

**Queue State After Dequeue:**
```
(empty)
```
*Queue is now empty*

---

## Step 7: ✅ Visit node B (position #2 in traversal)

**Mark Visited:** Node **B** is now fully processed

**Visited Set:**
```
{A, B}
```
*Total visited: **2** nodes*

**Traversal Progress:**
```
A → B
```

---

## Step 8: 🔍 Process neighbors of B: 0 new, 1 already seen

**Multi-Element Filtering: Process Neighbors of B**

**Step 1 - Full Neighbor List:**
- Node **B** has neighbors: **['A']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A, B}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **A**: visited ✓ → skip (already processed)

**Step 4 - Filtered Result:**
- No new neighbors to enqueue (all already visited)

---

## Step 9: 🏁 BFS complete: visited 2 out of 4 nodes

**BFS Traversal Complete**

**Final Statistics:**
- Nodes visited: **2** out of **4**
- Queue state: Empty (all reachable nodes processed)

⚠️ **Note:** 2 node(s) remain unvisited (disconnected component)

**Final Traversal Order:**
```
A → B
```

**Level Distribution:**
- Level 0: 1 node(s)
- Level 1: 1 node(s)

---

## Execution Summary

**Traversal Result:**
- Start node: **A**
- Nodes visited: **2** out of **4**
- Traversal order: A → B

**Level Assignments:**
- Node **A**: Level 0
- Node **B**: Level 1

**Algorithm Properties:**
- Time Complexity: O(V + E) where V = vertices, E = edges
- Space Complexity: O(V) for queue and visited set
- Guarantees: Finds shortest path (in terms of edge count) from start to all reachable nodes
- Traversal Pattern: Level-order (all nodes at distance d before distance d+1)

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Queue Contents** (`queue`) - Shows the frontier of exploration, critical for understanding BFS's level-order nature
- **Current Level** (`current_level`) - Demonstrates how BFS explores all nodes at distance d before moving to d+1
- **Traversal Order** (`traversal_order`) - Shows the sequence of node discovery, proving level-order exploration

### Visualization Priorities

1. **Animate queue operations** - Show enqueue (add to back) and dequeue (remove from front) with clear directional flow
2. **Highlight level boundaries** - Use distinct colors or visual grouping for nodes at the same level
3. **Emphasize the visiting node** - The `visiting` state is the active exploration moment
4. **Show neighbor filtering** - When processing neighbors, visually distinguish already-visited vs. newly-discovered
5. **Track traversal progress** - Display the growing traversal order sequence prominently

### Key JSON Paths

```
step.data.visualization.nodes[*].id
step.data.visualization.nodes[*].state  // 'unvisited' | 'enqueued' | 'visiting' | 'visited'
step.data.visualization.nodes[*].level
step.data.visualization.edges[*].from
step.data.visualization.edges[*].to
step.data.visualization.edges[*].state  // 'unexplored' | 'exploring' | 'traversed'
step.data.visualization.queue  // Array showing front → back order
step.data.visualization.visited  // Set of fully processed nodes
step.data.visualization.current_level
step.data.visualization.traversal_order  // Growing sequence of visited nodes
```

### Algorithm-Specific Guidance

BFS's defining characteristic is **level-order traversal** - it explores all neighbors at distance d before moving to distance d+1. The queue is the heart of this behavior: nodes are added to the back (enqueue) and removed from the front (dequeue), creating FIFO ordering. Visualize the queue as a **horizontal pipeline** with clear front/back indicators. When a node is dequeued and becomes `visiting`, show its neighbors being examined - some will be skipped (already visited), others will be enqueued (new discoveries). Use **level-based coloring** or **concentric rings** to show nodes at the same distance from the start. The traversal order sequence should be prominently displayed, growing with each VISIT_NODE step. For disconnected graphs, clearly indicate when nodes remain unvisited after the queue empties. BFS guarantees shortest paths (by edge count), so emphasize how the level assignments represent minimum distances from the start node.
