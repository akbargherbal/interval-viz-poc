# QA & Integration Compliance Checklist

**Version:** 2.0  
**Authority:** WORKFLOW.md v2.0 - QA Requirements  
**Purpose:** Two-phase validation - Narrative review BEFORE integration testing

**Changes from v1.0:**

- Added Phase 1: Narrative Review (NEW - quality gate)
- Updated authority reference from TENANT_GUIDE.md to WORKFLOW.md
- Updated modal sizing requirements (removed max-h-[85vh])
- Updated keyboard shortcuts (Space = Next step, not Toggle mode)
- Reorganized workflow: Narrative review → Integration tests

---

## WORKFLOW OVERVIEW

**v2.0 introduces a two-phase QA process:**

```
Phase 1: NARRATIVE REVIEW (NEW)
  ↓
  ├─→ APPROVED → Phase 2: Integration Testing
  └─→ REJECTED → Return to Backend
```

**Phase 1 happens BEFORE frontend integration.**  
**Phase 2 happens AFTER frontend integration.**

---

## Phase 1: Narrative Review (NEW in v2.0)

**Timing:** AFTER backend implementation, BEFORE frontend integration  
**Input:** Generated markdown narratives ONLY (no code, no JSON, no frontend)  
**Purpose:** Validate logical completeness of algorithm via human-readable narratives

### What QA Reviews

**ONLY the narratives in `docs/narratives/[algorithm-name]/*.md`**

QA does NOT look at:

- ❌ Backend code
- ❌ JSON trace structure
- ❌ Frontend components
- ❌ Visual rendering

### Review Criteria

For each example narrative:

#### 1. Logical Completeness

- [ ] Can I follow the algorithm logic from start to finish?
- [ ] Are all decision points explained?
- [ ] Is supporting data for each decision visible?
- [ ] Are there any undefined variable references?

**Example of FAILURE:**

```
❌ Narrative says: "Compare with max_end"
✅ Should say: "Compare 720 with max_end (660)"
```

#### 2. Temporal Coherence

- [ ] Does step N+1 logically follow from step N?
- [ ] Are there narrative gaps or jumps?
- [ ] Can I reconstruct the execution flow?
- [ ] Is the step sequence clear?

**Example of FAILURE:**

```
❌ Step 8: "Examining interval [900, 960]"
   Step 9: "Returning with 2 intervals kept"
   Problem: What happened to interval [900, 960]? Was it kept?
```

#### 3. Mental Visualization

- [ ] Can I imagine what the visualization would show?
- [ ] Are state changes clear enough to track?
- [ ] Can I understand this without seeing code or JSON?
- [ ] Would I know what to render if I were the frontend?

#### 4. Decision Transparency

For each decision (keep/discard, left/right, found/not found):

- [ ] Is the comparison data visible?
- [ ] Is the decision logic clear?
- [ ] Is the outcome explained?
- [ ] Can I verify the decision is correct?

**Example of FAILURE:**

```
❌ Narrative says: "Interval is covered"
✅ Should say: "Interval [900, 960] is covered because 900 >= max_end (660)"
```

---

### Narrative Review Checklist Template

```markdown
# Narrative Review: [Algorithm Name]

**Reviewer:** [Name]  
**Date:** [Date]  
**Examples Reviewed:** [List all example names]

## Example 1: [Example Name]

### Logical Completeness

- [ ] Algorithm logic followable start-to-finish
- [ ] All decision points explained
- [ ] No undefined variable references
- [ ] Supporting data visible

### Temporal Coherence

- [ ] Steps flow logically
- [ ] No narrative gaps
- [ ] Execution flow reconstructable

### Mental Visualization

- [ ] Can imagine visualization
- [ ] State changes clear
- [ ] No code/JSON needed

### Decision Transparency

- [ ] Comparison data visible
- [ ] Decision logic clear
- [ ] Outcomes explained

### Issues Found:

[List specific issues with step numbers, or write "None"]

## Example 2: [Example Name]

[Repeat checklist...]

## Overall Assessment

- [ ] ✅ APPROVED - All examples pass, ready for frontend integration
- [ ] ⚠️ MINOR ISSUES - Approved with documentation notes
- [ ] ❌ REJECTED - Backend must fix and resubmit

### Rejection Feedback (if rejected):

**Critical:** Provide feedback on WHAT is wrong (not HOW to fix).

**Example - CORRECT Feedback:**
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

**Example - WRONG Feedback:**
```

