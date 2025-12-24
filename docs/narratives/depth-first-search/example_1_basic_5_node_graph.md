# Depth-First Search (Iterative) Execution Narrative

**Algorithm:** Depth-First Search (Iterative)
**Start Node:** A
**Graph Size:** 5 nodes
**Traversal Order:** A → B → D → E → C
**Nodes Visited:** 5/5

---

## Step 0: 🔍 Initialize DFS from node A

**Graph Structure (Adjacency List):**
- A: [B, C]
- B: [A, D, E]
- C: [A]
- D: [B]
- E: [B]

**Initial Configuration:**
- Start node: **A**
- Stack: Empty (will push start node)
- Visited set: Empty
- Goal: Explore all reachable nodes depth-first

---

## Step 1: 📥 Push start node A onto stack

**Action:** Push node **A** onto stack

**Reason:** Starting node for traversal

**Stack State:**
```
[A] ← A on top (processed next)
```

**Visited Set:** {empty}

---

## Step 2: 📤 Pop node A from stack

**Action:** Pop node **A** from stack for processing

**Stack Before Pop:**
```
[A] ← A on top
```

**Stack After Pop:**
```
Empty
```

---

## Step 3: ✅ Visit node A (neighbor count: 2)

**Processing Node:** A

**Check Visited Status:**
- Visited set before: {empty}
- Is A in visited set? **No** ✓
- Action: Mark A as visited

**Updated Visited Set:** {A}

**Neighbors of A:** [B, C]

**Neighbor Processing:**
We will examine each neighbor to determine if it should be added to the stack.

---

## Step 4: 📥 Push neighbor C onto stack

**Action:** Push node **C** onto stack

**Reason:** Unvisited neighbor of A

**Stack State:**
```
[C] ← C on top (processed next)
```

**Visited Set:** {A}

---

## Step 5: 📥 Push neighbor B onto stack

**Action:** Push node **B** onto stack

**Reason:** Unvisited neighbor of A

**Stack State:**
```
[C, B] ← B on top (processed next)
```

**Visited Set:** {A}

---

## Step 6: 📤 Pop node B from stack

**Action:** Pop node **B** from stack for processing

**Stack Before Pop:**
```
[C, B] ← B on top
```

**Stack After Pop:**
```
[C] ← C on top (processed next)
```

---

## Step 7: ✅ Visit node B (neighbor count: 3)

**Processing Node:** B

**Check Visited Status:**
- Visited set before: {A}
- Is B in visited set? **No** ✓
- Action: Mark B as visited

**Updated Visited Set:** {A, B}

**Neighbors of B:** [A, D, E]

**Neighbor Processing:**
We will examine each neighbor to determine if it should be added to the stack.

---

## Step 8: 📥 Push neighbor E onto stack

**Action:** Push node **E** onto stack

**Reason:** Unvisited neighbor of B

**Stack State:**
```
[C, E] ← E on top (processed next)
```

**Visited Set:** {A, B}

---

## Step 9: 📥 Push neighbor D onto stack

**Action:** Push node **D** onto stack

**Reason:** Unvisited neighbor of B

**Stack State:**
```
[C, E, D] ← D on top (processed next)
```

**Visited Set:** {A, B}

---

## Step 10: ⏭️ Skip neighbor A (already visited)

**Examining Neighbor:** A (from node B)

**Check Visited Status:**
- Current visited set: {A, B}
- Is A in visited set? **Yes** ✓
- Decision: **Skip** A (already explored)

**Reason:** DFS only visits each node once. Since A is already in the visited set, we don't need to explore it again.

---

## Step 11: 📤 Pop node D from stack

**Action:** Pop node **D** from stack for processing

**Stack Before Pop:**
```
[C, E, D] ← D on top
```

**Stack After Pop:**
```
[C, E] ← E on top (processed next)
```

---

## Step 12: ✅ Visit node D (neighbor count: 1)

**Processing Node:** D

**Check Visited Status:**
- Visited set before: {A, B}
- Is D in visited set? **No** ✓
- Action: Mark D as visited

**Updated Visited Set:** {A, B, D}

**Neighbors of D:** [B]

**Neighbor Processing:**
We will examine each neighbor to determine if it should be added to the stack.

---

## Step 13: ⏭️ Skip neighbor B (already visited)

**Examining Neighbor:** B (from node D)

**Check Visited Status:**
- Current visited set: {A, B, D}
- Is B in visited set? **Yes** ✓
- Decision: **Skip** B (already explored)

**Reason:** DFS only visits each node once. Since B is already in the visited set, we don't need to explore it again.

---

## Step 14: ⬅️ Backtrack from D (all neighbors visited)

**Backtracking:**

- Finished exploring all neighbors of **D**
- No unvisited neighbors remain
- Return to previous node in stack (if any)

**Stack State:**
```
[C, E] ← E on top (processed next)
```

---

## Step 15: 📤 Pop node E from stack

