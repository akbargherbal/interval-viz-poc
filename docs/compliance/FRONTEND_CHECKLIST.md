# Frontend UI/UX Compliance Checklist

**Version:** 2.1  
**Authority:** WORKFLOW.md v2.1 - Frontend Requirements  
**Visual Authority:** `docs/static_mockup/*.html` - Single source of truth for all visual standards  
**Purpose:** Verify UI components comply with platform standards

**Changes from v2.0:**

- Added FAA audit completion to pre-integration validation
- Added "Using Narratives as Reference" section (optional but recommended)
- Updated authority reference to WORKFLOW.md v2.1
- Clarified narratives are supporting reference (JSON is primary)

**Changes from v1.2:**

- Updated authority reference from TENANT_GUIDE.md to WORKFLOW.md
- Corrected modal sizing based on UPDATED mockups (removed max-h-[85vh], updated padding)
- Added narrative validation prerequisite
- Updated keyboard shortcuts (Space = Next step, not Toggle mode)
- Added workflow integration (Stage 3)

---

## CRITICAL: Visual Standards Authority

**When text interpretation differs from mockups, mockups win.**

All visual decisions reference `docs/static_mockup/`:

- `algorithm_page_mockup.html` - Panel layout, keyboard shortcuts
- `prediction_modal_mockup.html` - Prediction modal standards
- `completion_modal_mockup.html` - Completion modal standards (Compact Redesign)

---

## Pre-Integration Validation

**Before starting frontend work:**

- [ ] **QA narrative review PASSED** - Narratives approved for logical completeness
- [ ] **FAA audit completed** - Arithmetic correctness verified (NEW in v2.1)
- [ ] **Backend JSON contract validated** - Narrative confirmed data completeness
- [ ] **FAA-approved narratives available** - Located in `docs/narratives/[algorithm-name]/` (NEW in v2.1)
- [ ] **Trust the JSON** - Frontend focuses on "how to render" not "what to render"

---

## Using Narratives as Reference (NEW in v2.1)

**Optional but Recommended**

### Narratives as Your "Script"

- **JSON is the fuel** (drives your React engine) ← PRIMARY
- **Markdown narratives provide context** (accelerates understanding) ← SUPPORTING

### When to Reference Narratives

- ✅ Understanding algorithm intent ("Why does this step happen?")
- ✅ Debugging visualization ("What should step 5 look like?")
- ✅ Verifying decision logic ("Is my rendering showing the right comparison?")
- ✅ Onboarding to new algorithm ("How does this work?")

### What Narratives Are NOT

- ❌ UI specifications (you have creative freedom - see mockups)
- ❌ Layout requirements (mockups govern visual standards)
- ❌ Binding constraints (JSON is the contract)
- ❌ Implementation instructions (you decide HOW to visualize)

### The Director Analogy

Think of it like theater production:

- **JSON** = Musical score (precise technical notation)
- **Narrative** = Director's notes (context, intent, interpretation)
- **Frontend** = Performance (you bring it to life on stage)

The score tells you exactly what notes to play. The director's notes help you understand why those notes were chosen and what emotion to convey. But you're the performer - you decide the staging, lighting, movements, and presentation.

**Remember:** Narratives describe WHAT the algorithm does. You decide HOW to visualize it. Your creative freedom is protected by WORKFLOW.md's three-tier system (LOCKED/CONSTRAINED/FREE).

### Narrative Quality Guarantees (NEW in v2.1)

All narratives you receive have passed:

1. **FAA Arithmetic Audit** - All mathematical claims verified correct
2. **QA Narrative Review** - Logical completeness and pedagogical quality validated

This means you can trust that:

- ✅ Arithmetic in narratives is correct
- ✅ Decision logic is complete
- ✅ Temporal flow makes sense
- ✅ All referenced data exists in JSON

---

## SECTION 1: LOCKED REQUIREMENTS (Zero Freedom)

### 1.1 Modal Standards

**Source:** `completion_modal_mockup.html` (Compact Redesign) and `prediction_modal_mockup.html`

#### Size Constraints

**CompletionModal (Compact Redesign):**

- [ ] **Width: `max-w-lg w-full`** (512px)
- [ ] **Padding: `p-5`** (20px - compact)
- [ ] **NO height constraint** - Content fits naturally through vertical efficiency

**PredictionModal:**

- [ ] **Width: `max-w-lg w-full`** (512px)
- [ ] **Padding: `p-6`** (24px)
- [ ] **NO height constraint** - Content fits naturally (≤3 choices limit)

