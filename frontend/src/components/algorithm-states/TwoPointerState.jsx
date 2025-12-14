import React from "react";
import PropTypes from "prop-types";

/**
 * TwoPointerState - Displays algorithm-specific state for the Two Pointer pattern.
 *
 * Shows:
 * - Pointers (slow, fast)
 * - Unique element count
 */
const TwoPointerState = ({ step }) => {
  if (!step?.data?.visualization) {
    return (
      <div className="text-gray-400 text-sm">
        No state data available for this step
      </div>
    );
  }

  const { pointers = {}, unique_count } = step.data.visualization;

  return (
    <div className="space-y-4">
      {/* Pointers Section */}
      <div className="bg-slate-700/50 rounded-lg p-4">
        <h3 className="text-white font-semibold mb-2">Pointers</h3>
        <div className="space-y-2 text-sm">
          {Object.entries(pointers).map(
            ([key, value]) =>
              (key === 'slow' || key === 'fast') && (
                <div key={key} className="flex justify-between">
                  <span className="text-gray-400 capitalize">{key}:</span>
                  <span className="text-white font-mono">{value !== null && value !== undefined ? value : 'N/A'}</span>
                </div>
              )
          )}
        </div>
      </div>

      {/* Unique Count Section */}
      {unique_count !== undefined && (
        <div className="bg-slate-700/50 rounded-lg p-4">
          <h3 className="text-white font-semibold mb-2">Progress</h3>
          <div className="text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Unique Elements Found:</span>
              <span className="text-white font-mono text-lg">{unique_count}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

TwoPointerState.propTypes = {
  step: PropTypes.shape({
    data: PropTypes.shape({
      visualization: PropTypes.shape({
        pointers: PropTypes.object,
        unique_count: PropTypes.number,
      }),
    }),
  }).isRequired,
};

export default TwoPointerState;
