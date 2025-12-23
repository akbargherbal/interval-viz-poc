# Depth-First Search (DFS) Execution Narrative

## Input Summary

**Start Node:** A
**Total Nodes:** 4
**Total Edges:** 3

**Graph Structure (Adjacency List):**

- A → ['B']
- B → ['A', 'C']
- C → ['B', 'D']
- D → ['C']

## Step 0: Initialize DFS with start node 'A'

**Stack:** (empty)
**Visited:** (none)


## Step 1: Push start node 'A' onto stack

**Stack:** ['A']
**Visited:** (none)

**Action:** Push start node 'A' onto stack to begin traversal.

## Step 2: Visit 'A', push neighbors ['B']

**Stack:** ['B']
**Visited:** ['A']

**1. Pop Operation:**
- Pop 'A' from stack.
- **Intermediate Stack:** (empty)
- Mark 'A' as visited (Visit #1).

**2. Neighbor Analysis:**
Check neighbors of 'A' (in alphabetical order):
- Node B: unvisited → Push to stack

**3. Stack Update:**
- Neighbors to push: ['B']
- **Push Order:** Pushed in reverse ['B'] so that B is at top.
- **Result:** Next pop will visit 'B'.

## Step 3: Visit 'B', push neighbors ['C']

**Stack:** ['C']
**Visited:** ['A', 'B']

**1. Pop Operation:**
- Pop 'B' from stack.
- **Intermediate Stack:** (empty)
- Mark 'B' as visited (Visit #2).

**2. Neighbor Analysis:**
Check neighbors of 'B' (in alphabetical order):
- Node A: visited → Already visited (do not push)
- Node C: unvisited → Push to stack

**3. Stack Update:**
- Neighbors to push: ['C']
- **Push Order:** Pushed in reverse ['C'] so that C is at top.
- **Result:** Next pop will visit 'C'.

## Step 4: Visit 'C', push neighbors ['D']

**Stack:** ['D']
**Visited:** ['A', 'B', 'C']

**1. Pop Operation:**
- Pop 'C' from stack.
- **Intermediate Stack:** (empty)
- Mark 'C' as visited (Visit #3).

**2. Neighbor Analysis:**
Check neighbors of 'C' (in alphabetical order):
- Node B: visited → Already visited (do not push)
- Node D: unvisited → Push to stack

**3. Stack Update:**
- Neighbors to push: ['D']
- **Push Order:** Pushed in reverse ['D'] so that D is at top.
- **Result:** Next pop will visit 'D'.

## Step 5: Visit 'D' (Backtrack point)

**Stack:** (empty)
**Visited:** ['A', 'B', 'C', 'D']

**1. Pop Operation:**
- Pop 'D' from stack.
- **Intermediate Stack:** (empty)
- Mark 'D' as visited (Visit #4).

**2. Neighbor Analysis:**
Check neighbors of 'D' (in alphabetical order):
- Node C: visited → Already visited (do not push)

**3. Stack Update:**
- No neighbors pushed.
- **Result:** No unvisited neighbors found. **Backtracking** (returning to previous node).

## Step 6: DFS complete - visited 4 nodes

**Stack:** (empty)
**Visited:** ['A', 'B', 'C', 'D']

**Completion:** Stack is empty.

## Final Result

**Visit Order:** ['A', 'B', 'C', 'D']
**Visited Count:** 4 / 4 nodes
**Graph Connectivity:** All nodes reachable from start node ✓

**Total Steps:** 7

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- Current node being visited (top of stack)
- Stack contents (showing exploration path)
- Visited vs unvisited nodes count
- Visit order numbering (1, 2, 3...)

### Visualization Priorities

1. **Topology context** - Use force-directed or hierarchical layout
2. **Traversal order** - Number nodes as visited (1, 2, 3...)
3. **Active structure** - Show stack as vertical sidebar with LIFO animations
4. **State transitions** - Node color changes (unvisited→visiting→visited)
5. **Backtracking visualization** - Highlight when popping from stack with no unvisited neighbors

### Key JSON Paths

- Node states: `step.data.visualization.graph.nodes[*].state`
- Stack contents: `step.data.visualization.stack`
- Current node: `step.data.current_node`
- Visited set: `step.data.visualization.visited_set`
- Neighbor analysis: `step.data.filtering_log` (for detailed tooltips)

### Algorithm-Specific Guidance

DFS is about exploring "as deep as possible" before backtracking. 
Emphasize the stack's role in remembering where to return. 
The moment of backtracking (stack pop with no unvisited neighbors) is crucial to highlight. 
Consider animating the "dive deep" vs "climb back up" phases distinctly.
