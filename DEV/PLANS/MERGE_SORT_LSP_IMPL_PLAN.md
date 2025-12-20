# 📋 Implementation Plan - Merge Sort LSP Recursive Tree

---

## 🎯 Implementation Scope

### **What's Done:**

- ✅ RSP (Right Side Panel) - 5-zone dashboard complete in `MergeSortState.jsx`
- ✅ Backend provides complete data structure via `call_stack_state` and `all_intervals`
- ✅ Static mockup approved: `/mnt/user-data/outputs/merge_sort_static_mockup_compact.html`

### **What We're Implementing:**

- 🔨 LSP (Left Side Panel) - Recursive call stack tree visualization
- 🔨 Integration with existing RSP dashboard
- 🔨 Main area array comparison view (if not already complete)

---

## 📂 File Structure Analysis

Let me first verify the current project structure:Let me check the frontend directory:Let me request the project structure:

---

## 🔍 Static Analysis Protocol - Project Structure Request

Before creating the implementation plan, I need to verify the current frontend structure:

```bash
# 1. Frontend directory structure
ls -la frontend/src/components/

# 2. Current visualization components
ls -la frontend/src/components/visualizations/

# 3. Current algorithm states
ls -la frontend/src/components/algorithm-states/

# 4. Main layout/app structure
cat frontend/src/App.jsx

# 5. How algorithms are rendered (to understand integration point)
cat frontend/src/components/AlgorithmVisualizer.jsx
# OR
cat frontend/src/components/VisualizationPanel.jsx
```

**Please provide:**

1. The main app/layout component that renders LSP, Main Area, and RSP
2. How `MergeSortState.jsx` is currently integrated
3. Whether there's already a main area component or if we need to create it

---

## 📐 Implementation Plan (Pending Structure Verification)

Based on the checklist and ADRs, here's the anticipated plan:

---

## **Stage 1: Component Architecture Design** (30 minutes)

### **1.1 Create RecursiveCallStackView Component**

**Location**: `frontend/src/components/visualizations/RecursiveCallStackView.jsx`

**Purpose**: Reusable visualization component for recursive call stacks

**Why visualizations/ directory?**

- Per ADR-002: Reusable visualization components go in `visualizations/`
- This can be used by QuickSort, Binary Search, other recursive algorithms

**Component Interface**:

```javascript
RecursiveCallStackView.propTypes = {
  callStackState: PropTypes.arrayOf(
    PropTypes.shape({
      array: PropTypes.array,
      depth: PropTypes.number,
      id: PropTypes.string,
      is_active: PropTypes.bool,
      operation: PropTypes.string,
    })
  ),
  allIntervals: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string,
      label: PropTypes.string,
      state: PropTypes.string,
      color: PropTypes.string,
      start: PropTypes.number,
      end: PropTypes.number,
    })
  ),
};
```

**Data Flow**:

```
Backend JSON step.data.visualization
  ↓
MergeSortState receives step prop
  ↓
Extracts call_stack_state + all_intervals
  ↓
Passes to RecursiveCallStackView
  ↓
Renders tree visualization
```

---

### **1.2 Update MergeSortState Component**

**Location**: `frontend/src/components/algorithm-states/MergeSortState.jsx`

**Current State**: Already has RSP dashboard implementation (5-zone layout)

**Changes Needed**:

1. Add layout wrapper for LSP + Main Area + RSP
2. Extract visualization data for tree
3. Integrate `RecursiveCallStackView` in LSP
4. Create/integrate main area array comparison view

**New Layout Structure**:

