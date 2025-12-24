import React from "react";
import { RotateCcw, SkipBack, ChevronRight } from "lucide-react";
import { useNavigation } from "../contexts/NavigationContext";

const ControlBar = ({ onPrev, onNext, onReset }) => {
  const {
    currentStep,
    totalSteps,
    prevStep: ctxPrevStep,
    nextStep: ctxNextStep,
    resetTrace: ctxResetTrace,
  } = useNavigation();

  console.log("ControlBar re-rendered", { currentStep, totalSteps });

  const isFirstStep = currentStep === 0;
  const isLastStep = currentStep >= totalSteps - 1;

  // Use prop handler if provided (for prediction logic), otherwise context default
  const handlePrev = onPrev || ctxPrevStep;
  const handleNext = onNext || ctxNextStep;
  const handleReset = onReset || ctxResetTrace;

  return (
    <>
      <button
        onClick={handleReset}
        className="flex items-center gap-2 rounded-lg bg-slate-700 px-4 py-2 text-white transition-colors hover:bg-slate-600"
      >
        <RotateCcw size={20} />
        Reset
      </button>

      <button
        onClick={handlePrev}
        disabled={isFirstStep}
        className="flex items-center gap-2 rounded-lg bg-slate-700 px-4 py-2 text-white transition-colors hover:bg-slate-600 disabled:cursor-not-allowed disabled:bg-slate-800"
      >
        <SkipBack size={20} />
        Previous
      </button>

      <button
        onClick={handleNext}
        disabled={isLastStep}
        className="flex items-center gap-2 rounded-lg bg-emerald-500 px-6 py-2 font-bold text-black transition-colors hover:bg-emerald-600 disabled:cursor-not-allowed disabled:bg-slate-600"
      >
        Next Step
        <ChevronRight size={20} />
      </button>
    </>
  );
};

export default ControlBar;
