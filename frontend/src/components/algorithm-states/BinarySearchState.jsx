// frontend/src/components/algorithm-states/BinarySearchState.jsx

import React from "react";
import PropTypes from "prop-types";

/**
 * BinarySearchState - Iterative Dashboard Implementation
 *
 * Uses the 5-zone dashboard layout defined in index.css (from iterative_metrics_algorithm_mockup.html).
 *
 * Zones:
 * 1. Primary: Mid Value (Hero)
 * 2. Goal: Target Value
 * 3. Logic: Comparison (Mid vs Target)
 * 4. Action: Next Step Description
 * 5. Overlay: Pointers (L, R) & Search Space
 */
const BinarySearchState = ({ step }) => {
  // Graceful degradation
  if (!step?.data?.visualization) {
    return <div className="p-4 text-slate-400">No state data available</div>;
  }

  const { pointers, array, search_space_size } = step.data.visualization;

  // Safe data extraction
  const leftIdx = pointers?.left ?? "-";
  const rightIdx = pointers?.right ?? "-"; // aka primaryValue
  const midIdx = pointers?.mid; // Can be null/undefined initially
  const target = pointers?.target ?? "?";
  const Z1_LONG_TEXT = 4;


  // Resolve Mid Value
  let midValue = "-";
  if (midIdx !== null && midIdx !== undefined && Array.isArray(array)) {
    const midElement = array.find((item) => item.index === midIdx);
    if (midElement) midValue = midElement.value;
  }

  // Logic & Action Derivation
  let logicText = "INITIALIZE";
  let logicSubtext = "Waiting to start";
  let actionText = "PREPARE SEARCH";
  let logicColor = "text-white";
  let actionColor = "text-slate-300";
  const Z3_LONG_TEXT = 5


  if (step.type === "CALCULATE_MID") {
    logicText = "CALC MID";
    logicSubtext = `(${leftIdx} + ${rightIdx}) / 2 = ${midIdx}`;
    actionText = "COMPARE MID WITH TARGET";
  } else if (midValue !== "-" && target !== "?") {
    if (midValue < target) {
      logicText = `${midValue} < ${target}`;
      logicSubtext = "Mid is smaller";
      logicColor = "text-blue-300";
      actionText = "SEARCH RIGHT →";
      actionColor = "text-blue-200";
    } else if (midValue > target) {
      logicText = `${midValue} > ${target}`;
      logicSubtext = "Mid is larger";
      logicColor = "text-amber-300";
      actionText = "← SEARCH LEFT";
      actionColor = "text-amber-200";
    } else {
      logicText = `${midValue} == ${target}`;
      logicSubtext = "Match found!";
      logicColor = "text-emerald-300";
      actionText = "RETURN INDEX";
      actionColor = "text-emerald-200";
    }
  }

  // Override action text based on specific step types if needed
  if (step.type === "SEARCH_RIGHT") {
    actionText = "ELIMINATE LEFT HALF";
    actionColor = "text-blue-200";
  }
  if (step.type === "SEARCH_LEFT") {
    actionText = "ELIMINATE RIGHT HALF";
    actionColor = "text-amber-200";
  }
  if (step.type === "FOUND") {
    actionText = "TARGET FOUND";
    actionColor = "text-emerald-200";
  }

  return (
    <div className="dashboard">
      {/* ZONE 1: PRIMARY FOCUS (Mid Value) */}
      <div className="zone zone-primary">
        <div className="zone-label">Mid</div>
        <div className="zone-meta">IDX {midIdx ?? "-"}</div>
        <div
          className={`primary-value ${
            // Reduce font size for long text
            typeof rightIdx === "string" && rightIdx.length > Z1_LONG_TEXT
              ? "long-text"
              : ""
          }`}
        >{midValue}</div>

        {/* ZONE 5: OVERLAY (Boundaries) */}
        <div className="zone-boundaries">
          <div className="boundary-cell">
            <div className="boundary-label">Left</div>
            <div className="boundary-value">{leftIdx}</div>
          </div>
          <div className="boundary-cell">
            <div className="boundary-label">Right</div>
            <div className="boundary-value">{rightIdx}</div>
          </div>
          <div className="boundary-cell">
            <div className="boundary-label">Space</div>
            <div className="boundary-value">{search_space_size ?? "-"}</div>
          </div>
        </div>
      </div>

      {/* ZONE 2: GOAL (Target) */}
      <div className="zone zone-goal">
        <div className="zone-label">Target</div>
        <div className="goal-value">{target}</div>
      </div>

      {/* ZONE 3: LOGIC (Comparison) */}
      <div className="zone zone-logic">
        <div className="zone-label">LOGIC</div>
        <div className="logic-content">
          <div className={`${logicColor} ${
            // Reduce font size for long text
            typeof logicText === "string" && logicText.length > Z3_LONG_TEXT
              ? "zone3-long-text"
              : ""
            }
          `}>{logicText}</div>
          <div
            className={`mt-1 text-[12px] font-normal ${logicColor}`}
          >
            {logicSubtext}
          </div>
        </div>
      </div>

      {/* ZONE 4: ACTION */}
      <div className="zone zone-action">
        <div className={`action-text ${actionColor}`}>{actionText}</div>
      </div>
    </div>
  );
};

BinarySearchState.propTypes = {
  step: PropTypes.shape({
    type: PropTypes.string,
    data: PropTypes.shape({
      visualization: PropTypes.shape({
        pointers: PropTypes.object,
        array: PropTypes.arrayOf(PropTypes.object),
        search_space_size: PropTypes.number,
      }),
    }),
  }).isRequired,
};

export default BinarySearchState;