```jsx
<div className="merge-sort-layout flex h-full gap-0">
  {/* LSP: Recursive Tree */}
  <div className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col overflow-hidden">
    <RecursiveCallStackView
      callStackState={step?.data?.visualization?.call_stack_state}
      allIntervals={step?.data?.visualization?.all_intervals}
    />
  </div>

  {/* Main Area: Array Comparison */}
  <div className="flex-1 bg-slate-900 overflow-hidden">
    <ArrayComparisonView step={step} />
  </div>

  {/* RSP: Dashboard (existing) */}
  <div className="w-96 bg-slate-800 rounded-xl shadow-2xl flex flex-col overflow-hidden">
    {/* Existing 5-zone dashboard code */}
  </div>
</div>
```

---

### **1.3 Create ArrayComparisonView Component** (If Needed)

**Location**: `frontend/src/components/visualizations/ArrayComparisonView.jsx`

**Purpose**: Shows left/right array comparison during merge phase

**When to Show**:

- `MERGE_START`: Initialize with left/right arrays
- `MERGE_COMPARE`: Show comparison with operator
- `MERGE_TAKE_LEFT/RIGHT`: Show selected value
- `MERGE_REMAINDER`: Show remaining elements
- `MERGE_COMPLETE`: Show final merged array

**Otherwise**: Show current array state for other step types

---

## **Stage 2: Implementation** (4-5 hours)

### **2.1 Create RecursiveCallStackView** (2 hours)

**File**: `frontend/src/components/visualizations/RecursiveCallStackView.jsx`

**Implementation Checklist**:

- [ ] Import React, PropTypes
- [ ] Define PropTypes matching backend data structure
- [ ] Extract and merge call_stack_state with all_intervals data
- [ ] Map backend colors to Tailwind classes
- [ ] Render tree nodes with depth-based indentation
- [ ] Apply active/complete state styling
- [ ] Add state badges (MERGE, SPLIT, DONE)
- [ ] Render collapsed base cases footer
- [ ] Add legend footer
- [ ] Handle missing/null data gracefully

**Reference**: `/mnt/user-data/outputs/merge_sort_static_mockup_compact.html` lines 60-115 (tree styles)

**Color Mapping**:

```javascript
const colorClassMap = {
  blue: "bg-blue-500/15 border-blue-500 text-blue-300",
  green: "bg-green-500/15 border-green-500 text-green-300",
  amber: "bg-amber-500/15 border-amber-500 text-amber-300",
};

const stateClassMap = {
  splitting: "bg-indigo-500/30 text-indigo-200",
  merging: "bg-purple-500/30 text-purple-200",
  complete: "bg-green-500/30 text-green-200",
};
```

**Depth Indentation**:

```javascript
const depthClassMap = {
  0: "ml-0",
  1: "ml-3 border-l-2 border-white/10",
  2: "ml-6 border-l-2 border-white/10",
};
```

---

### **2.2 Create ArrayComparisonView** (1.5 hours)

**File**: `frontend/src/components/visualizations/ArrayComparisonView.jsx`

**Implementation Checklist**:

- [ ] Import React, PropTypes
- [ ] Extract step type and data
- [ ] Render phase indicator badge
- [ ] Show left/right arrays during merge
- [ ] Show comparison operator (>, <, ≤, ≥)
- [ ] Highlight active pointers (L, R badges)
- [ ] Show merged result array with filled/empty slots
- [ ] Handle all merge step types
- [ ] Fallback to simple array view for non-merge steps
- [ ] Handle missing data gracefully

**Reference**: `/mnt/user-data/outputs/merge_sort_static_mockup_compact.html` lines 204-278 (main area)

**Step Type Mapping**:

```javascript
switch (step.type) {
  case "MERGE_START":
  // Show left + right arrays, empty result
  case "MERGE_COMPARE":
  // Show comparison with operator, highlight active elements
  case "MERGE_TAKE_LEFT":
  case "MERGE_TAKE_RIGHT":
  // Show selected value being added to result
  case "MERGE_REMAINDER":
  // Show remaining elements being flushed
  case "MERGE_COMPLETE":
  // Show final merged array
  default:
  // Show current array state
}
```

---

### **2.3 Update MergeSortState Component** (1 hour)

