import React, { useState } from "react";
import { useTrace } from "../../contexts/TraceContext";
import { useNavigation } from "../../contexts/NavigationContext";
import { useVisualHighlight } from "../../contexts/HighlightContext";
import { getVisualizationComponent } from "../../utils/visualizationRegistry";
import ErrorBoundary from "../ErrorBoundary";
import AlgorithmInfoModal from "../AlgorithmInfoModal";

const VisualizationPanel = () => {
  const [showAlgorithmInfo, setShowAlgorithmInfo] = useState(false);

  // 1. Consume Contexts
  const { trace } = useTrace();
  const { currentStepData } = useNavigation();
  const { effectiveHighlight, handleIntervalHover } = useVisualHighlight();

  // 2. Determine Component
  const visualizationType = trace?.metadata?.visualization_type || "timeline";
  const visualizationConfig = trace?.metadata?.visualization_config || {};
  const VisualizationComponent = getVisualizationComponent(visualizationType);

  // 3. Prepare Props (The Contract)
  const componentProps = {
    step: currentStepData,
    config: visualizationConfig,
    // Add highlight props only if needed (or pass generic handlers)
    highlightedIntervalId: effectiveHighlight,
    onIntervalHover: handleIntervalHover,
  };

  return (
    <div
      id="panel-visualization"
      className="flex flex-[3] select-none flex-col overflow-hidden rounded-xl border border-slate-700 bg-slate-800 shadow-2xl"
    >
      <div className="flex flex-shrink-0 items-center justify-between border-b border-slate-700 px-4 py-3">
        <h2 className="text-lg font-semibold text-white">
          {visualizationType.charAt(0).toUpperCase() +
            visualizationType.slice(1)}{" "}
          Visualization
        </h2>
        <button
          id="algorithm-info-trigger"
          onClick={() => setShowAlgorithmInfo(true)}
          className="group rounded-full bg-slate-700 p-2 transition-colors hover:bg-slate-600"
          title="Algorithm Details"
        >
          <svg
            className="h-5 w-5 text-blue-400 group-hover:text-blue-300"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12" y2="8" />
          </svg>
        </button>
      </div>
      <div className="flex flex-1 flex-col items-start overflow-auto">
        <div className="mx-auto h-full w-full">
          <ErrorBoundary>
            <VisualizationComponent {...componentProps} />
          </ErrorBoundary>
        </div>
      </div>
      <ErrorBoundary>
        <AlgorithmInfoModal
          isOpen={showAlgorithmInfo}
          onClose={() => setShowAlgorithmInfo(false)}
        />
      </ErrorBoundary>
    </div>
  );
};

export default VisualizationPanel;
