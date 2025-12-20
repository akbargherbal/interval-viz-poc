# Merge Sort Frontend Implementation Plan

**Created:** 2024-12-19  
**Status:** APPROVED - Ready for Implementation  
**Estimated Time:** 2-3 sessions (~90-120 minutes total)

---

## 📋 Session Context Preservation

### Critical Decisions Already Made:

1. ✅ **Template Classification:** RECURSIVE (not iterative)
2. ✅ **Architecture Pattern:** Stacked call cards with depth indentation
3. ✅ **Static Mockup:** Approved recursive template design
4. ✅ **Backend Complete:** Narratives generated, FAA approved, PE approved
5. ✅ **Visualization:** Reuse existing `TimelineView` component (no changes needed)

### Key Files to Reference:

- **Static Mockup:** `/mnt/user-data/outputs/merge_sort_recursive_template_mockup.html`
- **Narrative Example:** `docs/narratives/merge-sort/example_1_basic_8_elements.md`
- **Recursive Template:** `docs/static_mockup/recursive_context_algorithm_mockup.html`
- **Backend Registry:** `backend/algorithms/registry.py` (merge-sort registered)
- **Backend Tracer:** `backend/algorithms/merge_sort.py`

---

## 🎯 Implementation Phases

### **PHASE 1: Component Scaffolding** (Session 1, ~20 minutes)

**Objective:** Create the base component structure with proper imports and PropTypes

**Files to Create:**
1. `frontend/src/components/algorithm-states/MergeSortState.jsx`

**Implementation Steps:**

```jsx
// File: frontend/src/components/algorithm-states/MergeSortState.jsx

import React from "react";
import PropTypes from "prop-types";
import { useTrace, useNavigation } from "@/contexts";

/**
 * MergeSortState - Recursive algorithm state display
 * 
 * Displays merge sort execution as stacked call cards with depth indentation.
 * Follows recursive template pattern from Interval Coverage algorithm.
 * 
 * Key Features:
 * - Each trace step = one card in the stack
 * - Depth-based indentation (depth × 24px)
 * - Current step highlighted with #step-current ID
 * - Operation-specific card layouts (SPLIT, BASE, MERGE, COMPARE, etc.)
 * 
 * Data Structure:
 * - step.type: Operation type (SPLIT_ARRAY, BASE_CASE, MERGE_START, etc.)
 * - step.data.depth: Recursion depth (0-3 typical)
 * - step.data.array: Current array being processed
 * - step.data.left_half / right_half: Split results
 * - step.data.left / right: Arrays being merged
 */
const MergeSortState = ({ step, trace }) => {
  // Early return for no data
  if (!trace?.steps || trace.steps.length === 0) {
    return (
      <div className="text-gray-400 text-sm p-4">
        No trace data available
      </div>
    );
  }

  const { steps } = trace;
  const currentStepIndex = step?.step ?? 0;

  return (
    <div className="space-y-2">
      {steps.map((s, index) => {
        const isCurrent = index === currentStepIndex;
        const depth = s.data?.depth ?? 0;
        const indentation = depth * 24; // 24px per depth level

        return (
          <StepCard
            key={index}
            step={s}
            isCurrent={isCurrent}
            indentation={indentation}
          />
        );
      })}
    </div>
  );
};

// PropTypes definition
MergeSortState.propTypes = {
  step: PropTypes.shape({
    step: PropTypes.number,
    type: PropTypes.string,
    data: PropTypes.object,
  }).isRequired,
  trace: PropTypes.shape({
    steps: PropTypes.arrayOf(PropTypes.object).isRequired,
    metadata: PropTypes.object,
  }).isRequired,
};

export default MergeSortState;
```

**Sub-component to create:**
```jsx
/**
 * StepCard - Individual step card component
 * Renders different layouts based on step.type
 */
const StepCard = ({ step, isCurrent, indentation }) => {
  const cardClasses = `
    card p-3 rounded-lg border-2 transition-all
    ${isCurrent 
      ? 'border-yellow-400 bg-yellow-900/20 shadow-lg' 
      : 'border-slate-600 bg-slate-800'
    }
  `;

  return (
    <div
      id={isCurrent ? 'step-current' : undefined}
      className={cardClasses}
      style={{ marginLeft: `${indentation}px` }}
    >
      {renderCardContent(step)}
    </div>
  );
};
```