**File**: `frontend/src/components/algorithm-states/MergeSortState.jsx`

**Changes**:

1. Import new components
2. Wrap existing dashboard in 3-column layout
3. Add LSP with RecursiveCallStackView
4. Add Main Area with ArrayComparisonView
5. Keep RSP dashboard unchanged

**Implementation Checklist**:

- [ ] Import RecursiveCallStackView
- [ ] Import ArrayComparisonView
- [ ] Restructure return JSX to 3-column layout
- [ ] Pass step data to tree component
- [ ] Pass step data to array comparison component
- [ ] Maintain existing dashboard code in RSP
- [ ] Verify layout matches static mockup
- [ ] Test with sample data

**Before (Current)**:

```jsx
return <div className="dashboard">{/* 5-zone dashboard */}</div>;
```

**After (New)**:

```jsx
return (
  <div className="merge-sort-layout flex h-full gap-0">
    {/* LSP */}
    <div className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col overflow-hidden">
      <RecursiveCallStackView
        callStackState={step?.data?.visualization?.call_stack_state}
        allIntervals={step?.data?.visualization?.all_intervals}
      />
    </div>

    {/* Main Area */}
    <div className="flex-1 bg-slate-900 overflow-hidden">
      <ArrayComparisonView step={step} />
    </div>

    {/* RSP */}
    <div className="w-96 bg-slate-800 rounded-xl shadow-2xl flex flex-col overflow-hidden">
      <div className="flex justify-between px-5 pt-5 items-center mb-4 flex-shrink-0">
        {/* Existing header */}
      </div>
      <div
        id="panel-steps-list"
        className="flex-[2] flex flex-col overflow-hidden"
      >
        <div className="flex-1 overflow-hidden">
          <div className="dashboard">
            {/* Existing 5-zone dashboard code - UNCHANGED */}
          </div>
        </div>
      </div>
      <div
        id="panel-step-description"
        className="flex-[1] border-t border-slate-700 py-2 px-4 bg-gradient-to-br from-slate-700/60 to-slate-800/60 overflow-hidden flex flex-col"
      >
        {/* Existing description - UNCHANGED */}
      </div>
    </div>
  </div>
);
```

---

### **2.4 Register Components** (15 minutes)

**File**: `frontend/src/components/visualizations/index.js`

**Add**:

```javascript
export { default as RecursiveCallStackView } from "./RecursiveCallStackView";
export { default as ArrayComparisonView } from "./ArrayComparisonView";
```

**Verify**: No changes needed to `stateRegistry.js` (MergeSortState already registered)

---

## **Stage 3: Styling & Polish** (1 hour)

### **3.1 Extract Styles to CSS/Tailwind**

**Reference Static Mockup Styles**:

- Lines 60-115: Tree node styles
- Lines 38-152: Dashboard zone styles (already implemented)

**Create**: `frontend/src/styles/merge-sort.css` (if custom CSS needed)

**Or**: Use Tailwind utility classes inline (preferred)

**Implementation Checklist**:

- [ ] Verify all Tailwind classes from mockup are used
- [ ] Test tree node hover states
- [ ] Test active call glow effect
- [ ] Test completed call opacity
- [ ] Verify responsive behavior (desktop only)

---

### **3.2 Color Consistency Verification**

**Cross-check**:

- Tree colors (blue/green/amber) match backend intent ✅
- Dashboard colors match RSP design ✅
- Main area colors complement both panels ✅

**Colors to Verify**:

```javascript
// Tree (from backend)
Blue: #3b82f6 (Root level)
Green: #22c55e (Mid-level)
Amber: #f59e0b (Base cases)

// Dashboard (from RSP)
Purple: #a855f7 (Hero value)
Emerald: #34d399 (Goal value)
Indigo: #4f46e5 (Logic zone)

// Main Area
Yellow: #eab308 (Left pointer)
Green: #22c55e (Right pointer)
Emerald: #10b981 (Merged items)
```

