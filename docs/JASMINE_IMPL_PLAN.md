# 📋 Merge Sort Visualization Implementation Plan - Jasmine (Prototype 03)

**Status:** APPROVED - Proceed with Implementation  
**Prototype:** Jasmine (Data-Rich Hierarchical View)  
**Estimated Total Time:** 155-185 minutes across 4 phases  
**Primary Owner:** Frontend Developer  
**Supporting Roles:** PM (scaffolding), QA (testing)

---

## 🎯 Implementation Overview

**Goal:** Implement Jasmine visualization for Merge Sort algorithm with data-rich hierarchical display showing recursion depth, actual array values, and merge comparison logic.

**Key Deliverables:**
1. Static mockup adapted to platform theme (FAA-approved)
2. Two new reusable visualization components
3. Integrated MergeSortState component
4. Complete QA validation
5. Documentation for component reusability

---

## 📊 Phase Breakdown

### **PHASE 1: Static Mockup Adaptation & FAA Gate**
**Timeline:** 15-20 minutes  
**Owner:** Frontend Developer  
**Gate:** FAA Approval Required Before Phase 2

#### **Objective**
Adapt Jasmine prototype to match platform's visual standards (`iterative_metrics_algorithm_mockup.html` theme) and get FAA approval for visual-narrative correspondence.

#### **Tasks**

**1.1 Review Existing Standards** (5 min)
```bash
# Frontend Developer: Review platform visual standards
cat docs/static_mockup/iterative_metrics_algorithm_mockup.html
cat docs/static_mockup/prototyping/jasmine.html
```

**1.2 Create Adapted Static Mockup** (10 min)
- [ ] Create `docs/static_mockup/merge_sort_jasmine_adapted.html`
- [ ] Apply platform color scheme (Tailwind classes from existing mockups)
- [ ] Match panel proportions (40% left visualization, 60% right narrative)
- [ ] Ensure typography consistency with platform standards
- [ ] Include all Jasmine sections:
  - Recursion hierarchy (with DEPTH labels)
  - Current intervals (actual data values)
  - Merge comparison logic (boolean expressions)
  - Call stack ancestry

**1.3 Submit for FAA Review** (5 min)
- [ ] Document visual-narrative correspondence points
- [ ] Prepare comparison: Narrative Step 20 ↔ Mockup display
- [ ] Submit to FAA for visual accuracy audit

**Deliverable:** `merge_sort_jasmine_adapted.html` with FAA approval

**Success Criteria:**
- ✅ Mockup matches platform theme
- ✅ Visual elements correspond to narrative step data
- ✅ FAA confirms visual-narrative alignment
- ✅ No arithmetic or logical errors in displayed data

**BLOCKING GATE:** Phase 2 cannot begin until FAA approves mockup

---

### **PHASE 2: Component Development**
**Timeline:** 90-120 minutes  
**Owner:** Frontend Developer  
**Prerequisite:** FAA-approved static mockup from Phase 1

#### **Objective**
Create reusable visualization components and integrate into MergeSortState.

---

#### **2.1: RecursionHierarchyView Component** (60 min)

**Purpose:** Reusable component for displaying recursive algorithm call stacks and depth levels.

**Component Scaffolding:**

