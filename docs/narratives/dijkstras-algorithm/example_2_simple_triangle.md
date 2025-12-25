# Dijkstra's Algorithm Execution Narrative

**Algorithm:** Dijkstra's Algorithm
**Start Node:** X
**Graph Size:** 3 nodes
**Total Steps:** 19

---

## Step 0: 🎯 Initialize: Set distance to start node 'X' = 0, all others = ∞

**Purpose:** Initialize distance tracking for shortest path computation.

**Graph Structure (Adjacency List):**
- **X**: [Y (weight: 5), Z (weight: 10)]
- **Y**: [X (weight: 5), Z (weight: 3)]
- **Z**: [X (weight: 10), Y (weight: 3)]

**Initial Distances:**
- Start node **X**: distance = **0** (starting point)
- All other nodes: distance = **∞** (unreachable until proven otherwise)

**Initial Priority Queue:**
- Insert (X, 0) - start node with distance 0
- Queue state: `[(0, 'X')]` ← (0, 'X') has highest priority (smallest distance)

**Tracking Structures:**
- **Distance map** (`distances`): Tracks shortest known distance to each node
- **Previous map** (`previous`): Tracks previous node in shortest path (for path reconstruction)
- **Visited set**: Tracks nodes with finalized shortest distances

---

## Step 1: 📍 Select node 'X' with minimum distance 0 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(0, 'X')]`
- Extract minimum: **(distance: 0, node: 'X')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **X** as visited (distance is now finalized)
- Explore all neighbors of **X** to potentially improve their distances

**Visited Set:** {X}

---

## Step 2: 🔍 Visit node 'X' (distance: 0) - checking 2 neighbor(s)

**Current Node:** **X** (distance from start: **0**)

**Neighbors to Check:**
Node **X** has neighbors: **['Y', 'Z']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **X** is shorter than current known distance

---

## Step 3: 🔗 Check edge 'X' → 'Y' (weight: 5)

**Examining Edge:** **X** → **Y** (weight: **5**)

**Filter Check:** Is **Y** visited?
- **Y** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 4: ⚖️ Relax edge: 0 + 5 = 5 vs current None

**Edge Relaxation:** Attempt to improve distance to **Y**

**Calculation:**
- Current distance to **X**: **0**
- Edge weight **X** → **Y**: **5**
- Potential new distance: 0 + 5 = **5**

**Comparison:**
- Current distance to **Y**: **None**
- Compare: 5 < None?

**Result:** 5 < None ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[Y]` = **5** (was None)
2. Update `previous[Y]` = **'X'** (track path)
3. Insert (5, 'Y') into priority queue

---

## Step 5: ✅ Update: distance['Y'] = 5 (via 'X')

**Distance Update Confirmed:**
- Node: **Y**
- Old distance: **None**
- New distance: **5** (via **X**)
- Path tracking: `previous[Y]` = **'X'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| X ✓ | 0 | null |
| Y | 5 | X |
| Z | ∞ | null |

---

## Step 6: 🔗 Check edge 'X' → 'Z' (weight: 10)

**Examining Edge:** **X** → **Z** (weight: **10**)

**Filter Check:** Is **Z** visited?
- **Z** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 7: ⚖️ Relax edge: 0 + 10 = 10 vs current None

**Edge Relaxation:** Attempt to improve distance to **Z**

**Calculation:**
- Current distance to **X**: **0**
- Edge weight **X** → **Z**: **10**
- Potential new distance: 0 + 10 = **10**

**Comparison:**
- Current distance to **Z**: **None**
- Compare: 10 < None?

**Result:** 10 < None ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[Z]` = **10** (was None)
2. Update `previous[Z]` = **'X'** (track path)
3. Insert (10, 'Z') into priority queue

---

## Step 8: ✅ Update: distance['Z'] = 10 (via 'X')

**Distance Update Confirmed:**
- Node: **Z**
- Old distance: **None**
- New distance: **10** (via **X**)
- Path tracking: `previous[Z]` = **'X'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| X ✓ | 0 | null |
| Y | 5 | X |
| Z | 10 | X |

---

