import React, { useState, useEffect, useCallback } from "react";
import PropTypes from "prop-types";
import { CheckCircle, XCircle } from "lucide-react";
import { usePrediction } from "../contexts/PredictionContext";

const PredictionModal = ({
  // Props are now optional/deprecated as we use context
  predictionData: propData,
  onAnswer: propOnAnswer,
  onSkip: propOnSkip,
  isOpen: propIsOpen,
}) => {
  const {
    activePrediction,
    handlePredictionAnswer,
    handlePredictionSkip,
    showPrediction,
  } = usePrediction();

  // Use context values, fallback to props for backward compatibility/testing
  const predictionData = activePrediction || propData;
  const onAnswer = handlePredictionAnswer || propOnAnswer;
  const onSkip = handlePredictionSkip || propOnSkip;
  const isOpen = showPrediction || propIsOpen;

  console.log("PredictionModal re-rendered", { isOpen });
  const [selectedChoiceId, setSelectedChoiceId] = useState(null);
  const [feedbackState, setFeedbackState] = useState("idle"); // 'idle' | 'correct' | 'incorrect'

  // Reset local state when modal opens/closes or data changes
  useEffect(() => {
    if (isOpen) {
      setSelectedChoiceId(null);
      setFeedbackState("idle");
    }
  }, [isOpen, predictionData]);

  // Destructure data with safety checks
  const { question, choices = [], hint, correct_answer } = predictionData || {};

  // Map choices to include UI properties if missing
  const mappedChoices = choices.map((choice, index) => {
    // Default styling based on index if no specific class provided
    let colorClass = "bg-slate-600 hover:bg-slate-500"; // Fallback

    const labelLower = (choice.label || "").toLowerCase();
    const idLower = (choice.id || "").toLowerCase();

    // Semantic color mapping based on mockup guidelines
    if (
      labelLower.includes("found") ||
      labelLower.includes("keep") ||
      labelLower.includes("yes") ||
      idLower === "found"
    ) {
      colorClass = "bg-emerald-600 hover:bg-emerald-500";
    } else if (
      labelLower.includes("covered") ||
      labelLower.includes("discard") ||
      labelLower.includes("no") ||
      idLower.includes("covered")
    ) {
      colorClass = "bg-orange-600 hover:bg-orange-500";
    } else if (
      labelLower.includes("left") ||
      labelLower.includes("back") ||
      labelLower.includes("prev")
    ) {
      colorClass = "bg-amber-600 hover:bg-amber-500";
    } else if (labelLower.includes("right") || labelLower.includes("next")) {
      colorClass = "bg-red-600 hover:bg-red-500";
    } else {
      // Fallback cycle for generic choices
      const defaultColors = [
        "bg-amber-600 hover:bg-amber-500",
        "bg-purple-600 hover:bg-purple-500",
        "bg-emerald-600 hover:bg-emerald-500",
      ];
      colorClass = defaultColors[index % defaultColors.length];
    }

    // Default shortcuts
    const defaultShortcuts = ["1", "2", "3"];

    return {
      ...choice,
      id: choice.id || `choice-${index}`,
      className: choice.className || colorClass,
      shortcut:
        choice.shortcut || defaultShortcuts[index % defaultShortcuts.length],
    };
  });

  const handleSubmit = useCallback(() => {
    if (feedbackState === "idle") {
      if (selectedChoiceId) {
        // Local validation for feedback
        const isCorrect = selectedChoiceId === correct_answer;
        setFeedbackState(isCorrect ? "correct" : "incorrect");
      }
    } else {
      // Proceed to next step (calls hook which updates stats and closes modal)
      onAnswer(selectedChoiceId);
    }
  }, [feedbackState, selectedChoiceId, correct_answer, onAnswer]);

  // Handle keyboard shortcuts locally
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      const key = e.key.toLowerCase();

      // Skip if typing in inputs
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA")
        return;

      // If in feedback state, capture navigation keys to continue
      if (feedbackState !== "idle") {
        if (key === "enter" || key === "escape" || key === "s") {
          e.preventDefault();
          handleSubmit(); // Treat all exits as "Continue" to record stats
        }
        return;
      }

      // Choice selection shortcuts (only when idle)
      mappedChoices.forEach((choice) => {
        if (
          (choice.shortcut && key === choice.shortcut.toLowerCase()) ||
          key === (mappedChoices.indexOf(choice) + 1).toString()
        ) {
          setSelectedChoiceId(choice.id);
        }
      });

      // Action shortcuts
      if (key === "enter") {
        e.preventDefault();
        handleSubmit();
      } else if (key === "s" || key === "escape") {
        e.preventDefault();
        onSkip();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, mappedChoices, handleSubmit, onSkip, feedbackState]);

  if (!isOpen) return null;

  return (
    <div
      id="prediction-modal"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-md"
    >
      {/* LOCKED: max-w-lg (512px), p-6, NO height constraint */}
      <div className="w-full max-w-lg select-none rounded-2xl border-2 border-blue-500 bg-slate-800 p-6 text-white shadow-2xl">
        {/* Header Section */}
        <div className="mb-6">
          <h2 className="mb-2 text-2xl font-bold leading-tight text-white">
            {question}
          </h2>
        </div>

        {/* Feedback Banner (Replaces Hint or stacks) */}
        {feedbackState !== "idle" && (
          <div
            className={`animate-in fade-in slide-in-from-top-2 mb-6 flex items-center gap-3 rounded-lg p-4 duration-300 ${
              feedbackState === "correct"
                ? "border border-emerald-500/50 bg-emerald-900/30"
                : "border border-red-500/50 bg-red-900/30"
            }`}
          >
            {feedbackState === "correct" ? (
              <CheckCircle className="h-6 w-6 flex-shrink-0 text-emerald-400" />
            ) : (
              <XCircle className="h-6 w-6 flex-shrink-0 text-red-400" />
            )}
            <div>
              <h3
                className={`font-bold ${
                  feedbackState === "correct"
                    ? "text-emerald-400"
                    : "text-red-400"
                }`}
              >
                {feedbackState === "correct" ? "Correct!" : "Incorrect"}
              </h3>
              {feedbackState === "incorrect" && (
                <p className="mt-1 text-sm text-slate-300">
                  The correct answer was:{" "}
                  <span className="font-semibold text-white">
                    {mappedChoices.find((c) => c.id === correct_answer)
                      ?.label || "shown below"}
                  </span>
                </p>
              )}
            </div>
          </div>
        )}

        {/* Hint Box (Only show if idle or if it adds context) */}
        {hint && feedbackState === "idle" && (
          <div className="mb-6 rounded-lg border border-blue-500/30 bg-blue-900/20 p-4">
            <p className="text-sm text-blue-300">
              💡 <strong>Hint:</strong> {hint}
            </p>
          </div>
        )}

        {/* Choices Grid */}
        <div
          className={`grid ${
            mappedChoices.length > 2 ? "grid-cols-3" : "grid-cols-2"
          } mb-6 gap-5`}
        >
          {mappedChoices.map((choice) => {
            const isSelected = selectedChoiceId === choice.id;
            const isCorrectAnswer = choice.id === correct_answer;

            // Determine visual state
            let stateClasses = choice.className;
            let opacityClass = "opacity-100";
            let ringClass = "";
            let scaleClass = "";

            if (feedbackState === "idle") {
              // Normal interaction state
              const isOthersSelected = selectedChoiceId && !isSelected;
              opacityClass = isOthersSelected ? "opacity-60" : "opacity-100";

              // Extract base color for ring
              let ringColor = "ring-blue-400";
              if (choice.className.includes("emerald"))
                ringColor = "ring-emerald-400";
              else if (choice.className.includes("orange"))
                ringColor = "ring-orange-400";
              else if (choice.className.includes("red"))
                ringColor = "ring-red-400";
              else if (choice.className.includes("purple"))
                ringColor = "ring-purple-400";

              if (isSelected) {
                ringClass = `ring-2 ${ringColor} shadow-xl z-10`;
                scaleClass = "scale-105";
              } else {
                scaleClass = "hover:scale-105";
              }
            } else {
              // Feedback state
              if (isSelected) {
                if (isCorrectAnswer) {
                  // Selected & Correct
                  stateClasses = "bg-emerald-600";
                  ringClass = "ring-4 ring-emerald-400/50 shadow-xl z-10";
                  scaleClass = "scale-105";
                } else {
                  // Selected & Incorrect
                  stateClasses = "bg-red-600";
                  ringClass = "ring-4 ring-red-400/50 shadow-xl z-10";
                  scaleClass = "scale-105";
                }
              } else if (isCorrectAnswer) {
                // Not selected but Correct (show answer)
                stateClasses = "bg-emerald-600/80";
                ringClass = "ring-2 ring-emerald-400/50 border-dashed";
                opacityClass = "opacity-100";
              } else {
                // Not selected & Not correct
                opacityClass = "opacity-30 grayscale";
              }
            }

            return (
              <button
                key={choice.id}
                onClick={() =>
                  feedbackState === "idle" && setSelectedChoiceId(choice.id)
                }
                disabled={feedbackState !== "idle"}
                className={`py-4 ${mappedChoices.length > 2 ? "px-3" : "px-4"} flex flex-col items-center justify-center rounded-lg text-center font-semibold text-white transition-all duration-200 focus:outline-none ${stateClasses} ${ringClass} ${scaleClass} ${opacityClass} ${
                  feedbackState !== "idle"
                    ? "cursor-default"
                    : "cursor-pointer shadow-lg"
                } `}
              >
                <div
                  className={`${mappedChoices.length > 2 ? "text-sm" : "text-base"} mb-1`}
                >
                  {choice.label}
                </div>
                {feedbackState === "idle" && (
                  <div className="text-xs opacity-75">
                    Press {choice.shortcut}
                  </div>
                )}
                {feedbackState !== "idle" && isCorrectAnswer && (
                  <CheckCircle size={16} className="mt-1 text-white" />
                )}
                {feedbackState !== "idle" && isSelected && !isCorrectAnswer && (
                  <XCircle size={16} className="mt-1 text-white" />
                )}
              </button>
            );
          })}
        </div>

        {/* Actions - Two-Step Confirmation */}
        <div className="flex items-center justify-between border-t border-slate-700 pt-4">
          {feedbackState === "idle" ? (
            <>
              <button
                onClick={onSkip}
                className="text-sm text-slate-400 transition-colors hover:text-slate-300"
              >
                Skip (Press S)
              </button>
              <button
                onClick={handleSubmit}
                disabled={!selectedChoiceId}
                className={`rounded-lg px-6 py-2 font-semibold shadow-lg transition-all ${
                  selectedChoiceId
                    ? "animate-pulse bg-blue-600 text-white hover:scale-105 hover:bg-blue-500"
                    : "cursor-not-allowed bg-blue-600 text-white opacity-50"
                } `}
              >
                Submit (Enter)
              </button>
            </>
          ) : (
            <button
              onClick={handleSubmit}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 py-3 font-bold text-white shadow-lg transition-all hover:scale-[1.02] hover:bg-blue-500"
            >
              Continue (Enter)
              <span className="rounded bg-blue-700 px-2 py-0.5 text-xs font-normal opacity-80">
                ↵
              </span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

PredictionModal.propTypes = {
  predictionData: PropTypes.object,
  onAnswer: PropTypes.func,
  onSkip: PropTypes.func,
  isOpen: PropTypes.bool,
};

export default PredictionModal;