```jsx
import React from 'react';
import PropTypes from 'prop-types';

/**
 * RecursionHierarchyView - Displays recursive call hierarchy with depth labels
 * 
 * REUSABLE FOR: DFS, BFS, Quicksort, Backtracking, Tree Traversals
 * 
 * Requirements (from WORKFLOW.md Stage 3):
 * - Extract data from step.data.visualization
 * - Handle missing data gracefully
 * - Use consistent Tailwind styling
 * - See ADR-002 for component organization principles
 */
export const RecursionHierarchyView = ({ intervals, currentDepth, callStack }) => {
  /*
  Frontend Developer: Implement component logic

  Data Sources (from backend trace):
  - intervals: step.data.visualization.all_intervals (array of interval objects)
  - currentDepth: step.data.visualization.depth (integer)
  - callStack: step.data.visualization.call_stack_state (array of stack frames)

  Visual Requirements (from FAA-approved mockup):
  - Display "DEPTH 0", "DEPTH 1", "DEPTH 2" labels explicitly
  - Show actual array values: [38, 27, 43, 3] not [0...3]
  - Highlight current depth level
  - Display ancestry/call stack context
  - Use overflow-y-auto for scrollable content (scalability mitigation)

  Styling Pattern:
  - Follow existing ArrayView.jsx patterns for array display
  - Use Tailwind utility classes (bg-blue-100, text-sm, font-mono, etc.)
  - Consistent spacing with other visualization components

  Error Handling:
  - Gracefully handle missing intervals
  - Handle edge cases: single element, empty array
  - Provide meaningful fallback display
  */

  return (
    <div className="recursion-hierarchy">
      {/* Frontend Developer: Implement hierarchy display */}
    </div>
  );
};

RecursionHierarchyView.propTypes = {
  intervals: PropTypes.arrayOf(PropTypes.shape({
    start: PropTypes.number.isRequired,
    end: PropTypes.number.isRequired,
    values: PropTypes.arrayOf(PropTypes.number).isRequired,
    depth: PropTypes.number.isRequired
  })),
  currentDepth: PropTypes.number.isRequired,
  callStack: PropTypes.arrayOf(PropTypes.object)
};

RecursionHierarchyView.defaultProps = {
  intervals: [],
  callStack: []
};
```

**Tasks:**
- [ ] Create `frontend/src/components/visualizations/RecursionHierarchyView.jsx`
- [ ] Implement depth-based hierarchy display
- [ ] Show actual array values at each level
- [ ] Highlight current depth
- [ ] Display call stack ancestry
- [ ] Add overflow handling for scalability
- [ ] Follow Tailwind styling patterns from existing components
- [ ] Add PropTypes validation

**Reference Files to Review:**
```bash
# Frontend Developer: Review these patterns before implementing
cat frontend/src/components/visualizations/ArrayView.jsx
cat frontend/src/components/visualizations/TimelineView.jsx
cat frontend/src/components/algorithm-states/BinarySearchState.jsx
```

**Success Criteria:**
- ✅ Component renders hierarchy with explicit depth labels
- ✅ Shows actual data values (not index ranges)
- ✅ Handles edge cases gracefully
- ✅ Matches FAA-approved mockup visually
- ✅ Reusable for future recursive algorithms

---

#### **2.2: MergeCompareView Component** (30 min)

**Purpose:** Display merge comparison logic with boolean expressions and decision outcomes.

**Component Scaffolding:**

```jsx
import React from 'react';
import PropTypes from 'prop-types';

/**
 * MergeCompareView - Displays merge comparison logic with boolean expressions
 * 
 * REUSABLE FOR: Any merge-based algorithm (Merge Sort variants, K-way merge)
 * 
 * Requirements (from WORKFLOW.md Stage 3):
 * - Extract comparison data from step.data.visualization
 * - Display boolean expressions: "27 > 3" → "FALSE"
 * - Show decision outcome: "Take 3 from right"
 * - Highlight which element was selected
 */
export const MergeCompareView = ({ compareData }) => {
  /*
  Frontend Developer: Implement comparison display logic

  Data Source (from backend trace):
  - compareData: step.data.visualization.merge_comparison (object with:
      - leftValue: number
      - rightValue: number
      - comparison: string (e.g., "27 > 3")
      - result: boolean
      - action: string (e.g., "Take 3 from right")
    )

  Visual Requirements (from FAA-approved mockup):
  - Display comparison expression clearly
  - Show boolean result (TRUE/FALSE)
  - Highlight selected element
  - Use color coding for clarity (e.g., green for selected)

  Styling:
  - Font-mono for numbers and expressions
  - Color indicators for boolean results
  - Clear visual hierarchy

  Error Handling:
  - Handle missing comparison data
  - Handle non-merge steps (no comparison active)
  */

  if (!compareData) {
    return null; // Not a merge step
  }

  return (
    <div className="merge-compare">
      {/* Frontend Developer: Implement comparison display */}
    </div>
  );
};

MergeCompareView.propTypes = {
  compareData: PropTypes.shape({
    leftValue: PropTypes.number,
    rightValue: PropTypes.number,
    comparison: PropTypes.string,
    result: PropTypes.bool,
    action: PropTypes.string
  })
};

MergeCompareView.defaultProps = {
  compareData: null
};
```

