## Bug Report & Fix Plan: Sliding Window Frontend Issues

**Date:** 2023-10-27  
**Reported By:** ActionPlan PM  
**Assigned To:** Frontend Developer  
**Priority:** **HIGH** (Blocks feature usability and violates LOCKED requirements)

### 1. Overview

The frontend implementation for the **Sliding Window** algorithm is currently in an unusable state due to two critical bugs:

1.  **Missing State Display:** The right-hand state panel is nearly empty, failing to display the rich operational data (sum changes, window contents) provided by the backend.
2.  **Automatic Prediction Modal:** The prediction modal triggers automatically without user input, creating a disruptive and uncontrollable user experience. This violates a **LOCKED** 🔒 platform interaction pattern.

This plan provides a root cause analysis and a complete, step-by-step execution plan with code to resolve both issues.

### 2. Bug Details

#### Bug #1: Incomplete State Panel

*   **Symptom:** The "Algorithm State" panel for Sliding Window only shows "Current Sum" and "Max Sum". It fails to display the details of the slide operation (what element left, what element entered, how the sum changed) or the current contents of the window.
*   **Root Cause:** The `frontend/src/components/algorithm-states/SlidingWindowState.jsx` component is outdated. It was built for a previous version of the backend tracer and does not parse the new, consolidated `SLIDE_WINDOW` step type and its associated data structure.
*   **Impact:** Critical pedagogical information is hidden from the user, making it impossible to understand how the algorithm works. This defeats the primary purpose of the visualization.

#### Bug #2: Uncontrolled Prediction Modal

*   **Symptom:** When prediction mode is active, answering a prediction question immediately triggers the next prediction modal without waiting for the user to click "Next" or press the spacebar.
*   **Root Cause:** The `frontend/src/hooks/usePredictionMode.js` hook uses a `useEffect` that reacts to `currentStep` changes. This creates an uncontrolled loop: answering a prediction advances the step, which immediately triggers the effect for the next step if it's also a prediction point.
*   **Impact:** This breaks the core user interaction flow, which is a **LOCKED** 🔒 requirement. The user loses control of navigation, making the prediction feature frustrating and unusable.

---

### 3. Execution Plan

#### Task 1: Revamp `SlidingWindowState.jsx` Component

**Goal:** Replace the outdated state component with a new version that correctly parses and displays all data from the `SLIDE_WINDOW` trace steps.

**Action:** Replace the entire contents of the specified file with the code below.

```bash
code /home/akbar/Jupyter_Notebooks/interval-viz-poc/frontend/src/components/algorithm-states/SlidingWindowState.jsx
```

```jsx
import React from "react";
import PropTypes from "prop-types";

const MetricDisplay = ({ label, value, isHighlighted = false }) => (
  <div className="flex justify-between items-baseline">
    <span className="text-slate-400 text-sm">{label}:</span>
    <span
      className={`font-mono font-bold text-lg ${
        isHighlighted ? "text-emerald-400" : "text-white"
      }`}
    >
      {value ?? "N/A"}
    </span>
  </div>
);

MetricDisplay.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  isHighlighted: PropTypes.bool,
};

const SlidingWindowState = ({ step }) => {
  const viz = step?.data?.visualization;
  const metrics = viz?.metrics || {};
  const operationData = step?.type === "SLIDE_WINDOW" ? step.data : {};
  const isMaxSumUpdated = operationData.max_sum_updated || false;

  if (!viz) {
    return (
      <div className="p-4 text-slate-400 text-sm">
        Waiting for algorithm to start...
      </div>
    );
  }

  return (
    <div className="p-4 space-y-6">
      {/* Section 1: Core Metrics */}
      <div>
        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">
          Window Metrics
        </h3>
        <div className="space-y-3 rounded-md bg-slate-800/50 p-3">
          <MetricDisplay label="Window Size (k)" value={metrics.k} />
          <MetricDisplay label="Current Sum" value={metrics.current_sum} />
          <MetricDisplay
            label="Max Sum"
            value={metrics.max_sum}
            isHighlighted={isMaxSumUpdated}
          />
        </div>
        {isMaxSumUpdated && (
          <div className="text-center text-sm text-emerald-400 animate-pulse mt-2">
            🚀 New Maximum Sum Found!
          </div>
        )}
      </div>

      {/* Section 2: Current Operation Details */}
      {step.type === "SLIDE_WINDOW" && (
        <div>
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Slide Operation
          </h3>
          <div className="space-y-2 rounded-md bg-slate-800/50 p-3 font-mono text-sm">
            <p className="text-slate-300">
              <span className="text-slate-500 w-24 inline-block">Old Sum:</span> {operationData.old_sum}
            </p>
            <p className="text-red-400">
              <span className="text-slate-500 w-24 inline-block">- Outgoing:</span> {operationData.outgoing_element?.value} (idx {operationData.outgoing_element?.index})
            </p>
            <p className="text-green-400">
              <span className="text-slate-500 w-24 inline-block">+ Incoming:</span> {operationData.incoming_element?.value} (idx {operationData.incoming_element?.index})
            </p>
            <hr className="border-slate-700 my-2" />
            <p className="text-white font-bold">
              <span className="text-slate-500 w-24 inline-block">New Sum:</span> {operationData.new_sum}
            </p>
          </div>
        </div>
      )}

      {/* Section 3: Window State */}
      {operationData.window_indices && (
        <div>
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">
            Window State
          </h3>
          <div className="space-y-2 rounded-md bg-slate-800/50 p-3 text-sm">
            <p className="text-slate-300">
              <span className="text-slate-500">Indices:</span> {operationData.window_indices?.join(' - ')}
            </p>
            <p className="text-white font-mono bg-slate-900 p-2 rounded text-center tracking-wider">
              [ {operationData.window_subarray?.join(', ')} ]
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

SlidingWindowState.propTypes = {
  step: PropTypes.object.isRequired,
};

export default SlidingWindowState;
```

