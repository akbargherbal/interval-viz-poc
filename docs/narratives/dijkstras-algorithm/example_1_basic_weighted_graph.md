# Dijkstra's Algorithm Execution Narrative

**Algorithm:** Dijkstra's Algorithm
**Start Node:** A
**Graph Size:** 5 nodes
**Total Steps:** 39

---

## Step 0: 🎯 Initialize: Set distance to start node 'A' = 0, all others = ∞

**Purpose:** Initialize distance tracking for shortest path computation.

**Graph Structure (Adjacency List):**
- **A**: [B (weight: 4), C (weight: 2)]
- **B**: [A (weight: 4), C (weight: 1), D (weight: 5)]
- **C**: [A (weight: 2), B (weight: 1), D (weight: 8), E (weight: 10)]
- **D**: [B (weight: 5), C (weight: 8), E (weight: 2)]
- **E**: [C (weight: 10), D (weight: 2)]

**Initial Distances:**
- Start node **A**: distance = **0** (starting point)
- All other nodes: distance = **∞** (unreachable until proven otherwise)

**Initial Priority Queue:**
- Insert (A, 0) - start node with distance 0
- Queue state: `[(0, 'A')]` ← (0, 'A') has highest priority (smallest distance)

**Tracking Structures:**
- **Distance map** (`distances`): Tracks shortest known distance to each node
- **Previous map** (`previous`): Tracks previous node in shortest path (for path reconstruction)
- **Visited set**: Tracks nodes with finalized shortest distances

---

## Step 1: 📍 Select node 'A' with minimum distance 0 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(0, 'A')]`
- Extract minimum: **(distance: 0, node: 'A')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **A** as visited (distance is now finalized)
- Explore all neighbors of **A** to potentially improve their distances

---

## Step 2: 🔍 Visit node 'A' (distance: 0) - checking 2 neighbor(s)

**Current Node:** **A** (distance from start: **0**)

**Neighbors to Check:**
Node **A** has neighbors: **['B', 'C']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **A** is shorter than current known distance

---

## Step 3: 🔗 Check edge 'A' → 'B' (weight: 4)

**Examining Edge:** **A** → **B** (weight: **4**)

**Filter Check:** Is **B** visited?
- **B** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 4: ⚖️ Relax edge: 0 + 4 = 4 vs current None

**Edge Relaxation:** Attempt to improve distance to **B**

**Calculation:**
- Current distance to **A**: **0**
- Edge weight **A** → **B**: **4**
- Potential new distance: 0 + 4 = **4**

**Comparison:**
- Current distance to **B**: **None**
- Compare: 4 < None?

**Result:** 4 < None ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[B]` = **4** (was None)
2. Update `previous[B]` = **'A'** (track path)
3. Insert (4, 'B') into priority queue

---

## Step 5: ✅ Update: distance['B'] = 4 (via 'A')

**Distance Update Confirmed:**
- Node: **B**
- Old distance: **None**
- New distance: **4** (via **A**)
- Path tracking: `previous[B]` = **'A'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B | 4 | A |
| C | ∞ | null |
| D | ∞ | null |
| E | ∞ | null |

---

## Step 6: 🔗 Check edge 'A' → 'C' (weight: 2)

**Examining Edge:** **A** → **C** (weight: **2**)

**Filter Check:** Is **C** visited?
- **C** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 7: ⚖️ Relax edge: 0 + 2 = 2 vs current None

**Edge Relaxation:** Attempt to improve distance to **C**

**Calculation:**
- Current distance to **A**: **0**
- Edge weight **A** → **C**: **2**
- Potential new distance: 0 + 2 = **2**

**Comparison:**
- Current distance to **C**: **None**
- Compare: 2 < None?

**Result:** 2 < None ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[C]` = **2** (was None)
2. Update `previous[C]` = **'A'** (track path)
3. Insert (2, 'C') into priority queue

---

## Step 8: ✅ Update: distance['C'] = 2 (via 'A')

**Distance Update Confirmed:**
- Node: **C**
- Old distance: **None**
- New distance: **2** (via **A**)
- Path tracking: `previous[C]` = **'A'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B | 4 | A |
| C | 2 | A |
| D | ∞ | null |
| E | ∞ | null |

---

## Step 9: 📍 Select node 'C' with minimum distance 2 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(2, 'C'), (4, 'B')]`
- Extract minimum: **(distance: 2, node: 'C')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **C** as visited (distance is now finalized)
- Explore all neighbors of **C** to potentially improve their distances

**Visited Set:** {A}

---

## Step 10: 🔍 Visit node 'C' (distance: 2) - checking 4 neighbor(s)

**Current Node:** **C** (distance from start: **2**)

**Neighbors to Check:**
Node **C** has neighbors: **['A', 'B', 'D', 'E']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **C** is shorter than current known distance

---

## Step 11: 🔗 Check edge 'C' → 'A' (weight: 2)

**Examining Edge:** **C** → **A** (weight: **2**)

**Filter Check:** Is **A** visited?
- **A** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 12: 🔗 Check edge 'C' → 'B' (weight: 1)

**Examining Edge:** **C** → **B** (weight: **1**)

**Filter Check:** Is **B** visited?
- **B** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 13: ⚖️ Relax edge: 2 + 1 = 3 vs current 4

**Edge Relaxation:** Attempt to improve distance to **B**

**Calculation:**
- Current distance to **C**: **2**
- Edge weight **C** → **B**: **1**
- Potential new distance: 2 + 1 = **3**

**Comparison:**
- Current distance to **B**: **4**
- Compare: 3 < 4?

**Result:** 3 < 4 ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[B]` = **3** (was 4)
2. Update `previous[B]` = **'C'** (track path)
3. Insert (3, 'B') into priority queue

---

## Step 14: ✅ Update: distance['B'] = 3 (via 'C')

**Distance Update Confirmed:**
- Node: **B**
- Old distance: **4**
- New distance: **3** (via **C**)
- Path tracking: `previous[B]` = **'C'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B | 3 | C |
| C ✓ | 2 | A |
| D | ∞ | null |
| E | ∞ | null |

---

## Step 15: 🔗 Check edge 'C' → 'D' (weight: 8)

**Examining Edge:** **C** → **D** (weight: **8**)

**Filter Check:** Is **D** visited?
- **D** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 16: ⚖️ Relax edge: 2 + 8 = 10 vs current None

**Edge Relaxation:** Attempt to improve distance to **D**

**Calculation:**
- Current distance to **C**: **2**
- Edge weight **C** → **D**: **8**
- Potential new distance: 2 + 8 = **10**

**Comparison:**
- Current distance to **D**: **None**
- Compare: 10 < None?

**Result:** 10 < None ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[D]` = **10** (was None)
2. Update `previous[D]` = **'C'** (track path)
3. Insert (10, 'D') into priority queue

---

## Step 17: ✅ Update: distance['D'] = 10 (via 'C')

**Distance Update Confirmed:**
- Node: **D**
- Old distance: **None**
- New distance: **10** (via **C**)
- Path tracking: `previous[D]` = **'C'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B | 3 | C |
| C ✓ | 2 | A |
| D | 10 | C |
| E | ∞ | null |

---

## Step 18: 🔗 Check edge 'C' → 'E' (weight: 10)

**Examining Edge:** **C** → **E** (weight: **10**)

**Filter Check:** Is **E** visited?
- **E** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 19: ⚖️ Relax edge: 2 + 10 = 12 vs current None

**Edge Relaxation:** Attempt to improve distance to **E**

**Calculation:**
- Current distance to **C**: **2**
- Edge weight **C** → **E**: **10**
- Potential new distance: 2 + 10 = **12**

**Comparison:**
- Current distance to **E**: **None**
- Compare: 12 < None?

**Result:** 12 < None ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[E]` = **12** (was None)
2. Update `previous[E]` = **'C'** (track path)
3. Insert (12, 'E') into priority queue

---

## Step 20: ✅ Update: distance['E'] = 12 (via 'C')

**Distance Update Confirmed:**
- Node: **E**
- Old distance: **None**
- New distance: **12** (via **C**)
- Path tracking: `previous[E]` = **'C'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B | 3 | C |
| C ✓ | 2 | A |
| D | 10 | C |
| E | 12 | C |

---

## Step 21: 📍 Select node 'B' with minimum distance 3 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(3, 'B'), (4, 'B'), (12, 'E'), (10, 'D')]`
- Extract minimum: **(distance: 3, node: 'B')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **B** as visited (distance is now finalized)
- Explore all neighbors of **B** to potentially improve their distances