**Tasks:**
- [ ] Create `frontend/src/components/visualizations/MergeCompareView.jsx`
- [ ] Display boolean comparison expressions
- [ ] Show comparison result (TRUE/FALSE)
- [ ] Display decision outcome ("Take X from left/right")
- [ ] Highlight selected element
- [ ] Handle non-merge steps gracefully
- [ ] Add PropTypes validation

**Success Criteria:**
- ✅ Displays comparison logic transparently
- ✅ Boolean expressions match narrative descriptions
- ✅ Visual highlighting matches decision
- ✅ Handles missing data gracefully

---

#### **2.3: MergeSortState Integration** (30 min)

**Purpose:** Orchestrate RecursionHierarchyView and MergeCompareView within MergeSortState component.

**Integration Scaffolding:**

```jsx
import React from 'react';
import PropTypes from 'prop-types';
import { RecursionHierarchyView } from '../visualizations/RecursionHierarchyView';
import { MergeCompareView } from '../visualizations/MergeCompareView';

/**
 * MergeSortState - Algorithm-specific state component for Merge Sort
 * 
 * Requirements (from WORKFLOW.md Stage 3):
 * - Extract data from step.data.visualization
 * - Access metadata from trace.metadata
 * - Orchestrate multiple visualization components
 * - Follow component organization principles (ADR-002)
 */
export const MergeSortState = ({ step, trace }) => {
  /*
  Frontend Developer: Implement orchestration logic

  Data Extraction Pattern:
  const visualization = step?.data?.visualization || {};
  const intervals = visualization.all_intervals || [];
  const currentDepth = visualization.depth || 0;
  const callStack = visualization.call_stack_state || [];
  const mergeComparison = visualization.merge_comparison || null;

  Component Layout:
  - RecursionHierarchyView (top section)
  - Current interval display (middle section)
  - MergeCompareView (bottom section, conditional)

  Styling:
  - Consistent spacing with other algorithm states
  - Responsive layout
  - Overflow handling

  Error Handling:
  - Gracefully handle missing step data
  - Provide fallback display for incomplete traces
  */

  // Frontend Developer: Extract and validate data here

  return (
    <div className="merge-sort-state">
      {/* Frontend Developer: Compose visualization components */}
      
      {/* Section 1: Recursion Hierarchy */}
      <RecursionHierarchyView 
        intervals={intervals}
        currentDepth={currentDepth}
        callStack={callStack}
      />

      {/* Section 2: Current Interval (if needed) */}
      
      {/* Section 3: Merge Comparison Logic */}
      <MergeCompareView compareData={mergeComparison} />
    </div>
  );
};

MergeSortState.propTypes = {
  step: PropTypes.shape({
    data: PropTypes.shape({
      visualization: PropTypes.object
    })
  }).isRequired,
  trace: PropTypes.shape({
    metadata: PropTypes.object
  }).isRequired
};
```

**Tasks:**
- [ ] Create `frontend/src/components/algorithm-states/MergeSortState.jsx`
- [ ] Extract data from `step.data.visualization`
- [ ] Compose RecursionHierarchyView and MergeCompareView
- [ ] Handle missing data gracefully
- [ ] Match FAA-approved mockup layout
- [ ] Add PropTypes validation

**Success Criteria:**
- ✅ Components compose correctly
- ✅ Data flows from trace to visualizations
- ✅ Layout matches approved mockup
- ✅ Handles edge cases

---

#### **2.4: Registry Integration** (5 min)

**Purpose:** Register new components in platform registries for automatic discovery.

**Tasks:**

**stateRegistry.js:**
```javascript
// Frontend Developer: Add to frontend/src/utils/stateRegistry.js

import { MergeSortState } from '../components/algorithm-states/MergeSortState';

export const stateRegistry = {
  // ... existing registrations
  'merge-sort': MergeSortState,  // ADD THIS LINE
};
```

**visualizationRegistry.js:**
```javascript
// Frontend Developer: Add to frontend/src/utils/visualizationRegistry.js

import { RecursionHierarchyView } from '../components/visualizations/RecursionHierarchyView';
import { MergeCompareView } from '../components/visualizations/MergeCompareView';

export const visualizationRegistry = {
  // ... existing registrations
  recursionHierarchy: RecursionHierarchyView,  // ADD THIS LINE
  mergeCompare: MergeCompareView,              // ADD THIS LINE
};
```

