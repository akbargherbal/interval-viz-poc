"✅ Documentation reviewed:
- WORKFLOW.md v2.1 (FAA gate at Stage 1.5 confirmed)
- README.md (Architecture overview)

Key observations:
- **Prediction Modal** is a **LOCKED** element (ID `#prediction-modal`, dimensions, shortcuts).
- **Prediction Logic** is **CONSTRAINED** (max 3 choices).
- Current workflow Stages: 1, 1.5, 2, 3, 4.

Ready to proceed with planning."

---

## Bug: Prediction Modal Missing Feedback

**Triage:**

- **Symptom:** User selects an answer in Prediction Mode, but the modal closes immediately without indicating if the answer was correct or wrong.
- **Root Cause:** `PredictionModal.jsx` calls `onAnswer` immediately upon submission, and `usePredictionMode.js` closes the modal instantly to advance the step. There is no intermediate "Feedback" state.
- **Affected Systems:** Frontend (`PredictionModal.jsx`)
- **Affected Tier:** **CONSTRAINED** (UX behavior change, but must respect LOCKED modal dimensions/shortcuts).

**Code Review Findings:**

- Reviewed: `src/components/PredictionModal.jsx`, `src/hooks/usePredictionMode.js`
- Identified: `handleSubmit` in `PredictionModal.jsx` calls `onAnswer` directly.
- Identified: `handlePredictionAnswer` in `usePredictionMode.js` sets `setShowPrediction(false)` immediately.
- **Gap:** `predictionData` prop contains `correct_answer` (from backend contract), but `PredictionModal` ignores it.

**SWOT Analysis:**

- **Strengths:** Improves active learning loop; reinforces correct mental models immediately.
- **Weaknesses:** Adds a click/step to the user flow (must dismiss feedback).
- **Opportunities:** Can add "Explanation" field from backend in the future.
- **Threats:** Must ensure keyboard shortcuts (Enter) handle the new "Continue" state correctly to avoid getting stuck.

---

**Execution Plan:**

### Primary Owner: Frontend Developer

**Task:** Implement Feedback State in `PredictionModal`

**Context:**
Currently, the modal submits and closes instantly. We need to intercept the submission, validate the answer locally, show feedback (Correct/Incorrect), and *then* proceed.

**Requirements:**

- [ ] **Internal State:** Add `feedbackStatus` ('idle', 'correct', 'incorrect') to `PredictionModal`.
- [ ] **Validation:** In `handleSubmit`, compare `selectedChoiceId` with `predictionData.correct_answer`.
- [ ] **UI Feedback:**
    - If **Correct**: Show success message/icon (Green theme).
    - If **Incorrect**: Show error message and highlight the correct answer (Red theme).
    - Replace "Submit" button with "Continue" button.
- [ ] **Interaction Flow:**
    - User selects -> Clicks Submit (or Enter) -> **Show Feedback**.
    - User views result -> Clicks Continue (or Enter) -> **Call `onAnswer`**.
- [ ] **LOCKED Constraints:**
    - Must maintain `#prediction-modal` ID.
    - Must maintain max-width/dimensions.
    - Must support `Enter` key for both "Submit" and "Continue" actions.

**Scaffolding Reference (Structure Only):**

```javascript
// src/components/PredictionModal.jsx

const PredictionModal = ({ predictionData, onAnswer, ...props }) => {
    // Add state for feedback
    const [feedbackState, setFeedbackState] = useState('idle'); // 'idle' | 'correct' | 'incorrect'
    
    // Destructure correct_answer from data (it exists in backend contract)
    const { correct_answer } = predictionData || {};

    const handleSubmit = () => {
        if (feedbackState === 'idle') {
            // TODO: FE - Validate selectedChoiceId === correct_answer
            // TODO: FE - Set feedbackState
            // TODO: FE - Do NOT call onAnswer yet
        } else {
            // TODO: FE - Now call onAnswer(selectedChoiceId) to close and advance
        }
    };

    // TODO: FE - Render feedback UI overlay or replace content based on feedbackState
    // TODO: FE - Ensure 'Enter' key triggers handleSubmit in both states
};
```

**Success Criteria:**
- User sees "Correct!" or "Incorrect" message after submitting.
- "Incorrect" state identifies what the right answer was.
- Pressing `Enter` twice (Select -> Submit -> Continue) advances the step.
- Stats in `CompletionModal` still calculate correctly (handled by `usePredictionMode`).

**Reference:** `docs/compliance/FRONTEND_CHECKLIST.md`
**Time Estimate:** 30 min

---

### Validation (QA)

**Task:** Verify Prediction Feedback Loop

**Test Plan:**
- [ ] Enable Prediction Mode (`⚡ Watch` -> `⏳ Predict`).
- [ ] **Scenario 1 (Correct):** Select correct answer -> Verify Green feedback -> Click Continue -> Verify step advances.
- [ ] **Scenario 2 (Incorrect):** Select wrong answer -> Verify Red feedback -> Verify correct answer shown -> Click Continue -> Verify step advances.
- [ ] **Scenario 3 (Keyboard):** Use Number keys to select -> Enter to Submit -> Enter to Continue.
- [ ] **Regression:** Verify `CompletionModal` stats still reflect the actual results.

**Time Estimate:** 10 min

---

**Total Time Investment:** 40 min
**Rollback Plan:** Revert `PredictionModal.jsx` to direct `onAnswer` call.