# Algorithm Visualization Platform - Workflow & Architecture Guide

**Version:** 2.5.0  
**Status:** ACTIVE - Single Source of Truth

---

## Document Authority

### What This Document Governs

This document is the **single source of truth** for:

1. **Workflow** - How algorithms move from concept to production
2. **Architecture** - What is LOCKED, CONSTRAINED, and FREE
3. **Process** - Quality gates and validation stages
4. **Requirements** - Technical and functional constraints

### Authority Hierarchy

When conflicts arise, follow this hierarchy:

#### 1. Static Mockups (Highest Authority for Visual Standards)

- **Location:** `docs/static_mockup/*.html`
- **Authority for:** Visual appearance, sizing, spacing, colors, layout, typography
- **When to use:** All visual UI decisions

**Critical Principle:** Static mockups are the **visual source of truth**. All visual requirements must align with them. It's incumbent on the Frontend developer to make sure any update they do to existing components or newly created React components conform to the visual guidelines illustrated in the static mockup documents in `docs/static_mockup/*.html`.

#### 2. This Document (WORKFLOW.md)

- **Authority for:** Functional requirements, behavioral patterns, architectural constraints, development process
- **Must reference mockups** for all visual specifications

#### 3. Compliance Checklists

- **Location:** `docs/compliance/*.md`
- **Authority for:** Validation procedures, testing criteria
- **Derived from:** This document + Static Mockups

---

## Stage 1: Backend Implementation

### Developer Actions

1. ✅ Implement algorithm tracer (inherit from `AlgorithmTracer`)
2. ✅ Implement `generate_narrative()` method (REQUIRED - v2.0)
3. ✅ Run backend unit tests
4. ✅ Generate narratives for ALL registered examples
5. ✅ Self-review narratives for logical completeness
6. ✅ **Submit narratives to FAA audit**
7. ✅ **Fix arithmetic errors, regenerate until FAA passes**
8. ✅ Complete Backend Compliance Checklist
9. ✅ Submit PR with code, FAA-approved narratives, and checklist

### Deliverables

```
backend/algorithms/my_algorithm.py
├── MyAlgorithmTracer class
│   ├── execute()
│   ├── get_prediction_points()
│   ├── _get_visualization_state()
│   └── generate_narrative()  ← REQUIRED

docs/narratives/my_algorithm/
├── example_1_basic.md          ← FAA-approved narrative
├── example_2_edge_case.md      ← FAA-approved narrative
└── example_3_complex.md        ← FAA-approved narrative

docs/compliance/
└── backend_checklist_my_algorithm.md  ← Completed checklist
```

### Self-Review Criteria

Before submitting to FAA, verify your narratives:

- [ ] Can I follow the algorithm logic from narrative alone?
- [ ] Are all decisions explained with visible data?
- [ ] Does temporal flow make sense (step N → step N+1)?
- [ ] Can I mentally visualize this without seeing code/JSON?
- [ ] Are all arithmetic claims correct? (FAA will verify this)

---

## Stage 1.5: Forensic Arithmetic Audit

### Quality Gate: Mathematical Verification

**Timing:** After backend generates narratives, before PE review  
**Validator:** Backend developer using `FAA_PERSONA.md`  
**Purpose:** Catch arithmetic errors before human PE review

### How It Works

1. Backend developer completes narrative generation (Stage 1)
2. Developer submits narratives to FAA audit:
   - Uses `FAA_PERSONA.md` as review guide
   - Verifies every quantitative claim
   - Checks arithmetic correctness
3. FAA identifies any mathematical errors
4. Developer fixes errors and regenerates narratives
5. Process repeats until FAA passes

### FAA Validation Scope

**FAA ONLY validates:**

- ✅ Arithmetic correctness (e.g., "20 - 10 = 10" not "20")
- ✅ State transition math (e.g., "max_end updated from 660 → 720")
- ✅ Quantitative claims consistency (e.g., counts match operations)
- ✅ Visualization-text alignment (e.g., shown elements match claimed elements)

**FAA does NOT validate:**

- ❌ Pedagogical quality (PE handles this in Stage 2)
- ❌ Narrative completeness (PE handles this in Stage 2)
- ❌ Writing style or clarity (PE handles this in Stage 2)
- ❌ Logical flow (PE handles this in Stage 2)

### Decision Gate