**Action:** Pop node **E** from stack for processing

**Stack Before Pop:**
```
[C, E] ← E on top
```

**Stack After Pop:**
```
[C] ← C on top (processed next)
```

---

## Step 16: ✅ Visit node E (neighbor count: 1)

**Processing Node:** E

**Check Visited Status:**
- Visited set before: {A, B, D}
- Is E in visited set? **No** ✓
- Action: Mark E as visited

**Updated Visited Set:** {A, B, D, E}

**Neighbors of E:** [B]

**Neighbor Processing:**
We will examine each neighbor to determine if it should be added to the stack.

---

## Step 17: ⏭️ Skip neighbor B (already visited)

**Examining Neighbor:** B (from node E)

**Check Visited Status:**
- Current visited set: {A, B, D, E}
- Is B in visited set? **Yes** ✓
- Decision: **Skip** B (already explored)

**Reason:** DFS only visits each node once. Since B is already in the visited set, we don't need to explore it again.

---

## Step 18: ⬅️ Backtrack from E (all neighbors visited)

**Backtracking:**

- Finished exploring all neighbors of **E**
- No unvisited neighbors remain
- Return to previous node in stack (if any)

**Stack State:**
```
[C] ← C on top (processed next)
```

---

## Step 19: 📤 Pop node C from stack

**Action:** Pop node **C** from stack for processing

**Stack Before Pop:**
```
[C] ← C on top
```

**Stack After Pop:**
```
Empty
```

---

## Step 20: ✅ Visit node C (neighbor count: 1)

**Processing Node:** C

**Check Visited Status:**
- Visited set before: {A, B, D, E}
- Is C in visited set? **No** ✓
- Action: Mark C as visited

**Updated Visited Set:** {A, B, C, D, E}

**Neighbors of C:** [A]

**Neighbor Processing:**
We will examine each neighbor to determine if it should be added to the stack.

---

## Step 21: ⏭️ Skip neighbor A (already visited)

**Examining Neighbor:** A (from node C)

**Check Visited Status:**
- Current visited set: {A, B, C, D, E}
- Is A in visited set? **Yes** ✓
- Decision: **Skip** A (already explored)

**Reason:** DFS only visits each node once. Since A is already in the visited set, we don't need to explore it again.

---

## Step 22: ⬅️ Backtrack from C (all neighbors visited)

**Backtracking:**

- Finished exploring all neighbors of **C**
- No unvisited neighbors remain
- Return to previous node in stack (if any)

**Stack State:**
```
Empty (traversal complete)
```

---

## Execution Summary

**Traversal Complete:**
- Nodes visited: **5** out of 5
- Traversal order: A → B → D → E → C
- All nodes reachable from start node A

**Algorithm Characteristics:**
- Time Complexity: O(V + E) where V = vertices, E = edges
- Space Complexity: O(V) for stack and visited set
- Traversal Strategy: Depth-first (explore as far as possible before backtracking)

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Stack Contents** (`stack`) - Shows the exploration frontier and backtracking path
- **Visited Set Size** (`visited.length`) - Demonstrates progress through the graph
- **Current Node** (`current_node`) - The active exploration point

### Visualization Priorities

1. **Highlight the stack's LIFO behavior** - Use vertical stack visualization with top clearly marked
2. **Emphasize depth-first exploration** - Animate following one path to its end before backtracking
3. **Show visited vs. unvisited distinction** - Use distinct colors for `visited` vs `unvisited` node states
4. **Animate backtracking moments** - When stack pops without new pushes, show return to previous node
5. **Track traversal order** - Display the sequence of visited nodes to show exploration path

### Key JSON Paths

```
step.data.visualization.nodes[*].id
step.data.visualization.nodes[*].state  // 'unvisited' | 'examining' | 'visited'
step.data.visualization.edges[*].from
step.data.visualization.edges[*].to
step.data.visualization.edges[*].state  // 'unexplored' | 'traversed' | 'backtrack'
step.data.visualization.stack  // Array with top at end: [..., top]
step.data.visualization.visited  // Sorted array of visited node IDs
step.data.visualization.current_node  // Currently processing node
step.data.visualization.traversal_order  // Sequence of visited nodes
```

### Algorithm-Specific Guidance

DFS's defining characteristic is its **depth-first exploration strategy** - it follows one path as far as possible before backtracking. The most pedagogically important visualization is the **stack's LIFO behavior**: when we push neighbors onto the stack, the last one pushed is the first one explored (creating the depth-first pattern). Consider using a **vertical stack visualization** with clear directional indicators (arrows pointing to top). When backtracking occurs (popping without pushing), animate the 'return' to show we're unwinding the exploration path. The contrast between DFS and BFS becomes clear when students see the stack (LIFO) vs. queue (FIFO) - emphasize this by showing how the stack's top element determines the next exploration direction. For disconnected graphs, clearly show when the stack empties with unvisited nodes remaining, demonstrating that DFS only explores the connected component containing the start node.