**index.js exports:**
```javascript
// Frontend Developer: Update exports in visualization index

// frontend/src/components/visualizations/index.js
export { RecursionHierarchyView } from './RecursionHierarchyView';
export { MergeCompareView } from './MergeCompareView';

// frontend/src/components/algorithm-states/index.js
export { MergeSortState } from './MergeSortState';
```

**Checklist:**
- [ ] Register MergeSortState in stateRegistry.js
- [ ] Register RecursionHierarchyView in visualizationRegistry.js
- [ ] Register MergeCompareView in visualizationRegistry.js
- [ ] Export components from index.js files
- [ ] Verify no import path errors

**Success Criteria:**
- ✅ Algorithm switcher shows "Merge Sort" option
- ✅ Components load without errors
- ✅ Registry pattern follows existing conventions

---

### **PHASE 2 Deliverables Summary**

**Files Created:**
1. `frontend/src/components/visualizations/RecursionHierarchyView.jsx`
2. `frontend/src/components/visualizations/MergeCompareView.jsx`
3. `frontend/src/components/algorithm-states/MergeSortState.jsx`

**Files Modified:**
1. `frontend/src/utils/stateRegistry.js`
2. `frontend/src/utils/visualizationRegistry.js`
3. `frontend/src/components/visualizations/index.js`
4. `frontend/src/components/algorithm-states/index.js`

**Success Criteria:**
- ✅ All components created with proper scaffolding
- ✅ Components registered in platform registries
- ✅ Visual output matches FAA-approved mockup
- ✅ Data extraction follows backend trace structure
- ✅ Error handling for edge cases implemented

---

## **PHASE 3: Quality Assurance**
**Timeline:** 30 minutes  
**Owner:** QA  
**Prerequisite:** Phase 2 complete

#### **Objective**
Validate Merge Sort implementation against platform standards and ensure no regressions.

---

#### **3.1: Visual-Narrative Correspondence** (10 min)

**Tasks:**
- [ ] Load Merge Sort in UI with Example 1 (basic 8 elements)
- [ ] Navigate to Step 20 (critical merge point per executive summary)
- [ ] Verify visual display matches narrative description:
  - Depth labels visible and correct
  - Array values match narrative numbers
  - Merge comparison logic matches narrative explanation
  - Ancestry shows correct call stack
- [ ] Test all 6 merge sort examples (examples 1-6)
- [ ] Document any visual-narrative mismatches

**Reference:**
```bash
# QA: Review narratives for comparison
cat docs/narratives/merge-sort/example_1_basic_8_elements.md
```

**Success Criteria:**
- ✅ Visual display matches narrative at all steps
- ✅ No data discrepancies between UI and narrative
- ✅ Depth labels correspond to recursion level in narrative

---

#### **3.2: Functional Testing** (10 min)

**Test Cases:**

**TC1: Prediction Modal Functionality**
- [ ] Load Merge Sort Example 1
- [ ] Advance to first prediction point
- [ ] Verify prediction modal appears (LOCKED element - critical)
- [ ] Verify 2-3 choices maximum (HARD LIMIT from WORKFLOW.md)
- [ ] Select answer and verify feedback
- [ ] Ensure modal closes with keyboard shortcut

**TC2: Component Edge Cases**
- [ ] Test with 1-element array (Example 5: small array)
- [ ] Test with duplicate values (Example 4: with duplicates)
- [ ] Test with already sorted array (Example 2)
- [ ] Test with reverse sorted array (Example 3)
- [ ] Verify no crashes or rendering errors

**TC3: Responsive Behavior**
- [ ] Test at 1920x1080 resolution
- [ ] Test at 1366x768 resolution (minimum supported)
- [ ] Verify overflow-y-auto works for deep recursion
- [ ] Check panel proportions (40% left, 60% right)

**TC4: Keyboard Shortcuts (LOCKED elements)**
- [ ] Test all keyboard shortcuts still work:
  - `←` Previous step
  - `→` Next step
  - `Space` Play/Pause
  - `i` Info modal
  - `Esc` Close modal
- [ ] Verify no conflicts with new components

