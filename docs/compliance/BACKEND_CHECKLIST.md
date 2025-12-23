# Backend Checklist: Algorithm Tracer Compliance v2.4

**Authority:** WORKFLOW.md v2.4 - Backend Requirements  
**Purpose:** Verify new algorithm tracers comply with platform requirements

---

## LOCKED REQUIREMENTS (Mandatory)

### Metadata Structure

- [ ] **`algorithm`** (string) - Unique identifier present (e.g., "merge-sort")
- [ ] **`display_name`** (string) - Human-readable name present (e.g., "Merge Sort")
- [ ] **`visualization_type`** (string) - Valid type specified: "array" | "timeline" | "graph" | "tree"
- [ ] **`input_size`** (integer) - Number of elements/nodes documented

### Trace Structure

- [ ] **`metadata`** - Contains all required fields above
- [ ] **`trace.steps`** - Array of step objects present
- [ ] **Each step has `step` field** - 0-indexed integer step number
- [ ] **Each step has `type` field** - Algorithm-defined step type (string)
- [ ] **Each step has `description` field** - Human-readable description (string)
- [ ] **Each step has `data.visualization` field** - Current state for visualization (dict)

### Inheritance & Base Class

- [ ] **Inherits from `AlgorithmTracer`** - Uses base class provided in `backend/algorithms/base_tracer.py`
- [ ] **Implements `_get_visualization_state()`** - Returns dict with current visualization data
- [ ] **Implements `execute(input_data)`** - Main algorithm logic, returns trace dict
- [ ] **No modifications to `base_tracer.py`** - All customization via subclass methods

### Narrative Generation

- [ ] **Implements `generate_narrative(trace_result: dict) -> str`**

  - Abstract method from `AlgorithmTracer` base class
  - Converts own trace JSON to human-readable markdown
  - Must be implemented (will raise NotImplementedError if not)

- [ ] **Narrative generated for ALL registered examples**

  - Every example in `registry.py` has corresponding narrative
  - Files saved to `docs/narratives/[algorithm-name]/[example-name].md`
  - Naming convention: `example_1_basic.md`, `example_2_edge_case.md`, etc.

- [ ] **Narrative generation does NOT fail**

  - No `KeyError` exceptions when accessing visualization data
  - No missing field references
  - Fails loudly if data incomplete (this is good - catches bugs!)

- [ ] **Narrative passes FAA arithmetic audit**

  - Submit narratives to FAA review using `FAA_PERSONA.md`
  - Address all arithmetic errors flagged by FAA
  - Resubmit until FAA approves (blocking requirement)
  - See Stage 1.5 in WORKFLOW.md for details

- [ ] **Algorithm info markdown file exists**

  - File location: `docs/algorithm-info/[algorithm-name].md`
  - Naming convention: Match algorithm name exactly (e.g., `binary-search.md`, `interval-coverage.md`)
  - Content: Educational overview (what, why, where used, complexity, applications)
  - No code-heavy content - focus on conceptual understanding; why this algorithm exists
  - Verified markdown syntax is valid (no broken formatting)
  - Verify 150-250 words limit.

- [ ] **Registry provides `get_info()` method**

  - `registry.get_info('algorithm-name')` returns markdown string
  - Method handles missing files gracefully (raises ValueError with helpful message)
  - Path resolution works from registry location

- [ ] **Self-review completed before FAA submission**
  - [ ] Can I follow the algorithm logic from narrative alone?
  - [ ] Are all decision points explained with visible data?
  - [ ] Does temporal flow make sense (step N → step N+1)?
  - [ ] Can I mentally visualize this without code/JSON?
  - [ ] Are all arithmetic claims correct? (FAA will verify)

---

## Universal Pedagogical Principles

**Scope:** These principles apply to narratives for **all algorithm types** (array, timeline, graph, tree).  
**Purpose:** Ensure cognitive clarity, temporal coherence, and pedagogical effectiveness regardless of data structure.  
**Precedence:** Follow these principles unless algorithm-specific extensions (below) require adaptation.

---

### Principle 1: Operation Atomicity

**Guideline:** Present logically-related operations as unified conceptual steps.

- [ ] ✅ **NOT fragmenting "calculate → use" patterns** across step boundaries

  - Example ❌: Step 5: Calculate mid index. Step 6: Compare with mid.
  - Example ✅: Step 5: Compare target with mid element (calculation + comparison unified)

- [ ] ✅ **NOT separating "load → process" patterns** across steps

  - Example ❌: Step 3: Load interval. Step 4: Check overlap.
  - Example ✅: Step 3: Check if interval overlaps with current coverage

