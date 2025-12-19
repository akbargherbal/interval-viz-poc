// frontend/src/components/algorithm-states/TwoPointerState.jsx

import React from "react";
import PropTypes from "prop-types";

/**
 * TwoPointerState - Pure Content Component (Phase 0 Refactored)
 *
 * CRITICAL CHANGES (Session 53):
 * - REMOVED internal 2:1 layout (header/footer)
 * - REMOVED flex-[2] and flex-[1] containers
 * - Component now renders ONLY the metrics dashboard
 * - StatePanel provides unified header and footer
 *
 * Template: iterative-metrics
 * - Visualize "Write vs Read" operation
 * - Show Value[Slow] vs Value[Fast] comparison
 * - Highlight duplicate detection and unique element writes
 */
const TwoPointerState = ({ step, trace }) => {
  // Early return
  if (!step?.data?.visualization) {
    return (
      <div className="text-slate-400 text-sm p-4">No state data available</div>
    );
  }

  const viz = step.data.visualization;
  const pointers = viz.pointers || {};
  const metrics = viz.metrics || {};
  const array = viz.array || [];

  // Data Extraction
  const slow = pointers.slow ?? 0;
  const fast = pointers.fast ?? 0;
  const uniqueCount = metrics.unique_count ?? 0;

  // Get values at pointer positions
  const slowValue = array[slow]?.value ?? "-";
  const fastValue = array[fast]?.value ?? "-";

  // Determine operation type from step type
  const stepType = step.type || "STEP";
  const isCompare = stepType === "COMPARE";
  const isUnique = stepType === "HANDLE_UNIQUE";

  // Comparison result
  const valuesMatch = slowValue === fastValue;

  return (
    <div className="h-full flex flex-col bg-slate-800 p-4 gap-3">
      {/* Header: Context Info */}
      <div className="flex justify-between items-center shrink-0">
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
          Two Pointer Metrics
        </h2>
        <div className="text-[10px] font-mono text-slate-500 bg-slate-900/50 px-2 py-1 rounded">
          Array Length:{" "}
          <span className="text-slate-300 font-bold">{array.length}</span>
        </div>
      </div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-2 gap-3 flex-1 min-h-0">
        {/* Card 1: Slow Pointer (Write Position) */}
        <div className="bg-slate-700/30 border-l-4 border-purple-500/50 rounded-r-lg p-3 flex flex-col justify-between relative overflow-hidden">
          <div className="text-[10px] font-bold text-purple-400/80 uppercase tracking-wider">
            Slow (Write)
          </div>

          <div className="flex flex-col items-start my-1">
            <span className="text-4xl font-mono font-bold text-purple-300 tracking-tighter drop-shadow-lg">
              {slowValue}
            </span>
            <span className="text-[10px] text-slate-400 uppercase mt-1">
              Value at Index
            </span>
          </div>

          <div className="mt-auto pt-2 border-t border-slate-600/30 w-full">
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-slate-500">Position:</span>
              <span className="text-purple-200 bg-purple-900/30 px-1.5 py-0.5 rounded">
                [{slow}]
              </span>
            </div>
          </div>
        </div>

        {/* Card 2: Fast Pointer (Read Position) */}
        <div className="bg-slate-700/30 border-l-4 border-cyan-500/50 rounded-r-lg p-3 flex flex-col justify-between relative overflow-hidden">
          <div className="text-[10px] font-bold text-cyan-400/80 uppercase tracking-wider">
            Fast (Read)
          </div>

          <div className="flex flex-col items-start my-1">
            <span className="text-4xl font-mono font-bold text-cyan-300 tracking-tighter drop-shadow-lg">
              {fastValue}
            </span>
            <span className="text-[10px] text-slate-400 uppercase mt-1">
              Value at Index
            </span>
          </div>

          <div className="mt-auto pt-2 border-t border-slate-600/30 w-full">
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-slate-500">Position:</span>
              <span className="text-cyan-200 bg-cyan-900/30 px-1.5 py-0.5 rounded">
                [{fast}]
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Comparison Result Card */}
      {isCompare && (
        <div
          className={`shrink-0 border rounded-lg p-3 transition-all duration-300 ${
            valuesMatch
              ? "bg-red-900/20 border-red-700/30"
              : "bg-emerald-900/20 border-emerald-700/30"
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="text-[10px] font-bold uppercase tracking-wider">
              {valuesMatch ? (
                <span className="text-red-400/80">Duplicate Detected</span>
              ) : (
                <span className="text-emerald-400/80">New Unique Element</span>
              )}
            </div>
            <div className="flex items-center gap-2 font-mono text-sm">
              <span className="text-purple-300">{slowValue}</span>
              <span className="text-slate-500">{valuesMatch ? "=" : "≠"}</span>
              <span className="text-cyan-300">{fastValue}</span>
            </div>
          </div>
        </div>
      )}

      {/* Write Operation Indicator */}
      {isUnique && (
        <div className="shrink-0 bg-emerald-900/20 border border-emerald-700/30 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <div className="text-[10px] font-bold text-emerald-400/80 uppercase tracking-wider">
              ✨ Write Operation
            </div>
            <div className="flex items-center gap-2 font-mono text-sm">
              <span className="text-cyan-300">{fastValue}</span>
              <span className="text-slate-500">→</span>
              <span className="text-purple-300">arr[{slow}]</span>
            </div>
          </div>
        </div>
      )}

      {/* Unique Count Progress */}
      <div className="shrink-0">
        <div className="flex justify-between text-[9px] text-slate-500 mb-1 uppercase font-bold">
          <span>Unique Elements Found</span>
          <span className="text-emerald-400 text-base font-mono">
            {uniqueCount}
          </span>
        </div>
        <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-700/50">
          <div
            className="h-full bg-gradient-to-r from-purple-500 to-emerald-500 transition-all duration-500 ease-out"
            style={{ width: `${(uniqueCount / array.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
};

TwoPointerState.propTypes = {
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

export default TwoPointerState;