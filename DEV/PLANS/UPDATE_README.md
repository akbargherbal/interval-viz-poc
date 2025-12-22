# 📋 README.md Frontend Fact-Checking Plan

## Overview

This plan systematically verifies that the **Frontend sections** of README.md accurately reflect the current state of the frontend codebase after recent refactoring (context migration, deprecated hook cleanup, new components, etc.).

---

## 🎯 Scope: Frontend Only

**What We're Checking:**
- Frontend directory structure
- Component files and organization
- Hooks and contexts
- Registries (state & visualization)
- Frontend-specific architecture claims

**What We're NOT Checking:**
- Backend implementation
- API endpoints
- Algorithm tracers
- Compliance documentation
- Workflow stages

---

## 📊 Frontend Sections to Fact-Check

### **Section 1: Project Structure - Frontend Tree (Lines 348-384)**

**README Claims:**

```
frontend/
├── src/
│   ├── components/
│   │   ├── AlgorithmSwitcher.jsx
│   │   ├── ControlBar.jsx
│   │   ├── CompletionModal.jsx
│   │   ├── PredictionModal.jsx
│   │   ├── KeyboardHints.jsx
│   │   ├── panels/
│   │   │   ├── VisualizationPanel.jsx
│   │   │   └── StatePanel.jsx
│   │   ├── algorithm-states/
│   │   │   ├── BinarySearchState.jsx
│   │   │   ├── IntervalCoverageState.jsx
│   │   │   └── index.js
│   │   └── visualizations/
│   │       ├── ArrayView.jsx
│   │       ├── TimelineView.jsx
│   │       └── index.js
│   ├── contexts/
│   │   ├── TraceContext.jsx
│   │   ├── NavigationContext.jsx
│   │   ├── PredictionContext.jsx
│   │   ├── HighlightContext.jsx
│   │   └── KeyboardContext.jsx
│   ├── hooks/
│   │   ├── useTraceLoader.js          ⚠️ DEPRECATED
│   │   ├── useTraceNavigation.js      ⚠️ DEPRECATED
│   │   ├── usePredictionMode.js       ⚠️ DEPRECATED
│   │   ├── useVisualHighlight.js      ⚠️ DEPRECATED
│   │   └── useKeyboardShortcuts.js
│   ├── utils/
│   │   ├── stateRegistry.js
│   │   └── visualizationRegistry.js
```

**Verification Commands:**

```bash
# Get actual frontend structure
cd /home/akbar/Jupyter_Notebooks/avp/frontend/src

# Components directory
echo "=== COMPONENTS ==="
ls -1 components/*.jsx 2>/dev/null | sed 's|components/||'

# Algorithm states
echo -e "\n=== ALGORITHM STATES ==="
ls -1 components/algorithm-states/*.jsx 2>/dev/null | sed 's|components/algorithm-states/||'

# Visualizations
echo -e "\n=== VISUALIZATIONS ==="
ls -1 components/visualizations/*.jsx 2>/dev/null | sed 's|components/visualizations/||'

# Contexts
echo -e "\n=== CONTEXTS ==="
ls -1 contexts/*.jsx 2>/dev/null | sed 's|contexts/||'

# Hooks
echo -e "\n=== HOOKS ==="
ls -1 hooks/*.js 2>/dev/null | sed 's|hooks/||'

# Utils
echo -e "\n=== UTILS ==="
ls -1 utils/*.js 2>/dev/null | sed 's|utils/||'

# Constants (not in README)
echo -e "\n=== CONSTANTS (NOT IN README) ==="
ls -1 constants/*.js 2>/dev/null | sed 's|constants/||'
```

**Expected Discrepancies:**

| Item | README Claim | Actual State | Fix Needed |
|------|-------------|--------------|------------|
| **Hooks** | Lists 4 deprecated hooks | Hooks should be deleted | ✅ Remove from README |
| **Algorithm States** | Only lists 2 files | Should list 5 (Binary, Interval, Merge, Sliding, TwoPointer) | ✅ Add missing files |
| **Visualizations** | Only lists 2 files | Should list 5+ (Array, Timeline, Interval, MergeSort, RecursiveCallStack, ArrayItem) | ✅ Add missing files |
| **Components** | Lists 5 files | Missing ErrorBoundary, AlgorithmInfoModal | ✅ Add missing files |
| **Constants** | Not mentioned | `intervalColors.js` exists | ✅ Add section |

