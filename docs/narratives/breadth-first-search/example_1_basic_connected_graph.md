# Breadth-First Search Execution Narrative

**Algorithm:** Breadth-First Search
**Start Node:** A
**Graph Size:** 6 nodes, 5 edges
**Traversal Order:** A → B → C → D → E → F
**Total Nodes Visited:** 6

---

## Step 0: 🔍 Initialize BFS from start node A

**Graph Structure (Adjacency List):**

| Node | Neighbors |
|------|----------|
| A | B, C |
| B | A, D, E |
| C | A, F |
| D | B |
| E | B |
| F | C |

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

## Step 4: 🔍 Process neighbors of A: 2 new, 0 already seen

**Multi-Element Filtering: Process Neighbors of A**

**Step 1 - Full Neighbor List:**
- Node **A** has neighbors: **['B', 'C']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **B**: unvisited → enqueue (new discovery)
- **C**: unvisited → enqueue (new discovery)

**Step 4 - Filtered Result:**
- Neighbors to enqueue: **['B', 'C']**
- Count: **2** new node(s) added to queue

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

## Step 6: ➕ Enqueue neighbor C at level 1

**Action:** Add node **C** to queue

**Level Assignment:**
- Node **C** is at level **1** (distance 1 from start)

**Queue State:**
```
Front → ['B', 'C'] ← Back
```
*Queue now contains **2** node(s) waiting to be processed*

**Enqueued nodes:** B, C

---

## Step 7: ⬅️ Dequeue node B from front (level 1)

**Action:** Remove node **B** from front of queue

**Processing:**
- Current node: **B**
- Current level: **1**
- Traversal position: #2

**Queue State After Dequeue:**
```
Front → ['C'] ← Back
```
*Queue now contains **1** node(s)*

---

## Step 8: ✅ Visit node B (position #2 in traversal)

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

## Step 9: 🔍 Process neighbors of B: 2 new, 1 already seen

**Multi-Element Filtering: Process Neighbors of B**

**Step 1 - Full Neighbor List:**
- Node **B** has neighbors: **['A', 'D', 'E']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A, B}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **A**: visited ✓ → skip (already processed)
- **D**: unvisited → enqueue (new discovery)
- **E**: unvisited → enqueue (new discovery)

**Step 4 - Filtered Result:**
- Neighbors to enqueue: **['D', 'E']**
- Count: **2** new node(s) added to queue

**Updated Queue:**
```
Front → ['C'] ← Back
```

---

## Step 10: ➕ Enqueue neighbor D at level 2

**Action:** Add node **D** to queue

**Level Assignment:**
- Node **D** is at level **2** (distance 2 from start)

**Queue State:**
```
Front → ['C', 'D'] ← Back
```
*Queue now contains **2** node(s) waiting to be processed*

**Enqueued nodes:** C, D

---

## Step 11: ➕ Enqueue neighbor E at level 2

**Action:** Add node **E** to queue

**Level Assignment:**
- Node **E** is at level **2** (distance 2 from start)

**Queue State:**
```
Front → ['C', 'D', 'E'] ← Back
```
*Queue now contains **3** node(s) waiting to be processed*

**Enqueued nodes:** C, D, E

---

## Step 12: ⬅️ Dequeue node C from front (level 1)

**Action:** Remove node **C** from front of queue

**Processing:**
- Current node: **C**
- Current level: **1**
- Traversal position: #3

**Queue State After Dequeue:**
```
Front → ['D', 'E'] ← Back
```
*Queue now contains **2** node(s)*

---

## Step 13: ✅ Visit node C (position #3 in traversal)

**Mark Visited:** Node **C** is now fully processed

**Visited Set:**
```
{A, B, C}
```
*Total visited: **3** nodes*

**Traversal Progress:**
```
A → B → C
```

---

## Step 14: 🔍 Process neighbors of C: 1 new, 1 already seen

**Multi-Element Filtering: Process Neighbors of C**

**Step 1 - Full Neighbor List:**
- Node **C** has neighbors: **['A', 'F']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A, B, C}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **A**: visited ✓ → skip (already processed)
- **F**: unvisited → enqueue (new discovery)

**Step 4 - Filtered Result:**
- Neighbors to enqueue: **['F']**
- Count: **1** new node(s) added to queue

**Updated Queue:**
```
Front → ['D', 'E'] ← Back
```

---

## Step 15: ➕ Enqueue neighbor F at level 2