- **✅ APPROVED** → Proceed to Stage 2 (PE Narrative Review)
- **❌ REJECTED** → Return to Stage 1 (Fix arithmetic, regenerate)

**Critical:** FAA is a BLOCKING gate. No narrative proceeds to PE with arithmetic errors.

### Why This Gate Exists

**Problem discovered:** Generic narrative review has ~50% false-approval rate for arithmetic errors. Specialized mathematical validation catches errors that pedagogical review misses.

**Evidence:** Testing revealed 3 of 6 reviewers approved narratives with systematic arithmetic errors (claiming "20 elements remain" after "eliminating 10 from 20"). FAA persona caught 100% of arithmetic errors with 0% false positives.

**Cost-benefit:** 2 hours of FAA back-and-forth beats 2 days of integration debugging.

### FAA Audit Process

**Reference document:** `docs/compliance/FAA_PERSONA.md`

**Expected time:**

- Initial audit: 10-15 minutes
- Re-audit after fixes: 5 minutes
- Total for clean narrative: ~15 minutes
- Total for narrative with errors: ~35 minutes (including fixes)

**Common errors FAA catches:**

- Copy-paste errors (same number after different operations)
- Stale state propagation (previous step's value incorrectly carried forward)
- Off-by-one errors in index arithmetic
- Visualization-text mismatches

---

## Stage 2: PE (Pedagogical Experience) Narrative Review

### PE Specialist Role

**CRITICAL:** PE does NOT look at JSON, code, or frontend in this stage.

**ONLY INPUT:** FAA-approved markdown narratives; PE assumes arithmetic correctness has been verified by FAA.

### PE Reviews For

#### 1. Logical Completeness

- Can I follow the algorithm from start to finish?
- Are all decision points explained?
- Is the data supporting each decision visible?

#### 2. Temporal Coherence

- Does step N+1 logically follow from step N?
- Are there narrative gaps or jumps?
- Can I reconstruct the algorithm's flow?

#### 3. Mental Visualization

- Can I imagine what the visualization would show?
- Are state changes clear?
- Can I track what's happening without code?

#### 4. Decision Transparency

For each decision (keep/discard, left/right, etc.):

- Is the comparison data visible?
- Is the decision logic clear?
- Is the outcome explained?

### PE Does NOT Validate

❌ Whether JSON structure is correct (Backend Checklist handles this)  
❌ Whether frontend can render it (Integration Tests handle this)  
❌ Whether coordinates/scales are correct (rendering detail)  
❌ Performance or optimization (Integration Tests)  
❌ **Arithmetic correctness (FAA already validated)**

### Decision Gate

- **✅ APPROVED** → Proceed to Stage 3 (Frontend Integration)
- **⚠️ MINOR ISSUES** → Approved with documentation notes
- **❌ REJECTED** → Return to Stage 1 (Backend fixes and regenerates)

**Critical:** PE provides feedback on **WHY** narrative is rejected (what's missing/unclear), **NOT HOW** to fix it. Backend determines implementation.

### Common Issues to Catch

- Missing decision context (e.g., "compare with X" but X value not shown)
- Temporal gaps (step 8 → step 9 jump without explanation)
- Undefined variable references
- Unclear decision logic

**Note:** Arithmetic errors should NOT appear here (FAA caught them in Stage 1.5).

### PE Feedback Format

**✅ CORRECT Feedback (describes WHAT is wrong):**

```
❌ REJECTED - Binary Search Example 1

Issue 1: Missing decision context at Step 5
- Narrative states: "Compare target with mid"
- Problem: The actual values being compared are not visible
- Impact: Cannot verify the decision logic

Issue 2: Temporal gap between Steps 8-9
- Step 8: "Examining mid element"
- Step 9: "Search right half"
- Problem: The comparison result that led to "search right" is missing
- Impact: Cannot follow the decision flow
```

**❌ WRONG Feedback (prescribes HOW to fix):**

```
❌ REJECTED - Binary Search Example 1

Issue 1: Add mid value to Step 5
- Solution: Update narrative to include: "Compare target (5) with mid (3)"

Issue 2: Add comparison step
- Solution: Insert new step between 8-9 showing "5 > 3, search right"
```

---

## Stage 3: Frontend Integration

### Overview

Frontend integration applies a **unified dashboard architecture** to all algorithms. All algorithms use the same dashboard structure in the Right-Side Panel (RSP), while the Left-Side Panel (LSP) provides algorithm-specific visualizations.

**Key Principle:** The dashboard structure is universal; only the visualization pattern changes.

### Step 1: Visualization Pattern Selection (5-10 minutes)

**Goal:** Identify which LSP visualization pattern fits your algorithm.

#### Decision Tree

```
What type of algorithm are you implementing?

├── Iterative (step-by-step state changes)
│   └── Visualization Patterns:
│       ├── Array with pointers (Binary Search, Two Pointer)
│       ├── Sliding window on array (Sliding Window)
│       └── Custom iterative visualization
│
└── Recursive (call stack / context-dependent)
    └── Visualization Patterns:
        ├── Timeline with intervals (Interval Coverage)
        ├── Tree structure (future: tree algorithms)
        └── Custom recursive visualization
```

#### Pattern Examples

| Algorithm | Type | LSP Visualization | RSP Dashboard |
|-----------|------|-------------------|---------------|
| Binary Search | Iterative | Array with L/R/M pointers | Unified (Mid, Target, Logic, Action) |
| Interval Coverage | Recursive | Timeline with interval bars | Unified (Interval, max_end, Logic, Action) |
| Merge Sort | Recursive | Tree/timeline hybrid | Unified (Subarray, Pivot, Logic, Action) |
| Sliding Window | Iterative | Array with window highlight | Unified (Window Sum, Target, Logic, Action) |

**Note:** All algorithms use the same dashboard structure - only the content in zones changes.

**Action:** Identify your visualization needs, not a "template type."

### Step 2: Dashboard Content Planning (5 minutes)

**Goal:** Map your algorithm's key metrics to the 5-zone dashboard structure.

#### Dashboard Zones (RSP)

```
┌─────────────┬─────┐
│             │  2  │  Zone 1 (Primary): Main focus value
│      1      │─────│  Zone 2 (Goal): Target/objective
│             │  3  │  Zone 3 (Logic): Current comparison
│   ┌─────────┼─────┤  Zone 4 (Action): Next operation
│   │    5    │  4  │  Zone 5 (Overlay): Metadata strip
└───┴─────────┴─────┘
```

#### Content Mapping Guidelines

**Zone 1 (Primary Focus):**
- Iterative: Current element being examined (e.g., Mid value, Window sum)
- Recursive: Current context (e.g., Interval range, Subarray bounds)
- Large, centered display

**Zone 2 (Goal):**
- Target value, max_end, sorted position, etc.
- Single numeric or short text value

**Zone 3 (Logic):**
- Current comparison expression (e.g., "42 == 42", "720 > 720")
- Two-line format: expression + result

**Zone 4 (Action):**
- Next operation (e.g., "RETURN Index 5", "✓ KEEP INTERVAL", "MERGE LEFT")
- Action-oriented text

**Zone 5 (Overlay - Bottom Strip):**
- 2-3 metadata cells
- Iterative: Left/Right boundaries, Range, Index
- Recursive: Depth, Remaining, Kept count

**Action:** Document your zone content mapping before implementation.

### Step 3: Component Implementation (20-40 minutes)

#### 3.1 Create Algorithm State Component

**Location:** `frontend/src/components/algorithm-states/`

**Naming:** `{AlgorithmName}State.jsx`

**Structure:**

```jsx
import React from 'react';

export const {AlgorithmName}State = ({ step, trace }) => {
  // Extract data from step.data.visualization
  const visualizationData = step.data.visualization;
  
  // Map to dashboard zones
  const zone1 = {
    label: "...",
    meta: "...",
    value: "..."
  };
  // ... other zones
  
  // Render unified dashboard structure
  return (
    <div className="dashboard h-full">
      {/* Zone 1: Primary Focus */}
      <div className="zone zone-primary">
        <div className="zone-label">{zone1.label}</div>
        <div className="zone-meta">{zone1.meta}</div>
        <div className="primary-value">{zone1.value}</div>
        
        {/* Zone 5: Overlay (inside Zone 1) */}
        <div className="zone-boundaries">
          {zone5.map((cell, i) => (
            <div key={i} className="boundary-cell">
              <div className="boundary-label">{cell.label}</div>
              <div className="boundary-value">{cell.value}</div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Zone 2: Goal */}
      <div className="zone zone-goal">
        <div className="zone-label">{zone2.label}</div>
        <div className="goal-value">{zone2.value}</div>
      </div>
      
      {/* Zone 3: Logic */}
      <div className="zone zone-logic">
        <div className="zone-label">LOGIC</div>
        <div className="logic-content">{zone3.content}</div>
      </div>
      
      {/* Zone 4: Action */}
      <div className="zone zone-action">
        <div className="action-text">{zone4.text}</div>
      </div>
    </div>
  );
};
```

**Reference:** See `BinarySearchState.jsx` and `IntervalCoverageState.jsx` for complete examples.

#### 3.2 Register Component in State Registry

**Location:** `frontend/src/utils/stateRegistry.js`

```javascript
import { YourAlgorithmState } from '../components/algorithm-states/YourAlgorithmState';

export const stateRegistry = {
  'your-algorithm': YourAlgorithmState,
  // ... other algorithms
};
```

**Key:** Must match `trace.metadata.algorithm` value from backend.

#### 3.3 Create or Reuse LSP Visualization Component

**Location:** `frontend/src/components/visualizations/`

**Options:**

1. **Reuse Existing:**
   - `ArrayView.jsx` - Array-based iterative algorithms
   - `TimelineView.jsx` - Timeline-based recursive algorithms

2. **Create New:**
   - Follow patterns in existing components
   - Register in `visualizationRegistry.js`

#### 3.4 Create Algorithm Info Markdown

**Location:** `frontend/public/algorithm-info/{algorithm-id}.md`

**Template:**

```markdown
# {Algorithm Display Name}

{Brief description}

## How it works:

- Step 1 description
- Step 2 description
- Step 3 description

## Complexity

- **Time Complexity:** O(...)
- **Space Complexity:** O(...)

## Key Metrics

- **{Metric 1}:** {Description}
- **{Metric 2}:** {Description}
```

### Step 4: Visual Compliance Check (5-10 minutes)

**Goal:** Ensure implementation matches unified dashboard standards.

#### Dashboard Structure Checklist

- [ ] Uses 5-zone grid layout
- [ ] Zone 1 spans rows 1-2
- [ ] Zone 5 overlay at bottom of Zone 1
- [ ] Container query units (`cqh`) for responsive sizing
- [ ] Edge-to-edge filling (no padding on dashboard wrapper)

#### Visual Standards Checklist

- [ ] Dashboard fills 100% of `#panel-steps` height
- [ ] No borders/shadows on dashboard
- [ ] Zone labels positioned consistently (top-left, 6px inset)
- [ ] Metadata labels positioned consistently (top-right, 6px inset)

#### Reference Mockup

**Primary Reference:** `docs/static_mockup/unified_dashboard_reference.html`

**What to Verify:**
- Dashboard structure matches exactly (only content differs)
- Grid layout identical
- Container query behavior same
- Color palette aligned with algorithm theme

### Step 5: Integration Testing (10-15 minutes)

**Test Scenarios:**

1. **Algorithm Load**
   - [ ] Algorithm appears in dropdown
   - [ ] First step renders correctly
   - [ ] Dashboard shows initial state

2. **Step Navigation**
   - [ ] Dashboard updates on Next/Previous
   - [ ] All zones reflect current step data
   - [ ] LSP visualization syncs with dashboard

3. **Prediction Modal**
   - [ ] Predictions appear at correct steps
   - [ ] Modal content matches backend
   - [ ] Keyboard shortcuts work

4. **Completion Modal**
   - [ ] Appears after final step
   - [ ] Shows correct completion message
   - [ ] Reset functionality works

5. **Info Modal**
   - [ ] Info button opens modal
   - [ ] Markdown renders correctly
   - [ ] Modal scrolls if needed

### Step 6: Complete Frontend Compliance Checklist

**Action:** Complete `docs/compliance/FRONTEND_CHECKLIST.md` for your algorithm.

**Handoff to QA:** Provide completed checklist with Stage 4 integration testing.

### Success Criteria

**Stage 3 Complete When:**
- [ ] Algorithm state component created and registered
- [ ] LSP visualization component implemented or reused
- [ ] Algorithm info markdown created
- [ ] Visual compliance verified
- [ ] Integration testing passed
- [ ] Frontend compliance checklist completed

**Deliverable:** Fully integrated algorithm ready for Stage 4 QA testing.

### Time Breakdown

| Task | Time |
|------|------|
| Visualization pattern selection | 5-10 min |
| Dashboard content planning | 5 min |
| State component implementation | 15-25 min |
| Registry integration | 2-3 min |
| LSP visualization (reuse) | 5 min |
| LSP visualization (new) | 15-30 min |
| Algorithm info markdown | 5 min |
| Visual compliance check | 5-10 min |
| Integration testing | 10-15 min |
| **Total** | **30-60 min** |

### Reference Files

**Dashboard Implementation:**
- `docs/static_mockup/unified_dashboard_reference.html` - Unified dashboard reference
- `frontend/src/components/algorithm-states/BinarySearchState.jsx` - Iterative example
- `frontend/src/components/algorithm-states/IntervalCoverageState.jsx` - Recursive example

**Visualization Components:**
- `frontend/src/components/visualizations/ArrayView.jsx`
- `frontend/src/components/visualizations/TimelineView.jsx`

**Registry Architecture:**
- `frontend/src/utils/stateRegistry.js`
- `frontend/src/utils/visualizationRegistry.js`

**Documentation:**
- `docs/compliance/FRONTEND_CHECKLIST.md`

---

## Stage 4: Integration Testing

### QA Actions

1. ✅ Test full algorithm flow end-to-end
2. ✅ Verify narrative accuracy matches UI rendering
3. ✅ Test prediction modal functionality
4. ✅ Run regression tests on existing algorithms
5. ✅ Complete QA Integration Checklist
6. ✅ Document any integration issues

### Test Scenarios

**Full Flow:**
- Algorithm selection → Load → Navigation → Predictions → Completion

**Edge Cases:**
- First step, last step, missing data handling

**Cross-Browser:**
- Chrome, Firefox, Safari (latest versions)

**Regression:**
- All existing algorithms still work
- No visual regressions
- No functional regressions

### Decision Gate

- **✅ APPROVED** → Merge to main
- **⚠️ MINOR ISSUES** → Document and fix in follow-up
- **❌ REJECTED** → Return to appropriate stage (BE/FE)

---

## LOCKED REQUIREMENTS (Cannot Be Modified)

### Backend Requirements

#### Trace Structure

**Metadata (LOCKED):**

```python
metadata = {
    'algorithm': str,           # LOCKED - Registry key
    'display_name': str,        # LOCKED - UI display
    'visualization_type': str,  # LOCKED - "array", "timeline", "graph"
    'input_size': int          # LOCKED - Max input constraint
}
```

#### Step Structure (LOCKED)

```python
step = {
    'step': int,                # LOCKED - Step number
    'type': str,                # FREE - Algorithm-specific
    'description': str,         # LOCKED - Human-readable
    'data': {                   # LOCKED - Container
        'visualization': dict,  # LOCKED - Viz state
        'metrics': dict        # FREE - Optional metrics
    }
}
```

#### Prediction Points (LOCKED)

```python
prediction = {
    'step_index': int,          # LOCKED - When to pause
    'question': str,            # LOCKED - Question text
    'choices': list,            # LOCKED - 2-3 choices ONLY
    'correct_answer': str,      # LOCKED - Choice ID
    'explanation': str,         # LOCKED - Why correct
    'hint': str                # FREE - Optional
}
```

**HARD LIMIT: 2-3 choices maximum per prediction**

### Frontend Requirements

#### Modal IDs (LOCKED)

```javascript
// LOCKED - Used by keyboard shortcuts
'#modal-prediction'   // Prediction modal
'#modal-completion'   // Completion modal
'#modal-algorithm-info' // Info modal
```

#### Keyboard Shortcuts (LOCKED)

```
→ / ← : Next/Previous step
Space : Toggle prediction modal (if at prediction point)
R     : Reset algorithm
ESC   : Close modals
1/2/3 : Select prediction choice
S     : Skip prediction
Enter : Submit answer / Restart
```

#### Panel Dimensions (LOCKED)

```
Left Panel (Visualization): flex-[3] (responsive - fills remaining space)
Right Panel (State): w-96 (384px fixed width)
```

#### Overflow Pattern (LOCKED)

```
overflow-y: auto   // Vertical scrolling allowed
overflow-x: hidden // Horizontal scrolling forbidden
```

---

## CONSTRAINED REQUIREMENTS (Follow Architecture Patterns)

### Backend Patterns

#### Visualization State Structure

```python
# Pattern varies by visualization_type, but structure is CONSTRAINED
def _get_visualization_state(self, ...):
    return {
        # Follow existing patterns for your visualization_type
        # See examples in existing tracers
    }
```

#### Array Algorithms (visualization_type: "array")

```python
data['visualization'] = {
    'array': [
        {'index': 0, 'value': 1, 'state': 'active'},
        {'index': 1, 'value': 3, 'state': 'examining'},
        {'index': 2, 'value': 5, 'state': 'excluded'}
    ],
    'pointers': {                        # Optional
        'left': 0,
        'mid': 1,
        'right': 4
    }
}
```

#### Timeline Algorithms (visualization_type: "timeline")

```python
data['visualization'] = {
    'all_intervals': [
        {'id': 'i1', 'start': 0, 'end': 100, 'color': 'blue', 'state': 'kept'},
        {'id': 'i2', 'start': 50, 'end': 150, 'color': 'green', 'state': 'examining'}
    ],
    'call_stack_state': [
        {'id': 'call_1', 'is_active': True, 'depth': 0},
        {'id': 'call_2', 'is_active': False, 'depth': 1}
    ]
}
```

#### Graph Algorithms (visualization_type: "graph") - Future

```python
data['visualization'] = {
    'graph': {
        'nodes': [
            {'id': 'A', 'label': 'Node A', 'state': 'visiting'},
            {'id': 'B', 'label': 'Node B', 'state': 'unvisited'}
        ],
        'edges': [
            {'from': 'A', 'to': 'B', 'weight': 5}
        ]
    }
}
```

### Prediction Points

**HARD LIMIT: 2-3 choices maximum**

```python
def get_prediction_points(self):
    return [{
        'step_index': 5,                 # When to pause
        'question': 'What happens next?',
        'choices': [                     # 2-3 choices ONLY
            {'id': 'a', 'label': 'Search left'},
            {'id': 'b', 'label': 'Search right'},
            {'id': 'c', 'label': 'Target found'}
        ],
        'correct_answer': 'b',
        'explanation': 'Target (5) > mid (3), so search right',
        'hint': 'Compare target with mid value'  # Optional
    }]
```

### Narrative Generation

**LOCKED REQUIREMENT:**

```python
class MyAlgorithmTracer(AlgorithmTracer):
    def generate_narrative(self, trace_result: dict) -> str:
        """
        Convert trace JSON → human-readable markdown.

        Must:
        - Show all decision points with supporting data
        - Maintain temporal coherence
        - Enable mental visualization
        - Pass FAA arithmetic audit
        - Fail loudly if data incomplete
        """
        # Extract components from trace_result
        metadata = trace_result['metadata']
        steps = trace_result['trace']['steps']
        result = trace_result['result']

        # Header with algorithm information
        narrative = "# Algorithm Execution Narrative\n\n"
        narrative += f"**Algorithm:** {metadata['display_name']}\n"
        narrative += f"**Input Size:** {metadata['input_size']}\n\n"
        narrative += "---\n\n"

        # Step-by-step narrative
        for step in steps:
            # Show step number and description
            narrative += f"## Step {step['step']}: {step['description']}\n\n"

            # Show visualization state with ALL relevant data
            viz = step['data']['visualization']
            narrative += f"**Array:** {viz['array']}\n"
            narrative += f"**Pointers:** left={viz['pointers']['left']}, "
            narrative += f"mid={viz['pointers']['mid']}, "
            narrative += f"right={viz['pointers']['right']}\n\n"

            # Show decision with supporting data
            if step['type'] == 'COMPARE':
                narrative += f"**Decision:** Compare target ({self.target}) "
                narrative += f"with mid value ({viz['array'][viz['pointers']['mid']]['value']})\n"
                narrative += f"**Result:** Target {'>' if ... else '<'} mid → Search {'right' if ... else 'left'}\n\n"

            narrative += "---\n\n"

        # Summary
        narrative += "## Execution Summary\n\n"
        narrative += f"**Final Result:** {result}\n"
        narrative += f"**Performance Metrics:** [Include relevant metrics]\n"

        return narrative
```

**Key Principles:**

- Each algorithm narrates ITSELF (no centralized generator)
- Narratives must be self-contained (no external references)
- All decision data must be visible in narrative
- **All arithmetic must be correct (FAA will verify)**
- Fails loudly on missing data (KeyError is good!)
- Extract `metadata`, `steps`, and `result` from `trace_result` first

---

## FREE Implementation Choices

Developer's choice - not constrained.

### Component Architecture

- ✅ Functional components vs. class components
- ✅ Custom hooks organization
- ✅ State management approach (useState, useReducer, context)
- ✅ Component file structure

### Performance Optimizations

- ✅ Memoization strategy (useMemo, useCallback, React.memo)
- ✅ Virtualization for long lists
- ✅ Lazy loading
- ✅ Bundle optimization

### Testing Strategy

- ✅ Unit test framework choice
- ✅ Test coverage targets
- ✅ Integration test approach
- ✅ E2E test tools

### Backend Implementation Details

- ✅ Step type names (use algorithm-appropriate names)
- ✅ State names (e.g., "pivot", "partitioned", "merged")
- ✅ Custom metrics (comparisons, swaps, custom_metric)
- ✅ Additional visualization config

---

## Quick Reference

### Adding a New Algorithm

**Backend (Stage 1):**

1. Create tracer class inheriting `AlgorithmTracer`
2. Implement `execute()`, `get_prediction_points()`, `_get_visualization_state()`
3. Implement `generate_narrative()`
4. Register in `registry.py`
5. Generate narratives for all examples
6. **Submit narratives to FAA audit**
7. **Fix arithmetic errors, regenerate until FAA passes**
8. Complete Backend Checklist (include FAA-approved narratives)
9. Submit PR with code, narratives, and completed checklist

**FAA Audit (Stage 1.5)**

1. Use `FAA_PERSONA.md` to audit narratives
2. Verify all arithmetic claims
3. Reject if errors found
4. Backend fixes and resubmits
5. Approve when arithmetic verified

**PE (Pedagogical Experience) (Stage 2):**

1. Review FAA-approved narratives for logical completeness
2. Check temporal coherence
3. Verify decision transparency
4. APPROVE or REJECT with specific feedback
5. **Assume arithmetic already verified**

**Frontend (Stage 3):**

1. Receive FAA+PE approved narratives
2. Identify visualization pattern (not template type)
3. Map dashboard content to 5 zones
4. Create algorithm state component (`{Algorithm}State.jsx`)
5. Register in `stateRegistry.js`
6. Create or reuse LSP visualization component
7. Create algorithm info markdown (`public/algorithm-info/{algorithm-name}.md`)
8. Verify visual compliance against unified dashboard
9. Complete Frontend Checklist
10. **Trust arithmetic correctness**

**QA Integration (Stage 4):**

1. Test full algorithm flow end-to-end
2. Verify narrative accuracy matches UI rendering
3. Test prediction modal functionality
4. Run regression tests on existing algorithms
5. Complete QA Integration Checklist
6. Document any integration issues for team

### Checklist Locations

- Backend: `docs/compliance/BACKEND_CHECKLIST.md`
- **FAA Audit:** `docs/compliance/FAA_PERSONA.md`
- PE Review: `docs/compliance/PE_CHECKLIST.md`
- Frontend: `docs/compliance/FRONTEND_CHECKLIST.md`

### Visual Reference

All UI decisions: `docs/static_mockup/*.html`

**Dashboard Reference:** `docs/static_mockup/unified_dashboard_reference.html`

### Common Anti-Patterns

**Backend:**

- ❌ Omitting required metadata fields
- ❌ Missing visualization data in steps
- ❌ >3 prediction choices
- ❌ Narrative references undefined variables
- ❌ **Arithmetic errors in narratives (FAA will catch)**
- ❌ Modifying `base_tracer.py` for algorithm-specific code

**Frontend:**

- ❌ Deviating from visual standards defined in static mockups (`docs/static_mockup/*.html`)
- ❌ All updated or newly created components must conform to visual guidelines in mockups
- ❌ State components using contexts directly (use props)
- ❌ Algorithm-specific components in `visualizations/` directory

---

**Document Status:** ✅ ACTIVE - Single Source of Truth  
**Next Review:** When adding new algorithm types (graph, tree) or major workflow changes

---
