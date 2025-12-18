# Frontend Team: Iterative Template Migration

**To:** Frontend Development Team  
**From:** ActionPlan PM  
**Date:** December 18, 2025  
**Subject:** APPROVED - Migration to Dual-Mode Architecture: Iterative Template Implementation  
**Priority:** High  
**Timeline:** 2 weeks (20 dev hours total)

---

## Executive Summary

The Right-Hand Panel redesign has been **approved for implementation** using a dual-mode architecture. This email outlines your responsibilities for migrating three existing algorithms to the new **Iterative Metrics** template.

**What's changing:** ONLY the Right-Hand Panel (RHP) layout for Binary Search, Sliding Window, and Two Pointer. Everything else stays the same.

**What's NOT changing:**
- ✅ Left-Hand Panel (visualization) - unchanged
- ✅ Control bar, navigation, keyboard shortcuts - unchanged
- ✅ Prediction modal, completion modal - unchanged
- ✅ Backend trace data structure - unchanged
- ✅ Registry system, component architecture - unchanged
- ✅ Interval Coverage algorithm - unchanged (stays in recursive template)

**The ONLY change:** Right-Hand Panel adopts 2:1 ratio layout (Metrics : Narrative) from `iterative_metrics_algorithm_mockup.html` for the three iterative algorithms.

**Why:** User testing shows metric comprehension improves 5x (8 seconds → 2 seconds) with the iterative layout for simple algorithms.

---

## Migration Scope

### What's Changing: ONLY Right-Hand Panel (RHP)

**CRITICAL:** This is a **Right-Hand Panel ONLY** migration. Everything else in the platform remains unchanged.

| Component | Status | Notes |
|-----------|--------|-------|
| **Right-Hand Panel** | ✏️ CHANGING | Adopts iterative template (2:1 ratio layout) |
| Left-Hand Panel | ✅ UNCHANGED | ArrayView visualization stays exactly the same |
| Control Bar | ✅ UNCHANGED | Navigation buttons, reset, all controls stay the same |
| Prediction Modal | ✅ UNCHANGED | Modal behavior, keyboard shortcuts unchanged |
| Completion Modal | ✅ UNCHANGED | Success screen unchanged |
| Keyboard Shortcuts | ✅ UNCHANGED | All shortcuts (→←, R, K/C/S) remain the same |
| Backend API | ✅ UNCHANGED | Trace structure, endpoints unchanged |
| Registry System | ✅ UNCHANGED | `stateRegistry.js` entries unchanged |
| Other Algorithms | ✅ UNCHANGED | Interval Coverage stays in recursive template |

### Algorithms to Migrate (RHP Only)

| Algorithm | Current RHP Component | Target Template | Estimated Time |
|-----------|----------------------|----------------|----------------|
| **Binary Search** | `BinarySearchState.jsx` | Iterative Metrics (RHP only) | 3 hours |
| **Sliding Window** | `SlidingWindowState.jsx` | Iterative Metrics (RHP only) | 3.5 hours |
| **Two Pointer** | `TwoPointerState.jsx` | Iterative Metrics (RHP only) | 3.5 hours |

**Total implementation time:** 10 hours (Phase 3 of 4-phase rollout)

**Scope clarification:**
- You are ONLY modifying the state components in `algorithm-states/` directory
- Left-Hand Panel visualizations (`ArrayView.jsx`, `TimelineView.jsx`) remain untouched
- No changes to `visualizationRegistry.js`
- No changes to `App.jsx`, contexts, hooks, or shared components

---

## Visual Standards (CRITICAL)

### Reference Document

**LOCKED Visual Source of Truth:**
```
docs/static_mockup/iterative_metrics_algorithm_mockup.html
```

**YOU MUST:**
- ✅ Follow this mockup exactly for layout, spacing, typography, colors
- ✅ Maintain 2:1 ratio (Metrics section : Narrative section)
- ✅ Use LOCKED overflow pattern (`items-start` + `mx-auto`)
- ✅ Preserve LOCKED modal IDs and keyboard shortcuts
- ❌ DO NOT deviate without PM approval

