import React from "react";

/**
 * ArrayView - Visualization component for array-based algorithms
 *
 * Phase 3: Dynamic visualization for Binary Search and other array algorithms.
 * PERMANENT FIX (Session 14): Solved recurring overflow cutoff issue.
 *
 * ROOT CAUSE: Using `items-center` + `overflow-auto` causes flex centering
 * to cut off left content. This is a well-documented CSS flexbox issue.
 *
 * SOLUTION: Use `items-start` on outer container, then center inner content
 * with `mx-auto`. This allows proper scrolling without cutoff.
 *
 * Expected data structure:
 * step.data.visualization = {
 *   array: [{index, value, state}, ...],
 *   pointers: {left, right, mid, target},
 *   search_space_size: number
 * }
 *
 * Element states: 'active_range', 'examining', 'found', 'excluded'
 */
const ArrayView = ({ step, config = {} }) => {
  const visualization = step?.data?.visualization;

  if (!visualization || !visualization.array) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        No array data available
      </div>
    );
  }

  const { array, pointers, search_space_size } = visualization;
  const {
    show_indices = true,
    pointer_colors = {
      left: "blue",
      right: "red",
      mid: "yellow",
      target: "green"
    }
  } = config;

  // Map element states to Tailwind classes
  const getElementClasses = (element) => {
    const baseClasses = "w-16 h-16 flex items-center justify-center rounded-lg font-bold text-lg transition-all duration-300 border-2 flex-shrink-0";

    switch (element.state) {
      case "examining":
        return `${baseClasses} bg-yellow-500 border-yellow-400 text-black scale-110 shadow-lg animate-pulse`;
      case "found":
        return `${baseClasses} bg-green-500 border-green-400 text-white scale-110 shadow-lg`;
      case "active_range":
        return `${baseClasses} bg-blue-600 border-blue-500 text-white`;
      case "excluded":
        return `${baseClasses} bg-gray-700 border-gray-600 text-gray-500 opacity-50`;
      default:
        return `${baseClasses} bg-slate-600 border-slate-500 text-white`;
    }
  };

  // Render pointer indicator below array
  const renderPointers = () => {
    const pointerIcons = [];

    if (pointers.left !== null && pointers.left !== undefined) {
      pointerIcons.push({
        index: pointers.left,
        label: "L",
        color: "text-blue-400",
        bgColor: "bg-blue-900/50"
      });
    }

    if (pointers.right !== null && pointers.right !== undefined) {
      pointerIcons.push({
        index: pointers.right,
        label: "R",
        color: "text-red-400",
        bgColor: "bg-red-900/50"
      });
    }

    if (pointers.mid !== null && pointers.mid !== undefined) {
      pointerIcons.push({
        index: pointers.mid,
        label: "M",
        color: "text-yellow-400",
        bgColor: "bg-yellow-900/50"
      });
    }

    return (
      <div className="flex gap-2 mt-2">
        {array.map((element, idx) => (
          <div key={idx} className="w-16 h-8 flex flex-col items-center justify-end flex-shrink-0">
            {pointerIcons
              .filter(p => p.index === element.index)
              .map((pointer, pIdx) => (
                <div
                  key={pIdx}
                  className={`px-2 py-0.5 rounded text-xs font-bold ${pointer.color} ${pointer.bgColor} mb-0.5`}
                >
                  {pointer.label}
                </div>
              ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    // PERMANENT FIX: Use items-start + mx-auto pattern instead of items-center
    // This prevents flex centering from cutting off left overflow
    <div className="h-full flex flex-col items-start overflow-auto py-4 px-6">
      <div className="mx-auto flex flex-col items-center gap-6 min-h-0">
        {/* Target indicator */}
        {pointers.target !== null && pointers.target !== undefined && (
          <div className="px-4 py-2 bg-green-900/30 border border-green-600/50 rounded-lg flex-shrink-0">
            <span className="text-green-400 font-semibold">
              🎯 Target: <span className="text-white text-lg font-bold">{pointers.target}</span>
            </span>
          </div>
        )}

        {/* Array visualization */}
        <div className="flex flex-col items-center flex-shrink-0">
          {/* Index labels (top) */}
          {show_indices && (
            <div className="flex gap-2 mb-2">
              {array.map((element) => (
                <div
                  key={element.index}
                  className="w-16 text-center text-gray-400 text-xs font-mono flex-shrink-0"
                >
                  [{element.index}]
                </div>
              ))}
            </div>
          )}

          {/* Array elements */}
          <div className="flex gap-2">
            {array.map((element) => (
              <div
                key={element.index}
                className={getElementClasses(element)}
                title={`Index ${element.index}: ${element.value} (${element.state})`}
              >
                {element.value}
              </div>
            ))}
          </div>

          {/* Pointer indicators (bottom) */}
          {renderPointers()}
        </div>

        {/* Search space info */}
        <div className="text-sm text-gray-400 flex-shrink-0">
          Search space: <span className="text-white font-semibold">{search_space_size}</span> elements
        </div>

        {/* State legend */}
        <div className="flex flex-wrap gap-4 text-xs justify-center flex-shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-600 border border-blue-500 rounded flex-shrink-0"></div>
            <span className="text-gray-400">Active Range</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-yellow-500 border border-yellow-400 rounded flex-shrink-0"></div>
            <span className="text-gray-400">Examining</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 border border-green-400 rounded flex-shrink-0"></div>
            <span className="text-gray-400">Found</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-gray-700 border border-gray-600 rounded opacity-50 flex-shrink-0"></div>
            <span className="text-gray-400">Excluded</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArrayView;