// frontend/src/components/algorithm-states/BinarySearchState.jsx

import React, { useEffect } from "react";
import PropTypes from "prop-types";

/**
 * BinarySearchState - Iterative Metrics Template
 *
 * RHP Layout:
 * - Top 2/3: Key Metrics (Mid Value, Target, Pointers)
 * - Bottom 1/3: Narrative & Step Description
 *
 * NOTE: This component uses a DOM manipulation effect to hide the
 * parent StatePanel's default footer to prevent description duplication.
 */
const BinarySearchState = ({ step, trace }) => {
  // Effect to hide the parent StatePanel's default description footer
  useEffect(() => {
    const parentFooter = document.getElementById("panel-step-description");
    if (parentFooter) {
      parentFooter.style.display = "none";
    }

    return () => {
      if (parentFooter) {
        parentFooter.style.display = "";
      }
    };
  }, []);

  // Early return for graceful degradation
  if (!step?.data?.visualization) {
    return (
      <div className="text-slate-400 text-sm p-4">No state data available</div>
    );
  }

  const { pointers, array } = step.data.visualization;

  // Safe data extraction
  const leftIdx = pointers?.left ?? "-";
  const rightIdx = pointers?.right ?? "-";
  const midIdx = pointers?.mid ?? "-";
  const target = pointers?.target ?? "?";

  // Resolve Mid Value from Array if mid index exists
  let midValue = "-";
  if (midIdx !== "-" && Array.isArray(array)) {
    const midElement = array.find((item) => item.index === midIdx);
    if (midElement) midValue = midElement.value;
  }

  // Helper for step type coloring
  const getStepColor = (type) => {
    const t = type?.toUpperCase() || "";
    if (t.includes("FOUND"))
      return "bg-emerald-900/30 text-emerald-200 border-emerald-800";
    if (t.includes("COMPARE") || t.includes("DECISION"))
      return "bg-yellow-900/30 text-yellow-200 border-yellow-800";
    if (t.includes("CALCULATE"))
      return "bg-blue-900/30 text-blue-200 border-blue-800";
    return "bg-slate-700/20 text-slate-200 border-slate-700";
  };

  const stepType = step.type || "STEP";
  const stepColorClass = getStepColor(stepType);

  return (
    <div className="h-full flex flex-col bg-slate-800">
      {/* ==========================================
          SECTION 1: Metrics (Top 2/3 - flex-[2])
          ========================================== */}
      <div className="flex-[2] flex flex-col p-4 overflow-hidden relative border-b border-slate-700">
        {/* Primary Metrics Grid - Expanded to fill space */}
        <div className="grid grid-cols-2 gap-3 mb-2 flex-1">
          {/* Metric 1: Mid Value */}
          <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-2 flex flex-col items-center justify-center hover:bg-slate-700/50 transition-colors">
            <span className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-1">
              Mid Value
            </span>
            <span className="text-yellow-400 text-5xl font-mono font-bold tracking-tighter drop-shadow-lg">
              {midValue}
            </span>
          </div>

          {/* Metric 2: Target */}
          <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-2 flex flex-col items-center justify-center hover:bg-slate-700/50 transition-colors">
            <span className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-1">
              Target
            </span>
            <span className="text-emerald-400 text-5xl font-mono font-bold tracking-tighter drop-shadow-lg">
              {target}
            </span>
          </div>
        </div>

        {/* Secondary Metrics Strip - Increased size to reduce wasted space */}
        <div className="bg-slate-900/40 rounded-lg border border-slate-700/50 p-3 mt-auto shrink-0">
          <div className="grid grid-cols-3 divide-x divide-slate-700/50">
            {/* Left Index */}
            <div className="px-2 text-center">
              <div className="text-xs text-slate-500 font-semibold uppercase mb-1">
                Left Idx
              </div>
              <div className="text-blue-300 font-mono text-xl font-bold">
                {leftIdx}
              </div>
            </div>
            {/* Right Index */}
            <div className="px-2 text-center">
              <div className="text-xs text-slate-500 font-semibold uppercase mb-1">
                Right Idx
              </div>
              <div className="text-red-300 font-mono text-xl font-bold">
                {rightIdx}
              </div>
            </div>
            {/* Mid Index */}
            <div className="px-2 text-center">
              <div className="text-xs text-slate-500 font-semibold uppercase mb-1">
                Mid Idx
              </div>
              <div className="text-yellow-300 font-mono text-xl font-bold">
                {midIdx}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ==========================================
          SECTION 2: Narrative (Bottom 1/3 - flex-1)
          ========================================== */}
      <div className="flex-1 flex min-h-0">
        {/* Step Name Column */}
        <div
          className={`w-28 border-r flex items-center justify-center p-3 text-center shrink-0 ${stepColorClass}`}
        >
          <span className="text-xs font-bold leading-tight drop-shadow-md uppercase">
            {stepType.replace(/_/g, " ")}
          </span>
        </div>

        {/* Description Column */}
        <div className="flex-1 p-4 flex items-center bg-slate-800 overflow-y-auto">
          <p className="text-slate-300 text-sm font-medium leading-relaxed">
            {step.description}
          </p>
        </div>
      </div>
    </div>
  );
};

BinarySearchState.propTypes = {
  step: PropTypes.shape({
    type: PropTypes.string,
    description: PropTypes.string,
    data: PropTypes.shape({
      visualization: PropTypes.shape({
        pointers: PropTypes.object,
        array: PropTypes.arrayOf(PropTypes.object),
      }),
    }),
  }).isRequired,
  trace: PropTypes.object,
};

export default BinarySearchState;