- [ ] ✅ **NOT splitting state updates** from the decisions that caused them
  - Example ❌: Step 7: Check condition. Step 8: Update variable.
  - Example ✅: Step 7: Check condition → update variable (cause + effect together)

**Rationale:** Human working memory has limited capacity (~7 items). Fragmenting atomic operations forces readers to hold partial context across step boundaries, increasing cognitive load. Unified steps create complete mental models that can be processed and stored efficiently.

**Application Test:** Ask "Would a human perform these operations separately or as one unit of thought?" If one unit, make it one step.

---

### Principle 2: State Display Efficiency

**Guideline:** Display each state variable once per step in a consistent location.

- [ ] ✅ **NOT displaying state redundantly** (header and body showing same data)

  - Example ❌: Header: "Stack: [A]", Body: "Stack becomes [A]"
  - Example ✅: Header: "Stack: [A]", Body: "Pop A and visit it"

- [ ] ✅ **NOT repeating unchanged state** unnecessarily

  - Example ❌: Every step shows "Array: [1,2,3,4,5]" even when unchanged
  - Example ✅: Show array state only when elements change state or at key decision points

- [ ] ✅ **Choosing consistent presentation location** (header OR body, not both)
  - Option A: Show state in header, narrative explains changes
  - Option B: Show state in body with "Before/After" format
  - Pick one pattern per algorithm and maintain it

**Rationale:** Redundant information creates visual noise that competes with meaningful content. Readers scan for changes; repeated identical data slows comprehension and obscures actual state transitions.

**Application Test:** For each state variable, decide: "Header or body?" Then never show it in both locations within the same step.

---

### Principle 3: Explicit Comparison Logic

**Guideline:** Show operands, operator, and result for all decision points.

- [ ] ✅ **NOT stating conclusions without showing comparisons**

  - Example ❌: "Target is in right half"
  - Example ✅: "Compare target (7) with mid (5): 7 > 5 → search right half"

- [ ] ✅ **NOT hiding intermediate calculations**

  - Example ❌: "Update max_end to 720"
  - Example ✅: "max_end = max(660, 720) = 720"

- [ ] ✅ **For multi-element operations (filtering, set membership, subset selection):**
  - Show the full collection being operated on
  - Show the element(s) being checked
  - Show the explicit comparison/filter logic
  - Show the result of the operation
  - Example: "Check neighbors [A, B, C] against visited [A, D]: A visited (skip), B unvisited (keep), C unvisited (keep). Result: [B, C]"

**Rationale:** Decision points are where learning happens. Showing "what" without "how" forces readers to reverse-engineer the logic, which may lead to incorrect mental models. Explicit comparisons make the algorithm's reasoning transparent and verifiable.

**Application Template:** "Compare X (value) with Y (value): X op Y → consequence"

---

### Principle 4: Term Definition Protocol

**Guideline:** Define algorithm-specific terminology before or at first use.

- [ ] ✅ **NOT using jargon without definition**

  - Example ❌: "Backtrack from node D"
  - Example ✅: "Backtrack (return to explore alternative paths) from node D"

- [ ] ✅ **NOT assuming prior knowledge** of algorithm-specific concepts

  - Example ❌: "Partition array around pivot"
  - Example ✅: "Partition (rearrange array so elements < pivot are left of it) around pivot"

- [ ] ✅ **Providing inline definitions** on first use, then using term freely
  - First use: "Relax edge (update distance if shorter path found)"
  - Subsequent uses: "Relax edge A→B"

**Alternative Approach:** Use descriptive language instead of jargon

- Instead of: "Backtrack"
- Use: "Continue DFS by popping next node from stack"

**Rationale:** Technical jargon creates barriers for learners. Inline definitions preserve readability while ensuring accessibility. Once defined, terms can be used freely, creating efficient communication.

**Application Test:** Grep narrative for domain terms (partition, relax, backtrack, merge, etc.). Ensure first occurrence includes definition or use descriptive alternative.

---

### Principle 5: Data Structure Presentation

**Guideline:** Handle unordered data structures (sets, dicts) with care in narratives.

- [ ] ✅ **NOT showing unexplained ordering changes** in unordered collections

  - Example ❌: Step 3: visited = {A, B, D}, Step 5: visited = {D, A, B} (same elements, different order)
  - Example ✅: Use list for display: visited = [A, B, D] (maintains insertion order)

- [ ] ✅ **Choosing ordered collections for narrative display** when order matters pedagogically

  - Use `list` instead of `set` for visited tracking (shows visit sequence)
  - Use sorted dict display for distance maps (alphabetical is predictable)
  - Ensures temporal sequence is visible to learners

