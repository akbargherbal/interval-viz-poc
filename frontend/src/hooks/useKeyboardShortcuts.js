import { useEffect } from "react";

export const useKeyboardShortcuts = ({
  // Navigation
  onNext,
  onPrev,
  onReset,
  onJumpToEnd,
  isComplete,
  // Modals & Predictions
  modalOpen,
  predictionOpen,
  onSelectChoice,
  onSubmitAnswer,
  onSkipPrediction,
  onCloseModal,
}) => {
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (
        event.target.tagName === "INPUT" ||
        event.target.tagName === "TEXTAREA"
      ) {
        return;
      }

      // FIX: Handle prediction modal shortcuts separately
      if (predictionOpen) {
        switch (event.key.toLowerCase()) {
          case 'k': onSelectChoice?.(0); break;
          case 'c': onSelectChoice?.(1); break;
          case 's': onSkipPrediction?.(); break;
          case 'Enter': onSubmitAnswer?.(); break;
          case 'Escape': onSkipPrediction?.(); break; // Allow skipping with Escape
          default: break;
        }
        return;
      }
      
      // Handle general modal shortcuts (e.g., AlgorithmInfoModal)
      if (modalOpen) {
        if (event.key === 'Escape') {
          onCloseModal?.();
        }
        return;
      }

      // Handle navigation shortcuts
      switch (event.key) {
        case "ArrowRight":
        case " ":
          event.preventDefault();
          if (!isComplete) onNext?.();
          break;
        case "ArrowLeft":
          event.preventDefault();
          if (!isComplete) onPrev?.();
          break;
        case "r":
        case "R":
        case "Home":
          event.preventDefault();
          onReset?.();
          break;
        case "End":
          event.preventDefault();
          onJumpToEnd?.();
          break;
        case "Escape":
          if (isComplete) onCloseModal?.();
          break;
        default:
          break;
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [
      onNext, onPrev, onReset, onJumpToEnd, isComplete, modalOpen, predictionOpen,
      onSelectChoice, onSubmitAnswer, onSkipPrediction, onCloseModal
  ]);
};
