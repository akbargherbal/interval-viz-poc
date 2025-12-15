import { useState, useCallback, useMemo, useEffect } from "react";

export const useTraceNavigation = (trace, resetPredictionStats, activatePredictionForStep) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [showCompletionModal, setShowCompletionModal] = useState(false);
  const totalSteps = trace?.trace?.steps?.length || 0;

  const isViewingFinalStep = useMemo(
    () => currentStep === totalSteps - 1 && totalSteps > 0,
    [currentStep, totalSteps]
  );

  useEffect(() => {
    setCurrentStep(0);
    setShowCompletionModal(false);
    if (resetPredictionStats) {
      resetPredictionStats();
    }
  }, [trace, resetPredictionStats]);

  const nextStep = useCallback(() => {
    if (isViewingFinalStep) {
      setShowCompletionModal(true);
      return;
    }
    if (totalSteps > 0 && currentStep < totalSteps - 1) {
      const nextStepIndex = currentStep + 1;
      // FIX: Check for a prediction before advancing the step.
      // If activatePredictionForStep returns true, it means a modal is shown, so we halt navigation.
      if (activatePredictionForStep && activatePredictionForStep(nextStepIndex)) {
        return;
      }
      setCurrentStep(nextStepIndex);
    }
  }, [totalSteps, currentStep, isViewingFinalStep, activatePredictionForStep]);

  const prevStep = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  }, [currentStep]);

  const jumpToEnd = useCallback(() => {
    if (totalSteps > 0) {
      setCurrentStep(totalSteps - 1);
      setShowCompletionModal(false);
    }
  }, [totalSteps]);

  const resetTrace = useCallback(() => {
    setCurrentStep(0);
    setShowCompletionModal(false);
    if (resetPredictionStats) {
      resetPredictionStats();
    }
  }, [resetPredictionStats]);

  const closeCompletionModal = useCallback(() => {
    setShowCompletionModal(false);
  }, []);

  const currentStepData = useMemo(
    () => trace?.trace?.steps?.[currentStep],
    [trace, currentStep]
  );

  const isComplete = currentStepData?.type === "ALGORITHM_COMPLETE";

  return {
    currentStep,
    currentStepData,
    totalSteps,
    nextStep,
    prevStep,
    resetTrace,
    jumpToEnd,
    isComplete,
    setCurrentStep, // Expose setCurrentStep for the prediction hook
    showCompletionModal,
    closeCompletionModal,
  };
};