**Success Criteria for Task 1:**
*   The right-hand panel correctly displays three sections: "Window Metrics", "Slide Operation", and "Window State".
*   The "Max Sum" value turns green and a "New Maximum" message appears when `max_sum_updated` is true.
*   The "Slide Operation" section clearly shows the arithmetic: `Old Sum - Outgoing + Incoming = New Sum`.

---

#### Task 2: Refactor Prediction Control Flow

**Goal:** Change the prediction logic from a passive, reactive system to an active, imperative one, giving control back to the user.

**Action 1:** Replace the contents of `frontend/src/hooks/usePredictionMode.js` with the refactored version below. This removes the problematic `useEffect` and exposes a new function to be called by the main navigation handler.

```bash
code /home/akbar/Jupyter_Notebooks/interval-viz-poc/frontend/src/hooks/usePredictionMode.js
```

```javascript
import { useState, useCallback } from "react";

export const usePredictionMode = (trace, setCurrentStep) => {
  const [predictionMode, setPredictionMode] = useState(true);
  const [showPrediction, setShowPrediction] = useState(false);
  const [activePrediction, setActivePrediction] = useState(null);
  const [predictionStats, setPredictionStats] = useState({
    total: 0,
    correct: 0,
  });

  const predictionPoints = trace?.metadata?.prediction_points || [];

  const activatePredictionForStep = useCallback((stepIndex) => {
    if (!predictionMode || !predictionPoints.length) {
      return false;
    }
    const matchingPrediction = predictionPoints.find(
      (p) => p.step_index === stepIndex
    );
    if (matchingPrediction) {
      setActivePrediction(matchingPrediction);
      setShowPrediction(true);
      return true;
    }
    return false;
  }, [predictionPoints, predictionMode]);

  const handlePredictionAnswer = useCallback((userAnswer) => {
    if (!activePrediction) return;
    const isCorrect = userAnswer === activePrediction.correct_answer;
    const targetStep = activePrediction.step_index;
    setPredictionStats((prev) => ({
      total: prev.total + 1,
      correct: prev.correct + (isCorrect ? 1 : 0),
    }));
    setShowPrediction(false);
    setActivePrediction(null);
    setCurrentStep(targetStep);
  }, [activePrediction, setCurrentStep]);

  const handlePredictionSkip = useCallback(() => {
    if (!activePrediction) return;
    const targetStep = activePrediction.step_index;
    setShowPrediction(false);
    setActivePrediction(null);
    setCurrentStep(targetStep);
  }, [activePrediction, setCurrentStep]);

  const togglePredictionMode = useCallback(() => {
    setPredictionMode((prev) => !prev);
    setShowPrediction(false);
    setActivePrediction(null);
  }, []);

  const resetPredictionStats = useCallback(() => {
    setPredictionStats({ total: 0, correct: 0 });
  }, []);

  return {
    predictionMode,
    showPrediction,
    activePrediction,
    predictionStats,
    togglePredictionMode,
    handlePredictionAnswer,
    handlePredictionSkip,
    resetPredictionStats,
    activatePredictionForStep,
  };
};
```

**Action 2:** In `frontend/src/App.jsx`, apply the following two changes to orchestrate the new control flow.

1.  **Update the hook initializations** inside the `AlgorithmTracePlayer` component. The prediction hook now requires `setCurrentStep` from the navigation hook.

    ```javascript
    // Find this section in App.jsx and update it
    const {
      currentStep,
      currentStepData,
      totalSteps,
      nextStep: navNextStep,
      prevStep,
      resetTrace,
      jumpToEnd,
      showCompletionModal,
      closeCompletionModal,
      setCurrentStep, // <-- Ensure setCurrentStep is destructured from useTraceNavigation
    } = useTraceNavigation(trace, resetPredictionStatsRef.current);

    // Update the usePredictionMode call to pass setCurrentStep
    const prediction = usePredictionMode(trace, setCurrentStep);
    ```

2.  **Replace the `nextStep` handler function** with this new version, which actively checks for predictions before navigating.

    ```javascript
    // Find the --- HANDLERS --- section and replace the nextStep function
    const nextStep = () => {
      if (prediction.showPrediction) return; // Block if modal is already showing

      const nextStepIndex = currentStep + 1;

      if (nextStepIndex >= totalSteps) {
        navNextStep(); // Let navigation hook handle completion modal
        return;
      }

      // Ask the prediction hook if it needs to intercept this navigation
      const wasPredictionActivated = prediction.activatePredictionForStep(nextStepIndex);

      // Only navigate if a prediction modal was NOT shown
      if (!wasPredictionActivated) {
        navNextStep();
      }
    };
    ```

**Success Criteria for Task 2:**
*   The prediction modal **only** appears after a user clicks "Next" or presses the spacebar on a step immediately preceding a prediction point.
*   When the modal appears, the main visualization **does not** advance.
*   After answering or skipping, the visualization advances to the predicted step, allowing the user to see the outcome of their choice.
*   The user must initiate another "Next" action to proceed to the following step.

---

### 4. Verification

After implementing these fixes, perform the following checks:
1.  Load the Sliding Window algorithm.
2.  Verify the state panel is fully populated and updates correctly with each step.
3.  Enable "Predict" mode.
4.  Step through the trace, ensuring the prediction modal appears only on user command and that the flow described in the success criteria is met.
5.  Switch to another algorithm (e.g., Binary Search) to confirm no regressions were introduced.