- [ ] ✅ **Explicitly labeling unordered collections** if used
  - Example: "Visited (unordered set): {A, D, B} — ordering not semantically meaningful"
  - Prevents reader confusion about why order changes between steps

**Rationale:** Python sets and dicts have implementation-dependent ordering that creates cognitive noise in narratives. Readers waste mental effort trying to understand why order changes, not realizing it's an implementation detail rather than algorithmic significance.

**Application Rule:**

- Default: Use ordered collections (list, sorted dict) for all narrative display
- If using unordered: Label once at first appearance, ignore ordering thereafter

---

### Principle 6: Result Field Traceability

**Guideline:** Every field in the final result must have a narrative trail showing when/why it was computed.

- [ ] ✅ **NOT introducing surprise fields** in final result

  - Self-test: List all result fields → grep narrative for each → ensure introduced before final summary
  - Example ❌: Result contains `{"winning_position": 6}` but narrative never mentions position tracking
  - Example ✅: Narrative shows "We track this position (6) since it achieves best result so far"

- [ ] ✅ **NOT performing silent bookkeeping** (tracking data without explanation)

  - Example ❌: Code tracks `best_position` but narrative never mentions it until result
  - Example ✅: Explain purpose: "We track position because final result needs index, not just value"

- [ ] ✅ **Making hidden state updates pedagogically visible**
  - Explain WHY tracking matters: "We track previous[D]=C to reconstruct shortest path later"
  - Show WHEN updates occur: "Set previous[D]=C because we reached D via C"
  - Show HOW updates connect to result: "Final path uses previous pointers: D←C←A"

**Pattern to Follow:**

1. **Purpose:** "We track [X] because final result needs [Y]"
2. **Update:** "Current [X] becomes [value] due to [reason]"
3. **Application:** "Final result uses tracked [X]: [value]"

**Reader Reconstruction Test:** Cover result JSON, read only narrative. Can you predict all result fields? If any would be surprising, add narrative context.

**Rationale:** (Promoted from scattered mentions to universal principle) Result fields appearing without narrative context break the self-contained nature of the explanation and force readers to reverse-engineer algorithm logic.

---

### Testing Against Universal Principles

Before submitting narratives to FAA/PE, self-review using this checklist:

- [ ] **Principle 1 (Atomicity):** Have I fragmented any logically-related operations across step boundaries?
- [ ] **Principle 2 (Efficiency):** Is any state displayed redundantly in both header and body?
- [ ] **Principle 3 (Explicit Logic):** Do all decisions show comparison operands, operators, and results?
- [ ] **Principle 4 (Terms):** Are all algorithm-specific terms defined at or before first use?
- [ ] **Principle 5 (Data Structures):** Could unordered collection display cause confusion?
- [ ] **Principle 6 (Traceability):** Can I predict all result fields from narrative alone?

**Pass Criteria:** All 6 questions result in compliant answers.

---

### When Universal Principles Conflict With Algorithm Constraints

**Rare Case:** An algorithm's pedagogical value requires temporarily deviating from a principle.

**Example:** Teaching the difference between BFS (queue) and DFS (stack) might require showing both structures side-by-side to emphasize the contrast, even if this creates some redundancy.

**Resolution Protocol:**

1. Document the conflict in narrative
2. Explain to reader why the deviation serves pedagogical purpose
3. Return to principle adherence after concept is established

**Default:** Follow principles unless explicit pedagogical reason exists and is documented.

---

## Algorithm-Specific Extensions

The sections below build on Universal Pedagogical Principles with patterns specific to particular data structures or algorithm families.

---

### Graph Algorithm Narrative Requirements (Tier 3+)

**Foundation:** Graph algorithms must follow all **Universal Pedagogical Principles** above. The requirements below are **extensions** specific to graph data structures and traversal patterns.

**Why Extensions Are Needed:** Graphs introduce:

- Multi-dimensional topology (can't be displayed linearly like arrays)
- High variable density (20+ tracked variables vs 10 for arrays)
- Complex filtering operations (neighbor subset selection, cycle detection)
- Multi-step result construction (paths built incrementally across non-adjacent steps)

**Scope:** For algorithms with `visualization_type: "graph"`

---

#### Extension 1: Multi-Element Filtering Pattern (Builds on Principle 3)

When filtering neighbors, checking for cycles, or selecting edges:

- [ ] Show the **full collection** being filtered (complete neighbor list from adjacency)
- [ ] Show the **filter criteria** (visited set, distance comparison, indegree check, etc.)
- [ ] Show the **explicit comparison** for each element or subset
- [ ] Show the **filtered result**

**Example (DFS neighbor filtering):**

```markdown
Node B has neighbors [A, C, D].
Check against visited [B, A]:

- A: already visited → skip
- C: not visited → keep
- D: not visited → keep
  Result: 2 unvisited neighbors [C, D] to push onto stack
```

**Rationale:** Graph operations frequently involve set membership, filtering, and subset selection. Without explicit filtering logic, these operations appear to use "hidden information," breaking the self-contained narrative requirement and violating Principle 3 (Explicit Comparison Logic).

---

#### Extension 2: Traversal Structure Visibility (Builds on Principle 2)

Graph algorithms rely on auxiliary data structures (stack, queue, priority queue) as core algorithm components, not just implementation details.

- [ ] **Stack/Queue/Priority Queue contents shown explicitly** at each step
- [ ] **Format with directional indicators:**

  - Stack: `[A, B, C] ← C on top (processed next)`
  - Queue: `[A, B, C] ← A at front (processed next)`
  - Priority Queue: `[(3, C), (5, B), (8, D)] ← (3, C) has min priority`

- [ ] **Changes explained with before/after:**
  - Example: "Push D onto stack [A, B, C] → Stack becomes [A, B, C, D]"
  - Example: "Dequeue A from [A, B, C] → Queue becomes [B, C]"

**Rationale:** Unlike arrays where the data structure IS the input, graph traversal structures are algorithmic state that determines behavior. Stack vs queue distinguishes DFS from BFS—making these structures visible is pedagogically essential. This extends Principle 2 (State Display Efficiency) by ensuring traversal structures are shown consistently and clearly.

---

#### Extension 3: Graph Structure Representation

- [ ] **Use markdown tables or lists for adjacency** (not ASCII art)

  ```markdown
  **Graph Structure (Adjacency List):**

  - A → [B, C]
  - B → [D]
  - C → [D, E]
  ```

- [ ] **Show topology once at Step 0** (don't repeat full adjacency every step)
- [ ] **Reference topology implicitly thereafter:** "Node A's 2 neighbors" instead of re-listing [B, C]

**Rationale:** ASCII art breaks on mobile, fails accessibility requirements. Tables/lists are scannable, FAA-auditable, and mobile-friendly.

---

#### Extension 4: Multi-Variable State Tables

Graph algorithms often track parallel state for all nodes (distances, indegrees, previous pointers).

- [ ] **Present multi-variable state in markdown tables:**

  ```markdown
  | Node | Distance | Previous | State    |
  | ---- | -------- | -------- | -------- |
  | A    | 0        | None     | visited  |
  | B    | 5        | A        | visiting |
  | C    | 3        | A        | visited  |
  ```

- [ ] **Show incremental updates** (highlight changed rows when helpful)
- [ ] **Explain what each column represents** on first use (supports Principle 4)

**Rationale:** Verbal descriptions of parallel state ("A's distance is 0, B's distance is 5...") become unreadably verbose beyond 4-5 nodes. Tables present the same information in scannable format that FAA can verify row-by-row.

---

#### Extension 5: Multi-Step Result Construction (Extends Principle 6)

Graph results (shortest paths, spanning trees) are built incrementally across non-adjacent steps.

- [ ] **Make tracking decisions visible:**
  - Example: "Set previous[D]=C — we'll use this later to reconstruct the shortest path"
- [ ] **Show purpose before updates:**

  - Example: "We track previous pointers because the final result requires the complete path, not just distance"

- [ ] **Reference earlier tracking in result construction:**
  - Example: "Reconstruct path by following previous pointers: D ← C ← A (from Steps 7, 3)"

**Rationale:** Graph results violate the "result field appears in one step" pattern common in array algorithms. Making tracking decisions explicit prevents "phantom data" appearing only in final result (extension of Principle 6).

---

#### Extension 6: Conditional Logic in Decision Trees

Graph algorithms have complex branching (cycle detection, unreachable nodes, relaxation decisions).

- [ ] **Use explicit IF/THEN/ELSE format** for branches

  ```markdown
  **Condition:** IF indegree[B] == 0 THEN enqueue B ELSE skip
  **Evaluation:** indegree[B] = 0 (after decrement)
  **Result:** TRUE → Enqueue B
  ```

- [ ] **Explain failure cases:**
  - "Cycle detected: Cannot complete topological sort"
  - "Node E unreachable: No path exists from start node A"

**Rationale:** Graph algorithms have failure modes (cycles, disconnected components) that don't exist in arrays. Explicit conditional logic makes algorithm behavior predictable and debuggable (extends Principle 3).

---

#### Extension 7: Edge Operations (Weighted Graphs)

For weighted graphs, edge operations require arithmetic (extends Principle 3).

- [ ] **Show complete calculation:**

  ```markdown
  Relax edge A→B (weight=5):
  new_distance = dist[A] + weight(A→B) = 0 + 5 = 5
  Compare with current dist[B] = ∞
  Result: 5 < ∞ → Update dist[B] = 5
  ```

- [ ] **Make relaxation decision explicit:**
  - Show old distance, new distance, comparison, conclusion

**Rationale:** "Relax edge" is jargon (violates Principle 4). Showing arithmetic makes Dijkstra/Bellman-Ford transparent and FAA-auditable.

---

### Frontend Visualization Guidance

- [ ] **Visualization hints section included in narrative**
  - Add standardized "🎨 Frontend Visualization Hints" section at end of narrative
  - Provide backend insights to guide frontend visualization decisions
  - Include primary metrics, visualization priorities, and key JSON paths

**Required Hint Categories:**

```markdown
## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

[List 2-3 most important data points for user understanding]

### Visualization Priorities

[Suggest visual emphasis - what to highlight, when to animate]

### Key JSON Paths

[Provide exact paths to critical data for frontend access]

### Algorithm-Specific Guidance

[Custom insights about this algorithm's visualization needs]
```

**Example - Array Algorithm (Binary Search):**

```markdown
## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- Current search range (left/right pointers)
- Mid-point comparison value
- Number of elements eliminated per step

### Visualization Priorities

- Highlight the element being compared (mid position)
- Fade out eliminated ranges
- Animate pointer movements to show search space reduction

### Key JSON Paths

- Current range: `step.data.visualization.pointers.left/right`
- Comparison value: `step.data.visualization.array[mid].value`
- Element states: `step.data.visualization.array[*].state`

### Algorithm-Specific Guidance

Binary search is about visualizing the "shrinking search space" - emphasize how the range narrows with each decision. The moment of comparison (target vs mid) is the critical decision point to highlight.
```

**Example - Graph Algorithm (DFS):**

```markdown
## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- Current node being visited
- Stack contents (showing backtracking path)
- Visited vs unvisited nodes count

### Visualization Priorities

1. **Topology context** - Use force-directed or hierarchical layout
2. **Traversal order** - Number nodes as visited (1, 2, 3...)
3. **Active structure** - Show stack as vertical sidebar with LIFO animations
4. **State transitions** - Node color changes (unvisited→visiting→visited)
5. **Backtracking visualization** - Highlight when popping from stack

### Key JSON Paths

- Node states: `step.data.visualization.graph.nodes[*].state`
- Stack contents: `step.data.visualization.stack`
- Current node: `step.data.current_node` or infer from stack top
- Visited set: `step.data.visualization.visited_set`

### Algorithm-Specific Guidance

DFS is about exploring "as deep as possible" before backtracking. Emphasize the stack's role in remembering where to return. The moment of backtracking (stack pop with no unvisited neighbors) is crucial to highlight. Consider animating the "dive deep" vs "climb back up" phases distinctly.
```

---

## CONSTRAINED REQUIREMENTS (Follow Contract)

### Visualization Data Patterns

#### For Array Algorithms (visualization_type: "array")

- [ ] **`data.visualization.array`** - Array of element objects present
- [ ] Each element has **`index`** (int) - Array index
- [ ] Each element has **`value`** (any) - Element value
- [ ] Each element has **`state`** (string) - Element state (e.g., "examining", "excluded", "active_range")
- [ ] **`data.visualization.pointers`** (optional) - Algorithm pointers (left, right, mid, etc.)

#### For Timeline Algorithms (visualization_type: "timeline")

- [ ] **`data.visualization.all_intervals`** - Array of interval objects present
- [ ] Each interval has **`id`** (string) - Unique identifier
- [ ] Each interval has **`start`** (int) - Interval start
- [ ] Each interval has **`end`** (int) - Interval end
- [ ] Each interval has **`color`** (string) - Color identifier
- [ ] Each interval has **`state`** (string) - "examining" | "kept" | "covered"
- [ ] **`data.visualization.call_stack_state`** - Array of call frame objects
- [ ] Each frame has **`id`** (string) - Unique call frame ID
- [ ] Each frame has **`is_active`** (bool) - True for current call
- [ ] Each frame has **`depth`** (int) - Recursion depth

#### For Graph Algorithms (visualization_type: "graph")

**Required Core Fields:**

- [ ] **`data.visualization.graph.nodes`** - Array of node objects
- [ ] Each node has **`id`** (string) - Node identifier
- [ ] Each node has **`label`** (string) - Display label
- [ ] Each node has **`state`** (string) - "unvisited" | "visiting" | "visited"
- [ ] **`data.visualization.graph.edges`** - Array of edge objects
- [ ] Each edge has **`from`** (string) - Source node ID
- [ ] Each edge has **`to`** (string) - Target node ID
- [ ] Each edge has **`weight`** (int, optional) - Edge weight for weighted graphs

**Traversal Structure Fields (Algorithm-Dependent):**

- [ ] **`data.visualization.stack`** (optional) - Array for DFS stack state
  - Example: `["A", "B", "C"]` showing nodes in LIFO order
- [ ] **`data.visualization.queue`** (optional) - Array for BFS queue state
  - Example: `["D", "E", "F"]` showing nodes in FIFO order
- [ ] **`data.visualization.priority_queue`** (optional) - Array of tuples for Dijkstra
  - Example: `[[3, "C"], [5, "B"], [8, "D"]]` showing (priority, node) pairs

**Algorithm-Specific State Maps (Optional):**

- [ ] **`data.visualization.distance_map`** - Dict for shortest path distances
  - Example: `{"A": 0, "B": 5, "C": 3}` - distance from source to each node
- [ ] **`data.visualization.previous_map`** - Dict for path reconstruction
  - Example: `{"B": "A", "C": "A", "D": "C"}` - previous node in shortest path
- [ ] **`data.visualization.indegree_map`** - Dict for topological sort
  - Example: `{"A": 0, "B": 2, "C": 1}` - number of incoming edges per node
- [ ] **`data.visualization.visited_set`** - List of visited node IDs
  - Example: `["A", "B", "C"]` - nodes visited so far

**Metadata Configuration:**

- [ ] **`metadata.visualization_config.directed`** (bool) - Whether graph is directed
- [ ] **`metadata.visualization_config.weighted`** (bool) - Whether edges have weights

### Prediction Points (Optional)

If implementing prediction mode:

- [ ] **Implements `get_prediction_points()`** - Returns list of prediction dicts
- [ ] Each prediction has **`step_index`** (int) - Step where prediction occurs
- [ ] Each prediction has **`question`** (string) - Clear, concise question
- [ ] Each prediction has **`choices`** (list) - **HARD LIMIT: 2-3 choices maximum**
- [ ] Each choice has **`id`** (string) - Unique choice identifier
- [ ] Each choice has **`label`** (string) - Display text
- [ ] Each prediction has **`correct_answer`** (string) - Choice ID of correct answer
- [ ] Each prediction has **`explanation`** (string) - Feedback after answer
- [ ] **`hint`** (string, optional) - Hint text shown before answer

### Custom Fields (Allowed)

- [ ] **Algorithm-specific fields** - Added to `data` alongside `visualization`
- [ ] **Custom visualization config** - Added to `metadata.visualization_config`
- [ ] **State names** - Use algorithm-appropriate names (e.g., "pivot" for quicksort)

---

## ANTI-PATTERNS (Never Do)

### Contract Violations

- [ ] ✅ **NOT omitting required metadata fields** (algorithm, display_name, etc.)
- [ ] ✅ **NOT using non-standard visualization_type** (must be array/timeline/graph/tree)
- [ ] ✅ **NOT returning steps without visualization data**
- [ ] ✅ **NOT exceeding 3 prediction choices** (HARD LIMIT)

### Base Class Violations

- [ ] ✅ **NOT modifying `base_tracer.py`** for algorithm-specific code
- [ ] ✅ **NOT hardcoding step types in base class**
- [ ] ✅ **NOT bypassing `_add_step()` method**

### Universal Narrative Anti-Patterns (Apply to ALL Algorithms)

**Note:** These anti-patterns are violations of Universal Pedagogical Principles and apply regardless of visualization type.

- [ ] ✅ **NOT fragmenting atomic operations** across step boundaries

  - Violates Principle 1 (Operation Atomicity)
  - Example ❌: Separate steps for "calculate mid" and "compare with mid"
  - Example ✅: Unified step: "Compare target with mid element"

- [ ] ✅ **NOT displaying state redundantly**

  - Violates Principle 2 (State Display Efficiency)
  - Example ❌: Header: "Stack: [A]", Body: "Stack becomes [A]"
  - Example ✅: Show stack once per step, describe changes narratively

- [ ] ✅ **NOT hiding comparison logic**

  - Violates Principle 3 (Explicit Comparison Logic)
  - Example ❌: "Target is in right half" (how determined?)
  - Example ✅: "Compare target (7) with mid (5): 7 > 5 → search right half"

- [ ] ✅ **NOT using undefined terminology**

  - Violates Principle 4 (Term Definition Protocol)
  - Example ❌: "Partition array" (undefined jargon)
  - Example ✅: "Partition (rearrange so elements < pivot are left of it)"

- [ ] ✅ **NOT showing unexplained ordering changes** in unordered collections

  - Violates Principle 5 (Data Structure Presentation)
  - Example ❌: visited = {A, B, D} then {D, A, B} (unexplained reordering)
  - Example ✅: Use ordered list [A, B, D] or label as "unordered set"

- [ ] ✅ **NOT introducing surprise result fields**
  - Violates Principle 6 (Result Field Traceability)
  - Example ❌: Result contains `{"winning_position": 6}` but narrative never explains position tracking
  - Example ✅: Narrative shows "We track this position (6) since it achieved our best result so far"

### Algorithm-Specific Narrative Anti-Patterns

The items below are now subsumed by Universal Pedagogical Principles but retained for historical reference:

- [ ] ✅ **NOT referencing undefined variables in narrative**

  - Now covered by Principle 3 (Explicit Comparison Logic)
  - Example ❌: "Compare with max_end" (but max_end value not shown)
  - Example ✅: "Compare 720 with max_end (660)"

- [ ] ✅ **NOT skipping decision outcomes**

  - Now covered by Principle 1 (Operation Atomicity)
  - Example ❌: "Examining interval... [next step unrelated]"
  - Example ✅: "Examining interval [900, 960] → KEPT (extends coverage)"

- [ ] ✅ **NOT creating narratives that require code to understand**

  - Now covered by Principle 3 (Explicit Comparison Logic) + Principle 6 (Result Traceability)
  - Narrative must be self-contained
  - All data referenced must be visible in narrative

- [ ] ✅ **NOT performing silent bookkeeping**
  - Now covered by Principle 6 (Result Field Traceability)
  - Example ❌: Algorithm tracks data but treats it as "implementation detail"
  - Example ✅: Explain why tracking matters: "We track X because final answer needs Y"

---

#### Graph Algorithm Narrative Anti-Patterns (Tier 3+)

**Note:** These extend universal anti-patterns with graph-specific concerns.

- [ ] ✅ **NOT using ASCII art for graph topology**

  - Example ❌: Drawing complex node-edge diagrams in fixed-width text
  - Example ✅: Using markdown lists/tables for adjacency
  - Rationale: ASCII art breaks on different screen sizes, hard to parse, fails accessibility

- [ ] ✅ **NOT hiding traversal structure state**

  - Example ❌: "Process next node from queue" (but queue contents not shown)
  - Example ✅: "Dequeue B from [B, C, D] → Queue becomes [C, D]"
  - Rationale: Stack/queue mechanics are pedagogically critical for graph algorithms

- [ ] ✅ **NOT omitting path construction steps**

  - Example ❌: Final result shows path [A, C, D] but never explained how it was built
  - Example ✅: Step 7: "Set previous[D]=C (for path reconstruction)"
  - Rationale: Path reconstruction is often hidden "bookkeeping" that must be made visible

- [ ] ✅ **NOT showing incomplete distance/state maps**

  - Example ❌: "Update distance to B" (but distance map not shown)
  - Example ✅: Show full table with B's row highlighted as updated
  - Rationale: FAA cannot verify arithmetic without seeing all tracked values

- [ ] ✅ **NOT explaining conditional branches inadequately**

  - Example ❌: "Cycle detected" (but no explanation of how/why)
  - Example ✅: "IF visited[B]==True THEN cycle exists ELSE continue"
  - Rationale: Graph algorithms have complex failure modes that need explicit explanation

- [ ] ✅ **NOT repeating full graph structure every step**
  - Example ❌: Re-listing all edges at every step
  - Example ✅: Show adjacency once at Step 0, then reference specific neighbors
  - Rationale: Reduces narrative bloat while maintaining context

---

### Architectural Anti-Patterns

- [ ] ✅ **NOT using centralized narrative generator**

  - Each algorithm narrates ITSELF
  - No shared generator with if/elif chains

- [ ] ✅ **NOT including arithmetic errors in narratives** (covered by FAA audit requirement)

  - Example ❌: "20 - 10 = 20 elements remain"
  - Example ✅: "20 - 10 = 10 elements remain"
  - FAA will catch these before QA review

- [ ] ✅ **NOT omitting visualization guidance**
  - Example ❌: Narrative ends without helping frontend understand data priorities
  - Example ✅: Include standardized visualization hints section with backend insights

---

## FREE CHOICES (Your Decision)

### Allowed Customizations

- [ ] **Step types** - Define your own (e.g., "CALCULATE_MID", "PARTITION", "MERGE")
- [ ] **State names** - Use algorithm-appropriate names (e.g., "unsorted", "pivot", "partitioned")
- [ ] **Additional metrics** - Add custom fields (comparisons, swaps, custom_metric)
- [ ] **Visualization config** - Extend with algorithm-specific settings
- [ ] **Execution stats** - Add to `metadata.execution_stats`
- [ ] **Narrative formatting** - Markdown style choices (headers, emphasis, lists)
- [ ] **Visualization hint depth** - Provide detailed or minimal frontend guidance

### Graph Algorithm Customizations (Tier 3+)

- [ ] **Graph layout hints** - Suggest node positioning for frontend (optional)
  - Example: `metadata.visualization_config.layout_hint = "hierarchical"`
- [ ] **Edge styling** - Custom edge colors/thickness for algorithm semantics
  - Example: Mark "tree edges" vs "back edges" in DFS
- [ ] **Cycle highlighting** - Mark detected cycles in topological sort
- [ ] **Path emphasis** - Highlight current best path in shortest path algorithms
- [ ] **Node numbering** - Add visit order numbers (1, 2, 3...) for traversal visualization

---

## Testing Checklist

### Unit Tests

- [ ] **Valid trace structure** - Trace follows contract
- [ ] **Visualization data complete** - All required fields present
- [ ] **Step sequence logical** - Steps progress correctly
- [ ] **Prediction points valid** - If implemented, ≤3 choices each
- [ ] **Handles edge cases** - Empty input, single element, etc.

### Narrative Tests

- [ ] **All examples generate narratives** - No exceptions raised
- [ ] **Narratives reveal missing data** - Method fails loudly on incomplete visualization data
- [ ] **Narratives are logically complete** - QA can follow algorithm logic
- [ ] **Narratives demonstrate temporal coherence** - Step flow makes sense
- [ ] **Result field traceability verified** - All output fields have narrative trail
- [ ] **Visualization hints included** - Frontend guidance section present
- [ ] **Universal principles followed** - Self-review against 6 principles passes

### Graph Algorithm Narrative Tests (Tier 3+)

For algorithms with `visualization_type: "graph"`:

- [ ] **Graph topology shown in Step 0** - Adjacency list/structure present and scannable
- [ ] **Traversal structures tracked** - Stack/queue/priority queue visible at each step
- [ ] **Multi-variable state tables present** - Distance maps, indegree maps, previous maps shown
- [ ] **Path construction traceable** - Can follow how final paths were built incrementally
- [ ] **Conditional branches explained** - Cycle detection, unreachable nodes, relaxation decisions covered
- [ ] **Edge weight calculations shown** - For weighted graphs, arithmetic is explicit
- [ ] **No repeated structure dumps** - Full adjacency shown once, then referenced implicitly

### FAA Audit

- [ ] **Narratives pass arithmetic verification** - All quantitative claims verified correct
- [ ] **FAA approval obtained** - No arithmetic errors detected
- [ ] **Arithmetic errors fixed if found** - Regenerate and resubmit until FAA passes

### Integration Tests

- [ ] **Flask endpoint works** - `/api/trace/unified` accepts algorithm
- [ ] **Registry integration** - Algorithm registered correctly
- [ ] **Frontend can load** - Trace visible in browser console
- [ ] **No base class changes** - `base_tracer.py` unchanged

---

## Workflow Integration

**Stage 1: Backend Implementation**

1. ✅ Implement tracer class
2. ✅ Implement `generate_narrative()` method following Universal Pedagogical Principles
3. ✅ Run unit tests
4. ✅ Generate narratives for ALL registered examples
5. ✅ Self-review narratives against Universal Principles (6 questions)
6. ✅ **Verify result field traceability**
7. ✅ **Submit narratives to FAA audit** (using `FAA_PERSONA.md`)
8. ✅ **Fix arithmetic errors, regenerate until FAA passes**
9. ✅ Complete this checklist
10. ✅ Submit PR with code + FAA-approved narratives + checklist

**Next Stage:** PE Narrative Review (see WORKFLOW.md Stage 2)

---

**Remember:**

- If your tracer requires changes to `base_tracer.py`, you've misunderstood the architecture
- If your narrative violates Universal Pedagogical Principles, PE will block (fix before submission)
- If your narrative has undefined variable references, you've missed required visualization data
- If your result has surprise fields, you've missed narrative context requirements (Principle 6)
- If your narrative lacks visualization hints, you've missed a LOCKED requirement