**Reference WORKFLOW.md Section 3.3:**
> "Visual Compliance: UI follows static mockup specifications (docs/static_mockup/*.html). No deviation from established visual patterns without justification."

---

## Implementation Requirements

### Component Structure Pattern

Each migrated component MUST follow this structure:

**REMINDER: You are ONLY modifying the Right-Hand Panel component. Left-Hand Panel (ArrayView) remains unchanged.**

```javascript
// Example: BinarySearchState.jsx (Iterative Metrics Mode - RHP ONLY)

import React from 'react';
import PropTypes from 'prop-types';

const BinarySearchState = ({ step, trace }) => {
  // Early return if no data
  if (!step?.data?.visualization) {
    return <div>No state data available</div>;
  }

  // Extract visualization data
  const vizData = step.data.visualization;
  const metadata = trace?.metadata;

  return (
    // ⚠️ THIS IS THE ONLY THING CHANGING - RHP layout adapts iterative template
    <div className="h-full flex flex-col">
      {/* CRITICAL: 2:1 Ratio Layout from iterative_metrics mockup */}
      
      {/* Metrics Section (2/3 height) - NEW LAYOUT */}
      <div className="h-2/3 border-b">
        {/* Frontend Developer: Implement metrics display
            Requirements:
            - Display ≤6 key numeric state variables
            - Follow typography/spacing from mockup
            - Use LOCKED overflow pattern if needed
        */}
      </div>

      {/* Narrative Section (1/3 height) - NEW LAYOUT */}
      <div className="h-1/3">
        {/* Frontend Developer: Implement narrative display
            Requirements:
            - Show step description from step.description
            - Auto-scroll to current step
            - Follow mockup text styles
        */}
      </div>
    </div>
  );
};

BinarySearchState.propTypes = {
  step: PropTypes.shape({
    data: PropTypes.shape({
      visualization: PropTypes.object,
    }),
    description: PropTypes.string,
  }).isRequired,
  trace: PropTypes.shape({
    metadata: PropTypes.object,
  }),
};

export default BinarySearchState;
```

**What stays the same:**
- ✅ Props interface: `{ step, trace }` - unchanged
- ✅ Data extraction: `step.data.visualization` - unchanged
- ✅ PropTypes validation - same pattern
- ✅ Component exports - same
- ✅ Context-agnostic architecture - unchanged

**What changes:**
- ✏️ Internal JSX layout - adopts 2:1 ratio from iterative template
- ✏️ Metrics section prominence - moves to top 2/3
- ✏️ Narrative section position - bottom 1/3

### LOCKED Requirements (Cannot Change)

From WORKFLOW.md, these are **non-negotiable:**

#### 1. Overflow Pattern
```javascript
// ✅ CORRECT: Prevents left-side cutoff
<div className="h-full flex flex-col items-start overflow-auto py-4 px-6">
  <div className="mx-auto">
    {/* content centers but doesn't cut off */}
  </div>
</div>

// ❌ INCORRECT: Causes overflow cutoff on left side
<div className="h-full flex flex-col items-center overflow-auto">
  {/* content gets cut off */}
</div>
```

#### 2. Props Interface
- MUST accept: `{ step, trace }`
- MUST extract data from: `step.data.visualization`
- MUST access metadata from: `trace.metadata`
- MUST be context-agnostic (no direct context consumption)

#### 3. Component Organization
- Components remain in: `frontend/src/components/algorithm-states/`
- Naming convention: `{AlgorithmName}State.jsx` (no changes)
- Registry entries: No changes to `stateRegistry.js`
- **Left-Hand Panel components**: No changes to `visualizations/` directory

#### 4. Keyboard Shortcuts (Platform-Wide)
All shortcuts MUST continue working:
- `→` / `Space` → Next step
- `←` → Previous step  
- `R` / `Home` → Reset
- `End` → Jump to end
- `K`, `C`, `S` → Prediction mode

---

## Implementation Process

### Phase 3: Component Implementation (Your Work)

**Duration:** 10 hours over Week 1-2