**Visited Set:** {A, C}

---

## Step 22: 🔍 Visit node 'B' (distance: 3) - checking 3 neighbor(s)

**Current Node:** **B** (distance from start: **3**)

**Neighbors to Check:**
Node **B** has neighbors: **['A', 'C', 'D']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **B** is shorter than current known distance

---

## Step 23: 🔗 Check edge 'B' → 'A' (weight: 4)

**Examining Edge:** **B** → **A** (weight: **4**)

**Filter Check:** Is **A** visited?
- **A** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 24: 🔗 Check edge 'B' → 'C' (weight: 1)

**Examining Edge:** **B** → **C** (weight: **1**)

**Filter Check:** Is **C** visited?
- **C** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 25: 🔗 Check edge 'B' → 'D' (weight: 5)

**Examining Edge:** **B** → **D** (weight: **5**)

**Filter Check:** Is **D** visited?
- **D** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 26: ⚖️ Relax edge: 3 + 5 = 8 vs current 10

**Edge Relaxation:** Attempt to improve distance to **D**

**Calculation:**
- Current distance to **B**: **3**
- Edge weight **B** → **D**: **5**
- Potential new distance: 3 + 5 = **8**

**Comparison:**
- Current distance to **D**: **10**
- Compare: 8 < 10?

**Result:** 8 < 10 ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[D]` = **8** (was 10)
2. Update `previous[D]` = **'B'** (track path)
3. Insert (8, 'D') into priority queue

---

## Step 27: ✅ Update: distance['D'] = 8 (via 'B')

**Distance Update Confirmed:**
- Node: **D**
- Old distance: **10**
- New distance: **8** (via **B**)
- Path tracking: `previous[D]` = **'B'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B ✓ | 3 | C |
| C ✓ | 2 | A |
| D | 8 | B |
| E | 12 | C |

---

## Step 28: 📍 Select node 'D' with minimum distance 8 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(8, 'D'), (10, 'D'), (12, 'E')]`
- Extract minimum: **(distance: 8, node: 'D')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **D** as visited (distance is now finalized)
- Explore all neighbors of **D** to potentially improve their distances

**Visited Set:** {A, B, C}

---

## Step 29: 🔍 Visit node 'D' (distance: 8) - checking 3 neighbor(s)

**Current Node:** **D** (distance from start: **8**)

**Neighbors to Check:**
Node **D** has neighbors: **['B', 'C', 'E']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **D** is shorter than current known distance

---

## Step 30: 🔗 Check edge 'D' → 'B' (weight: 5)

**Examining Edge:** **D** → **B** (weight: **5**)

**Filter Check:** Is **B** visited?
- **B** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 31: 🔗 Check edge 'D' → 'C' (weight: 8)

**Examining Edge:** **D** → **C** (weight: **8**)

**Filter Check:** Is **C** visited?
- **C** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 32: 🔗 Check edge 'D' → 'E' (weight: 2)

**Examining Edge:** **D** → **E** (weight: **2**)

**Filter Check:** Is **E** visited?
- **E** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 33: ⚖️ Relax edge: 8 + 2 = 10 vs current 12

**Edge Relaxation:** Attempt to improve distance to **E**

**Calculation:**
- Current distance to **D**: **8**
- Edge weight **D** → **E**: **2**
- Potential new distance: 8 + 2 = **10**

**Comparison:**
- Current distance to **E**: **12**
- Compare: 10 < 12?

