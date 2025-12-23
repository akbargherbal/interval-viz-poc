# Depth-First Search (DFS) Execution Narrative

## Input Summary

**Start Node:** A
**Total Nodes:** 5
**Total Edges:** 2

**Graph Structure (Adjacency List):**

- A → ['B']
- B → ['A']
- C → ['D']
- D → ['C']
- E → []

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

## Step 3: Visit 'B' (Backtrack point)

**Stack:** (empty)
**Visited:** ['A', 'B']

**1. Pop Operation:**
- Pop 'B' from stack.
- **Intermediate Stack:** (empty)
- Mark 'B' as visited (Visit #2).

**2. Neighbor Analysis:**
Check neighbors of 'B' (in alphabetical order):
- Node A: visited → Already visited (do not push)

**3. Stack Update:**
- No neighbors pushed.
- **Result:** No unvisited neighbors found. **Backtracking** (returning to previous node).

## Step 4: DFS complete - visited 2 nodes

**Stack:** (empty)
**Visited:** ['A', 'B']

**Completion:** Stack is empty.
**Note:** Nodes ['C', 'D', 'E'] remain unvisited.
This indicates the graph has **disconnected components**.
DFS only explores the component containing the start node.

## Final Result

**Visit Order:** ['A', 'B']
**Visited Count:** 2 / 5 nodes
**Unreachable Nodes:** ['C', 'D', 'E']

**Total Steps:** 5

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
