✅ **Documentation Reviewed:**
- `WORKFLOW.md` v2.1 (Confirmed: FAA gate active, LOCKED requirements for Modals/Shortcuts)
- `README.md` (Architecture overview)
- `FE_codebase.txt` (Current implementation state)

**Key Observations:**
- **LOCKED Violation:** `PredictionModal` styling does not match the strict dimensions defined in `WORKFLOW.md` (Width: 600px).
- **LOCKED Violation:** Keyboard shortcuts (Esc) are failing across multiple modals, violating the Platform-Wide Shortcut requirements.
- **Architecture Gap:** `App.jsx` uses `useKeyboardShortcuts` but fails to pass the required `onCloseModal` callback, causing the "Esc" failure for Info/Prediction modals.

Ready to proceed with the Bug Report and Execution Plan.

---

## Bug Report: UI/UX Regressions & Modal Behavior

**Classification:** **LOCKED** 🔒 (Violates Platform Architecture & Visual Standards)

### Triage Analysis

| Issue | Affected Component | Severity | Root Cause |
| :--- | :--- | :--- | :--- |
| **1. Prediction Modal Styling** | `PredictionModal.jsx` | **High** | Component uses generic Tailwind (`max-w-lg`) instead of LOCKED pixel-perfect dimensions defined in mockups. |
| **2. Info Modal Styling & Esc** | `AlgorithmInfoModal.jsx` | **Medium** | `App.jsx` fails to pass a close handler to the shortcut hook. Styling deviates from dark theme standards. |
| **3. Keyboard Hints Esc** | `KeyboardHints.jsx` | **Medium** | Component manages local state but lacks a local event listener for the `Escape` key. |

---

## Execution Plan

**Primary Owner:** Frontend Developer
**Reviewer:** QA (Visual & Functional)

### Stage 3: Frontend Fixes (FE)

#### Task 1: Enforce LOCKED Dimensions on Prediction Modal
**Context:** `WORKFLOW.md` explicitly locks modal dimensions to ensure consistent UX.
**File:** `src/components/PredictionModal.jsx`

**Requirements:**
- [ ] Remove generic width classes (e.g., `max-w-lg`).
- [ ] Apply **LOCKED** dimensions: `width: 600px` and `max-height: 80vh`.
- [ ] Update background/border colors to match `docs/static_mockup/prediction_modal_mockup.html` (Dark Slate theme).
- [ ] Ensure the ID `prediction-modal` remains present (LOCKED).

#### Task 2: Fix Global Modal "Escape" Logic
**Context:** `App.jsx` manages state for `PredictionModal` and `AlgorithmInfoModal`, but the keyboard hook isn't wired to close them.
**File:** `src/components/AlgorithmInfoModal.jsx` & `src/App.jsx`

**Requirements for `AlgorithmInfoModal.jsx`:**
- [ ] Update styling to match the "Outcome Theme" used in `CompletionModal` (consistent headers, borders, and backdrop).
- [ ] Ensure content area handles overflow correctly (`overflow-y-auto`).

**Requirements for `App.jsx`:**
- [ ] Create a unified `handleCloseModals` function that:
    - Sets `showAlgorithmInfo(false)`
    - Calls `prediction.handlePredictionSkip()` (if prediction is open)
- [ ] Pass this function to `useKeyboardShortcuts` as the `onCloseModal` prop.
- [ ] **Constraint:** Do not modify the hook logic itself; fix the *usage* in `App.jsx`.

#### Task 3: Fix Keyboard Hints "Escape" Logic
**Context:** `KeyboardHints` is self-contained (local state). It needs its own listener.
**File:** `src/components/KeyboardHints.jsx`

**Requirements:**
- [ ] Add a `useEffect` hook to listen for the `keydown` event.
- [ ] Check for `event.key === 'Escape'`.
- [ ] If pressed, set local state `isOpen` to `false`.
- [ ] Ensure event listener is cleaned up on unmount.

---

### Stage 4: Validation (QA)

**Test Scope:**
1. **Visual Regression:**
   - Open Prediction Modal. Verify width is exactly 600px.
   - Verify colors match the static mockup (no generic blue/gray defaults).
2. **Functional Testing (Keyboard):**
   - Open Algorithm Info → Press `Esc` → Should close.
   - Open Prediction Modal → Press `Esc` → Should skip/close.
   - Open Keyboard Hints → Press `Esc` → Should close.
   - Open Info Modal, then click "Keyboard Hints" → Press `Esc` → Should close Hints first (stacking order check).

**Success Criteria:**
- All modals close via `Esc`.
- Prediction Modal matches `docs/static_mockup/prediction_modal_mockup.html`.
- No console errors regarding missing props.

---

### Scaffolding Reference (For FE Developer)

**1. App.jsx Wiring (Conceptual):**

```javascript
// In App.jsx
const handleCloseModals = () => {
  // TODO: FE - Implement logic to close whichever modal is active
  // 1. If showAlgorithmInfo is true, set to false
  // 2. If prediction.showPrediction is true, call prediction.handlePredictionSkip()
};

useKeyboardShortcuts({
  // ... existing props ...
  onCloseModal: handleCloseModals // <--- Connect this prop
});
```

**2. KeyboardHints.jsx Listener (Conceptual):**

```javascript
// In KeyboardHints.jsx
useEffect(() => {
  // TODO: FE - Implement local keydown listener
  // If key is 'Escape' and isOpen is true -> setIsOpen(false)
  // Don't forget cleanup return () => ...
}, [isOpen]);
```

**Time Estimate:** 45 Minutes
**Rollback Plan:** Revert `App.jsx` and component style changes if layout breaks on mobile.