❌ Don't do this!

Issue 1: Add mid value to Step 5

- Solution: Update narrative to include "Compare target (5) with mid (3)"

^ This tells HOW to fix, not WHAT is wrong

```

### Sign-off:

- QA Engineer: [Name]
- Date: [Date]
- Next Action: [APPROVED → Frontend Integration | REJECTED → Backend Revision]
```

---

### Decision Gate

**If APPROVED:**

- ✅ Narratives are logically complete
- ✅ Backend proceeds to Stage 3: Frontend Integration
- ✅ Narratives serve as reference documentation for frontend

**If REJECTED:**

- ❌ Backend must fix issues and regenerate narratives
- ❌ QA re-reviews updated narratives
- ❌ Frontend work does NOT begin until approved

---

## Phase 2: Integration Testing

**Timing:** AFTER frontend integration  
**Input:** Fully integrated algorithm in browser  
**Purpose:** End-to-end validation of rendering, interactions, and standards compliance

**Note:** This phase should have ZERO "missing data" bugs - Phase 1 narrative review should have caught them.

---

### Pre-Integration Validation

**Before running integration tests, verify:**

- [ ] **Phase 1 APPROVED** - Narrative review passed
- [ ] **Backend checklist completed** - Backend developer signed off
- [ ] **Frontend checklist completed** - Frontend developer signed off
- [ ] **Component tests pass** - All visualization tests green
- [ ] **No console errors** - Clean browser console

---

## Integration Tests: LOCKED Requirements

### Test Suite 1: Modal Standards

**Source:** `docs/static_mockup/completion_modal_mockup.html` and `prediction_modal_mockup.html`

#### Prediction Modal

**Test Case: Modal Size**

```
GIVEN: Algorithm with prediction points
WHEN: Prediction modal opens
THEN:
  ✅ Modal max-width is max-w-lg (512px)
  ✅ Modal padding is p-6
  ✅ No internal scrollbars visible
  ✅ All content fits naturally
```

**Test Case: Modal Positioning**

```
GIVEN: Prediction modal open
THEN:
  ✅ Modal is centered (flex items-center justify-center)
  ✅ Background is semi-transparent with blur (bg-black/80 backdrop-blur-sm)
  ✅ z-index is 50 (above main content)
  ✅ Padding prevents edge collision (p-4 on backdrop)
```

#### Completion Modal

**Test Case: Modal Size (Compact Redesign)**

```
GIVEN: Algorithm completes with results
WHEN: Completion modal opens
THEN:
  ✅ Modal max-width is max-w-lg (512px)
  ✅ Modal padding is p-5 (compact)
  ✅ No internal scrolling (uses horizontal layouts + flex-wrap)
  ✅ All stats visible without scroll
```

**Test Case: Vertical Efficiency**

```
GIVEN: Completion modal with complex data
THEN:
  ✅ Header uses horizontal layout (icon + text in row)
  ✅ Compact spacing (mb-3, mb-4 instead of mb-6)
  ✅ Stats use grid with dividers (border-l)
  ✅ Prediction accuracy in horizontal layout
  ✅ Complex results show subset + "+N more" summary
```

---

### Test Suite 2: Panel Layout

**Source:** `docs/static_mockup/algorithm_page_mockup.html`

**Test Case: Flex Ratio Verification**

```
GIVEN: Algorithm loaded
THEN:
  ✅ Visualization panel has flex-[3] (66.67% width)
  ✅ Steps panel has w-96 (384px)
  ✅ Gap between panels is gap-4 (1rem)
  ✅ Ratio maintained at 1920px, 1366px, 1024px viewports
```

**Test Case: Minimum Width Enforcement**

```
GIVEN: Viewport narrowed to 1024px
THEN:
  ✅ Steps panel never smaller than 384px
  ✅ Visualization panel shrinks to accommodate
  ✅ No horizontal scrollbar on body
  ✅ Content remains readable
```

**Test Case: Overflow Behavior**