**Validation Checklist:**
- [ ] Component file created in correct directory
- [ ] Imports are correct (React, PropTypes, contexts)
- [ ] PropTypes defined for step and trace
- [ ] Early return for missing data
- [ ] Basic structure renders without errors

---

### **PHASE 2: Step Type Handlers** (Session 1, ~30 minutes)

**Objective:** Implement `renderCardContent()` function with handlers for each step type

**Step Types from Backend:**
- `INITIAL_STATE`
- `SPLIT_ARRAY`
- `BASE_CASE`
- `MERGE_START`
- `COMPARE`
- `TAKE_LEFT` / `TAKE_RIGHT`
- `APPEND_REMAINING`
- `MERGE_COMPLETE`
- `COMPLETE`

**Implementation Pattern:**

```jsx
const renderCardContent = (step) => {
  switch (step.type) {
    case 'INITIAL_STATE':
      return <InitialStateCard step={step} />;
    case 'SPLIT_ARRAY':
      return <SplitCard step={step} />;
    case 'BASE_CASE':
      return <BaseCard step={step} />;
    case 'MERGE_START':
      return <MergeStartCard step={step} />;
    case 'COMPARE':
      return <CompareCard step={step} />;
    case 'TAKE_LEFT':
    case 'TAKE_RIGHT':
      return <TakeCard step={step} />;
    case 'APPEND_REMAINING':
      return <AppendCard step={step} />;
    case 'MERGE_COMPLETE':
      return <MergeCompleteCard step={step} />;
    case 'COMPLETE':
      return <CompleteCard step={step} />;
    default:
      return <DefaultCard step={step} />;
  }
};
```

**Each Card Component Template:**

```jsx
const SplitCard = ({ step }) => {
  const { array, left_half, right_half, depth } = step.data;

  return (
    <>
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <span className="op-badge badge-split">🔀 SPLIT</span>
        <span className="text-xs text-slate-400">Depth: {depth}</span>
      </div>

      {/* Array Being Split */}
      <div className="text-xs text-slate-400 mb-1">
        Array: <ArrayDisplay array={array} size="xs" />
      </div>

      {/* Split Result */}
      <div className="flex gap-2">
        <div className="flex-1 bg-blue-900/30 rounded p-1.5">
          <span className="text-xs text-blue-400">
            L: <ArrayDisplay array={left_half} size="xs" />
          </span>
        </div>
        <div className="flex-1 bg-blue-900/30 rounded p-1.5">
          <span className="text-xs text-blue-400">
            R: <ArrayDisplay array={right_half} size="xs" />
          </span>
        </div>
      </div>
    </>
  );
};
```

**Reusable Components to Create:**

```jsx
// Displays array elements with proper formatting
const ArrayDisplay = ({ array, size = "sm" }) => {
  if (!array || array.length === 0) return <span>[]</span>;
  
  const sizeClasses = {
    xs: "text-xs",
    sm: "text-sm",
    md: "text-base"
  };

  return (
    <span className={`font-mono text-white ${sizeClasses[size]}`}>
      [{array.join(', ')}]
    </span>
  );
};

// Operation badge component
const OperationBadge = ({ type, icon, label }) => {
  const badgeClasses = {
    split: "badge-split",
    base: "badge-base",
    merge: "badge-merge",
    compare: "badge-compare",
    complete: "badge-complete"
  };

  return (
    <span className={`op-badge ${badgeClasses[type]}`}>
      {icon} {label}
    </span>
  );
};
```

**Card Implementations Priority Order:**
1. `SplitCard` (most common)
2. `BaseCard` (simplest)
3. `MergeStartCard`
4. `CompareCard` (most complex - shows comparison decision)
5. `MergeCompleteCard`
6. `TakeCard` / `AppendCard` (optional - can skip initially)
7. `InitialStateCard` / `CompleteCard`

**Validation Checklist:**
- [ ] All step types have handlers
- [ ] Cards render with correct data
- [ ] Depth-based indentation works
- [ ] Operation badges display correctly
- [ ] Arrays display properly (not [object Object])

---

### **PHASE 3: Styling & Visual Polish** (Session 1, ~15 minutes)

**Objective:** Add CSS classes and ensure visual consistency with mockup

**CSS Classes to Add:**

