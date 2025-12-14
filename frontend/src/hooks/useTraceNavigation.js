import { useState, useCallback, useMemo, useEffect } from "react";

export const useTraceNavigation = (trace, resetPredictionStats) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [showCompletionModal, setShowCompletionModal] = useState(false); // State to control the modal
  const totalSteps = trace?.trace?.steps?.length || 0;

  const isViewingFinalStep = useMemo(
    () => currentStep === totalSteps - 1 && totalSteps > 0,
    [currentStep, totalSteps]
  );

  // Reset state when the trace (algorithm) changes
  useEffect(() => {
    setCurrentStep(0);
    setShowCompletionModal(false);
    if (resetPredictionStats) {
      resetPredictionStats();
    }
  }, [trace, resetPredictionStats]);

  const nextStep = useCallback(() => {
    // If viewing the final step, the next action is to show the modal.
    if (isViewingFinalStep) {
      setShowCompletionModal(true);
      return;
    }
    if (totalSteps > 0 && currentStep < totalSteps - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  }, [totalSteps, currentStep, isViewingFinalStep]);

  const prevStep = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  }, [currentStep]);

  const jumpToEnd = useCallback(() => {
    if (totalSteps > 0) {
      setCurrentStep(totalSteps - 1);
      setShowCompletionModal(false); // Ensure modal is hidden when jumping
    }
  }, [totalSteps]);

  const resetTrace = useCallback(() => {
    setCurrentStep(0);
    setShowCompletionModal(false); // Also reset modal state
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

  // This property is no longer used for modal logic but may be useful elsewhere.
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
    setCurrentStep,
    showCompletionModal, // New state for modal visibility
    closeCompletionModal, // New function to close modal
  };
};