---

### **Section 2: Dynamic Component Selection (Lines 292-332)**

**README Claims:**

```javascript
// Frontend LEFT panel - dynamically selects visualization
const VisualizationComponent = getVisualizationComponent(
  trace.metadata.visualization_type // 'array' → ArrayView
);

// Frontend RIGHT panel - dynamically selects state component
const StateComponent = getStateComponent(
  currentAlgorithm // 'binary-search' → BinarySearchState
);
```

**Available Visualization Types:**
- `array` - For Binary Search, Sorting algorithms
- `timeline` - For Interval Coverage
- `graph` - Future: DFS, BFS, Dijkstra
- `tree` - Future: BST, Heap operations

**Verification Commands:**

```bash
# Check actual visualization types registered
cat /home/akbar/Jupyter_Notebooks/avp/frontend/src/utils/visualizationRegistry.js | grep -A 30 "VISUALIZATION_REGISTRY = {"

# Check actual state component keys
cat /home/akbar/Jupyter_Notebooks/avp/frontend/src/utils/stateRegistry.js | grep -A 20 "STATE_REGISTRY = {"
```

**Expected Discrepancies:**

| Item | README Claim | Actual State | Fix Needed |
|------|-------------|--------------|------------|
| **Viz Types** | `array, timeline, graph, tree` | `interval-coverage, timeline, array, merge-sort` | ✅ Update list |
| **graph type** | Listed as available | Commented as "Future" | ✅ Mark as Future |
| **tree type** | Listed as available | Commented as "Future" | ✅ Mark as Future |
| **interval-coverage** | Not mentioned | Actually registered | ✅ Add to list |
| **merge-sort** | Not mentioned | Actually registered | ✅ Add to list |

---

### **Section 3: App.jsx Import Pattern (Implied in docs)**

**README May Imply (via examples):**

```javascript
import { useTraceLoader } from "./hooks/useTraceLoader";
import { useTraceNavigation } from "./hooks/useTraceNavigation";
import { usePredictionMode } from "./hooks/usePredictionMode";
```

**Verification Command:**

```bash
# Check actual imports in App.jsx
head -30 /home/akbar/Jupyter_Notebooks/avp/frontend/src/App.jsx | grep "^import"
```

**Expected Discrepancies:**

| Item | README Pattern | Actual State | Fix Needed |
|------|---------------|--------------|------------|
| **Hook imports** | Shows deprecated wrappers | Should show direct context imports | ✅ Update to show `useTrace`, `useNavigation`, `usePrediction` |

---

### **Section 4: Overflow Pattern (Lines 517-530)**

**README Claims:**

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

**Verification Commands:**

```bash
# Check if actual components follow this pattern
grep -rn "items-start" /home/akbar/Jupyter_Notebooks/avp/frontend/src/components/panels/*.jsx
grep -rn "items-center" /home/akbar/Jupyter_Notebooks/avp/frontend/src/components/panels/*.jsx

# Check visualizations
grep -rn "items-start" /home/akbar/Jupyter_Notebooks/avp/frontend/src/components/visualizations/*.jsx
```

**Expected State:**
- ✅ Should find `items-start` pattern in panel components
- ✅ Pattern should be followed consistently

---

### **Section 5: Keyboard Shortcuts (Lines 1099-1112)**

**README Claims:**

| Keys | Action | Context |
|------|--------|---------|
| `→` or `Space` | Next step | During navigation |
| `←` | Previous step | During navigation |
| `R` or `Home` | Reset to start | Anytime |
| `End` | Jump to end | During navigation |
| `K` | Predict first option | In prediction modal |
| `C` | Predict second option | In prediction modal |
| `S` | Skip question | In prediction modal |
| `Enter` | Submit answer | In prediction modal |
| `Esc` | Close modal | In completion modal |

**Verification Commands:**

```bash
# Check actual keyboard shortcuts implementation
cat /home/akbar/Jupyter_Notebooks/avp/frontend/src/hooks/useKeyboardShortcuts.js | grep -A 5 "case 'Arrow\|case 'Key\|case 'Home\|case 'End\|case 'Enter\|case 'Escape'"

# Check if shortcuts are documented in component
cat /home/akbar/Jupyter_Notebooks/avp/frontend/src/components/KeyboardHints.jsx | grep -i "arrow\|key\|home\|end\|enter\|escape" | head -20
```