**Success Criteria:**
- ✅ All test cases pass
- ✅ No edge case crashes
- ✅ Keyboard shortcuts functional
- ✅ Responsive at all resolutions

---

#### **3.3: Regression Testing** (10 min)

**Tasks:**
- [ ] Load Binary Search algorithm - verify still works
- [ ] Load Two Pointer algorithm - verify still works
- [ ] Load Sliding Window algorithm - verify still works
- [ ] Load Interval Coverage algorithm - verify still works
- [ ] Verify algorithm switcher shows all algorithms
- [ ] Test navigation between algorithms
- [ ] Verify no console errors in browser

**Success Criteria:**
- ✅ All existing algorithms still functional
- ✅ No regressions introduced
- ✅ Clean console (no errors/warnings)

---

#### **3.4: Complete QA Checklist** (5 min)

**Tasks:**
- [ ] Complete `docs/compliance/QA_INTEGRATION_CHECKLIST.md` for Merge Sort
- [ ] Document any issues found with severity levels
- [ ] Create bug reports for any failures (route to Frontend Developer)
- [ ] Confirm all critical path tests passed

**Reference:**
```bash
# QA: Use this checklist
cat docs/compliance/QA_INTEGRATION_CHECKLIST.md
```

**Deliverable:** Completed QA checklist with pass/fail results

---

### **PHASE 3 Deliverables**

**Documents:**
1. Completed QA Integration Checklist
2. Visual-narrative correspondence validation report
3. Bug reports (if any issues found)
4. Regression test results

**Success Criteria:**
- ✅ All functional tests pass
- ✅ No regressions in existing algorithms
- ✅ Visual-narrative correspondence confirmed
- ✅ QA checklist 100% complete

---

## **PHASE 4: Documentation & Finalization**
**Timeline:** 20 minutes  
**Owner:** Frontend Developer (documentation), PM (reusability notes)  
**Prerequisite:** Phase 3 QA approval

#### **Objective**
Document component usage, create algorithm info markdown, and prepare reusability notes for future algorithms.

---

#### **4.1: Component Documentation** (10 min)

**Tasks:**

**RecursionHierarchyView Documentation:**
```javascript
// Frontend Developer: Add JSDoc comments at top of file

/**
 * RecursionHierarchyView Component
 * 
 * Purpose: Displays recursive algorithm call hierarchy with explicit depth labels
 * and actual data values at each recursion level.
 * 
 * Reusable For:
 * - Depth-First Search (DFS)
 * - Breadth-First Search (BFS)
 * - Quicksort
 * - Backtracking algorithms
 * - Tree traversals
 * 
 * Props:
 * @param {Array} intervals - Array of interval objects with start, end, values, depth
 * @param {number} currentDepth - Current recursion depth (0-indexed)
 * @param {Array} callStack - Array of stack frame objects showing ancestry
 * 
 * Data Source: step.data.visualization.all_intervals (backend trace)
 * 
 * Visual Features:
 * - Explicit "DEPTH N" labels for clarity
 * - Actual array values displayed (not index ranges)
 * - Current depth highlighted
 * - Call stack ancestry for context
 * - Overflow-y-auto for scalability
 * 
 * Example Usage:
 * ```jsx
 * <RecursionHierarchyView 
 *   intervals={step.data.visualization.all_intervals}
 *   currentDepth={step.data.visualization.depth}
 *   callStack={step.data.visualization.call_stack_state}
 * />
 * ```
 * 
 * Integration Pattern:
 * See MergeSortState.jsx for complete example
 */
```

**MergeCompareView Documentation:**
```javascript
// Frontend Developer: Add JSDoc comments

/**
 * MergeCompareView Component
 * 
 * Purpose: Displays merge comparison logic with boolean expressions and
 * decision outcomes for pedagogical transparency.
 * 
 * Reusable For:
 * - Merge Sort variants
 * - K-way merge algorithms
 * - Any merge-based sorting/processing
 * 
 * Props:
 * @param {Object} compareData - Comparison data object with leftValue, rightValue,
 *                                comparison, result, action
 * 
 * Data Source: step.data.visualization.merge_comparison (backend trace)
 * 
 * Visual Features:
 * - Boolean expressions: "27 > 3" → "FALSE"
 * - Decision outcomes: "Take 3 from right"
 * - Element highlighting for clarity
 * - Conditional rendering (only shows during merge steps)
 * 
 * Example Usage:
 * ```jsx
 * <MergeCompareView 
 *   compareData={step.data.visualization.merge_comparison}
 * />
 * ```
 */
```

