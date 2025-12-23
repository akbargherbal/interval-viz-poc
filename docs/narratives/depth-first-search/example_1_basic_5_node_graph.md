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

## Step 3: Push unvisited neighbors ['B', 'C'] from 'A' onto stack

**Stack:** ['C', 'B']
**Visited:** ['A']

**From Node:** 'A'
**Neighbors:** ['B', 'C']
**Decision:** Push 2 unvisited neighbor(s) onto stack
**Order:** ['B', 'C'] (pushed in reverse for alphabetical traversal)

## Step 4: Visit node 'B' (#2)

**Stack:** ['C']
**Visited:** ['B', 'A']

**Action:** Mark 'B' as visited (visit #2)
**Decision:** Add 'B' to visited set

## Step 5: Push unvisited neighbors ['D', 'E'] from 'B' onto stack

**Stack:** ['C', 'E', 'D']
**Visited:** ['B', 'A']

**From Node:** 'B'
**Neighbors:** ['D', 'E']
**Decision:** Push 2 unvisited neighbor(s) onto stack
**Order:** ['D', 'E'] (pushed in reverse for alphabetical traversal)

## Step 6: Visit node 'D' (#3)

**Stack:** ['C', 'E']
**Visited:** ['B', 'D', 'A']

**Action:** Mark 'D' as visited (visit #3)
**Decision:** Add 'D' to visited set

## Step 7: No unvisited neighbors from 'D', backtrack

**Stack:** ['C', 'E']
**Visited:** ['B', 'D', 'A']

**Condition:** IF 'D' has unvisited neighbors
**Result:** FALSE → No unvisited neighbors
**Action:** Backtrack (pop next node from stack)

## Step 8: Visit node 'E' (#4)

**Stack:** ['C']
**Visited:** ['B', 'D', 'E', 'A']

**Action:** Mark 'E' as visited (visit #4)
**Decision:** Add 'E' to visited set

## Step 9: No unvisited neighbors from 'E', backtrack

**Stack:** ['C']
**Visited:** ['B', 'D', 'E', 'A']

**Condition:** IF 'E' has unvisited neighbors
**Result:** FALSE → No unvisited neighbors
**Action:** Backtrack (pop next node from stack)

## Step 10: Visit node 'C' (#5)

**Stack:** (empty)
**Visited:** ['C', 'B', 'E', 'D', 'A']

**Action:** Mark 'C' as visited (visit #5)
**Decision:** Add 'C' to visited set

## Step 11: No unvisited neighbors from 'C', backtrack

**Stack:** (empty)
**Visited:** ['C', 'B', 'E', 'D', 'A']

**Condition:** IF 'C' has unvisited neighbors
**Result:** FALSE → No unvisited neighbors
**Action:** Backtrack (pop next node from stack)

## Step 12: DFS complete - visited 5 nodes

**Stack:** (empty)
**Visited:** ['C', 'B', 'E', 'D', 'A']

## Final Result

**Visit Order:** ['A', 'B', 'D', 'E', 'C']
**Visited Count:** 5 / 5 nodes
**Graph Connectivity:** All nodes reachable from start node ✓

**Total Steps:** 13

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