**Result:** 10 < 12 ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[E]` = **10** (was 12)
2. Update `previous[E]` = **'D'** (track path)
3. Insert (10, 'E') into priority queue

---

## Step 34: ✅ Update: distance['E'] = 10 (via 'D')

**Distance Update Confirmed:**
- Node: **E**
- Old distance: **12**
- New distance: **10** (via **D**)
- Path tracking: `previous[E]` = **'D'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| A ✓ | 0 | null |
| B ✓ | 3 | C |
| C ✓ | 2 | A |
| D ✓ | 8 | B |
| E | 10 | D |

---

## Step 35: 📍 Select node 'E' with minimum distance 10 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(10, 'E'), (12, 'E')]`
- Extract minimum: **(distance: 10, node: 'E')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **E** as visited (distance is now finalized)
- Explore all neighbors of **E** to potentially improve their distances

**Visited Set:** {A, B, C, D}

---

## Step 36: 🔍 Visit node 'E' (distance: 10) - checking 2 neighbor(s)

**Current Node:** **E** (distance from start: **10**)

**Neighbors to Check:**
Node **E** has neighbors: **['C', 'D']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **E** is shorter than current known distance

---

## Step 37: 🔗 Check edge 'E' → 'C' (weight: 10)

**Examining Edge:** **E** → **C** (weight: **10**)

**Filter Check:** Is **C** visited?
- **C** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 38: 🔗 Check edge 'E' → 'D' (weight: 2)

**Examining Edge:** **E** → **D** (weight: **2**)

**Filter Check:** Is **D** visited?
- **D** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Final Result

**Shortest Distances from Start Node:**

| Node | Distance | Path |
|------|----------|------|
| A | 0 | A |
| B | 3 | A → C → B |
| C | 2 | A → C |
| D | 8 | A → C → B → D |
| E | 10 | A → C → B → D → E |

**Algorithm Completion:**
- All reachable nodes have finalized shortest distances
- Unreachable nodes remain at distance ∞
- Paths can be reconstructed using `previous` map

**Complexity Analysis:**
- Time Complexity: O((V + E) log V) with binary heap
  - V = 5 nodes, E = 7 edges
- Space Complexity: O(V) for distance/previous maps and priority queue

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Priority Queue State** (`priority_queue`) - Shows which nodes are candidates for processing, ordered by distance
- **Distance Map** (`distance_map`) - Real-time view of shortest known distances evolving
- **Current Node** (`current_node`) - The node being processed in this step

### Visualization Priorities

1. **Highlight the greedy selection** - When a node is popped from priority queue, emphasize this is the 'closest unvisited node'
2. **Animate edge relaxation** - Show the comparison (new_distance < old_distance) visually with the actual numbers
3. **Show distance improvements** - When a distance updates, use color transitions or animations to show the change
4. **Visualize the shortest path tree** - Edges in the `previous` map form the tree - highlight these differently
5. **Priority queue as sorted list** - Display queue contents sorted by distance to show why certain nodes are selected

### Key JSON Paths

```
step.data.visualization.nodes[*].id
step.data.visualization.nodes[*].state  // 'unvisited' | 'examining' | 'visited'
step.data.visualization.nodes[*].distance
step.data.visualization.nodes[*].previous
step.data.visualization.edges[*].from
step.data.visualization.edges[*].to
step.data.visualization.edges[*].weight
step.data.visualization.edges[*].state  // 'unexplored' | 'examining' | 'relaxed'
step.data.visualization.priority_queue[*].distance
step.data.visualization.priority_queue[*].node
step.data.visualization.distance_map
step.data.visualization.previous_map
step.data.visualization.visited_set
step.data.visualization.current_node
```

### Algorithm-Specific Guidance

Dijkstra's algorithm is fundamentally about **greedy selection** and **edge relaxation**. The most important visualization moments are: (1) **Priority queue pop** - show why this node has the smallest distance, (2) **Edge relaxation comparison** - display the arithmetic (current_dist + edge_weight vs old_dist) with actual values, (3) **Distance map updates** - animate the change from old to new distance. The priority queue should be visualized as a **sorted list** (not a tree) to make the 'minimum distance' selection obvious. Use a **table view** for the distance/previous maps to show all nodes at once - this helps learners see the global state. When an edge is relaxed successfully, highlight both the edge AND the distance update simultaneously. The final shortest path tree (edges in `previous` map) should be visually distinct - consider using a different color or thickness. For unreachable nodes (distance = ∞), use a clear visual indicator like a grayed-out state or a special symbol.
