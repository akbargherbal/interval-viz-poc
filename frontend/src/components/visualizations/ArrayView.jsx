import React from "react";
import ArrayItem from "./ArrayItem";

/**
 * ArrayView - Visualization component for array-based algorithms
 *
 * Phase 3: Dynamic visualization for Binary Search and other array algorithms.
 * REFACTOR (Session): Implemented "No-Scroll" wrapping grid layout.
 * 
 * ARCHITECTURE: Atomic Item Pattern
 * - Each array element is a vertical slice (index + value + pointer)
 * - Grid uses flex-wrap to automatically wrap to multiple rows
 * - Eliminates horizontal scrolling for arrays up to N=20
 * 
 * OVERFLOW PATTERN (PERMANENT FIX from Session 14):
 * - Outer container: `items-start` + `overflow-auto`
 * - Inner wrapper: `mx-auto`
 * - This prevents flex centering from cutting off left content
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
  // UPDATED: Reduced sizing from w-16 h-16 to w-12 h-12, text-lg to text-base
  const getElementClasses = (element) => {
    const baseClasses = "w-12 h-12 flex items-center justify-center rounded-md font-bold text-base transition-all duration-300 border-2 flex-shrink-0";

    switch (element.state) {
      case "examining":
        return `${baseClasses} bg-yellow-500 border-yellow-400 text-black scale-110 shadow-lg animate-pulse`;
      case "found":
        return `${baseClasses} bg-green-500 border-green-400 text-white scale-110 shadow-lg`;
      case "active_range":
        return `${baseClasses} bg-blue-600 border-blue-500 text-white shadow-md`;
      case "excluded":
        return `${baseClasses} bg-gray-700 border-gray-600 text-gray-500 opacity-50`;
      default:
        return `${baseClasses} bg-slate-600 border-slate-500 text-white`;
    }
  };

  /**
   * Get pointer data for a specific array index
   * @param {number} index - Array index to check for pointers
   * @returns {Object|null} Pointer data {label, color, bgColor} or null if no pointer at this index
   */
  const getPointerForIndex = (index) => {
    // Check each pointer type and return the appropriate styling
    if (pointers.left !== null && pointers.left !== undefined && pointers.left === index) {
      return { 
        label: 'L', 
        color: 'text-blue-400', 
        bgColor: 'bg-blue-900/50' 
      };
    }
    
    if (pointers.right !== null && pointers.right !== undefined && pointers.right === index) {
      return { 
        label: 'R', 
        color: 'text-red-400', 
        bgColor: 'bg-red-900/50' 
      };
    }
    
    if (pointers.mid !== null && pointers.mid !== undefined && pointers.mid === index) {
      return { 
        label: 'M', 
        color: 'text-yellow-400', 
        bgColor: 'bg-yellow-900/50' 
      };
    }
    
    return null;
  };

  return (
    // PERMANENT FIX: Use items-start + mx-auto pattern instead of items-center
    // This prevents flex centering from cutting off left overflow
    <div className="h-full flex flex-col items-start overflow-auto py-4 px-6">
      <div className="mx-auto flex flex-col items-center gap-4 min-h-0 w-full">
        {/* Target indicator */}
        {pointers.target !== null && pointers.target !== undefined && (
          <div className="px-4 py-1.5 bg-green-900/30 border border-green-600/50 rounded-lg flex-shrink-0">
            <span className="text-green-400 font-semibold text-sm">
              🎯 Target: <span className="text-white text-base font-bold">{pointers.target}</span>
            </span>
          </div>
        )}

        {/* Array visualization - Wrapping Grid Layout */}
        <div className="flex flex-wrap justify-center gap-2 w-full max-w-4xl">
          {array.map((element) => (
            <ArrayItem
              key={element.index}
              element={element}
              pointer={getPointerForIndex(element.index)}
              getElementClasses={getElementClasses}
            />
          ))}
        </div>

        {/* Search space info */}
        <div className="text-xs text-gray-400 flex-shrink-0">
          Search space: <span className="text-white font-semibold">{search_space_size}</span> elements
        </div>

        {/* State legend */}
        <div className="flex flex-wrap gap-3 text-[10px] justify-center flex-shrink-0">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 bg-blue-600 border border-blue-500 rounded flex-shrink-0"></div>
            <span className="text-gray-400">Active Range</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 bg-yellow-500 border border-yellow-400 rounded flex-shrink-0"></div>
            <span className="text-gray-400">Examining</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 bg-green-500 border border-green-400 rounded flex-shrink-0"></div>
            <span className="text-gray-400">Found</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 bg-gray-700 border border-gray-600 rounded opacity-50 flex-shrink-0"></div>
            <span className="text-gray-400">Excluded</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArrayView;
