## Reconnaissance Summary

Since you have provided the full codebase, I have accelerated the audit process to combine Phase 1 (Reconnaissance) and Phase 2 (Deep Analysis).

- **Total components**: ~15 active components (excluding generic UI wrappers).
- **Largest components**:
  - `src/components/PredictionModal.jsx`: ~280 lines (Complex UI logic + internal state).
  - `src/App.jsx`: ~260 lines (Orchestration, Layout, State).
  - `src/components/visualizations/TimelineView.jsx`: ~160 lines (Visualization logic).
- **State management**: Pure React Hooks (`useState`, `useEffect`). No global store (Redux/Context), which is good for this size but leading to prop-drilling in `App.jsx`.
- **Architecture**: Registry-based pattern (`stateRegistry.js`, `visualizationRegistry.js`) is a **major strength**, allowing the backend to drive frontend behavior without code changes.
- **Hotspots Identified**:
  1.  **`App.jsx`**: Acts as a "God Component," mixing layout, data fetching, and event orchestration.
  2.  **`TimelineView.jsx`**: Relies on "magic number" CSS math (`4 + left * 0.92`), making it fragile to styling changes.
  3.  **Keyboard Event Chaos**: Listeners are scattered across `App.jsx`, `PredictionModal`, and `TwoPointerState`, creating potential race conditions.

---

## Priority 1: High-Impact, Low-Effort Fixes

### Issue 1: Layout/Logic Coupling in `App.jsx`

- **Location**: `src/App.jsx:L230-330`
- **Problem**: `App.jsx` is responsible for both **orchestrating logic** (hooks, data loading) and **defining the DOM structure** (headers, panels, flex containers). This makes the file hard to read and means any visual change risks breaking logic.
- **Impact**: High. Adding new features (like a Settings menu) will make this file unmaintainable.
- **Effort**: 1.5 hours.
- **Fix Strategy**: Extract the visual shell into a dumb `DashboardLayout` component.
  1. Create `src/components/layout/DashboardLayout.jsx`.
  2. Move the JSX from `App.jsx` (lines 230-330) into this new component.
  3. Pass logic elements (ControlBar, Visualizations) as `children` or named slots (e.g., `headerContent`, `leftPanel`, `rightPanel`).

### Issue 2: Fragile CSS Math in `TimelineView.jsx`

- **Location**: `src/components/visualizations/TimelineView.jsx:L60-65`
- **Problem**: The positioning logic uses magic numbers to compensate for padding:
  ```javascript
  left: `${4 + left * 0.92}%`, // 4% padding + 92% content width
  ```
  If you change the container padding from `p-4` to `p-6`, the visualization breaks alignment.
- **Impact**: Medium. Simple CSS updates break the core visualization.
- **Effort**: 45 mins.
- **Fix Strategy**:
  1. Remove the padding from the parent container's calculation context.
  2. Create an inner `relative` container that is exactly 100% width of the _content area_.
  3. Position elements using pure percentages (`left: ${left}%`, `width: ${width}%`) without the `0.92` multiplier.

### Issue 3: Keyboard Shortcut Race Condition

- **Location**: `src/components/algorithm-states/TwoPointerState.jsx:L19-33`
- **Problem**: `TwoPointerState` adds a global `keydown` listener for the 'P' key.
  ```javascript
  window.addEventListener("keydown", handleKeyDown); // No check for modalOpen!
  ```
  If the user is typing in a future input field or if a modal is open, pressing 'P' will still trigger the pointer action.
- **Impact**: Medium. Unexpected behavior when modals are open.
- **Effort**: 30 mins.
- **Fix Strategy**:
  1. Accept `modalOpen` as a prop in `TwoPointerState` (passed down from `App.jsx`).
  2. Add `if (modalOpen) return;` to the event handler.
  3. **Better yet**: Move this specific shortcut into the centralized `useKeyboardShortcuts` hook to maintain a single source of truth for input handling.

---

## Priority 2: Quick Wins

### Issue 4: Render-Blocking Logic in `PredictionModal.jsx`

- **Location**: `src/components/PredictionModal.jsx:L18-60`
- **Problem**: The `mappedChoices` logic iterates through choices and performs string matching to assign colors _inside the render body_. This runs on every re-render.
- **Fix**: Move the `getChoiceStyle(label)` logic to a utility function outside the component or in `src/utils/styleUtils.js`.
- **Effort**: 30 mins.

### Issue 5: Hardcoded Constants in `ArrayView.jsx`

- **Location**: `src/components/visualizations/ArrayView.jsx:L21-32`
- **Problem**: `POINTER_STYLES` object is redefined on every render.
- **Fix**: Move `POINTER_STYLES` outside the component function (it's constant data).
- **Effort**: 10 mins.

---

## Priority 3: Strategic Improvements

### Architectural: Trace Context

- **Problem**: You are prop-drilling `trace`, `step`, and `metadata` through `App` -> `Visualization` -> `Child`.
- **Recommendation**: Introduce a `TraceContext`.
  - `App.jsx` fetches data and provides `<TraceProvider value={{ trace, step, metadata }}>`.
  - Child components like `BinarySearchState` consume it directly.
  - **Benefit**: Removes ~10 props from `App.jsx` and makes adding new components trivial.

---

## SWOT Analysis

### Strengths

- **Registry Pattern**: The use of `stateRegistry` and `visualizationRegistry` is excellent. It decouples the backend algorithm list from the frontend code. You can add 10 new algorithms without changing `App.jsx` routing.
- **Zero-Logic Principle**: The frontend correctly treats the backend trace as the source of truth, avoiding complex client-side state recalculations.

### Weaknesses

- **God Component (`App.jsx`)**: Too many responsibilities (Layout + Logic + State).
- **Fragile Visualization CSS**: Magic numbers in `TimelineView` make styling changes risky.
- **Distributed Event Handling**: Keyboard listeners are scattered, risking conflicts.

### Opportunities

- **Standardize Layouts**: Creating a `DashboardLayout` component will make the app look more professional and easier to maintain.
- **Centralize Shortcuts**: Moving all keyboard logic to `useKeyboardShortcuts` prevents "ghost" triggers.

### Threats

- **Scalability**: As you add more algorithms (like Graph or Tree), `App.jsx` will become unmanageable if layout isn't separated from logic.

## Recommended Action Plan

1.  **Hour 1**: Fix **Issue 3** (Keyboard Race Condition) and **Issue 5** (ArrayView Constants). These are quick and prevent bugs.
2.  **Hour 2**: Tackle **Issue 2** (TimelineView CSS). This stabilizes your visualization against future CSS changes.
3.  **Hour 3**: Refactor **Issue 1** (App.jsx Layout). Create `DashboardLayout.jsx` and move the JSX there. This is the highest value architectural change.
