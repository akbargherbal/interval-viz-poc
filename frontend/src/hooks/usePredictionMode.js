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