**Checklist:**
- [ ] Add JSDoc comments to RecursionHierarchyView.jsx
- [ ] Add JSDoc comments to MergeCompareView.jsx
- [ ] Add JSDoc comments to MergeSortState.jsx
- [ ] Document PropTypes in detail
- [ ] Include usage examples in comments

---

#### **4.2: Algorithm Info Markdown** (5 min)

**Tasks:**
- [ ] Create `frontend/public/algorithm-info/merge-sort.md`
- [ ] Follow pattern from existing algorithm info files
- [ ] Include:
  - Algorithm description
  - Time/space complexity
  - Use cases
  - Visualization features (Jasmine-specific)
  - Key learning points

**Reference Pattern:**
```bash
# Frontend Developer: Follow this pattern
cat frontend/public/algorithm-info/binary-search.md
```

**Template:**
```markdown
# Merge Sort

## Overview
[Description of merge sort algorithm]

## Complexity
- **Time:** O(n log n)
- **Space:** O(n)

## Visualization Features
This visualization uses a **hierarchical view** to show:
- Recursive splitting down to single elements
- Explicit depth labels (DEPTH 0, DEPTH 1, etc.)
- Actual array values at each level
- Merge comparison logic with boolean expressions
- Call stack ancestry for context

## Key Learning Points
1. Base case: Single elements are already sorted
2. Merge logic: Always take the smaller front element
3. [Additional points...]
```

---

#### **4.3: Reusability Roadmap** (5 min)

