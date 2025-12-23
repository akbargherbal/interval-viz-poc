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

## Step 0: Starting DFS from node A

**Stack:** (empty)
**Visited:** (none)

## Step 1: Push start node 'A' onto stack

**Stack:** ['A']
**Visited:** (none)

**Action:** Initialize stack with start node
**Stack becomes:** ['A']

## Step 2: Visit node 'A' (#1)

**Stack:** (empty)
**Visited:** ['A']

**Action:** Mark 'A' as visited (visit #1)
**Decision:** Add 'A' to visited set

## Step 3: Push unvisited neighbors ['B'] from 'A' onto stack

**Stack:** ['B']
**Visited:** ['A']

**From Node:** 'A'
**Neighbors:** ['B']
**Decision:** Push 1 unvisited neighbor(s) onto stack
**Order:** ['B'] (pushed in reverse for alphabetical traversal)

## Step 4: Visit node 'B' (#2)

**Stack:** (empty)
**Visited:** ['B', 'A']

**Action:** Mark 'B' as visited (visit #2)
**Decision:** Add 'B' to visited set

## Step 5: No unvisited neighbors from 'B', backtrack

**Stack:** (empty)
**Visited:** ['B', 'A']

**Condition:** IF 'B' has unvisited neighbors
**Result:** FALSE → No unvisited neighbors
**Action:** Backtrack (pop next node from stack)

## Step 6: DFS complete - visited 2 nodes

**Stack:** (empty)
**Visited:** ['B', 'A']

## Final Result

**Visit Order:** ['A', 'B']
**Visited Count:** 2 / 5 nodes
**Unreachable Nodes:** ['C', 'D', 'E']
*(These nodes are not connected to the start node)*

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
- Current node: Infer from stack top or `step.data.current_node`
- Visited set: `step.data.visualization.visited_set`
- Visit order: `step.data.visit_number` at VISIT_NODE steps

### Algorithm-Specific Guidance

DFS is about exploring "as deep as possible" before backtracking. 
Emphasize the stack's role in remembering where to return. 
The moment of backtracking (stack pop with no unvisited neighbors) is crucial to highlight. 
Consider animating the "dive deep" vs "climb back up" phases distinctly.
