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
      <div className="mb-0.5 font-mono text-[10px] text-gray-500">
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
      <div className="mt-1 flex h-6 flex-col items-center justify-start">
        {pointer && (
          <div
            className={`rounded-[4px] px-1.5 py-0.5 text-[10px] font-bold ${pointer.color} ${pointer.bgColor} leading-none`}
          >
            {pointer.label}
          </div>
        )}
      </div>
    </div>
  );
};

export default ArrayItem;