**Rationale (from mockup):**

- Title: "Redesigned for Vertical Efficiency (No Element Removal / No Font Scaling)"
- Horizontal layouts reduce vertical space
- Compact spacing prevents overflow
- No need for max-height constraint

#### Positioning

- [ ] **`fixed inset-0`** - Full viewport overlay
- [ ] **`bg-black/80 backdrop-blur-sm`** - Semi-transparent blurred background
- [ ] **`flex items-center justify-center`** - Centered modal
- [ ] **`z-50`** - Above all other content
- [ ] **`p-4`** on overlay - Padding to prevent viewport edge collision

#### Vertical Efficiency Patterns (CompletionModal)

- [ ] **Header: Horizontal layout** - Icon + text in row (NOT column)

  ```jsx
  <div className="flex items-center gap-4 mb-4">
    <div className="flex-shrink-0 w-12 h-12">/* Icon */</div>
    <div>/* Title + subtitle */</div>
  </div>
  ```

- [ ] **Compact spacing:**

  - Section margins: `mb-3`, `mb-4` (NOT mb-6)
  - Inner padding: `p-3` (stats, results)
  - Grid gaps: `gap-2` (stats columns)

- [ ] **Grid with dividers:**

  ```jsx
  <div className="grid grid-cols-3 gap-2">
    <div>/* Column 1 */</div>
    <div className="border-l border-slate-700">/* Column 2 */</div>
    <div className="border-l border-slate-700">/* Column 3 */</div>
  </div>
  ```

- [ ] **Prediction accuracy: Horizontal layout**

  ```jsx
  <div className="flex items-center justify-between">
    <div>/* Label + feedback */</div>
    <div className="text-right">/* Percentage + fraction */</div>
  </div>
  ```

- [ ] **Complex results: Subset + summary**
  ```jsx
  <div className="flex flex-wrap gap-1.5">
    {/* Show first 7-8 items */}
    <div>+1 more</div>
  </div>
  ```

#### Content Fitting Strategy

- [ ] **NO internal scrolling** - Content must fit without `overflow-y-auto`
- [ ] **Use flex-wrap** for lists (intervals, results, badges)
- [ ] **Use compact spacing** throughout
- [ ] **Show summary** for long lists (e.g., "+1 more")

---

### 1.1.1 Modal Spacing Standards

**Source:** Mockup HTML structure

#### CompletionModal Spacing (Compact)

- [ ] **Outer padding: `p-5`** (20px - NOT p-6)
- [ ] **Header section: `mb-4`** (16px below header)
- [ ] **Section gaps: `mb-3` or `mb-4`** (12-16px between sections)
- [ ] **Inner content padding: `p-3`** (12px - stats, results boxes)
- [ ] **Grid gaps: `gap-2`** (8px between stat columns)
- [ ] **Actions section: `pt-3`** (12px above buttons)
- [ ] **Actions gap: `gap-3`** (12px between Close and Start Over)

#### PredictionModal Spacing

- [ ] **Outer padding: `p-6`** (24px)
- [ ] **Question header margin: `mb-6`** (24px - major section break)
- [ ] **Hint box margin: `mb-6`** (24px)
- [ ] **Hint box padding: `p-4`** (16px internal)
- [ ] **Choices grid margin: `mb-6`** (24px below choices)
- [ ] **Choices grid gap: `gap-3`** (12px between buttons)
- [ ] **Actions section: `pt-4`** (16px above actions)

#### Typography Verification

- [ ] **Modal titles: `text-2xl`** (NOT text-3xl)
- [ ] **Subtitle: `text-sm`** (step count, algorithm name)
- [ ] **Section headers: `text-sm` + `font-bold`**
- [ ] **Stat values: `text-xl` + `font-bold`** (NOT text-2xl)
- [ ] **Percentage emphasis: `text-2xl`** (accuracy percentage only)
- [ ] **Labels: `text-xs uppercase tracking-wide`** (stat labels)
- [ ] **Body text: `text-sm`** (descriptions)
- [ ] **Button text: `text-base`** (choice button main text)
- [ ] **Button shortcuts: `text-xs`** (keyboard hints)

#### Visual Quality Checks

- [ ] **Compact without cramped** - Breathing room without waste
- [ ] **Text hierarchy clear** - Size differences create structure
- [ ] **Matches static mockup** - Side-by-side comparison passes

---

