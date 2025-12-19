// frontend/src/components/algorithm-states/SlidingWindowState.jsx

import React from "react";
import PropTypes from "prop-types";

/**
 * SlidingWindowState - Pure Content Component (Phase 0 Refactored)
 *
 * CRITICAL CHANGES (Session 53):
 * - REMOVED internal 2:1 layout (header/footer)
 * - REMOVED flex-[2] and flex-[1] containers
 * - Component now renders ONLY the metrics dashboard
 * - StatePanel provides unified header and footer
 *
 * Template: iterative-metrics
 * - Dashboard with Window Operation Math
 * - Shows "Prev - Out + In = New" calculation
 * - Performance bar and active/best window metrics
 */
const SlidingWindowState = ({ step, trace }) => {
  // Early return
  if (!step?.data?.visualization) {
    return (
      <div className="text-slate-400 text-sm p-4">No state data available</div>
    );
  }

  const viz = step.data.visualization;
  const metrics = viz.metrics || {};
  const pointers = viz.pointers || {};
  const array = viz.array || [];

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

  // Step Type
  const stepType = step.type || "STEP";

  // === Window Operation Calculation ===
  const calculateWindowOperation = () => {
    // Only show for SLIDE_WINDOW steps
    if (stepType !== "SLIDE_WINDOW") return null;

    // Extract previous sum from description (e.g., "Sum changes from 8 to 7")
    const desc = step.description || "";
    const match = desc.match(/from (\d+) to (\d+)/);
    if (!match) return null;

    const prevSum = parseInt(match[1]);
    const newSum = parseInt(match[2]);

    // Verify newSum matches currentSum
    if (newSum !== currentSum) return null;

    // Calculate outgoing and incoming values
    const outgoingIndex = currStart - 1;
    const incomingIndex = currEnd;

    if (outgoingIndex < 0 || outgoingIndex >= array.length) return null;
    if (incomingIndex < 0 || incomingIndex >= array.length) return null;

    const outgoingValue = array[outgoingIndex]?.value;
    const incomingValue = array[incomingIndex]?.value;

    if (outgoingValue === undefined || incomingValue === undefined) return null;

    // Verify the math
    const calculatedSum = prevSum - outgoingValue + incomingValue;
    if (calculatedSum !== currentSum) return null;

    return {
      prevSum,
      outgoingValue,
      incomingValue,
      newSum,
      outgoingIndex,
      incomingIndex,
    };
  };

  const operation = calculateWindowOperation();

  return (
    <div className="h-full flex flex-col bg-slate-800 p-4 gap-3">
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

      {/* Window Operation Card */}
      {operation && (
        <div className="shrink-0 bg-amber-900/20 border border-amber-700/30 rounded-lg p-3">
          <div className="text-[10px] font-bold text-amber-400/80 uppercase tracking-wider mb-2">
            Window Operation
          </div>
          <div className="flex items-center justify-center gap-2 font-mono text-sm">
            <span className="text-slate-300">{operation.prevSum}</span>
            <span className="text-slate-500">−</span>
            <span className="text-red-400 font-bold">
              {operation.outgoingValue}
              <span className="text-[9px] text-red-300/60 ml-0.5">
                [↗{operation.outgoingIndex}]
              </span>
            </span>
            <span className="text-slate-500">+</span>
            <span className="text-green-400 font-bold">
              {operation.incomingValue}
              <span className="text-[9px] text-green-300/60 ml-0.5">
                [↘{operation.incomingIndex}]
              </span>
            </span>
            <span className="text-slate-500">=</span>
            <span className="text-cyan-300 font-bold text-lg">
              {operation.newSum}
            </span>
          </div>
        </div>
      )}

      {/* Performance Bar */}
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
  );
};

SlidingWindowState.propTypes = {
  step: PropTypes.shape({
    type: PropTypes.string,
    description: PropTypes.string,
    data: PropTypes.shape({
      visualization: PropTypes.shape({
        array: PropTypes.array,
        metrics: PropTypes.object,
        pointers: PropTypes.object,
      }),
    }),
  }).isRequired,
  trace: PropTypes.object,
};

export default SlidingWindowState;