**Expected State:**
- ✅ Should match README claims
- ⚠️ Verify `Space` for next step (might not be implemented)

---

### **Section 6: Context State Management (Implied)**

**README Shows (via Project Structure):**
- 5 contexts listed

**Verification Command:**

```bash
# List all contexts and their exports
for file in /home/akbar/Jupyter_Notebooks/avp/frontend/src/contexts/*.jsx; do
  echo "=== $(basename $file) ==="
  grep "^export" "$file"
  echo ""
done
```

**Expected Discrepancies:**
- ✅ All 5 contexts should exist
- ✅ Each should export a Provider and a hook

---

## 🔍 Comprehensive Frontend Verification Script

```bash
#!/bin/bash
# README Frontend Fact-Checking Script
# Run from: /home/akbar/Jupyter_Notebooks/avp/frontend

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         README.md FRONTEND FACT-CHECK REPORT                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Generated: $(date)"
echo "Scope: Frontend codebase only"
echo ""

cd src

# ============================================================================
# 1. DIRECTORY STRUCTURE VERIFICATION
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  DIRECTORY STRUCTURE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📁 COMPONENTS (Top-level)"
echo "README lists: AlgorithmSwitcher, ControlBar, CompletionModal, PredictionModal, KeyboardHints"
echo "Actual files:"
ls -1 components/*.jsx 2>/dev/null | sed 's|components/||' | sed 's/^/  ✓ /'
echo ""

echo "📁 ALGORITHM STATES"
echo "README lists: BinarySearchState.jsx, IntervalCoverageState.jsx"
echo "Actual files:"
ls -1 components/algorithm-states/*.jsx 2>/dev/null | sed 's|components/algorithm-states/||' | sed 's/^/  ✓ /'
echo ""

echo "📁 VISUALIZATIONS"
echo "README lists: ArrayView.jsx, TimelineView.jsx"
echo "Actual files:"
ls -1 components/visualizations/*.jsx 2>/dev/null | sed 's|components/visualizations/||' | sed 's/^/  ✓ /'
echo ""

echo "📁 CONTEXTS"
echo "README lists: TraceContext, NavigationContext, PredictionContext, HighlightContext, KeyboardContext"
echo "Actual files:"
ls -1 contexts/*.jsx 2>/dev/null | sed 's|contexts/||' | sed 's/^/  ✓ /'
echo ""

echo "📁 HOOKS"
echo "README lists: useTraceLoader, useTraceNavigation, usePredictionMode, useVisualHighlight, useKeyboardShortcuts"
echo "Actual files:"
ls -1 hooks/*.js 2>/dev/null | sed 's|hooks/||' | sed 's/^/  ✓ /'
echo ""

echo "📁 UTILS"
echo "README lists: stateRegistry.js, visualizationRegistry.js"
echo "Actual files:"
ls -1 utils/*.js 2>/dev/null | sed 's|utils/||' | sed 's/^/  ✓ /'
echo ""

echo "📁 CONSTANTS (NOT IN README)"
echo "Actual files:"
ls -1 constants/*.js 2>/dev/null | sed 's|constants/||' | sed 's/^/  ! /' || echo "  (no constants directory)"
echo ""

# ============================================================================
# 2. VISUALIZATION REGISTRY
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  VISUALIZATION REGISTRY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "README claims: array, timeline, graph (future), tree (future)"
echo ""
echo "Actual registered types:"
grep -A 30 "VISUALIZATION_REGISTRY = {" utils/visualizationRegistry.js | grep '":' | grep -v '//' | sed 's/.*"\([^"]*\)".*/  ✓ \1/'
echo ""
echo "Future/commented types:"
grep -A 30 "VISUALIZATION_REGISTRY = {" utils/visualizationRegistry.js | grep '//' | grep '":' | sed 's|.*// ||' | sed 's/^/  ○ /'
echo ""

# ============================================================================
# 3. STATE REGISTRY
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  STATE REGISTRY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Registered algorithm state components:"
grep -A 20 "STATE_REGISTRY = {" utils/stateRegistry.js | grep '":' | sed 's/.*"\([^"]*\)".*/  ✓ \1/'
echo ""

# ============================================================================
# 4. APP.JSX IMPORTS
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  APP.JSX IMPORT PATTERN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Hook/Context imports:"
head -30 App.jsx | grep "from.*hooks\|from.*contexts" | sed 's/^/  /'
echo ""

# ============================================================================
# 5. KEYBOARD SHORTCUTS
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  KEYBOARD SHORTCUTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Implemented shortcuts (from useKeyboardShortcuts.js):"
grep "case '" hooks/useKeyboardShortcuts.js | sed "s/.*case '\([^']*\)'.*/  ✓ \1/" | sort -u
echo ""

# ============================================================================
# 6. OVERFLOW PATTERN COMPLIANCE
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  OVERFLOW PATTERN COMPLIANCE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "README claims: Should use 'items-start' NOT 'items-center'"
echo ""
echo "Checking panels:"
grep -n "items-start\|items-center" components/panels/*.jsx | sed 's/^/  /'
echo ""
echo "Checking visualizations:"
grep -n "items-start\|items-center" components/visualizations/*.jsx | head -10 | sed 's/^/  /'
echo ""

# ============================================================================
# 7. CONTEXT EXPORTS
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣  CONTEXT EXPORTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
for file in contexts/*.jsx; do
  echo "📄 $(basename $file)"
  grep "^export" "$file" | sed 's/^/  /'
  echo ""
done

# ============================================================================
# 8. DEPRECATED FILES CHECK
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8️⃣  DEPRECATED FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Checking for @deprecated annotations:"
grep -r "@deprecated" hooks/ --include="*.js" | sed 's/^/  ⚠️  /'
echo ""
echo "Files README lists that may be deprecated:"
echo "  - hooks/useTraceLoader.js"
echo "  - hooks/useTraceNavigation.js"
echo "  - hooks/usePredictionMode.js"
echo "  - hooks/useVisualHighlight.js"
echo ""
echo "Checking if these files exist:"
for file in useTraceLoader.js useTraceNavigation.js usePredictionMode.js useVisualHighlight.js; do
  if [ -f "hooks/$file" ]; then
    echo "  ⚠️  hooks/$file EXISTS (should be removed from README)"
  else
    echo "  ✓ hooks/$file REMOVED (README needs update)"
  fi
done
echo ""

# ============================================================================
# SUMMARY
# ============================================================================
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    FACT-CHECK COMPLETE                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Review the output above for discrepancies"
echo ""
echo "Common expected issues:"
echo "  • Deprecated hooks still listed in README"
echo "  • Missing new components (MergeSortState, RecursiveCallStackView, etc.)"
echo "  • Outdated visualization type list"
echo "  • Missing constants directory"
echo ""
```