---

## **Stage 4: Testing** (2 hours)

### **4.1 Unit Testing - Component Rendering**

**Test File**: `frontend/src/components/visualizations/RecursiveCallStackView.test.jsx`

**Test Cases**:

- [ ] Renders with valid call_stack_state data
- [ ] Renders with null/undefined data (graceful degradation)
- [ ] Renders with empty call_stack_state array
- [ ] Maps backend colors correctly
- [ ] Applies depth indentation correctly
- [ ] Shows active state highlighting
- [ ] Shows completed state styling
- [ ] Renders state badges correctly
- [ ] Renders legend footer

**Test File**: `frontend/src/components/visualizations/ArrayComparisonView.test.jsx`

**Test Cases**:

- [ ] Renders MERGE_COMPARE step correctly
- [ ] Renders MERGE_START step correctly
- [ ] Renders MERGE_COMPLETE step correctly
- [ ] Renders non-merge steps with fallback
- [ ] Handles missing left/right arrays
- [ ] Handles null step data

---

### **4.2 Integration Testing - Full Layout**

**Test Scenarios**:

**Scenario 1: Small Array (4 elements)**

```bash
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "merge-sort", "input": {"array": [38, 27, 43, 3]}}'
```

- [ ] Tree shows depth 0-2 calls
- [ ] All tree nodes visible without scrolling
- [ ] Dashboard updates for each step
- [ ] Main area shows comparison correctly

**Scenario 2: Single Element Array**

```bash
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "merge-sort", "input": {"array": [42]}}'
```

- [ ] Tree shows only base case
- [ ] Dashboard shows BASE_CASE state
- [ ] No comparison view (single element)

**Scenario 3: Larger Array (8 elements)**

```bash
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "merge-sort", "input": {"array": [64, 34, 25, 12, 22, 11, 90, 88]}}'
```

- [ ] Tree scrollable for deep recursion
- [ ] All depth levels color-coded correctly
- [ ] Active path highlighted through navigation
- [ ] Completed nodes dimmed appropriately

**Scenario 4: Odd-Length Array**

```bash
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "merge-sort", "input": {"array": [5, 2, 8]}}'
```

- [ ] Tree handles unbalanced splits
- [ ] Comparison view handles odd subarrays

---

### **4.3 Navigation Testing**

**Test Cases**:

- [ ] Forward navigation: Tree updates to show active call
- [ ] Backward navigation: Tree rebuilds previous state
- [ ] Jump to arbitrary step: Tree reflects correct call stack
- [ ] Reset: Tree returns to initial state
- [ ] Keyboard shortcuts work (Space, Shift+Space, R)

---

### **4.4 Visual Regression Testing**

**Side-by-Side Comparison**:

1. Open static mockup: `merge_sort_static_mockup_compact.html`
2. Open running app at step 18 (MERGE_COMPARE)
3. Compare visually:
   - [ ] LSP tree width matches (w-64)
   - [ ] Tree node sizes match
   - [ ] Colors match (blue/green/amber)
   - [ ] Active state glow matches
   - [ ] Main area layout matches
   - [ ] RSP dashboard matches (already done)
   - [ ] Spacing and gaps match

---

## **Stage 5: Documentation** (30 minutes)

### **5.1 Component Documentation**

**Add JSDoc comments**:

```javascript
/**
 * RecursiveCallStackView - Displays recursive call stack as a tree
 *
 * Used by recursive algorithms (Merge Sort, Quick Sort, etc.) to show
 * the hierarchy of recursive calls with depth-based color coding.
 *
 * @param {Array} callStackState - Array of call objects from backend
 * @param {Array} allIntervals - Array of interval metadata from backend
 * @returns {JSX.Element} Tree visualization with header and legend
 */
```

---

### **5.2 Update Algorithm Info**

