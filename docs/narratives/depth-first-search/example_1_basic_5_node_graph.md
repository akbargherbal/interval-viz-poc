# Depth-First Search (DFS) Execution Narrative

## Input Summary

**Start Node:** A
**Total Nodes:** 5
**Total Edges:** 4

**Graph Structure (Adjacency List):**

- A → ['B', 'C']
- B → ['A', 'D', 'E']
- C → ['A']
- D → ['B']
- E → ['B']

## Step 0: Initialize DFS with start node 'A'

**Stack:** (empty)
**Visited:** (none)


## Step 1: Push start node 'A' onto stack

**Stack:** ['A']
**Visited:** (none)

**Action:** Push start node 'A' onto stack to begin traversal.

## Step 2: Visit 'A', push neighbors ['C', 'B']

**Stack:** ['C', 'B']
**Visited:** ['A']

**1. Pop Operation:**
- Pop 'A' from stack.
- **Intermediate Stack:** (empty)
- Mark 'A' as visited (Visit #1).

**2. Neighbor Analysis:**
Check neighbors of 'A' (in alphabetical order):
- Node B: unvisited → Push to stack
- Node C: unvisited → Push to stack

**3. Stack Update:**
- Neighbors to push: ['C', 'B']
- **Push Order:** Pushed in reverse ['C', 'B'] so that B is at top.
- **Result:** Next pop will visit 'B'.

## Step 3: Visit 'B', push neighbors ['E', 'D']

**Stack:** ['C', 'E', 'D']
**Visited:** ['A', 'B']

**1. Pop Operation:**
- Pop 'B' from stack.
- **Intermediate Stack:** ['C']
- Mark 'B' as visited (Visit #2).

**2. Neighbor Analysis:**
Check neighbors of 'B' (in alphabetical order):
- Node A: visited → Already visited (do not push)
- Node D: unvisited → Push to stack
- Node E: unvisited → Push to stack

**3. Stack Update:**
- Neighbors to push: ['E', 'D']
- **Push Order:** Pushed in reverse ['E', 'D'] so that D is at top.
- **Result:** Next pop will visit 'D'.

## Step 4: Visit 'D' (Backtrack point)

**Stack:** ['C', 'E']
**Visited:** ['A', 'B', 'D']

**1. Pop Operation:**
- Pop 'D' from stack.
- **Intermediate Stack:** ['C', 'E']
- Mark 'D' as visited (Visit #3).

**2. Neighbor Analysis:**
Check neighbors of 'D' (in alphabetical order):
- Node B: visited → Already visited (do not push)

**3. Stack Update:**
- No neighbors pushed.
- **Result:** No unvisited neighbors found. **Backtracking** (returning to previous node).

## Step 5: Visit 'E' (Backtrack point)

**Stack:** ['C']
**Visited:** ['A', 'B', 'D', 'E']

**1. Pop Operation:**
- Pop 'E' from stack.
- **Intermediate Stack:** ['C']
- Mark 'E' as visited (Visit #4).

**2. Neighbor Analysis:**
Check neighbors of 'E' (in alphabetical order):
- Node B: visited → Already visited (do not push)

**3. Stack Update:**
- No neighbors pushed.
- **Result:** No unvisited neighbors found. Backtracking.

## Step 6: Visit 'C' (Backtrack point)

**Stack:** (empty)
**Visited:** ['A', 'B', 'D', 'E', 'C']

**1. Pop Operation:**
- Pop 'C' from stack.
- **Intermediate Stack:** (empty)
- Mark 'C' as visited (Visit #5).

**2. Neighbor Analysis:**
Check neighbors of 'C' (in alphabetical order):
- Node A: visited → Already visited (do not push)

**3. Stack Update:**
- No neighbors pushed.
- **Result:** No unvisited neighbors found. Backtracking.

## Step 7: DFS complete - visited 5 nodes

**Stack:** (empty)
**Visited:** ['A', 'B', 'D', 'E', 'C']

**Completion:** Stack is empty.

## Final Result

**Visit Order:** ['A', 'B', 'D', 'E', 'C']
**Visited Count:** 5 / 5 nodes
**Graph Connectivity:** All nodes reachable from start node ✓

**Total Steps:** 8

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