```jsx
// In MergeSortState.jsx (top-level style or Tailwind config)
const styles = `
  .op-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-weight: 700;
    font-size: 0.75rem;
    text-transform: uppercase;
  }
  .badge-split { background-color: #3b82f6; color: white; }
  .badge-base { background-color: #8b5cf6; color: white; }
  .badge-merge { background-color: #10b981; color: white; }
  .badge-compare { background-color: #f59e0b; color: white; }
  .badge-complete { background-color: #06b6d4; color: white; }
  
  .card {
    transition: all 0.2s ease;
  }
  .card:hover {
    transform: translateX(4px);
  }
`;
```

**Alternative (Tailwind-only approach):**
```jsx
const getBadgeClasses = (type) => {
  const baseClasses = "inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-bold uppercase";
  const typeClasses = {
    split: "bg-blue-600 text-white",
    base: "bg-purple-600 text-white",
    merge: "bg-green-600 text-white",
    compare: "bg-amber-500 text-white",
    complete: "bg-cyan-600 text-white"
  };
  return `${baseClasses} ${typeClasses[type] || "bg-slate-600 text-white"}`;
};
```

**Validation Checklist:**
- [ ] Colors match approved mockup
- [ ] Indentation is exactly 24px per depth level
- [ ] Current step has yellow border
- [ ] Hover effects work (subtle translateX)
- [ ] Text is readable (sufficient contrast)

---

### **PHASE 4: Registry Integration** (Session 2, ~10 minutes)

**Objective:** Register component in state registry

**File to Modify:**
- `frontend/src/utils/stateRegistry.js`

**Changes:**

```javascript
// Add import at top
import MergeSortState from "../components/algorithm-states/MergeSortState";

// Add to STATE_REGISTRY object
const STATE_REGISTRY = {
  'binary-search': BinarySearchState,
  'interval-coverage': IntervalCoverageState,
  'merge-sort': MergeSortState,  // ← ADD THIS LINE
};
```

**Validation:**
- [ ] Import path is correct
- [ ] Key matches backend algorithm name ('merge-sort')
- [ ] No console errors on app load
- [ ] Component appears in algorithm switcher

---

### **PHASE 5: Algorithm Info Markdown** (Session 2, ~10 minutes)

**Objective:** Create algorithm information page

**File to Create:**
- `frontend/public/algorithm-info/merge-sort.md`

**Content Template:**

```markdown
# Merge Sort

## Overview

Merge Sort is a **divide-and-conquer** sorting algorithm that recursively splits an array into smaller subarrays, sorts them, and merges them back together. It guarantees **O(n log n)** time complexity in all cases (best, average, and worst).

## How It Works

### 1. Divide Phase
- Recursively split the array in half until each subarray contains only one element
- A single element is considered already sorted (base case)

### 2. Conquer Phase
- Merge pairs of sorted subarrays back together
- During merge, compare front elements from each subarray
- Always take the smaller element to maintain sorted order

### 3. Combine Phase
- Continue merging larger and larger sorted subarrays
- Build solution bottom-up from base cases to final sorted array

## Time Complexity

- **Best Case:** O(n log n)
- **Average Case:** O(n log n)
- **Worst Case:** O(n log n)

*Merge sort's time complexity is **guaranteed** - it doesn't depend on input order.*

## Space Complexity

- **O(n)** - Requires auxiliary arrays for merging

## Key Concepts

### Divide and Conquer
- Break problem into smaller subproblems
- Solve subproblems recursively
- Combine solutions to solve original problem

### Recursion Tree
- Each level of recursion represents a depth level
- Tree height is log₂(n) where n is array size
- Total work per level is O(n) (merge operations)
- Total work: O(n) × log₂(n) levels = O(n log n)

### Stable Sorting
Merge sort is **stable** - equal elements maintain their relative order from the original array.

## When to Use Merge Sort

**Good For:**
- Guaranteed O(n log n) performance required
- Stable sorting needed
- Sorting linked lists (O(1) extra space)
- External sorting (large datasets on disk)

**Not Ideal For:**
- Small arrays (overhead of recursion)
- Memory-constrained environments (O(n) space)
- In-place sorting required (use Quick Sort or Heap Sort)

## Visualization Tips

- Watch the **recursion depth** - shows divide phase progressing
- Track **merge operations** - shows how sorted subarrays combine
- Notice **comparison decisions** - smaller element always goes first
- Observe **bottom-up building** - solution emerges from leaves to root

## Example Trace

```
Input: [38, 27, 43, 3]

Split Phase:
  [38, 27, 43, 3]
    ↓
  [38, 27] | [43, 3]
    ↓          ↓
  [38] [27]  [43] [3]  ← Base cases

Merge Phase:
  [27, 38]  [3, 43]  ← Merge pairs
    ↓
  [3, 27, 38, 43]    ← Final merge
```

## Practice Exercises

1. **Trace Prediction:** Given `[5, 2, 8, 1]`, predict the first merge operation
2. **Complexity Analysis:** Why is space complexity O(n) not O(log n)?
3. **Stability Test:** How does merge sort maintain stable ordering?
4. **Optimization:** Can you reduce space complexity for linked lists?

## Related Algorithms

- **Quick Sort:** Another O(n log n) divide-and-conquer sort (in-place, but unstable)
- **Heap Sort:** O(n log n) comparison sort (in-place, but unstable)
- **Tim Sort:** Hybrid merge sort + insertion sort (used in Python/Java)
```

**Validation:**
- [ ] File created in correct directory
- [ ] Markdown renders properly in info modal
- [ ] Code blocks have syntax highlighting
- [ ] Links work (if any)

---

### **PHASE 6: Testing & Integration** (Session 2, ~30 minutes)

**Objective:** Test component with actual backend data and fix issues

**Test Cases to Validate:**

1. **Basic Rendering**
   ```bash
   # Start backend
   cd backend && python app.py
   
   # Start frontend
   cd frontend && npm run dev
   
   # Navigate to Merge Sort in algorithm switcher
   ```

2. **Data Structure Tests**
   - [ ] Initial state renders (Step 0)
   - [ ] Split steps show left/right halves
   - [ ] Base cases show single elements
   - [ ] Merge steps show arrays being combined
   - [ ] Depth indentation increases correctly
   - [ ] Current step has yellow border and #step-current ID

3. **Navigation Tests**
   - [ ] Arrow keys move through steps
   - [ ] Current step scrolls into view automatically
   - [ ] Step description updates correctly
   - [ ] Cards remain stable (no re-rendering flicker)

4. **Edge Cases**
   - [ ] Array with 4 elements (minimum)
   - [ ] Array with 12 elements (maximum)
   - [ ] Already sorted array
   - [ ] Reverse sorted array
   - [ ] Array with duplicates

5. **Visual Tests**
   - [ ] Cards align properly at all depths (0-3)
   - [ ] Text is readable and not cut off
   - [ ] Colors match mockup
   - [ ] No horizontal scrolling
   - [ ] Fits in 384px width (w-96)

**Common Issues & Fixes:**

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| "Cannot read property 'steps'" | Missing null check | Add `trace?.steps` with optional chaining |
| Arrays show `[object Object]` | Not calling `.join()` | Use `array.join(', ')` in ArrayDisplay |
| Indentation not working | Inline styles not applied | Check `style={{ marginLeft }}` syntax |
| Current step not highlighting | Wrong comparison | Check `index === currentStepIndex` |
| No auto-scroll | Missing ID | Verify `id="step-current"` on current card |
| Cards cut off | Overflow issue | Add `overflow-y-auto` to parent |

**Debug Commands:**

```javascript
// Add to component for debugging
console.log('MergeSortState render:', {
  totalSteps: steps.length,
  currentStep: currentStepIndex,
  firstStepType: steps[0]?.type,
  currentStepType: steps[currentStepIndex]?.type
});
```

---

### **PHASE 7: Final Validation** (Session 2-3, ~20 minutes)

**Objective:** Complete frontend checklist and verify compliance

**Checklist Items:**

**Component Organization (ADR-002):**
- [ ] Component in `algorithm-states/` directory
- [ ] Named `MergeSortState.jsx` (PascalCase + State suffix)
- [ ] Not in `visualizations/` directory

**Registry Integration (ADR-001):**
- [ ] Registered in `stateRegistry.js`
- [ ] Key matches backend (`merge-sort`)
- [ ] Component exported as default

**Context Usage (ADR-003):**
- [ ] Uses `useTrace()` or receives trace as prop
- [ ] Uses `useNavigation()` or receives step as prop
- [ ] No prop drilling for context data

**LOCKED Elements:**
- [ ] No keyboard shortcut conflicts
- [ ] Panel ratio respected (RIGHT panel is w-96)
- [ ] No horizontal overflow (`overflow-x-hidden`)

**Recursive Template Compliance:**
- [ ] Stacked cards pattern (not single dashboard)
- [ ] Depth indentation (24px per level)
- [ ] `#step-current` ID on active card
- [ ] Scrollable `#panel-steps-list`
- [ ] Fixed `#panel-step-description` at bottom

**Static Mockup Compliance:**
- [ ] Visual design matches approved mockup
- [ ] Colors: Blue (split), Purple (base), Green (merge), etc.
- [ ] Typography: `font-mono` for arrays, `font-sans` for labels
- [ ] Spacing: Consistent with existing algorithms

**Quality Assurance:**
- [ ] No console errors
- [ ] No console warnings
- [ ] PropTypes defined and validated
- [ ] Graceful degradation for missing data
- [ ] Responsive at different screen widths

---

## 🚀 Session Execution Guide

### **Session 1 Target: Phases 1-3 Complete**
- Create component file
- Implement core step type handlers
- Add styling
- **Deliverable:** Component renders locally (even if not fully integrated)

### **Session 2 Target: Phases 4-6 Complete**
- Register component
- Create algorithm info
- Test with backend
- Fix issues
- **Deliverable:** Fully functional integration

### **Session 3 Target: Phase 7 Complete** (if needed)
- Final polish
- Complete checklist
- Handle edge cases
- **Deliverable:** Production-ready component

---

## 📂 Quick Reference: File Locations

```
frontend/
├── src/
│   ├── components/
│   │   └── algorithm-states/
│   │       └── MergeSortState.jsx  ← CREATE THIS
│   └── utils/
│       └── stateRegistry.js        ← MODIFY THIS
└── public/
    └── algorithm-info/
        └── merge-sort.md           ← CREATE THIS

backend/
└── algorithms/
    └── merge_sort.py               ✅ ALREADY EXISTS
```

---

## 🎯 Success Criteria

**Component is complete when:**
1. ✅ Merge Sort appears in algorithm switcher
2. ✅ All 72 steps render as cards
3. ✅ Depth indentation works (0px, 24px, 48px, 72px)
4. ✅ Current step scrolls into view
5. ✅ Split/Base/Merge operations display correctly
6. ✅ No console errors
7. ✅ Algorithm info modal works
8. ✅ Visual design matches mockup
9. ✅ All checklist items pass
10. ✅ Works with all 6 backend examples

---

## 🔧 Development Commands

```bash
# Backend
cd backend
python app.py  # Runs on http://localhost:5000

# Frontend
cd frontend
npm run dev    # Runs on http://localhost:5173

# Verify backend registration
curl http://localhost:5000/api/algorithms | jq '.[] | select(.name=="merge-sort")'

# Test trace generation
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "merge-sort", "input": {"array": [38, 27, 43, 3, 9, 82, 10, 5]}}' \
  | jq '.trace.steps | length'
```

---

## 📝 Notes for Future Sessions

### Context to Preserve:
- This plan is the authoritative guide
- Static mockup approved: `/mnt/user-data/outputs/merge_sort_recursive_template_mockup.html`
- Template pattern: RECURSIVE (stacked cards, not single dashboard)
- Backend complete: No changes needed there

### If Session Gets Interrupted:
1. Note which phase was in progress
2. Document any deviations from this plan
3. List any issues encountered
4. Update this plan with lessons learned

### Potential Challenges:
- **Step type naming:** Backend may use slightly different names (e.g., `MERGE_BEGIN` vs `MERGE_START`)
- **Data structure:** May need to adjust field access paths (`step.data.left` vs `step.data.left_array`)
- **Depth calculation:** Verify backend provides `depth` field in all steps
- **Performance:** 72 steps rendering at once - may need React.memo() optimization

---

## ✅ Pre-Implementation Checklist

Before starting Session 1:
- [ ] Backend is running
- [ ] Frontend is running
- [ ] Can access Merge Sort via API (`/api/algorithms`)
- [ ] Have this plan open
- [ ] Have static mockup open for reference
- [ ] Have recursive template open for reference

---

**END OF PLAN**

*This plan is comprehensive but flexible. Adjust phases as needed based on actual implementation discoveries. The goal is working code, not perfect adherence to the plan.*