---

## 📝 Frontend-Specific Updates Needed

### **Priority 1: Critical Inaccuracies**

1. **Remove Deprecated Hooks from Project Structure**
   - Lines 374-377: Delete references to 4 deprecated hooks
   - Add note: "Context hooks are now imported directly from `contexts/`"

2. **Update Visualization Types List**
   - Lines 326-331: Replace with actual types
   - Mark `graph` and `tree` as "Future (not yet implemented)"

3. **Update Algorithm States List**
   - Lines 360-362: Add missing files (MergeSortState, SlidingWindowState, TwoPointerState)

### **Priority 2: Missing Information**

4. **Add Missing Components Section**
   - Add: ErrorBoundary.jsx, AlgorithmInfoModal.jsx
   - Add: visualizations/ArrayItem.jsx, RecursiveCallStackView.jsx, IntervalCoverageVisualization.jsx, MergeSortVisualization.jsx

5. **Add Constants Section**
   - Document `constants/intervalColors.js`

### **Priority 3: Pattern Updates**

6. **Update Import Examples**
   - Show direct context imports instead of deprecated wrapper hooks

---

## 📦 Deliverable Template

```markdown
# Frontend Fact-Check Report
**Date:** [SESSION_DATE]
**Scope:** Frontend codebase only

## Summary
- **Total Discrepancies Found:** X
- **Critical:** X
- **Moderate:** X
- **Minor:** X

## Detailed Findings

### 1. Project Structure
**Issue:** [Description]
**Location:** README.md lines X-Y
**Current README:** [What it says]
**Actual State:** [What actually exists]
**Fix Required:** [What to change]

[Repeat for each finding...]

## Recommended Changes
[List of specific edits to make]

## Sign-off
- [ ] All frontend sections verified
- [ ] All discrepancies documented
- [ ] Recommended changes clear and actionable
```

---

**Estimated Time:** 20-30 minutes to run script + review results

Would you like me to create this as a standalone file you can save for next session?