### 1.1.2 Outcome-Driven Theming (LOCKED)

**Source:** `completion_modal_mockup.html`

- [ ] **Theming Mandatory** - Modal border and header icon color must reflect result
- [ ] **Success Theme:** Emerald/Green (`border-emerald-500`, `bg-emerald-500`)
- [ ] **Failure Theme:** Red (`border-red-500`, `bg-red-500`)
- [ ] **Neutral/Completion Theme:** Blue (`border-blue-500`, `bg-blue-500`)
- [ ] **Standardized Actions:**
  - Primary (Start Over): Blue (`bg-blue-600`)
  - Secondary (Close): Slate/Gray (`bg-slate-600`)

---

### 1.2 Panel Layout Architecture

**Source:** `algorithm_page_mockup.html`

#### Mandatory Flex Ratio

- [ ] **Visualization panel: `flex-[3]`** - 66.67% width (left panel)
- [ ] **Steps panel: `w-96`** - Fixed 384px (right panel)
- [ ] **Gap between panels: `gap-4`** - 1rem spacing

#### Minimum Widths

- [ ] **Steps panel: 384px minimum** (`w-96`) - Never smaller
- [ ] **Visualization panel: No minimum** - Can shrink with viewport

#### Overflow Handling

- [ ] **Each panel manages own overflow** - `overflow-hidden` on parent
- [ ] **Scrollable content: `overflow-auto`** on inner div
- [ ] **Visualization uses `items-start + mx-auto`** pattern (see 1.6)

---

### 1.3 HTML Landmark IDs

#### Required IDs (6 Mandatory)

- [ ] **`#app-root`** - Top-level app container
- [ ] **`#app-header`** - Main header bar
- [ ] **`#panel-visualization`** - Main visualization area (left panel)
- [ ] **`#panel-steps`** - Right panel container
- [ ] **`#panel-steps-list`** - Scrollable steps/stack list
- [ ] **`#panel-step-description`** - Current step description

#### Dynamic ID

- [ ] **`#step-current`** - Currently executing step (auto-scroll target)
  - Only ONE element has this ID at a time
  - Updates on step navigation

---

### 1.4 Keyboard Navigation

**Source:** `algorithm_page_mockup.html` lines 854-874

#### Standard Shortcuts (Always Active)

- [ ] **`ArrowRight` or `Space`** - Next step
- [ ] **`ArrowLeft`** - Previous step
- [ ] **`r` (lowercase)** - Reset to step 0
- [ ] **`Home`** - Jump to first step (optional)
- [ ] **`End`** - Jump to last step (optional)

#### Prediction Mode Shortcuts

- [ ] **`Enter`** - Submit selected choice
- [ ] **`s`** - Skip prediction (continue without answering)
- [ ] **First letter of choice** - Select choice (e.g., `k`, `c`)
  - Derive from choice labels
  - Fallback to numbers: `1`, `2`, `3`

#### Shortcut Restrictions

- [ ] **Input fields exempt** - Arrow keys move cursor, not steps
- [ ] **Modal open exempts navigation** - Only modal shortcuts active
- [ ] **Respect focus states** - Don't hijack browser controls

---

### 1.5 Auto-Scroll Behavior

**Target:** `#step-current`

- [ ] **Trigger:** On step navigation
- [ ] **Target element:** Current step (has `id="step-current"`)
- [ ] **Scroll behavior:** `smooth` (NOT instant)
- [ ] **Scroll into view:** `scrollIntoView({ behavior: 'smooth', block: 'nearest' })`

---

### 1.6 Overflow Pattern (Critical Fix)

**Problem:** `items-center` + `overflow-auto` cuts off left edge of wide content

**Correct Pattern:**

```jsx
{/* Outer container */}
<div className="... items-start overflow-auto">
  {/* Inner wrapper for centering */}
  <div className="mx-auto">
    {/* Content that might overflow */}
    <svg className="flex-shrink-0">...</svg>
  </div>
</div>
```

#### Checklist

- [ ] **Visualization panel uses `items-start`** - NOT `items-center`
- [ ] **Inner wrapper has `mx-auto`** - For centering when content fits
- [ ] **`overflow-auto` on outer container** - Enables scrolling
- [ ] **`flex-shrink-0` on elements** - Prevent squishing
- [ ] **Tested with wide content** - Verify left edge accessible

---

## SECTION 2: CONSTRAINED REQUIREMENTS (Limited Freedom)

### 2.1 Visualization Component Interface