**Action:** Add node **F** to queue

**Level Assignment:**
- Node **F** is at level **2** (distance 2 from start)

**Queue State:**
```
Front → ['D', 'E', 'F'] ← Back
```
*Queue now contains **3** node(s) waiting to be processed*

**Enqueued nodes:** D, E, F

---

## Step 16: ⬅️ Dequeue node D from front (level 2)

**Action:** Remove node **D** from front of queue

**Processing:**
- Current node: **D**
- Current level: **2**
- Traversal position: #4

**Queue State After Dequeue:**
```
Front → ['E', 'F'] ← Back
```
*Queue now contains **2** node(s)*

---

## Step 17: ✅ Visit node D (position #4 in traversal)

**Mark Visited:** Node **D** is now fully processed

**Visited Set:**
```
{A, B, C, D}
```
*Total visited: **4** nodes*

**Traversal Progress:**
```
A → B → C → D
```

---

## Step 18: 🔍 Process neighbors of D: 0 new, 1 already seen

**Multi-Element Filtering: Process Neighbors of D**

**Step 1 - Full Neighbor List:**
- Node **D** has neighbors: **['B']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A, B, C, D}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **B**: visited ✓ → skip (already processed)

**Step 4 - Filtered Result:**
- No new neighbors to enqueue (all already visited)

**Updated Queue:**
```
Front → ['E', 'F'] ← Back
```

---

## Step 19: ⬅️ Dequeue node E from front (level 2)

**Action:** Remove node **E** from front of queue

**Processing:**
- Current node: **E**
- Current level: **2**
- Traversal position: #5

**Queue State After Dequeue:**
```
Front → ['F'] ← Back
```
*Queue now contains **1** node(s)*

---

## Step 20: ✅ Visit node E (position #5 in traversal)

**Mark Visited:** Node **E** is now fully processed

**Visited Set:**
```
{A, B, C, D, E}
```
*Total visited: **5** nodes*

**Traversal Progress:**
```
A → B → C → D → E
```

---

## Step 21: 🔍 Process neighbors of E: 0 new, 1 already seen

**Multi-Element Filtering: Process Neighbors of E**

**Step 1 - Full Neighbor List:**
- Node **E** has neighbors: **['B']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A, B, C, D, E}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **B**: visited ✓ → skip (already processed)

**Step 4 - Filtered Result:**
- No new neighbors to enqueue (all already visited)

**Updated Queue:**
```
Front → ['F'] ← Back
```

---

## Step 22: ⬅️ Dequeue node F from front (level 2)

**Action:** Remove node **F** from front of queue

**Processing:**
- Current node: **F**
- Current level: **2**
- Traversal position: #6

**Queue State After Dequeue:**
```
(empty)
```
*Queue is now empty*

---

## Step 23: ✅ Visit node F (position #6 in traversal)

**Mark Visited:** Node **F** is now fully processed

**Visited Set:**
```
{A, B, C, D, E, F}
```
*Total visited: **6** nodes*

**Traversal Progress:**
```
A → B → C → D → E → F
```

---

## Step 24: 🔍 Process neighbors of F: 0 new, 1 already seen

**Multi-Element Filtering: Process Neighbors of F**

**Step 1 - Full Neighbor List:**
- Node **F** has neighbors: **['C']**

**Step 2 - Filter Criteria:**
- Check against visited set: `{A, B, C, D, E, F}`
- Rule: Only enqueue **unvisited** neighbors

**Step 3 - Explicit Neighbor Checks:**
- **C**: visited ✓ → skip (already processed)

**Step 4 - Filtered Result:**
- No new neighbors to enqueue (all already visited)

---

## Step 25: 🏁 BFS complete: visited 6 out of 6 nodes

**BFS Traversal Complete**

**Final Statistics:**
- Nodes visited: **6** out of **6**
- Queue state: Empty (all reachable nodes processed)

**Final Traversal Order:**
```
A → B → C → D → E → F
```

**Level Distribution:**
- Level 0: 1 node(s)
- Level 1: 2 node(s)
- Level 2: 3 node(s)

---

## Execution Summary

**Traversal Result:**
- Start node: **A**
- Nodes visited: **6** out of **6**
- Traversal order: A → B → C → D → E → F

**Level Assignments:**
- Node **A**: Level 0
- Node **B**: Level 1
- Node **C**: Level 1
- Node **D**: Level 2
- Node **E**: Level 2
- Node **F**: Level 2

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
