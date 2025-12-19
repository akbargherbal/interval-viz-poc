import React from "react";
import PropTypes from "prop-types";
import { useTrace } from "../../contexts/TraceContext";
import { useNavigation } from "../../contexts/NavigationContext";
import { useVisualHighlight } from "../../contexts/HighlightContext";
import { getStateComponent, getAlgorithmTemplate } from "../../utils/stateRegistry";
import { getStepTypeBadge } from "../../utils/stepBadges";
import ErrorBoundary from "../ErrorBoundary";

const StatePanel = () => {
  // 1. Consume Contexts
  const { trace, currentAlgorithm } = useTrace();
  const { currentStepData, currentStep } = useNavigation();
  const { handleIntervalHover } = useVisualHighlight();

  // 2. Determine Component and Template
  const StateComponent = getStateComponent(currentAlgorithm);
  const template = getAlgorithmTemplate(currentAlgorithm);
  const badge = getStepTypeBadge(currentStepData?.type);

  // 3. Template-specific behavior
  const isIterativeMetrics = template === "iterative-metrics";
  
  // For iterative-metrics: no padding, overflow handled by child
  // For recursive-context: padding and overflow in wrapper
  const contentClasses = isIterativeMetrics
    ? "flex-1 overflow-hidden"
    : "flex-1 overflow-y-auto px-6 py-4";

  return (
    <div
      id="panel-steps"
      className="w-96 bg-slate-800 rounded-xl shadow-2xl flex flex-col overflow-hidden"
    >
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-700">
        <h2 className="text-white font-bold">Algorithm State</h2>
      </div>

      {/* Registry Component Render */}
      <div id="panel-steps-list" className={contentClasses}>
        <ErrorBoundary>
          <StateComponent
            step={currentStepData}
            trace={trace}
            currentStep={currentStep}
            onIntervalHover={handleIntervalHover}
          />
        </ErrorBoundary>
      </div>

      {/* Description Footer - Only for recursive-context templates */}
      {!isIterativeMetrics && (
        <div
          id="panel-step-description"
          className="border-t border-slate-700 p-4 bg-slate-800"
        >
          <div className="p-4 bg-gradient-to-br from-slate-700/60 to-slate-800/60 rounded-lg border border-slate-600/50 shadow-lg">
            <div className="mb-3">
              <span
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold ${badge.color}`}
              >
                {badge.label}
              </span>
            </div>
            <p className="text-white text-base font-medium leading-relaxed">
              {currentStepData?.description || "No description available"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

StatePanel.propTypes = {
  // No props needed - uses context
};

export default StatePanel;