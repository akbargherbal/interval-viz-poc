import React from "react";
import PropTypes from "prop-types";
import RecursiveCallStackView from "./RecursiveCallStackView";

/**
 * MergeSortVisualization - Custom visualization for Merge Sort algorithm
 *
 * Renders a 2-column layout:
 * - LEFT (LSP): Recursive call stack tree
 * - RIGHT (Main): Array comparison view during merge
 *
 * Backend Contract:
 * - step.data.visualization.call_stack_state (for LSP tree)
 * - step.data.visualization.all_intervals (for LSP tree)
 * - step.data.left, step.data.right (for merge comparison)
 * - step.data.merged_array, step.data.array (for result display)
 * - step.type (MERGE_COMPARE, MERGE_START, SPLIT_ARRAY, etc.)
 *
 * Design Reference: merge_sort_static_mockup_compact.html
 *
 * @param {Object} step - Current step data from backend
 * @param {Object} config - Visualization config from backend metadata
 */
const MergeSortVisualization = ({ step, config = {} }) => {
  // Extract backend data
  const visualization = step?.data?.visualization || {};
  const stepType = step?.type || "UNKNOWN";
  const stepData = step?.data || {};

  /**
   * Render array comparison view for merge phase
   * Shows left/right arrays with active pointers and comparison operator
   */
  const renderMergeComparison = () => {
    const { left, right, left_value, right_value, chose } = stepData;

    // Only show during merge operations
    if (!left || !right) return null;

    // Determine which side was chosen
    const leftActive = chose === "left";
    const rightActive = chose === "right";

    // Comparison operator (backend provides chose field)
    let operator = "?";
    let operatorResult = "";
    if (left_value !== undefined && right_value !== undefined) {
      if (leftActive) {
        operator = "≤";
        operatorResult = "TRUE";
      } else if (rightActive) {
        operator = ">";
        operatorResult = "TRUE";
      }
    }

    return (
      <div className="flex items-center gap-12">
        {/* Left Array */}
        <div className="flex flex-col items-center gap-2">
          <div className="text-[11px] text-slate-500 font-bold uppercase tracking-wider">
            Left Sorted
          </div>
          <div className="flex gap-2 p-2 bg-slate-800/50 rounded-lg border border-slate-700">
            {left.map((val, idx) => (
              <div
                key={idx}
                className={`
                  w-12 h-12 flex items-center justify-center rounded font-bold text-lg border-2
                  ${
                    idx === 0 && leftActive
                      ? "bg-slate-800 border-yellow-500 text-white shadow-[0_0_12px_rgba(234,179,8,0.3)]"
                      : "bg-slate-800 border-slate-700 text-slate-500 opacity-40"
                  }
                `}
              >
                {val}
                {idx === 0 && leftActive && (
                  <div className="absolute -top-2 -left-2 w-5 h-5 bg-yellow-500 rounded-full text-[9px] text-black flex items-center justify-center font-bold">
                    L
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Operator */}
        {left_value !== undefined && right_value !== undefined && (
          <div className="flex flex-col items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-slate-800 border-2 border-slate-600 flex items-center justify-center text-xl font-bold text-white shadow-lg">
              {operator}
            </div>
            {operatorResult && (
              <div className="px-3 py-1 bg-green-900/80 text-green-400 text-xs font-bold rounded-full border border-green-700 shadow-lg">
                {operatorResult}
              </div>
            )}
          </div>
        )}

        {/* Right Array */}
        <div className="flex flex-col items-center gap-2">
          <div className="text-[11px] text-slate-500 font-bold uppercase tracking-wider">
            Right Sorted
          </div>
          <div className="flex gap-2 p-2 bg-slate-800/50 rounded-lg border border-slate-700">
            {right.map((val, idx) => (
              <div
                key={idx}
                className={`
                  w-12 h-12 flex items-center justify-center rounded font-bold text-lg border-2
                  ${
                    idx === 0 && rightActive
                      ? "bg-slate-800 border-green-500 text-white shadow-[0_0_12px_rgba(34,197,94,0.3)]"
                      : "bg-slate-800 border-slate-700 text-slate-500 opacity-40"
                  }
                `}
              >
                {val}
                {idx === 0 && rightActive && (
                  <div className="absolute -top-2 -right-2 w-5 h-5 bg-green-500 rounded-full text-[9px] text-black flex items-center justify-center font-bold">
                    R
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  /**
   * Render merged result array
   * Shows elements that have been merged so far
   */
  const renderMergedResult = () => {
    const { merged_array, left, right } = stepData;
    
    // Don't show result during splits
    if (stepType.includes("SPLIT") || stepType === "BASE_CASE") return null;
    if (!left || !right) return null;

    const totalSize = (left?.length || 0) + (right?.length || 0);
    const filledCount = merged_array?.length || 0;
    const emptyCount = totalSize - filledCount;

    return (
      <div className="flex flex-col items-center gap-2 w-full max-w-lg">
        <div className="text-[11px] text-slate-500 font-bold uppercase w-full text-left border-b border-slate-800 pb-1 flex justify-between px-1">
          <span>Merged Result</span>
          <span className="text-purple-400">
            {filledCount === totalSize ? "Complete" : "Building..."}
          </span>
        </div>
        <div className="flex gap-2 w-full p-4 bg-slate-950/50 rounded-lg border border-slate-800 min-h-[68px] items-center overflow-x-auto custom-scrollbar flex-wrap justify-center">
          {/* Filled elements */}
          {(merged_array || []).map((val, idx) => (
            <div
              key={`filled-${idx}`}
              className="w-12 h-12 bg-emerald-900/30 border-2 border-emerald-500 rounded flex items-center justify-center text-emerald-300 text-lg font-bold flex-shrink-0"
            >
              {val}
            </div>
          ))}
          {/* Empty slots */}
          {Array.from({ length: emptyCount }).map((_, idx) => (
            <div
              key={`empty-${idx}`}
              className={`w-12 h-12 border-2 border-dashed border-slate-700 rounded flex items-center justify-center text-slate-600 text-sm font-medium flex-shrink-0 ${
                idx === 0 ? "animate-pulse" : ""
              }`}
            >
              ?
            </div>
          ))}
        </div>
      </div>
    );
  };

  /**
   * Render simple array view for non-merge steps
   * Shows current array state during splits or base cases
   */
  const renderSimpleArray = () => {
    const array = stepData.array || stepData.merged_array || [];
    if (array.length === 0) return null;

    return (
      <div className="flex flex-col items-center gap-3">
        <div className="text-slate-400 text-sm font-mono">
          Current Array [{array.length} elements]
        </div>
        <div className="flex gap-2 flex-wrap justify-center">
          {array.map((val, idx) => (
            <div
              key={idx}
              className="w-12 h-12 bg-slate-800 border-2 border-slate-600 rounded flex items-center justify-center text-white text-lg font-bold"
            >
              {val}
            </div>
          ))}
        </div>
      </div>
    );
  };

  /**
   * Determine phase for badge
   * Backend provides step.type - we map to user-friendly phase names
   */
  const getPhase = () => {
    if (stepType.includes("MERGE")) return "MERGE PHASE";
    if (stepType.includes("SPLIT")) return "DIVIDE PHASE";
    if (stepType.includes("BASE")) return "BASE CASE";
    if (stepType.includes("COMPLETE")) return "COMPLETE";
    return "PROCESSING";
  };

  return (
    <div className="flex h-full gap-0 overflow-hidden">
      {/* LEFT SIDE: Recursive Call Stack Tree (LSP) */}
      <RecursiveCallStackView
        callStackState={visualization.call_stack_state}
        allIntervals={visualization.all_intervals}
      />

      {/* RIGHT SIDE: Array Comparison (Main Area) */}
      <div className="flex-1 bg-slate-900 flex flex-col relative overflow-hidden">
        {/* Phase Indicator */}
        <div className="absolute top-3 right-3 px-3 py-1 bg-purple-900/50 border border-purple-500/50 rounded-full text-purple-300 text-xs font-bold backdrop-blur-sm z-10">
          {getPhase()}
        </div>

        <div className="flex-1 flex flex-col items-center justify-center gap-8 p-6 overflow-auto">
          {/* Render based on step type */}
          {stepType.includes("MERGE") && !stepType.includes("COMPLETE") ? (
            <>
              {renderMergeComparison()}
              {renderMergedResult()}
            </>
          ) : (
            renderSimpleArray()
          )}
        </div>
      </div>
    </div>
  );
};

MergeSortVisualization.propTypes = {
  step: PropTypes.shape({
    type: PropTypes.string,
    data: PropTypes.shape({
      array: PropTypes.array,
      left: PropTypes.array,
      right: PropTypes.array,
      merged_array: PropTypes.array,
      left_value: PropTypes.number,
      right_value: PropTypes.number,
      chose: PropTypes.string,
      visualization: PropTypes.shape({
        call_stack_state: PropTypes.array,
        all_intervals: PropTypes.array,
        comparison_count: PropTypes.number,
        merge_count: PropTypes.number,
      }),
    }),
  }).isRequired,
  config: PropTypes.object,
};

export default React.memo(MergeSortVisualization);