#### Required Props

- [ ] **`step` prop** - Current step data (includes `step.data.visualization`)
- [ ] **`config` prop** - Visualization config from metadata

#### Required Behavior

- [ ] **Extract visualization data** - From `step?.data?.visualization`
- [ ] **Graceful fallback** - Handle missing data (show message)
- [ ] **State-based styling** - Map element states to visual styles
- [ ] **Overflow pattern** - Use `items-start + mx-auto` (Section 1.6)

#### Allowed Customizations

- [ ] ✅ **Custom animation styles** (transitions, hover effects)
- [ ] ✅ **Algorithm-specific visual elements** (pivot indicators, etc.)
- [ ] ✅ **Color scheme variations** (within Tailwind palette)
- [ ] ✅ **Layout within panel** (grid vs flex vs custom)

#### Restrictions

- [ ] ❌ **NOT ignoring `step.data.visualization` structure**
- [ ] ❌ **NOT violating overflow pattern** (no `items-center + overflow-auto`)
- [ ] ❌ **NOT exceeding panel boundaries** (use `overflow-auto`)

---

### 2.2 Prediction Questions

#### HARD LIMIT: Maximum 3 Choices

- [ ] **≤3 choices per question** - Strictly enforced
- [ ] **2-choice grid: `grid-cols-2`** - Side-by-side layout
- [ ] **3-choice grid: `grid-cols-3`** - Three columns layout

#### Question Simplification (If >3 Natural Choices)

- [ ] **Strategy 1: Higher-level questions** - Yes/No/Maybe
- [ ] **Strategy 2: Group choices conceptually** - Regions/categories
- [ ] **Strategy 3: Skip prediction** - Not every step needs one

#### Button States

- [ ] **Default: `bg-{color}-600`**
- [ ] **Hover: `hover:bg-{color}-500 hover:scale-105`**
- [ ] **Selected: `scale-105 ring-2 ring-{color}-400 shadow-xl`**
- [ ] **Unselected (after selection): `opacity-60`**

---

### 2.3 Completion Modal

#### Detection Strategy

- [ ] **Last-step detection** - Check if `step === trace.trace.steps.length - 1`
- [ ] ❌ **NOT step type check** - Algorithm-agnostic

#### Algorithm-Specific Rendering

- [ ] **Detect algorithm** - From `trace?.metadata?.algorithm`
- [ ] **Render appropriate results** - Binary Search vs Interval Coverage vs Generic
- [ ] **Generic fallback** - Always provide for unknown algorithms

#### Prediction Accuracy Display

- [ ] **Calculate accuracy** - If `predictionStats.total > 0`
- [ ] **Show stats** - Correct/total, percentage
- [ ] **Feedback message** - Based on accuracy percentage
- [ ] **Hide section** - If prediction mode not used

---

## SECTION 3: FREE CHOICES (Your Decision)

### Component Architecture

- [ ] **File organization** - Flat vs nested (your choice)
- [ ] **Component patterns** - Functional vs class (prefer functional)
- [ ] **Code splitting** - React.lazy if needed

### State Management

- [ ] **Built-in React state** - useState, useReducer, useContext
- [ ] **External libraries** - Redux, Zustand, MobX (if needed)

### Performance

- [ ] **Memoization** - React.memo, useMemo, useCallback (when profiled)
- [ ] **Virtualization** - React Virtual/Window (for >100 steps)

---

## Testing Checklist

### LOCKED Requirements Test

- [ ] **CompletionModal uses `max-w-lg p-5`** - Measure width/padding
- [ ] **PredictionModal uses `max-w-lg p-6`** - Measure width/padding
- [ ] **NO height constraint on modals** - Verify no `max-h-[85vh]`
- [ ] **Vertical efficiency patterns** - Horizontal layouts, compact spacing
- [ ] **Outcome theming correct** - Border/Icon color matches result
- [ ] **Panel layout uses 3:1.5 ratio** - Measure widths
- [ ] **All 6 required IDs present** - Inspect DOM
- [ ] **Keyboard shortcuts work** - Arrow keys, Space, R, Home, Enter, S
- [ ] **Auto-scroll works** - `#step-current` scrolls into view
- [ ] **Overflow pattern correct** - Left edge accessible on wide content
- [ ] **Spacing matches mockup** - Side-by-side visual comparison

### CONSTRAINED Requirements Test

