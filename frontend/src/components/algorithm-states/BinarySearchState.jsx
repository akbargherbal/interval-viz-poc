// frontend/src/components/algorithm-states/BinarySearchState.jsx

import React from "react";
import PropTypes from "prop-types";

/**
 * BinarySearchState - Pure Content Component (Phase 0 Refactored)
 *
 * CRITICAL CHANGES (Session 53):
 * - REMOVED internal 2:1 layout (header/footer)
 * - REMOVED flex-[2] and flex-[1] containers
 * - Component now renders ONLY the metrics dashboard
 * - StatePanel provides unified header and footer
 *
 * Template: iterative-metrics
 * - Dashboard fills available space edge-to-edge
 * - No internal padding (container queries handle scaling)
 * - Step description handled by StatePanel footer
 */
const BinarySearchState = ({ step, trace }) => {
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

  return (
    <div className="h-full flex flex-col bg-slate-800 p-4 gap-3">
      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 flex-1">
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

      {/* Secondary Metrics Strip */}
      <div className="bg-slate-900/40 rounded-lg border border-slate-700/50 p-3 shrink-0">
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