```
GIVEN: Trace with 20+ steps
WHEN: Steps exceed viewport height
THEN:
  ✅ Steps panel scrolls independently (overflow-y-auto)
  ✅ Visualization panel scrolls independently (overflow-auto)
  ✅ Scrollbars appear only where needed
  ✅ No nested scrolling issues
```

---

### Test Suite 3: HTML Landmark IDs

**Test Case: Required IDs Present**

```
GIVEN: Algorithm loaded
THEN:
  ✅ document.getElementById('app-root') !== null
  ✅ document.getElementById('app-header') !== null
  ✅ document.getElementById('panel-visualization') !== null
  ✅ document.getElementById('panel-steps') !== null
  ✅ document.getElementById('panel-steps-list') !== null
  ✅ document.getElementById('panel-step-description') !== null
```

**Test Case: Dynamic ID Behavior**

```
GIVEN: Algorithm trace with 10 steps
WHEN: Navigate to step 5
THEN:
  ✅ Only ONE element has id="step-current"
  ✅ Element corresponds to current execution context
  ✅ ID updates on step navigation
```

---

### Test Suite 4: Keyboard Navigation

**Source:** `docs/static_mockup/algorithm_page_mockup.html` (lines 854-874)

**Test Case: Standard Shortcuts**

```
GIVEN: Algorithm loaded, no modal open
WHEN: Press Arrow Right (→)
THEN: ✅ Advances to next step

WHEN: Press Space
THEN: ✅ Advances to next step (alternative to Arrow Right)

WHEN: Press Arrow Left (←)
THEN: ✅ Goes to previous step

WHEN: Press R
THEN: ✅ Resets trace to step 0

WHEN: Press Home
THEN: ✅ Resets trace to step 0 (alternative to R)
```

**Test Case: Modal Shortcuts**

**Source:** `docs/static_mockup/prediction_modal_mockup.html` (lines 329-335)

```
GIVEN: Prediction modal open
WHEN: Press F/L/R/K/C (semantic letter from choice text)
THEN: ✅ Selects corresponding choice

WHEN: Press 1/2/3 (numeric fallback)
THEN: ✅ Selects corresponding choice

WHEN: Press Enter
THEN: ✅ Submits selected answer

WHEN: Press S
THEN: ✅ Skips prediction
```

**Test Case: Shortcut Conflicts**

```
GIVEN: Input field focused
WHEN: Press Arrow Right
THEN: ✅ Does NOT navigate (ignores shortcut when typing)

GIVEN: Modal open
WHEN: Press Arrow Right
THEN: ✅ Modal ignores it (doesn't navigate main app)
```

---

### Test Suite 5: Auto-Scroll

**Test Case: Scroll to Current Step**

```
GIVEN: Trace with 15+ steps (exceeds viewport)
WHEN: Navigate to step 10
THEN:
  ✅ Element with #step-current scrolls into view
  ✅ Scroll is smooth (behavior: 'smooth')
  ✅ Element centered in viewport (block: 'center')
  ✅ No jarring jumps
```

**Test Case: Scroll Triggers**

```
GIVEN: Step 1 visible, step 10 off-screen
WHEN: Click Next button repeatedly
THEN: ✅ Auto-scrolls to keep current step visible

WHEN: User manually scrolls
THEN: ❌ Does NOT auto-scroll (respects user intent)

WHEN: Switch algorithms
THEN: ❌ Does NOT auto-scroll (resets to top)
```

---

### Test Suite 6: Overflow Pattern

**Test Case: Wide Array Visualization**

```
GIVEN: Binary Search with 20-element array
WHEN: Viewport width is 1024px
THEN:
  ✅ Left edge of array is scrollable
  ✅ Right edge of array is scrollable
  ✅ No content cut off on left
  ✅ Horizontal scrollbar appears
```

**Test Case: Correct Pattern Applied**

```
GIVEN: ArrayView component
THEN:
  ✅ Outer container has items-start (NOT items-center)
  ✅ Outer container has overflow-auto
  ✅ Inner wrapper has mx-auto
  ✅ Elements have flex-shrink-0
```

**Anti-Pattern Test:**

```
GIVEN: Wide content
WHEN: Using items-center + overflow-auto
THEN: ❌ FAIL - Left content inaccessible (this is the bug!)
```