#### Step 1: Setup (30 minutes)
1. Pull latest from `main` branch
2. Create feature branch: `feature/iterative-template-migration`
3. Verify mockup exists: `cat docs/static_mockup/iterative_metrics_algorithm_mockup.html`
4. Review WORKFLOW.md Stage 3 requirements

#### Step 2: Migrate Components (3-3.5 hours each)

**For each algorithm (Binary Search, Sliding Window, Two Pointer):**

1. **Backup current component** (5 min)
   ```bash
   cp src/components/algorithm-states/BinarySearchState.jsx \
      src/components/algorithm-states/BinarySearchState.jsx.backup
   ```

2. **Review backend trace data** (15 min)
   ```bash
   # Verify what data is available
   curl -X POST http://localhost:5000/api/trace/unified \
     -H "Content-Type: application/json" \
     -d '{"algorithm": "binary-search", "input": {"array": [1,3,5,7,9], "target": 5}}' | jq '.trace.steps[0].data.visualization'
   ```

3. **Identify key metrics** (10 min)
   - Extract ≤6 numeric state variables from `step.data.visualization`
   - Examples: `left`, `right`, `mid`, `target`, `comparisons`, `current_sum`

4. **Implement 2:1 layout** (90 min)
   - **ONLY modify Right-Hand Panel (RHP) JSX structure**
   - Follow `iterative_metrics_algorithm_mockup.html` exactly
   - Metrics section: 2/3 height, display numeric state
   - Narrative section: 1/3 height, show `step.description`
   - **DO NOT touch Left-Hand Panel (ArrayView) - it stays the same**

5. **Handle edge cases** (30 min)
   - Missing data (early return pattern)
   - Undefined metrics (graceful fallback)
   - PropTypes validation

6. **Manual testing** (30 min)
   - Test with all example inputs
   - Verify overflow pattern works
   - Check keyboard shortcuts still function
   - Test prediction mode integration

#### Step 3: Quality Assurance (1 hour)

Complete Frontend Compliance Checklist for each component:

- [ ] Component functionality
  - [ ] Renders without errors
  - [ ] Handles missing/malformed data gracefully
  - [ ] PropTypes defined and validated

- [ ] Visual compliance
  - [ ] Follows `iterative_metrics_algorithm_mockup.html` exactly
  - [ ] 2:1 ratio maintained (Metrics : Narrative)
  - [ ] Typography matches mockup
  - [ ] Spacing/padding matches mockup
  - [ ] No deviation from mockup without PM approval

- [ ] Architectural compliance
  - [ ] Component in `algorithm-states/` directory
  - [ ] Naming convention followed
  - [ ] Context-agnostic (uses props, not contexts)
  - [ ] LOCKED overflow pattern used

- [ ] Regression testing
  - [ ] Existing functionality preserved
  - [ ] Keyboard shortcuts work
  - [ ] Prediction mode works
  - [ ] No visual regressions in other algorithms
  - [ ] **Left-Hand Panel (ArrayView) unchanged and still renders correctly**
  - [ ] **Control bar, modals, navigation all unchanged**

#### Step 4: Handoff to QA (Stage 4)

**Deliverables to QA Engineer:**

1. ✅ Three migrated RHP components (BinarySearchState, SlidingWindowState, TwoPointerState)
2. ✅ Completed Frontend Compliance Checklist (one per algorithm)
3. ✅ Testing notes documenting edge cases handled
4. ✅ Screenshots comparing old RHP vs new RHP layout

**QA will verify:**
- Full algorithm flow end-to-end
- Visual correctness (RHP matches mockup)
- UI interactions (keyboard shortcuts, predictions)
- No regressions in existing algorithms (Interval Coverage should be unaffected)
- **Left-Hand Panel still renders correctly (unchanged)**
- **Control bar, modals still function correctly (unchanged)**

---

## Timeline & Milestones

### Week 1 (December 18-22, 2025)
- **Day 1-2:** Binary Search migration (3 hours)
- **Day 3-4:** Sliding Window migration (3.5 hours)
- **Day 5:** Testing & documentation (1 hour)