**Tasks (PM):**
- [ ] Document future algorithms that can reuse RecursionHierarchyView
- [ ] Create `docs/COMPONENT_REUSABILITY_ROADMAP.md` (if doesn't exist)
- [ ] Add Jasmine components to roadmap

**Roadmap Entry:**

```markdown
## RecursionHierarchyView - Reusability Analysis

**Created For:** Merge Sort (Jasmine visualization)  
**Created:** December 20, 2025  
**Development Cost:** 60 minutes  

**Reusable For (Estimated 50% time savings per algorithm):**

1. **Quicksort** (Priority: High)
   - Similar recursive splitting pattern
   - Different merge logic (in-place partitioning)
   - Estimated adaptation: 30 minutes

2. **Depth-First Search (DFS)** (Priority: Medium)
   - Tree/graph traversal with depth tracking
   - Call stack visualization directly applicable
   - Estimated adaptation: 20 minutes

3. **Backtracking Algorithms** (Priority: Medium)
   - Shows choice points at each depth
   - Call stack = decision tree
   - Estimated adaptation: 25 minutes

4. **Binary Tree Traversals** (Priority: Low)
   - Preorder, Inorder, Postorder
   - Depth levels map to tree levels
   - Estimated adaptation: 15 minutes

**ROI Calculation:**
- Initial investment: 60 minutes
- Expected reuses: 4+ algorithms
- Time saved per reuse: ~30 minutes average
- Total savings: 120+ minutes
- **Net ROI: +100% after 2 algorithm implementations**
```

---

### **PHASE 4 Deliverables**

**Documentation Created:**
1. Component JSDoc comments (inline in code)
2. `frontend/public/algorithm-info/merge-sort.md`
3. Component reusability roadmap entry

**Success Criteria:**
- ✅ All components fully documented
- ✅ Algorithm info markdown complete
- ✅ Reusability roadmap updated
- ✅ Future developers have clear guidance

---

## 🎯 **Overall Success Criteria**

**Functional Requirements:**
- ✅ Merge Sort loads in algorithm switcher
- ✅ Jasmine visualization renders correctly
- ✅ Visual display matches narrative at all steps
- ✅ Prediction modal appears at correct points
- ✅ All keyboard shortcuts work
- ✅ No regressions in existing algorithms

**Quality Requirements:**
- ✅ Code follows WORKFLOW.md Stage 3 patterns
- ✅ Components registered correctly in registries
- ✅ PropTypes validation on all components
- ✅ Error handling for edge cases
- ✅ QA checklist 100% complete

**Documentation Requirements:**
- ✅ JSDoc comments complete
- ✅ Algorithm info markdown created
- ✅ Reusability roadmap updated

**Performance Requirements:**
- ✅ No console errors or warnings
- ✅ Responsive at all supported resolutions
- ✅ Overflow handling works for deep recursion

---

## ⚠️ **Risk Factors & Mitigation**

### **Risk 1: Data Structure Mismatch**
**Risk:** Backend trace structure doesn't match expected format for Jasmine visualization.

**Mitigation:**
- **Action:** Frontend Developer review backend trace before Phase 2
  ```bash
  # Verify trace structure
  cat backend/algorithms/merge_sort.py
  # Check example trace output
  curl -X POST http://localhost:5001/api/trace \
    -H "Content-Type: application/json" \
    -d '{"algorithm": "merge-sort", "example": "1"}' | jq '.trace.steps[20]'
  ```
- **Fallback:** If structure differs, create adapter layer in MergeSortState

### **Risk 2: FAA Mockup Rejection**
**Risk:** FAA rejects Phase 1 mockup due to visual-narrative misalignment.

**Mitigation:**
- **Action:** Iterate on mockup until approved (may add 10-20 minutes)
- **Prevention:** Review existing narratives before creating mockup
- **Escalation:** If >2 iterations needed, consult PM for guidance

### **Risk 3: Scalability Issues**
**Risk:** Deep recursion exceeds panel vertical space.

**Mitigation:**
- **Implemented:** Overflow-y-auto on RecursionHierarchyView
- **Tested:** QA validates with 16-element array (depth 4)
- **Future:** Collapsible sections if needed (deferred to future enhancement)

### **Risk 4: Component Complexity Underestimate**
**Risk:** RecursionHierarchyView takes longer than 60 minutes.

**Mitigation:**
- **Buffer:** Phase 2 has 90-120 minute range (30-minute buffer)
- **Simplification:** If blocked, create minimal viable version first
- **Escalation:** If >90 minutes, consult PM for scope reduction

---

## 📅 **Recommended Execution Schedule**

**Single Development Session (Recommended):**
- **Total Time:** 2.5-3 hours
- **Break Points:** After each phase for review
- **QA Integration:** Can run parallel with documentation (Phase 4)

**Split Session Alternative:**
- **Session 1 (90 min):** Phase 1 + Phase 2.1-2.2
- **Session 2 (90 min):** Phase 2.3-2.4 + Phase 3 + Phase 4

---

## 📋 **Phase Handoff Checklist**

### **Phase 1 → Phase 2**
- [ ] FAA approval received for static mockup
- [ ] Mockup file committed to repo
- [ ] Visual requirements documented

### **Phase 2 → Phase 3**
- [ ] All components created and registered
- [ ] No build errors
- [ ] Visual output matches mockup
- [ ] Ready for QA testing

### **Phase 3 → Phase 4**
- [ ] All QA tests passed
- [ ] No critical bugs blocking release
- [ ] Regression tests clean

### **Phase 4 → Complete**
- [ ] All documentation complete
- [ ] Components fully commented
- [ ] Algorithm info markdown published
- [ ] Ready for production deployment

---

## 🚀 **Next Steps**

**Immediate Action (Frontend Developer):**

1. **Begin Phase 1:**
   ```bash
   # Review visual standards
   cat docs/static_mockup/iterative_metrics_algorithm_mockup.html
   cat docs/static_mockup/prototyping/jasmine.html
   
   # Create adapted mockup
   # File: docs/static_mockup/merge_sort_jasmine_adapted.html
   ```

2. **Verify Backend Trace Structure:**
   ```bash
   # Check merge_sort.py trace output format
   cat backend/algorithms/merge_sort.py
   
   # Verify visualization data structure
   grep -A 20 "visualization" backend/algorithms/merge_sort.py
   ```

3. **Submit Phase 1 Deliverable:**
   - Create mockup file
   - Document visual-narrative correspondence
   - Request FAA review

**Questions for Frontend Developer Before Starting:**

- Do you need PM to review backend trace structure first?
- Do you have access to FAA reviewer for Phase 1 gate?
- Any questions about component scaffolding or data extraction patterns?

---

**Ready to begin Phase 1?** Confirm and I'll provide any additional scaffolding or code review support needed.