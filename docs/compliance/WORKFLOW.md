# Algorithm Visualization Platform - Workflow & Architecture Guide

**Version:** 2.1  
**Status:** ACTIVE - Single Source of Truth  
**Replaces:** TENANT_GUIDE.md (v1.0, now deprecated)  
**Last Updated:** Session 35 (FAA gate added)

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
- [v2.1 Workflow: Narrative-Driven Quality Gate with FAA](#v21-workflow-narrative-driven-quality-gate-with-faa)
- [Stage 1: Backend Implementation](#stage-1-backend-implementation)
- [Stage 1.5: Forensic Arithmetic Audit (NEW)](#stage-15-forensic-arithmetic-audit-new---v21)
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

## v2.1 Workflow: Narrative-Driven Quality Gate with FAA

### What Changed from v2.0

**Version 2.0:**
```
[BE Implementation]
    ↓
[BE Self-Narrates]
    ↓
[BE Checklist + Narrative]
    ↓
[QA Reviews NARRATIVE ONLY]
    ↓
    ├─→ APPROVED → [FE Integration] → [FE Checklist] → [Integration Tests]
    └─→ REJECTED → [BE Fixes & Regenerates]
```

**Version 2.1 (Current):**
```
[BE Implementation]
    ↓
[BE Self-Narrates]
    ↓
[FAA Arithmetic Audit] ← NEW BLOCKING GATE
    ↓
    ├─→ ARITHMETIC ERRORS → [BE Fixes & Regenerates]
    └─→ APPROVED ↓
[BE Checklist + FAA-Approved Narrative]
    ↓
[QA Reviews NARRATIVE ONLY] ← Now assumes arithmetic verified
    ↓
    ├─→ APPROVED → [FE Integration] → [FE Checklist] → [Integration Tests]
    └─→ REJECTED → [BE Fixes & Regenerates]
```

### Key Innovation in v2.1

**FAA (Forensic Arithmetic Audit) catches mathematical errors BEFORE human QA review.**

**Benefits:**
- Arithmetic errors caught in 10-15 minutes (vs. 2 days of integration debugging)
- QA focuses on logic/pedagogy, not math verification
- Reduces false-approval rate from ~50% to <5%
- Saves ~85 minutes per arithmetic error caught
- Frontend receives mathematically verified narratives

---

## Stage 1: Backend Implementation

### Developer Actions

1. ✅ Implement algorithm tracer (inherit from `AlgorithmTracer`)
2. ✅ Implement `generate_narrative()` method (REQUIRED - v2.0)
3. ✅ Run backend unit tests
4. ✅ Generate narratives for ALL registered examples
5. ✅ Self-review narratives for logical completeness
6. ✅ **Submit narratives to FAA audit (NEW - v2.1)**
7. ✅ **Fix arithmetic errors, regenerate until FAA passes (NEW - v2.1)**
8. ✅ Complete Backend Compliance Checklist
9. ✅ Submit PR with code, FAA-approved narratives, and checklist

### Deliverables

```
backend/algorithms/my_algorithm.py
├── MyAlgorithmTracer class
│   ├── execute()
│   ├── get_prediction_points()
│   ├── _get_visualization_state()
│   └── generate_narrative()  ← REQUIRED (v2.0)

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

## Stage 1.5: Forensic Arithmetic Audit (NEW - v2.1)

### Quality Gate: Mathematical Verification

**Timing:** After backend generates narratives, before QA review  
**Validator:** Backend developer using `FAA_PERSONA.md`  
**Purpose:** Catch arithmetic errors before human QA review

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
- ❌ Pedagogical quality (QA handles this in Stage 2)
- ❌ Narrative completeness (QA handles this in Stage 2)
- ❌ Writing style or clarity (QA handles this in Stage 2)
- ❌ Logical flow (QA handles this in Stage 2)

### Decision Gate

- **✅ APPROVED** → Proceed to Stage 2 (QA Narrative Review)
- **❌ REJECTED** → Return to Stage 1 (Fix arithmetic, regenerate)

**Critical:** FAA is a BLOCKING gate. No narrative proceeds to QA with arithmetic errors.

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

## Stage 2: QA Narrative Review

### QA Engineer Role (v2.0, Enhanced in v2.1)

**CRITICAL:** QA does NOT look at JSON, code, or frontend in this stage.

**ONLY INPUT:** FAA-approved markdown narratives

**NEW in v2.1:** QA assumes arithmetic correctness has been verified by FAA.

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
❌ **Arithmetic correctness (FAA already validated) ← NEW in v2.1**

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

**Note:** Arithmetic errors should NOT appear here (FAA caught them in Stage 1.5).

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

1. ✅ Receive QA-approved backend code and FAA-approved narratives
2. ✅ Create or select visualization component
3. ✅ Register in visualization registry
4. ✅ Complete Frontend Compliance Checklist
5. ✅ Submit PR

### Changed Expectations in v2.1

- **Frontend should NOT discover missing data** (QA narrative review caught it)
- **Frontend should NOT discover arithmetic errors** (FAA caught them)
- **Frontend focuses on "how to render" not "what to render"**
- **FAA-approved narratives serve as mathematically verified reference**
- **Trust that JSON is logically complete AND arithmetically correct**

### Using Narratives as Reference (Optional but Recommended)

**Narratives are your "script":**
- **JSON is the fuel** (drives your React engine) ← PRIMARY
- **Markdown narratives provide context** (accelerates understanding) ← SUPPORTING

**When to reference narratives:**
- ✅ Understanding algorithm intent ("Why does this step happen?")
- ✅ Debugging visualization ("What should step 5 look like?")
- ✅ Verifying decision logic ("Is my rendering showing the right comparison?")
- ✅ Onboarding to new algorithm ("How does this work?")

**What narratives are NOT:**
- ❌ UI specifications (you have creative freedom - see mockups)
- ❌ Layout requirements (mockups govern visual standards)
- ❌ Binding constraints (JSON is the contract)
- ❌ Implementation instructions (you decide HOW to visualize)

---

## Stage 4: Integration Testing

### QA Engineer Actions

1. ✅ Run automated integration test suite (Suites 1-14)
2. ✅ Visual comparison to mockups
3. ✅ Cross-algorithm regression tests
4. ✅ Complete QA Integration Checklist

### Expected Outcome

**Zero "missing data" bugs** - narrative review should have caught them.  
**Zero "arithmetic error" bugs** - FAA should have caught them.

If integration tests find data issues or arithmetic errors, it indicates:
- Narrative review missed something (data completeness), OR
- FAA missed something (arithmetic correctness)

Both are unlikely but possible with edge cases.

---

## LOCKED Requirements

Cannot be changed without breaking platform architecture.

### Frontend LOCKED Elements

#### Modal Dimensions (🔒 Hardcoded in CSS)

**Source:** `docs/static_mockup/prediction_modal_mockup.html`, `docs/static_mockup/completion_modal_mockup.html`

```css
/* Prediction Modal */
#prediction-modal {
  width: 600px;
  max-height: 80vh;
  /* All modals MUST use these exact dimensions */
}

/* Completion Modal */
#completion-modal {
  width: 600px;
  max-height: 80vh;
  /* All modals MUST use these exact dimensions */
}
```

**Why LOCKED:** Ensures consistent UX, prevents modal overflow bugs.

#### HTML IDs (🔒 Required for Testing & Accessibility)

**Source:** All static mockups

```html
<!-- Required IDs - DO NOT CHANGE -->
<div id="prediction-modal">...</div>
<div id="completion-modal">...</div>
<div id="step-current">Step {N}</div>
```

**Why LOCKED:** Automated tests rely on these IDs. Changing them breaks test suite.

#### Keyboard Shortcuts (🔒 Platform-Wide)

**Source:** `docs/static_mockup/algorithm_page_mockup.html`

```javascript
// Required shortcuts - ALL algorithms must support
'ArrowRight' → Next step
'ArrowLeft'  → Previous step
'r'          → Reset
'k' or 'c'   → Select prediction choice K/C
's'          → Skip prediction
```

**Why LOCKED:** Consistent user experience across all algorithms.

#### Overflow Pattern (🔒 Fixed Layout Bug)

**Source:** Frontend debugging session

```jsx
// ❌ WRONG - Cuts off left edge
<div className="... items-center overflow-auto">
  <svg>...</svg>
</div>

// ✅ CORRECT - Full scrollable area
<div className="... items-start overflow-auto">
  <div className="mx-auto">
    <svg>...</svg>
  </div>
</div>
```

**Why LOCKED:** `items-center` + `overflow-auto` causes layout bug where left edge is cut off.

#### Panel Ratio (🔒 30-70 Split)

**Source:** `docs/static_mockup/algorithm_page_mockup.html`

```jsx
<div className="grid grid-cols-[30%_70%]">
  <div>{/* Left: Controls */}</div>
  <div>{/* Right: Visualization */}</div>
</div>
```

**Why LOCKED:** Optimized for readability on standard displays.

---

## CONSTRAINED Requirements

Must follow contract, but flexible in implementation.

### Backend Trace Contract

#### Metadata Structure (🎨 Required Fields)

```python
self.metadata = {
    'algorithm': 'my-algorithm',           # REQUIRED
    'display_name': 'My Algorithm',        # REQUIRED
    'visualization_type': 'array',         # REQUIRED: array|timeline|graph|tree
    'input_size': 20                       # REQUIRED
}
```

#### Trace Steps (🎨 Required Structure)

```python
{
    'step': 0,                   # REQUIRED: 0-indexed
    'type': 'COMPARE',           # REQUIRED: algorithm-defined
    'description': '...',        # REQUIRED: human-readable
    'data': {
        'visualization': {...}   # REQUIRED: current state
    }
}
```

#### Visualization Data Patterns

##### Array Algorithms (visualization_type: "array")

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

##### Timeline Algorithms (visualization_type: "timeline")

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

##### Graph Algorithms (visualization_type: "graph") - Future

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

### Narrative Generation (REQUIRED - v2.0, Enhanced v2.1)

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
        - Pass FAA arithmetic audit (v2.1)
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
- **All arithmetic must be correct (FAA will verify) ← NEW v2.1**
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
3. Implement `generate_narrative()`
4. Register in `registry.py`
5. Generate narratives for all examples
6. **Submit to FAA audit (v2.1)**
7. **Fix arithmetic errors, regenerate until FAA passes (v2.1)**
8. Complete Backend Checklist

**FAA Audit (Stage 1.5) - NEW v2.1:**
1. Use `FAA_PERSONA.md` to audit narratives
2. Verify all arithmetic claims
3. Reject if errors found
4. Backend fixes and resubmits
5. Approve when arithmetic verified

**QA (Stage 2):**
1. Review FAA-approved narratives for logical completeness
2. Check temporal coherence
3. Verify decision transparency
4. APPROVE or REJECT with specific feedback
5. **Assume arithmetic already verified (v2.1)**

**Frontend (Stage 3):**
1. Receive FAA+QA approved narratives
2. Select or create visualization component
3. Register in visualization registry
4. Complete Frontend Checklist
5. **Trust arithmetic correctness (v2.1)**

**QA (Stage 4):**
1. Run integration tests
2. Visual comparison to mockups
3. Regression testing

### Checklist Locations

- Backend: `docs/compliance/BACKEND_CHECKLIST.md`
- **FAA Audit: `docs/compliance/FAA_PERSONA.md` ← NEW v2.1**
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
- ❌ **Arithmetic errors in narratives (FAA will catch) ← NEW v2.1**
- ❌ Modifying `base_tracer.py` for algorithm-specific code

**Frontend:**
- ❌ Using `items-center` + `overflow-auto` (cuts off left edge)
- ❌ Different modal widths
- ❌ Multiple elements with `id="step-current"`
- ❌ Ignoring keyboard shortcuts in input fields
- ❌ Deviating from mockups without justification

---

## Migration Notes

**From WORKFLOW.md v2.0 to v2.1:**

- Added Stage 1.5: Forensic Arithmetic Audit (FAA)
- Added FAA_PERSONA.md reference
- Updated Stage 2 to assume arithmetic pre-verified
- Updated Stage 3 to note FAA-approved narratives
- Updated workflow diagrams
- Preserved all v2.0 functionality

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

| Version | Date       | Changes                                                                          |
| ------- | ---------- | -------------------------------------------------------------------------------- |
| 2.1     | Session 35 | Added Stage 1.5 (FAA gate), updated all stages to reflect FAA integration       |
| 2.0     | Session 34 | Initial WORKFLOW.md, narrative workflow added, replaces TENANT_GUIDE.md         |
| 1.0     | Session 15 | TENANT_GUIDE.md (now deprecated)                                                 |

---

**Document Status:** ✅ ACTIVE - Single Source of Truth  
**Next Review:** When adding new algorithm types (graph, tree) or major workflow changes

---
