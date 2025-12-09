import React from "react";
import { RotateCcw, SkipBack, ChevronRight } from "lucide-react";

const ControlBar = ({
  currentStep,
  totalSteps,
  onPrev,
  onNext,
  onReset,
  isComplete,
}) => {
  const isFirstStep = currentStep === 0;
  const isLastStep = currentStep >= totalSteps - 1;

  return (
    <div className="flex items-center justify-between mb-4">
      <div>
        <h1 className="text-2xl font-bold text-white">
          Remove Covered Intervals
        </h1>
        <p className="text-slate-400 text-sm">
          Step {currentStep + 1} of {totalSteps}
        </p>
      </div>

      <div className="flex gap-2">
        <button
          onClick={onReset}
          className="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
        >
          <RotateCcw size={20} />
          Reset
        </button>

        <button
          onClick={onPrev}
          disabled={isFirstStep}
          className="bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
        >
          <SkipBack size={20} />
          Previous
        </button>

        <button
          onClick={onNext}
          disabled={isLastStep}
          className="bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-600 disabled:cursor-not-allowed text-black px-6 py-2 rounded-lg flex items-center gap-2 transition-colors font-bold"
        >
          Next Step
          <ChevronRight size={20} />
        </button>
      </div>
    </div>
  );
};

export default ControlBar;