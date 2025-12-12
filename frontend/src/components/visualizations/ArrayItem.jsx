import React from "react";

/**
 * ArrayItem - Atomic component for array element visualization
 * 
 * Represents a single array element with vertically stacked components:
 * - Index label (top)
 * - Value box (middle) 
 * - Pointer indicator (bottom)
 * 
 * This "atomic" structure allows the parent to use a wrapping grid layout
 * while maintaining visual alignment between index, value, and pointer.
 * 
 * @param {Object} props
 * @param {Object} props.element - Array element data {index, value, state}
 * @param {Object|null} props.pointer - Pointer data {label, color, bgColor} or null
 * @param {Function} props.getElementClasses - Function to generate Tailwind classes based on element state
 */
const ArrayItem = ({ element, pointer, getElementClasses }) => {
  return (
    <div className="flex flex-col items-center">
      {/* Index Label */}
      <div className="text-gray-500 text-[10px] font-mono mb-0.5">
        [{element.index}]
      </div>
      
      {/* Value Box */}
      <div 
        className={getElementClasses(element)}
        title={`Index ${element.index}: ${element.value} (${element.state})`}
      >
        {element.value}
      </div>
      
      {/* Pointer Area - Fixed height to maintain alignment even when empty */}
      <div className="h-6 flex flex-col items-center justify-start mt-1">
        {pointer && (
          <div 
            className={`px-1.5 py-0.5 rounded-[4px] text-[10px] font-bold ${pointer.color} ${pointer.bgColor} leading-none`}
          >
            {pointer.label}
          </div>
        )}
      </div>
    </div>
  );
};

export default ArrayItem;
