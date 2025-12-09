// frontend/src/utils/predictionUtils.js
/**
 * Prediction Mode Utilities
 * 
 * Helpers for determining when to show prediction prompts
 * and validating user predictions against algorithm decisions.
 */

/**
 * Check if a step is a prediction point (decision moment)
 * @param {Object} step - The current trace step
 * @returns {boolean} - True if this step requires a prediction
 */
export const isPredictionPoint = (step) => {
  return step?.type === 'EXAMINING_INTERVAL' && 
         step?.data?.interval &&
         step?.data?.comparison;
};

/**
 * Extract prediction data from an EXAMINING_INTERVAL step
 * @param {Object} step - The EXAMINING_INTERVAL step
 * @returns {Object} - Prediction data including interval, max_end, and comparison
 */
export const getPredictionData = (step) => {
  if (!isPredictionPoint(step)) {
    return null;
  }

  const interval = step.data.interval;
  const maxEnd = step.data.max_end;
  const comparison = step.data.comparison;

  return {
    interval,
    maxEnd,
    comparison,
    intervalEnd: interval.end,
    // max_end can be null (meaning -∞), so handle it
    maxEndValue: maxEnd === null ? -Infinity : maxEnd,
  };
};

/**
 * Get the correct answer for a prediction point
 * @param {Object} step - The EXAMINING_INTERVAL step
 * @param {Object} nextStep - The DECISION_MADE step (next step in trace)
 * @returns {string|null} - "keep" or "covered", or null if can't determine
 */
export const getCorrectAnswer = (step, nextStep) => {
  // Validate we have the right steps
  if (!isPredictionPoint(step)) {
    return null;
  }

  if (nextStep?.type !== 'DECISION_MADE') {
    console.warn('Expected DECISION_MADE step after EXAMINING_INTERVAL');
    return null;
  }

  return nextStep.data.decision; // "keep" or "covered"
};

/**
 * Calculate if user's prediction was correct
 * @param {string} userAnswer - User's choice: "keep" or "covered"
 * @param {string} correctAnswer - Actual decision from trace
 * @returns {boolean} - True if prediction matches
 */
export const isPredictionCorrect = (userAnswer, correctAnswer) => {
  return userAnswer === correctAnswer;
};

/**
 * Get encouraging feedback based on accuracy percentage
 * @param {number} accuracy - Percentage correct (0-100)
 * @returns {Object} - Object with message and color
 */
export const getAccuracyFeedback = (accuracy) => {
  if (accuracy >= 90) {
    return {
      message: "🎉 Excellent! You've mastered this algorithm!",
      color: "emerald",
      emoji: "🎉"
    };
  } else if (accuracy >= 70) {
    return {
      message: "👍 Great job! You understand the core logic.",
      color: "emerald",
      emoji: "👍"
    };
  } else if (accuracy >= 50) {
    return {
      message: "📚 Good start! Review the max_end comparison rule.",
      color: "amber",
      emoji: "📚"
    };
  } else {
    return {
      message: "💡 Keep practicing! Try the step-by-step mode to understand each decision.",
      color: "red",
      emoji: "💡"
    };
  }
};

/**
 * Get hint text for a prediction point
 * @param {Object} predictionData - Data from getPredictionData()
 * @returns {string} - Hint text
 */
export const getHintText = (predictionData) => {
  const { intervalEnd, maxEndValue } = predictionData;
  
  if (maxEndValue === -Infinity) {
    return `Hint: This is the first interval (max_end = -∞). Will it extend coverage?`;
  }
  
  return `Hint: Compare interval.end (${intervalEnd}) with max_end (${maxEndValue})`;
};

/**
 * Get explanation for the correct answer
 * @param {string} correctAnswer - "keep" or "covered"
 * @param {Object} predictionData - Data from getPredictionData()
 * @returns {string} - Explanation text
 */
export const getExplanation = (correctAnswer, predictionData) => {
  const { intervalEnd, maxEndValue } = predictionData;
  
  if (correctAnswer === "keep") {
    if (maxEndValue === -Infinity) {
      return `✓ KEEP: First interval always extends coverage (${intervalEnd} > -∞)`;
    }
    return `✓ KEEP: interval.end (${intervalEnd}) > max_end (${maxEndValue}), extending coverage`;
  } else {
    return `✗ COVERED: interval.end (${intervalEnd}) ≤ max_end (${maxEndValue}), already covered`;
  }
};