- [ ] **Visualization component accepts props** - step, config
- [ ] **Prediction questions ≤3 choices** - Count buttons
- [ ] **Completion modal uses last-step detection** - Check logic

### User Experience Test

- [ ] **No regressions** - Existing algorithms work
- [ ] **Visualization clear** - Easy to understand
- [ ] **Step descriptions helpful** - Meaningful text
- [ ] **Prediction questions meaningful** - Not arbitrary
- [ ] **Modals feel compact** - Efficient use of space
- [ ] **Visual consistency** - All modals look similar

---

## Quick Reference: Modal Standards

| Property          | CompletionModal    | PredictionModal    | Source              |
| ----------------- | ------------------ | ------------------ | ------------------- |
| **Width**         | `max-w-lg` (512px) | `max-w-lg` (512px) | Both mockups        |
| **Height**        | No constraint      | No constraint      | Compact Redesign    |
| **Padding**       | `p-5` (20px)       | `p-6` (24px)       | Updated mockups     |
| **Header layout** | Horizontal (row)   | Vertical (column)  | Compact Redesign    |
| **Section gaps**  | `mb-3`, `mb-4`     | `mb-6`             | Compact vs Standard |
| **Inner padding** | `p-3` (12px)       | `p-4` (16px)       | Content boxes       |
| **Grid gaps**     | `gap-2` (8px)      | `gap-3` (12px)     | Stats/choices       |
| **Title font**    | `text-2xl`         | `text-2xl`         | Both mockups        |

---

## Quick Reference: Required IDs

```jsx
<div id="app-root">
  <div id="app-header">/* Controls */</div>
  <div className="flex gap-4">
    <div id="panel-visualization" className="flex-[3]">
      /* Visualization */
    </div>
    <div id="panel-steps" className="w-96">
      <div id="panel-steps-list" className="overflow-y-auto">
        <div id="step-current">/* Active step - auto-scroll target */</div>
      </div>
      <div id="panel-step-description">/* Current action */</div>
    </div>
  </div>
</div>
```

---

## Workflow Integration (v2.1)

**Stage 3: Frontend Integration**

**Before starting:**

1. ✅ FAA audit completed (NEW in v2.1)
2. ✅ QA narrative review APPROVED
3. ✅ Backend code available
4. ✅ FAA-approved narratives available as reference (NEW in v2.1)

**Your focus:**

- Frontend implements "how to render" (backend already defined "what to render")
- Trust that JSON is logically complete (narrative validated it)
- Trust that JSON is arithmetically correct (FAA validated it) (NEW in v2.1)
- Reference narratives for expected behavior and algorithm understanding

**After completing:**

1. ✅ Complete this Frontend Checklist
2. ✅ Submit PR with code + checklist
3. ✅ Proceed to Stage 4: QA Integration Testing

---

## Approval Criteria

✅ **PASS** - All LOCKED requirements met, spacing matches mockups, no anti-patterns  
⚠️ **MINOR ISSUES** - CONSTRAINED choices questionable but acceptable  
❌ **FAIL** - LOCKED requirements violated, spacing doesn't match mockups, regressions

---

**Remember:**

- The three static mockups are your **visual source of truth**
- When text interpretation differs from mockups, **mockups win**
- Narratives are your **behavioral reference** (what should happen at each step)
- Narratives have been **FAA-verified** for arithmetic correctness (NEW in v2.1)

**For detailed workflow information, see:** WORKFLOW.md v2.1

---

**Version History:**

- v1.0: Initial checklist (Session 17)
- v1.1: Corrected modal standards based on mockup analysis (Session 22)
- v1.2: Critical correction based on explicit documentation (Session 23)
- v2.0: Updated for WORKFLOW.md v2.0 (Session 34)
  - Updated authority reference from TENANT_GUIDE.md to WORKFLOW.md
  - Corrected modal sizing based on UPDATED mockups (Compact Redesign)
  - Removed max-h-[85vh] requirement (not in updated mockups)
  - Updated CompletionModal padding to p-5 (compact)
  - Added vertical efficiency patterns
  - Updated keyboard shortcuts (Space = Next, Home = Reset)
  - Added narrative validation prerequisite
  - Added workflow integration section
- v2.1: Updated for WORKFLOW.md v2.1 (Session 35)
  - Added FAA audit completion to pre-integration validation
  - Added "Using Narratives as Reference" section
  - Clarified narrative quality guarantees (FAA + QA approved)
  - Updated workflow integration to include FAA
  - Updated authority reference to WORKFLOW.md v2.1
