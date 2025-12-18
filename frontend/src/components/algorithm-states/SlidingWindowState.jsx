// frontend/src/components/algorithm-states/SlidingWindowState.jsx

import React, { useEffect } from "react";
import PropTypes from "prop-types";

/**
 * SlidingWindowState - Iterative Metrics Template (Dashboard Edition)
 *
 * RHP Layout:
 * - Top 2/3: Metrics Dashboard (Current vs Max, Indices, Performance Bar)
 * - Bottom 1/3: Narrative
 *
 * Improvements:
 * - "Dashboard" feel: Grouped data (Sum + Indices) in unified cards
 * - Vertical Density: Indices moved inside cards to save space
 * - Visual Context: Added a progress bar comparing Current vs Max
 */
const SlidingWindowState = ({ step, trace }) => {
  // Effect to hide the parent StatePanel's default description footer
  useEffect(() => {
    const parentFooter = document.getElementById("panel-step-description");
    if (parentFooter) {
      parentFooter.style.display = "none";
    }
    return () => {
      if (parentFooter) parentFooter.style.display = "";
    };
  }, []);

  // Early return
  if (!step?.data?.visualization) {
    return (
      <div className="text-slate-400 text-sm p-4">No state data available</div>
    );
  }

  const viz = step.data.visualization;
  const metrics = viz.metrics || {};
  const pointers = viz.pointers || {};

  // Data Extraction
  const currentSum = metrics.current_sum ?? 0;
  const maxSum = metrics.max_sum ?? 0;
  const k = metrics.k ?? "-";

  // Window Indices
  const currStart = pointers.window_start ?? "-";
  const currEnd = pointers.window_end ?? "-";

  // Best Window Calculation
  const bestStart = metrics.max_window_start ?? "-";
  let bestEnd = "-";
  if (bestStart !== "-" && k !== "-") {
    bestEnd = bestStart + k - 1;
  }

  // "New Max" Detection
  const isMax = currentSum > 0 && currentSum === maxSum;

  // Progress Bar Calculation
  const progressPercent =
    maxSum > 0 ? Math.min(100, (currentSum / maxSum) * 100) : 0;

  // Step Type Coloring
  const getStepColor = (type) => {
    const t = type?.toUpperCase() || "";
    if (t.includes("MAX") || t.includes("UPDATE"))
      return "bg-emerald-900/30 text-emerald-200 border-emerald-800";
    if (t.includes("SLIDE") || t.includes("MOVE"))
      return "bg-blue-900/30 text-blue-200 border-blue-800";
    return "bg-slate-700/20 text-slate-200 border-slate-700";
  };

  const stepType = step.type || "STEP";
  const stepColorClass = getStepColor(stepType);

  return (
    <div className="h-full flex flex-col bg-slate-800">
      {/* ==========================================
          SECTION 1: Metrics Dashboard (Top 2/3)
          ========================================== */}
      <div className="flex-[2] flex flex-col p-4 overflow-hidden relative border-b border-slate-700 gap-3">
        {/* Header: Context Info */}
        <div className="flex justify-between items-center shrink-0">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
            Window Metrics
          </h2>
          <div className="text-[10px] font-mono text-slate-500 bg-slate-900/50 px-2 py-1 rounded">
            Window Size: <span className="text-slate-300 font-bold">{k}</span>
          </div>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-2 gap-3 flex-1 min-h-0">
          {/* Card 1: Active Window (Cyan Theme) */}
          <div className="bg-slate-700/30 border-l-4 border-cyan-500/50 rounded-r-lg p-3 flex flex-col justify-between relative overflow-hidden">
            <div className="text-[10px] font-bold text-cyan-400/80 uppercase tracking-wider">
              Active Window
            </div>

            <div className="flex flex-col items-start my-1">
              <span className="text-4xl font-mono font-bold text-cyan-300 tracking-tighter drop-shadow-lg">
                {currentSum}
              </span>
              <span className="text-[10px] text-slate-400 uppercase mt-1">
                Current Sum
              </span>
            </div>

            <div className="mt-auto pt-2 border-t border-slate-600/30 w-full">
              <div className="flex justify-between items-center text-xs font-mono">
                <span className="text-slate-500">Indices:</span>
                <span className="text-cyan-200 bg-cyan-900/30 px-1.5 py-0.5 rounded">
                  [{currStart}-{currEnd}]
                </span>
              </div>
            </div>
          </div>

          {/* Card 2: Best Record (Emerald Theme) */}
          <div
            className={`border-l-4 rounded-r-lg p-3 flex flex-col justify-between relative overflow-hidden transition-all duration-500 ${
              isMax
                ? "bg-emerald-900/10 border-emerald-500"
                : "bg-slate-700/30 border-emerald-500/30"
            }`}
          >
            <div className="flex justify-between items-start">
              <div className="text-[10px] font-bold text-emerald-400/80 uppercase tracking-wider">
                All-Time Best
              </div>
              {isMax && (
                <span className="flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
              )}
            </div>

            <div className="flex flex-col items-start my-1">
              <span className="text-4xl font-mono font-bold text-emerald-400 tracking-tighter drop-shadow-lg">
                {maxSum}
              </span>
              <span className="text-[10px] text-slate-400 uppercase mt-1">
                Max Sum Found
              </span>
            </div>

            <div className="mt-auto pt-2 border-t border-slate-600/30 w-full">
              <div className="flex justify-between items-center text-xs font-mono">
                <span className="text-slate-500">Indices:</span>
                <span className="text-emerald-200 bg-emerald-900/30 px-1.5 py-0.5 rounded">
                  [{bestStart}-{bestEnd}]
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Bar (Visual Context) */}
        <div className="shrink-0 pt-1">
          <div className="flex justify-between text-[9px] text-slate-500 mb-1 uppercase font-bold">
            <span>Performance</span>
            <span>{Math.round(progressPercent)}% of Max</span>
          </div>
          <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-700/50">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-emerald-500 transition-all duration-500 ease-out"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* ==========================================
          SECTION 2: Narrative (Bottom 1/3)
          ========================================== */}
      <div className="flex-1 flex min-h-0">
        {/* Step Name */}
        <div
          className={`w-28 border-r flex items-center justify-center p-3 text-center shrink-0 ${stepColorClass}`}
        >
          <span className="text-xs font-bold leading-tight drop-shadow-md uppercase">
            {stepType.replace(/_/g, " ")}
          </span>
        </div>

        {/* Description */}
        <div className="flex-1 p-4 flex items-center bg-slate-800 overflow-y-auto">
          <p className="text-slate-300 text-sm font-medium leading-relaxed">
            {step.description}
          </p>
        </div>
      </div>
    </div>
  );
};

SlidingWindowState.propTypes = {
  step: PropTypes.shape({
    type: PropTypes.string,
    description: PropTypes.string,
    data: PropTypes.shape({
      visualization: PropTypes.shape({
        metrics: PropTypes.object,
        pointers: PropTypes.object,
      }),
    }),
  }).isRequired,
  trace: PropTypes.object,
};

export default SlidingWindowState;
