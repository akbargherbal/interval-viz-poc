# Algorithm Visualization Platform - Workflow & Architecture Guide

**Version:** 2.0  
**Status:** ACTIVE - Single Source of Truth  
**Replaces:** TENANT_GUIDE.md (v1.0, now deprecated)  
**Last Updated:** Session 34

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

**Critical Principle:** Static mockups are the **visual source of truth**. All visual requirements must align with them.

#### 2. This Document (WORKFLOW.md)

- **Authority for:** Functional requirements, behavioral patterns, architectural constraints, development process
- **Must reference mockups** for all visual specifications

#### 3. Compliance Checklists

- **Location:** `docs/compliance/*.md`
- **Authority for:** Validation procedures, testing criteria
- **Derived from:** This document + Static Mockups

---

## Table of Contents

- [The Three-Tier Jurisdiction System](#the-three-tier-jurisdiction-system)
- [v2.0 Workflow: Narrative-Driven Quality Gate](#v20-workflow-narrative-driven-quality-gate)
- [Stage 1: Backend Implementation](#stage-1-backend-implementation)
- [Stage 2: QA Narrative Review](#stage-2-qa-narrative-review)
- [Stage 3: Frontend Integration](#stage-3-frontend-integration)
- [Stage 4: Integration Testing](#stage-4-integration-testing)
- [LOCKED Requirements](#locked-requirements)
- [CONSTRAINED Requirements](#constrained-requirements)
- [FREE Implementation Choices](#free-implementation-choices)
- [Quick Reference](#quick-reference)

---

## The Three-Tier Jurisdiction System

This platform categorizes all elements into three jurisdictions:

| Jurisdiction    | Symbol | Freedom Level                              | Examples                                                         |
| --------------- | ------ | ------------------------------------------ | ---------------------------------------------------------------- |
| **LOCKED**      | 🔒     | Zero - Must implement exactly as specified | Modal sizes, panel ratios, HTML IDs, keyboard shortcuts          |
| **CONSTRAINED** | 🎨     | Limited - Parameters defined, flexible     | Visualization components, prediction questions, backend contract |
| **FREE**        | 🚀     | Full - Developer's choice                  | Component architecture, state management, optimizations          |

**Critical Principle:** LOCKED elements are **architectural invariants**. Violating them breaks user experience, testing infrastructure, or accessibility.

---

## v2.0 Workflow: Narrative-Driven Quality Gate

### What Changed from v1.0

**Version 1.0 (Deprecated):**
```
[BE] → [BE Checklist] → [FE] → [FE Checklist] → [QA Tests]
```

**Version 2.0 (Current):**
```
[BE Implementation]
    ↓
[BE Self-Narrates] ← NEW STEP
    ↓
[BE Checklist + Narrative]
    ↓
[QA Reviews NARRATIVE ONLY] ← CHANGED ROLE
    ↓
    ├─→ APPROVED → [FE Integration] → [FE Checklist] → [Integration Tests]
    └─→ REJECTED → [BE Fixes & Regenerates]
```

### Key Innovation

**QA becomes a NARRATIVE GATEKEEPER**, validating logical completeness BEFORE frontend integration.

**Benefits:**
- Issues caught earlier (60-70% found in narrative review)
- Fewer backend-frontend round-trips
- Frontend trusts JSON completeness
- Narratives serve as living documentation

---

## Stage 1: Backend Implementation

### Developer Actions

1. ✅ Implement algorithm tracer (inherit from `AlgorithmTracer`)
2. ✅ Implement `generate_narrative()` method (NEW REQUIREMENT - v2.0)
3. ✅ Run backend unit tests
4. ✅ Generate narratives for ALL registered examples
5. ✅ Self-review narratives for logical completeness
6. ✅ Complete Backend Compliance Checklist
7. ✅ Submit PR with code, checklist, and narratives

### Deliverables

```
backend/algorithms/my_algorithm.py
├── MyAlgorithmTracer class
│   ├── execute()
│   ├── get_prediction_points()
│   ├── _get_visualization_state()
│   └── generate_narrative()  ← NEW METHOD (v2.0)

docs/narratives/my_algorithm/
├── example_1_basic.md          ← Generated narrative
├── example_2_edge_case.md      ← Generated narrative
└── example_3_complex.md        ← Generated narrative

docs/compliance/
└── backend_checklist_my_algorithm.md  ← Completed checklist
```

### Self-Review Criteria

Before submitting, verify your narratives:

- [ ] Can I follow the algorithm logic from narrative alone?
- [ ] Are all decisions explained with visible data?
- [ ] Does temporal flow make sense (step N → step N+1)?
- [ ] Can I mentally visualize this without seeing code/JSON?

---

## Stage 2: QA Narrative Review

### QA Engineer Role (NEW in v2.0)

**CRITICAL:** QA does NOT look at JSON, code, or frontend in this stage.

**ONLY INPUT:** Generated markdown narratives

### QA Reviews For

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

### QA Does NOT Validate

❌ Whether JSON structure is correct (Backend Checklist handles this)  
❌ Whether frontend can render it (Integration Tests handle this)  
❌ Whether coordinates/scales are correct (rendering detail)  
❌ Performance or optimization (Integration Tests)

### Decision Gate

- **✅ APPROVED** → Proceed to Stage 3 (Frontend Integration)
- **⚠️ MINOR ISSUES** → Approved with documentation notes
- **❌ REJECTED** → Return to Stage 1 (Backend fixes and regenerates)

**Critical:** QA provides feedback on **WHY** narrative is rejected (what's missing/unclear), **NOT HOW** to fix it. Backend determines implementation.

### Common Issues to Catch

- Missing decision context (e.g., "compare with X" but X value not shown)
- Temporal gaps (step 8 → step 9 jump without explanation)
- Undefined variable references
- Unclear decision logic

### QA Feedback Format

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

**Principle:** QA identifies gaps, Backend decides implementation.

---

## Stage 3: Frontend Integration

### Frontend Developer Actions

1. ✅ Receive QA-approved backend code and narratives
2. ✅ Create or select visualization component
3. ✅ Register in visualization registry
4. ✅ Complete Frontend Compliance Checklist
5. ✅ Submit PR

### Changed Expectations in v2.0

- **Frontend should NOT discover missing data** (QA narrative review caught it)
- **Frontend focuses on "how to render" not "what to render"**
- **Narratives serve as reference documentation**
- **Trust that JSON is logically complete**

---

## Stage 4: Integration Testing

### QA Engineer Actions

1. ✅ Run automated integration test suite (Suites 1-14)
2. ✅ Visual comparison to mockups
3. ✅ Cross-algorithm regression tests
4. ✅ Complete QA Integration Checklist

### Expected Outcome

**Zero "missing data" bugs** - narrative review should have caught them.

If integration tests find data issues, it indicates narrative review missed something.

---

## LOCKED Requirements

These are **architectural invariants**. Must implement exactly as specified.

### Modal Standards

**All modals use consistent sizing without height constraints.**

**Source:** `docs/static_mockup/completion_modal_mockup.html` (Compact Redesign) and `prediction_modal_mockup.html`

```jsx
// ✅ CORRECT: CompletionModal (redesigned for vertical efficiency)
<div className="max-w-lg w-full p-5">
  {/* 512px max width, no height constraint, compact padding */}
</div>

// ✅ CORRECT: PredictionModal
<div className="max-w-lg w-full p-6">
  {/* 512px max width, no height constraint */}
</div>

// ❌ WRONG: Different widths
<div className="max-w-2xl w-full">  {/* Contradicts mockup */}
</div>
```

**Rationale:**
- **Width:** `max-w-lg` (512px) - Consistent across all modals
- **Height:** No constraint - Content designed to fit naturally
- **Vertical efficiency:** Compact layouts prevent overflow
- PredictionModal: Limited to ≤3 choices + compact spacing prevents overflow
- CompletionModal: Horizontal layouts + flex-wrap for complex data
- **Padding:** `p-5` for CompletionModal (more compact), `p-6` for PredictionModal

**Design Philosophy (from updated mockup):**
- "Redesigned for Vertical Efficiency (No Element Removal / No Font Scaling)"
- Use horizontal layouts where possible (e.g., icon + text in row instead of column)
- Compact spacing (`mb-3`, `mb-4` instead of `mb-6`)
- Grid layouts with dividers for visual separation without extra space

**Positioning:**

```jsx
<div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
  <div className="bg-slate-800 rounded-2xl shadow-2xl border-2 border-blue-500 max-w-lg w-full p-5">
    {/* CompletionModal content */}
  </div>
</div>

<div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
  <div className="bg-slate-800 rounded-2xl shadow-2xl border-2 border-blue-500 max-w-lg w-full p-6">
    {/* PredictionModal content */}
  </div>
</div>
```

**Scrolling Prohibition:**
- NO internal scrollbars in modals
- Content must fit naturally through compact design
- Use horizontal layouts to reduce vertical space
- For complex results: Show subset + summary (e.g., "+1 more") rather than scrolling

### Panel Layout

**Source:** `docs/static_mockup/algorithm_page_mockup.html`

```jsx
// ✅ CORRECT: Panel ratio
<div className="flex gap-4">
  <div className="flex-[3]">           {/* Visualization: 66.67% */}
    {/* Main visualization */}
  </div>
  <div className="w-96">               {/* Steps: 384px fixed */}
    {/* Steps panel */}
  </div>
</div>
```

**Key Requirements:**
- Visualization panel: `flex-[3]` (66.67% width)
- Steps panel: `w-96` (384px) OR `flex-[1.5]`
- Gap: `gap-4` (1rem)
- Ratio maintained at all supported viewports

### HTML Landmark IDs

**Required IDs (must be present):**

```jsx
#app-root              // Main application container
#app-header            // Header section
#panel-visualization   // Visualization panel
#panel-steps           // Steps panel
#panel-steps-list      // Steps list container
#panel-step-description // Step description area
#step-current          // Current active step (dynamic, one at a time)
```

**Dynamic ID Behavior:**
- Only ONE element has `id="step-current"` at a time
- ID updates on step navigation
- Corresponds to current execution context

### Keyboard Shortcuts

**Standard Shortcuts (global, when no modal open):**

**Source:** `docs/static_mockup/algorithm_page_mockup.html` lines 854-874

| Key         | Action             |
| ----------- | ------------------ |
| Arrow Right (→) | Next step          |
| Space       | Next step (alternative) |
| Arrow Left (←)  | Previous step      |
| R           | Reset to step 0    |
| Home        | Reset to step 0 (alternative) |

**Modal Shortcuts (when prediction modal open):**

**Source:** `docs/static_mockup/prediction_modal_mockup.html` lines 329-335

| Key         | Action                      |
| ----------- | --------------------------- |
| F/L/R/K/C (semantic) | Select choice (first letter of choice text) |
| 1/2/3 (numeric) | Select choice (fallback numbers) |
| Enter       | Submit selected answer      |
| S           | Skip prediction             |

**Conflict Resolution:**
- Input fields: Ignore shortcuts when typing
- Modals: Handle own shortcuts, prevent propagation to main app

### Auto-Scroll Behavior

**When navigating steps:**

```javascript
// Element with #step-current scrolls into view
element.scrollIntoView({
  behavior: 'smooth',
  block: 'center'
});
```

**Triggers:**
- ✅ Step navigation (Next/Prev buttons, keyboard)
- ❌ Manual user scroll (respect user intent)
- ❌ Algorithm switch (reset to top)

### Overflow Pattern

**Critical for wide content (arrays, timelines):**

```jsx
// ✅ CORRECT: items-start + mx-auto pattern
<div className="flex flex-col items-start overflow-auto">
  <div className="mx-auto">
    <div className="flex gap-2">
      {elements.map(el => (
        <div className="flex-shrink-0">{el}</div>
      ))}
    </div>
  </div>
</div>

// ❌ WRONG: items-center cuts off left edge
<div className="flex flex-col items-center overflow-auto">
  {/* Left content becomes inaccessible! */}
</div>
```

**Why this matters:**
- `items-center` + `overflow-auto` = left edge cut off (bug!)
- `items-start` + `mx-auto` = both edges scrollable

---

## CONSTRAINED Requirements

Parameters defined, implementation flexible.

### Backend JSON Contract

#### Required Metadata

```python
self.metadata = {
    'algorithm': 'my-algo',              # Unique identifier
    'display_name': 'My Algorithm',      # Human-readable name
    'visualization_type': 'array',       # array | timeline | graph | tree
    'input_size': 10,                    # Number of elements
}
```

#### Required Trace Structure

```python
{
  "metadata": { ... },
  "trace": {
    "steps": [
      {
        "step": 0,                       # 0-indexed step number
        "type": "INITIALIZE",            # Algorithm-defined type
        "description": "...",            # Human-readable
        "data": {
          "visualization": { ... },      # REQUIRED: Current state
          "custom_field": ...            # Optional: Algorithm-specific
        }
      }
    ]
  },
  "metadata": {
    "prediction_points": [ ... ]         # Optional
  }
}
```

### Visualization Data Patterns

#### Array Algorithms (visualization_type: "array")

```python
data['visualization'] = {
    'array': [
        {'index': 0, 'value': 1, 'state': 'active_range'},
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

### Narrative Generation (NEW in v2.0)

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
        - Fail loudly if data incomplete
        """
        narrative = "# Algorithm Execution Narrative\n\n"
        
        for step in trace_result['trace']['steps']:
            # Show step number
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
        
        return narrative
```

**Key Principles:**
- Each algorithm narrates ITSELF (no centralized generator)
- Narratives must be self-contained (no external references)
- All decision data must be visible in narrative
- Fails loudly on missing data (KeyError is good!)

### Completion Modal

**Algorithm-specific results:**

```jsx
// Binary Search
<CompletionModal
  title={found ? "Target Found!" : "Target Not Found"}
  stats={{
    comparisons: 5,
    foundIndex: 3,
    found: true
  }}
  borderColor={found ? "emerald" : "red"}
/>

// Interval Coverage
<CompletionModal
  title="Coverage Complete"
  stats={{
    intervalsKept: 3,
    coverage: [0, 1000]
  }}
/>
```

**Prediction Accuracy (if predictions used):**

```jsx
{predictionStats.total > 0 && (
  <div>
    <p>Accuracy: {accuracy}%</p>
    <p>Correct: {correct}/{total}</p>
  </div>
)}
```

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
3. **NEW:** Implement `generate_narrative()`
4. Register in `registry.py`
5. Generate narratives for all examples
6. Complete Backend Checklist

**QA (Stage 2):**
1. Review narratives for logical completeness
2. Check temporal coherence
3. Verify decision transparency
4. APPROVE or REJECT with specific feedback

**Frontend (Stage 3):**
1. Select or create visualization component
2. Register in visualization registry
3. Complete Frontend Checklist

**QA (Stage 4):**
1. Run integration tests
2. Visual comparison to mockups
3. Regression testing

### Checklist Locations

- Backend: `docs/compliance/BACKEND_CHECKLIST.md`
- Frontend: `docs/compliance/FRONTEND_CHECKLIST.md`
- QA: `docs/compliance/QA_INTEGRATION_CHECKLIST.md`

### Visual Reference

All UI decisions: `docs/static_mockup/*.html`

### Common Anti-Patterns

**Backend:**
- ❌ Omitting required metadata fields
- ❌ Missing visualization data in steps
- ❌ >3 prediction choices
- ❌ Narrative references undefined variables
- ❌ Modifying `base_tracer.py` for algorithm-specific code

**Frontend:**
- ❌ Using `items-center` + `overflow-auto` (cuts off left edge)
- ❌ Different modal widths
- ❌ Multiple elements with `id="step-current"`
- ❌ Ignoring keyboard shortcuts in input fields
- ❌ Deviating from mockups without justification

---

## Migration Notes

**From TENANT_GUIDE.md (v1.0) to WORKFLOW.md (v2.0):**

- All architectural principles preserved
- Added narrative generation workflow (v2.0)
- Removed time/duration references (LLM-managed workflow)
- Positioned as single source of truth
- Integrated compliance checklists into workflow

**Deprecated Documents:**
- `TENANT_GUIDE.md` → Archived to `docs/proposal/DEPRECATED_TENANT_GUIDE.md`

---

## Document Version History

| Version | Date    | Changes                              |
| ------- | ------- | ------------------------------------ |
| 2.0     | Session 34 | Initial WORKFLOW.md, narrative workflow added, replaces TENANT_GUIDE.md |
| 1.0     | Session 15 | TENANT_GUIDE.md (now deprecated)     |

---

**Document Status:** ✅ ACTIVE - Single Source of Truth  
**Next Review:** When adding new algorithm types (graph, tree) or major workflow changes

---