---

## Integration Tests: CONSTRAINED Requirements

### Test Suite 7: Backend Contract

**Test Case: Metadata Structure**

```
GIVEN: Algorithm trace loaded
THEN:
  ✅ trace.metadata.algorithm === string
  ✅ trace.metadata.display_name === string
  ✅ trace.metadata.visualization_type in ['array', 'timeline', 'graph', 'tree']
  ✅ trace.metadata.input_size === number
```

**Test Case: Trace Structure**

```
GIVEN: Trace with N steps
THEN:
  ✅ trace.trace.steps.length === N
  ✅ Each step has .step, .type, .description, .data
  ✅ Each step.data has .visualization
  ✅ Visualization data matches visualization_type
```

---

### Test Suite 8: Visualization Components

**Test Case: Component Props**

```
GIVEN: Visualization component
THEN:
  ✅ Accepts step prop
  ✅ Accepts config prop
  ✅ Handles missing step.data.visualization gracefully
  ✅ Shows fallback message on null data
```

**Test Case: State-Based Styling**

```
GIVEN: Binary Search examining mid element
THEN:
  ✅ Mid element has distinct visual state (e.g., yellow, pulsing)
  ✅ Active range elements have different state (e.g., blue)
  ✅ Excluded elements have different state (e.g., gray, dimmed)
```

---

### Test Suite 9: Prediction Mode

**Test Case: Choice Limit**

```
GIVEN: Algorithm with prediction points
THEN:
  ✅ Every prediction has ≤3 choices
  ❌ FAIL if any prediction has 4+ choices
```

**Test Case: Shortcut Derivation**

```
GIVEN: Choices ["Found!", "Search Left", "Search Right"]
THEN:
  ✅ Shortcuts are F, L, R (semantic first letters)
  ✅ Fallback numbers 1, 2, 3 also work
```

**Test Case: Two-Step Confirmation**

```
GIVEN: Prediction modal open
WHEN: Select choice (press F)
THEN:
  ✅ Choice button highlights (scale-105, ring-2)
  ✅ Other choices dim (opacity-60)
  ✅ Submit button activates (removes opacity-50)

WHEN: Press Enter
THEN:
  ✅ Submits answer
  ✅ Shows feedback (correct/incorrect)
```

---

### Test Suite 10: Completion Modal

**Test Case: Last-Step Detection**

```
GIVEN: Trace with 8 steps
WHEN: Navigate to step 7 (last step, 0-indexed)
THEN:
  ✅ Completion modal appears
  ✅ Uses last-step check (NOT step.type check)
```

**Test Case: Algorithm-Specific Results**

```
GIVEN: Binary Search trace (found=true)
THEN:
  ✅ Shows "Target Found!" message
  ✅ Shows comparisons count
  ✅ Shows found index
  ✅ Border is emerald (success color)

GIVEN: Binary Search trace (found=false)
THEN:
  ✅ Shows "Target Not Found" message
  ✅ Border is red (failure color)
```

**Test Case: Prediction Accuracy**

```
GIVEN: Completed trace with predictions
THEN:
  ✅ Shows accuracy percentage
  ✅ Shows correct/total (e.g., 19/20)
  ✅ Shows feedback message based on accuracy

GIVEN: Completed trace WITHOUT predictions
THEN:
  ✅ Accuracy section hidden
  ✅ No prediction stats displayed
```

---

## Cross-Algorithm Tests

### Test Suite 11: Algorithm Switching

**Test Case: Switch Between Algorithms**

```
GIVEN: Interval Coverage loaded and running
WHEN: Select Binary Search from dropdown
THEN:
  ✅ Trace resets to step 0
  ✅ Visualization changes to ArrayView
  ✅ No console errors
  ✅ No visual glitches
  ✅ Prediction stats reset
```

**Test Case: State Isolation**

```
GIVEN: Interval Coverage at step 5
WHEN: Switch to Binary Search
THEN:
  ✅ Binary Search starts at step 0 (not step 5)
  ✅ No data leakage between algorithms
  ✅ Each algorithm has independent state
```

---

### Test Suite 12: Responsive Behavior

**Test Case: Viewport Sizes**

