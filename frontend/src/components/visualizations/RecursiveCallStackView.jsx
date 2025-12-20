import React from "react";
import PropTypes from "prop-types";

/**
 * RecursiveCallStackView - Displays recursive call stack as a tree
 *
 * Renders the call stack tree structure provided by the backend.
 * Uses backend-provided metadata (call_stack_state + all_intervals)
 * to visualize recursion hierarchy with depth-based color coding.
 *
 * Backend Contract:
 * - call_stack_state: Array of call objects with {id, depth, array, operation, is_active}
 * - all_intervals: Array of interval metadata with {id, label, state, color, start, end}
 *
 * Design Reference: merge_sort_static_mockup_compact.html
 *
 * @param {Array} callStackState - Call stack from backend (step.data.visualization.call_stack_state)
 * @param {Array} allIntervals - Interval metadata from backend (step.data.visualization.all_intervals)
 */
const RecursiveCallStackView = ({ callStackState = [], allIntervals = [] }) => {
  // Graceful degradation: no data
  if (!callStackState || callStackState.length === 0) {
    return (
      <div className="w-1/4 flex items-center justify-center h-full text-slate-500 text-sm">
       <p className="text-center">No call stack data available</p>
      </div>
    );
  }

  /**
   * Merge call stack with interval metadata
   * Backend provides data in two arrays - we join them by call ID
   */
  const enrichedCalls = callStackState.map((call) => {
    const interval = allIntervals?.find((i) => i.id === call.id) || {};
    return {
      ...call,
      label: interval.label || `Call ${call.id}`,
      state: interval.state || "unknown",
      color: interval.color || "gray",
    };
  });

  /**
   * Backend color mapping to Tailwind classes
   * Colors come from backend visualization_config.color_by_depth
   */
  const getColorClasses = (color) => {
    // Note: Backend provides semantic colors (blue/green/amber) for depth levels
    // We map these to Tailwind classes that match the static mockup
    const colorMap = {
      blue: "bg-blue-500/15 border-blue-500 text-blue-300",
      green: "bg-green-500/15 border-green-500 text-green-300",
      amber: "bg-amber-500/15 border-amber-500 text-amber-300",
    };
    return colorMap[color] || "bg-slate-700/15 border-slate-600 text-slate-400";
  };

  /**
   * State badge styling based on backend operation type
   * Backend provides: "split", "merge", "base_case"
   */
  const getStateBadgeClasses = (state, operation) => {
    // Backend state: "splitting", "merging", "complete"
    const stateMap = {
      splitting: "bg-indigo-500/30 text-indigo-200",
      merging: "bg-purple-500/30 text-purple-200",
      complete: "bg-green-500/30 text-green-200",
    };
    return stateMap[state] || "bg-slate-600/30 text-slate-300";
  };

  /**
   * State badge label based on backend state
   * Note: Changed "merging" -> "MERGE" for brevity in compact UI
   */
  const getStateBadgeLabel = (state, operation) => {
    if (state === "complete") return "DONE";
    if (state === "merging") return "MERGE";
    if (state === "splitting") return "SPLIT";
    // Fallback to operation if state unclear
    return operation?.toUpperCase() || "ACTIVE";
  };

  /**
   * Depth-based indentation classes
   * Backend provides depth (0, 1, 2, ...) - we use it for visual hierarchy
   */
  const getDepthClasses = (depth) => {
    const depthMap = {
      0: "ml-0",
      1: "ml-3 border-l-2 border-white/10",
      2: "ml-6 border-l-2 border-white/10",
    };
    return depthMap[depth] || `ml-${Math.min(depth * 3, 12)} border-l-2 border-white/10`;
  };

  // Separate base cases (depth >= 2, state complete) for collapsed footer
  const activeCalls = enrichedCalls.filter(
    (call) => call.depth < 2 || call.state !== "complete"
  );
  const baseCases = enrichedCalls.filter(
    (call) => call.depth >= 2 && call.state === "complete"
  );

  // Calculate depth range for header
  const depths = enrichedCalls.map((c) => c.depth);
  const minDepth = Math.min(...depths);
  const maxDepth = Math.max(...depths);

  return (
    <div className="w-1/4 bg-slate-800 border-r border-slate-700 flex flex-col overflow-hidden h-full">
      {/* Header */}
      <div className="flex justify-between px-3 pt-3 pb-2 items-center border-b border-slate-700 flex-shrink-0">
        <h2 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
          Recursion Tree
        </h2>
        <div className="text-[9px] text-slate-500 font-mono">
          D: {minDepth}-{maxDepth}
        </div>
      </div>

      {/* Tree Content - Scrollable */}
      <div className="flex-1 overflow-y-auto custom-scrollbar bg-slate-900/30">
        <div className="p-2">
          {/* Active Calls */}
          {activeCalls.map((call) => (
            <div
              key={call.id}
              className={`
                flex items-center gap-1.5 px-2 py-1.5 mb-1 rounded border-2 font-mono text-[10px] font-semibold transition-all
                ${getDepthClasses(call.depth)}
                ${getColorClasses(call.color)}
                ${call.is_active ? "shadow-[0_0_16px_rgba(168,85,247,0.4)]" : ""}
                ${call.state === "complete" ? "opacity-50 border-dashed" : ""}
              `}
            >
              <div className="font-bold tracking-tight">{call.label}</div>
              <div
                className={`
                  ml-auto text-[8px] uppercase px-1 py-0.5 rounded font-extrabold whitespace-nowrap
                  ${getStateBadgeClasses(call.state, call.operation)}
                `}
              >
                {getStateBadgeLabel(call.state, call.operation)}
              </div>
            </div>
          ))}

          {/* Collapsed Base Cases (if any) */}
          {baseCases.length > 0 && (
            <>
              <div className="border-t border-slate-700/50 my-1.5 mx-1"></div>
              <div className="px-1.5 py-1 text-[9px] text-slate-500 font-mono">
                <div className="opacity-40 leading-tight">
                  {baseCases.map((call, idx) => (
                    <div key={call.id} className="mb-0.5">
                      {idx === baseCases.length - 1 ? "└─" : "├─"} {call.label} ✓
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Legend Footer */}
      <div className="px-3 py-1.5 border-t border-slate-700 bg-slate-800/50 flex-shrink-0">
        <div className="text-[9px] text-slate-400 flex items-center gap-1.5 flex-wrap">
          <div className="flex items-center gap-1">
            <div className="w-2.5 h-2.5 rounded-sm bg-blue-500/30 border border-blue-500"></div>
            <span>Root</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2.5 h-2.5 rounded-sm bg-green-500/30 border border-green-500"></div>
            <span>Mid</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-2.5 h-2.5 rounded-sm bg-amber-500/30 border border-amber-500"></div>
            <span>Base</span>
          </div>
        </div>
      </div>
    </div>
  );
};

RecursiveCallStackView.propTypes = {
  callStackState: PropTypes.arrayOf(
    PropTypes.shape({
      array: PropTypes.array,
      depth: PropTypes.number.isRequired,
      id: PropTypes.string.isRequired,
      is_active: PropTypes.bool,
      operation: PropTypes.string,
    })
  ),
  allIntervals: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      label: PropTypes.string,
      state: PropTypes.string,
      color: PropTypes.string,
      start: PropTypes.number,
      end: PropTypes.number,
    })
  ),
};

export default React.memo(RecursiveCallStackView);