**File**: `docs/algorithm-info/merge-sort.md` (create if doesn't exist)

**Content**:

```markdown
# Merge Sort

## Visualization Features

### Recursive Call Stack (LSP)

- Shows the tree of recursive calls
- Color-coded by depth (blue → green → amber)
- Active path highlighted
- Completed calls dimmed

### Array Comparison (Main Area)

- Side-by-side comparison during merge
- Active pointers (L/R)
- Building merged result array

### Algorithm State (RSP)

- 5-zone dashboard showing current operation
- Comparison logic and decision
- Merge count and progress
```

---

### **5.3 Update FRONTEND_CHECKLIST.md**

**Add to "Completed Algorithms" section**:

```markdown
## Merge Sort ✅

- State Component: `MergeSortState.jsx`
- Visualizations:
  - `RecursiveCallStackView.jsx` (reusable)
  - `ArrayComparisonView.jsx` (reusable)
- Layout: LSP (tree) + Main (comparison) + RSP (dashboard)
- Reference Mockup: `docs/static_mockup/merge_sort_static_mockup_compact.html`
```

---

## **Stage 6: Code Review & Cleanup** (30 minutes)

### **6.1 Code Quality Checklist**

- [ ] All PropTypes defined
- [ ] No prop drilling (use contexts if needed)
- [ ] Safe data access with optional chaining
- [ ] Early returns for error states
- [ ] No hardcoded values (use constants)
- [ ] No magic numbers in styling
- [ ] Comments explain "why" not "what"
- [ ] No console.logs left in code
- [ ] Imports organized alphabetically
- [ ] No unused imports

---

### **6.2 Anti-Pattern Audit**

- [ ] No registry violations
- [ ] Components in correct directories
- [ ] No LOCKED element modifications
- [ ] No keyboard shortcut conflicts
- [ ] Context hooks used appropriately
- [ ] No algorithm logic reimplementation
- [ ] Defensive programming for data access

---

## 📋 Implementation Checklist Summary

### **Pre-Implementation** (Stage 1.5 - FAA Gate)

- [x] Static mockup created
- [x] Static mockup approved
- [ ] Project structure verified
- [ ] Integration points identified

### **Component Creation** (Stage 2)

- [ ] RecursiveCallStackView.jsx created
- [ ] ArrayComparisonView.jsx created
- [ ] MergeSortState.jsx updated
- [ ] Components registered in index.js

### **Styling** (Stage 3)

- [ ] Tailwind classes applied
- [ ] Color consistency verified
- [ ] Mockup compliance checked

### **Testing** (Stage 4)

- [ ] Component unit tests written
- [ ] Integration tests passed
- [ ] Navigation tests passed
- [ ] Visual regression test passed

### **Documentation** (Stage 5)

- [ ] JSDoc comments added
- [ ] Algorithm info created
- [ ] Checklist updated

### **Review** (Stage 6)

- [ ] Code quality verified
- [ ] Anti-patterns audited
- [ ] Ready for merge

---

## 🚀 Next Steps

**Please provide the following files so I can create concrete implementations:**

```bash
# 1. Current MergeSortState.jsx (we saw it earlier but need to verify latest)
cat frontend/src/components/algorithm-states/MergeSortState.jsx

# 2. Main app/layout component
cat frontend/src/App.jsx
# OR the component that renders algorithm visualizations

# 3. Visualization registry/index
cat frontend/src/components/visualizations/index.js

# 4. Any existing array visualization components
ls -la frontend/src/components/visualizations/
cat frontend/src/components/visualizations/ArrayView.jsx
```

Once I have these, I'll create:

1. ✅ Complete `RecursiveCallStackView.jsx` implementation
2. ✅ Complete `ArrayComparisonView.jsx` implementation
3. ✅ Updated `MergeSortState.jsx` with 3-column layout
4. ✅ Component tests
5. ✅ Integration guide

**Ready to implement once you share the current frontend structure.** 🎯