## Step 9: 📍 Select node 'Y' with minimum distance 5 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(5, 'Y'), (10, 'Z')]`
- Extract minimum: **(distance: 5, node: 'Y')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **Y** as visited (distance is now finalized)
- Explore all neighbors of **Y** to potentially improve their distances

**Visited Set:** {X, Y}

---

## Step 10: 🔍 Visit node 'Y' (distance: 5) - checking 2 neighbor(s)

**Current Node:** **Y** (distance from start: **5**)

**Neighbors to Check:**
Node **Y** has neighbors: **['X', 'Z']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **Y** is shorter than current known distance

---

## Step 11: 🔗 Check edge 'Y' → 'X' (weight: 5)

**Examining Edge:** **Y** → **X** (weight: **5**)

**Filter Check:** Is **X** visited?
- **X** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 12: 🔗 Check edge 'Y' → 'Z' (weight: 3)

**Examining Edge:** **Y** → **Z** (weight: **3**)

**Filter Check:** Is **Z** visited?
- **Z** ∉ visited set ✓
- **Decision:** Proceed to edge relaxation

---

## Step 13: ⚖️ Relax edge: 5 + 3 = 8 vs current 10

**Edge Relaxation:** Attempt to improve distance to **Z**

**Calculation:**
- Current distance to **Y**: **5**
- Edge weight **Y** → **Z**: **3**
- Potential new distance: 5 + 3 = **8**

**Comparison:**
- Current distance to **Z**: **10**
- Compare: 8 < 10?

**Result:** 8 < 10 ✓ (shorter path found)

**Actions Taken:**
1. Update `distances[Z]` = **8** (was 10)
2. Update `previous[Z]` = **'Y'** (track path)
3. Insert (8, 'Z') into priority queue

---

## Step 14: ✅ Update: distance['Z'] = 8 (via 'Y')

**Distance Update Confirmed:**
- Node: **Z**
- Old distance: **10**
- New distance: **8** (via **Y**)
- Path tracking: `previous[Z]` = **'Y'**

**Current Distance Map:**

| Node | Distance | Previous |
|------|----------|----------|
| X ✓ | 0 | null |
| Y ✓ | 5 | X |
| Z | 8 | Y |

---

## Step 15: 📍 Select node 'Z' with minimum distance 8 from priority queue

**Priority Queue Selection:**
Queue before pop: `[(8, 'Z'), (10, 'Z')]`
- Extract minimum: **(distance: 8, node: 'Z')**
- This node has the smallest unfinalized distance

**Decision:** Process node **{node}** with distance **{dist}**
- Mark **Z** as visited (distance is now finalized)
- Explore all neighbors of **Z** to potentially improve their distances

**Visited Set:** {X, Y, Z}

---

## Step 16: 🔍 Visit node 'Z' (distance: 8) - checking 2 neighbor(s)

**Current Node:** **Z** (distance from start: **8**)

**Neighbors to Check:**
Node **Z** has neighbors: **['Y', 'X']**
- Will attempt to relax edges to each unvisited neighbor
- Edge relaxation: Check if path through **Z** is shorter than current known distance

---

## Step 17: 🔗 Check edge 'Z' → 'Y' (weight: 3)

**Examining Edge:** **Z** → **Y** (weight: **3**)

**Filter Check:** Is **Y** visited?
- **Y** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Step 18: 🔗 Check edge 'Z' → 'X' (weight: 10)

**Examining Edge:** **Z** → **X** (weight: **10**)

**Filter Check:** Is **X** visited?
- **X** ∈ visited set ✓
- **Decision:** Skip (already has finalized shortest distance)

---

## Final Result

**Shortest Distances from Start Node:**

| Node | Distance | Path |
|------|----------|------|
| X | 0 | X |
| Y | 5 | X → Y |
| Z | 8 | X → Y → Z |

**Algorithm Completion:**
- All reachable nodes have finalized shortest distances
- Unreachable nodes remain at distance ∞
- Paths can be reconstructed using `previous` map

**Complexity Analysis:**
- Time Complexity: O((V + E) log V) with binary heap
  - V = 3 nodes, E = 3 edges
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