```
Test at: 1920px, 1366px, 1024px

At each size:
  ✅ Panel ratio maintained (3:1.5)
  ✅ Steps panel never < 384px
  ✅ Modals fit in viewport
  ✅ No horizontal body scrollbar
  ✅ All content accessible
```

---

## Performance Tests

### Test Suite 13: Large Traces

**Test Case: 50+ Steps**

```
GIVEN: Algorithm with 50 steps
WHEN: Navigate through entire trace
THEN:
  ✅ No lag or stuttering
  ✅ Auto-scroll remains smooth
  ✅ Memory usage stable
  ✅ No memory leaks
```

**Test Case: Wide Arrays**

```
GIVEN: Binary Search with 100-element array
THEN:
  ✅ Renders without lag
  ✅ Scrolling is smooth
  ✅ All elements accessible
```

---

## Regression Tests

### Test Suite 14: Existing Algorithms

**Test Case: All Existing Algorithms Still Work**

```
GIVEN: Each existing algorithm
THEN:
  ✅ Visualization renders correctly
  ✅ Prediction mode works
  ✅ Completion modal appears
  ✅ Auto-scroll functions
  ✅ All features intact
```

**Test Case: No New Bugs**

```
GIVEN: All algorithms loaded
THEN:
  ✅ No console errors
  ✅ No visual regressions
  ✅ No broken interactions
  ✅ Performance unchanged
```

---

## Acceptance Criteria

### PASS ✅

**All of the following must be true:**

- ✅ Phase 1: Narrative review APPROVED
- ✅ All LOCKED requirement tests pass (Suites 1-6)
- ✅ All CONSTRAINED requirement tests pass (Suites 7-10)
- ✅ Cross-algorithm tests pass (Suite 11)
- ✅ Responsive tests pass (Suite 12)
- ✅ No regressions (Suite 14)

### MINOR ISSUES ⚠️

**One or more of the following:**

- ⚠️ Performance test warnings (Suite 13) but not failures
- ⚠️ Minor visual inconsistencies (but no LOCKED violations)
- ⚠️ Documentation updates needed

### FAIL ❌

**Any of the following:**

- ❌ Phase 1: Narrative review REJECTED
- ❌ Any LOCKED requirement test fails
- ❌ Overflow pattern violated (left edge cut off)
- ❌ >3 prediction choices found
- ❌ Required IDs missing
- ❌ Keyboard shortcuts broken
- ❌ Existing algorithm regressed

---

## Test Execution Template

```markdown
# Integration Test Run: [Algorithm Name] - [Date]

## Phase 1: Narrative Review

- [x] APPROVED on [Date] by [Reviewer Name]

## Test Environment

- Browser: Chrome 120+, Firefox 121+, Safari 17+
- Viewport: 1920x1080, 1366x768, 1024x768
- OS: Windows 11, macOS 14, Ubuntu 22.04

## Suite 1: Modal Standards

- [ ] Prediction modal size: PASS/FAIL
- [ ] Completion modal size: PASS/FAIL
- [ ] Vertical efficiency: PASS/FAIL

## Suite 2: Panel Layout

- [ ] Flex ratio 3:1.5: PASS/FAIL
- [ ] Min width 384px: PASS/FAIL
- [ ] Overflow behavior: PASS/FAIL

[... continue for all suites ...]

## Overall Result: PASS/FAIL

## Notes:

- [Any observations or issues]

## Sign-off:

- QA Engineer: [Name], [Date]
```

---

## Workflow Summary

```
Stage 1: Backend Implementation
  ↓
Stage 2: QA Phase 1 - Narrative Review
  ↓
  ├─→ APPROVED → Stage 3: Frontend Integration
  │                ↓
  │              Stage 4: QA Phase 2 - Integration Testing
  │                ↓
  │              DONE
  │
  └─→ REJECTED → Back to Stage 1
```

**Key Innovation:** Narrative review catches 60-70% of issues BEFORE frontend work begins.

---

**Remember:**

- Phase 1 (narrative review) is the quality gate
- Phase 2 (integration testing) should have minimal surprises
- The goal is to ensure standards are consistently applied
- Use this checklist as a conversation starter, not a gotcha list

**For detailed workflow information, see:** WORKFLOW.md v2.0