### Week 2 (December 23-29, 2025)
- **Day 1-2:** Two Pointer migration (3.5 hours)
- **Day 3:** Final QA & checklist completion (1 hour)
- **Day 4:** Handoff to QA (Stage 4)
- **Day 5:** Integration testing complete

**Target completion:** December 29, 2025

---

## Risk Mitigation

### Known Risks & Mitigation Strategies

**Risk 1: Mockup not ready**
- **Mitigation:** If `iterative_metrics_algorithm_mockup.html` doesn't exist, STOP and notify PM immediately. Do not proceed with implementation.
- **Fallback:** Phase 1 (mockup creation) must complete before Phase 3.

**Risk 2: Backend data insufficient for ≤6 metrics**
- **Mitigation:** If trace data doesn't contain required metrics, coordinate with Backend Developer to add to `step.data.visualization`.
- **Reference:** WORKFLOW.md Stage 1 - Backend Implementation.

**Risk 3: Breaking existing functionality**
- **Mitigation:** Create backup files before modification. Run full regression test suite before handoff to QA.

**Risk 4: Inconsistent visual implementation**
- **Mitigation:** PM will conduct visual compliance review before QA handoff. Any deviations require PM approval.

---

## Success Criteria

Migration is considered complete when:

- ✅ All 3 algorithms render correctly in iterative template
- ✅ Visual compliance verified against mockup (PM approval)
- ✅ Frontend Compliance Checklist completed for each algorithm
- ✅ No regressions in existing algorithms (Interval Coverage unaffected)
- ✅ QA Integration Checklist passes (Stage 4)
- ✅ Metric comprehension improvement measured (target: 5x faster)

---

## Support & Resources

### Documentation
- **Visual Standard:** `docs/static_mockup/iterative_metrics_algorithm_mockup.html`
- **Workflow:** `docs/compliance/WORKFLOW.md` (Stage 3)
- **Frontend Checklist:** `docs/compliance/FRONTEND_CHECKLIST.md`
- **ADRs:** 
  - `docs/ADR/FRONTEND/ADR-001-registry-based-architecture.md`
  - `docs/ADR/FRONTEND/ADR-002-component-organization-principles.md`

### Questions?
- **Visual compliance questions:** Tag PM in PR with mockup reference
- **Backend data questions:** Coordinate with Backend Developer
- **Architecture questions:** Reference WORKFLOW.md or escalate to PM

### Code Review
- **Reviewer:** PM (visual compliance) + Lead Developer (technical review)
- **Approval required:** Both PM and Lead Dev must approve before QA handoff

---

## Important Reminders

1. **THIS IS A RIGHT-HAND PANEL ONLY MIGRATION** - Left-Hand Panel, control bar, modals, navigation all stay the same
2. **NEVER deviate from mockup** without PM approval - visual consistency is LOCKED
3. **ONLY modify algorithm-states/ components** - do not touch visualizations/, contexts/, hooks/, or shared components
4. **ALWAYS use LOCKED overflow pattern** - prevents left-side cutoff bugs
5. **ALWAYS complete Frontend Compliance Checklist** - required for Stage 4 handoff
6. **DO NOT modify registry entries** - algorithm IDs remain unchanged
7. **DO NOT break keyboard shortcuts** - platform-wide LOCKED requirement
8. **ASSUME arithmetic correctness** - narratives already passed FAA audit (Stage 1.5)
9. **DO NOT modify ArrayView, TimelineView, or any Left-Hand Panel components** - they remain unchanged

---

## Next Steps

**Immediate Actions (Today):**
1. ✅ Acknowledge receipt of this email
2. ✅ Review `docs/static_mockup/iterative_metrics_algorithm_mockup.html`
3. ✅ Review WORKFLOW.md Stage 3 requirements
4. ✅ Create feature branch: `feature/iterative-template-migration`
5. ✅ Confirm mockup exists (if not, notify PM immediately)

**This Week:**
- Start Binary Search migration (Day 1-2)
- Complete Sliding Window migration (Day 3-4)
- Begin testing & documentation (Day 5)

**Questions or blockers?** Reply to this email or tag PM in Slack.

---

**Let's ship this! 🚀**

ActionPlan PM  
Algorithm Visualization Platform