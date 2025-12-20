import React from "react";
import PropTypes from "prop-types";
import { useTrace } from "../../contexts/TraceContext";
import { useNavigation } from "../../contexts/NavigationContext";
import { useVisualHighlight } from "../../contexts/HighlightContext";
import { getStateComponent, getAlgorithmTemplate } from "../../utils/stateRegistry";
import { getStepTypeBadge } from "../../utils/stepBadges";
import { useKeyboardHintsModal } from "../KeyboardHints";
import ErrorBoundary from "../ErrorBoundary";

/**
 * StatePanel - Unified container for algorithm state display (RIGHT panel)
 *
 * Phase 0 Refactoring (Session 53 - Dec 19, 2025):
 * - Extracted common header (Algorithm State + Keyboard Hints) outside #panel-steps-list
 * - Implemented 2:1 flex ratio (flex-[2] for content, flex-[1] for description)
 * - Footer now renders for BOTH templates (iterative-metrics AND recursive-context)
 * - Template-specific behavior isolated to content padding only
 *
 * Architecture:
 * ┌─────────────────────────────────────┐
 * │ HEADER (Unified - All Algorithms)   │ ← OUTSIDE #panel-steps-list
 * │ - Algorithm State title             │
 * │ - Keyboard Hints button             │
 * ├─────────────────────────────────────┤
 * │ #panel-steps-list (flex-[2])        │ ← TOP 2/3
 * │ Template-specific content:          │
 * │ - iterative-metrics: Dashboard      │
 * │ - recursive-context: Call Stack     │
 * ├─────────────────────────────────────┤
 * │ #panel-step-description (flex-[1])  │ ← BOTTOM 1/3
 * │ - Badge + Description               │
 * │ - ALWAYS PRESENT (both templates)   │
 * └─────────────────────────────────────┘
 */
const StatePanel = () => {
  // 1. Consume Contexts
  const { trace, currentAlgorithm } = useTrace();
  const { currentStepData, currentStep } = useNavigation();
  const { handleIntervalHover } = useVisualHighlight();
  const { openModal } = useKeyboardHintsModal();

  // 2. Determine Component and Template
  const StateComponent = getStateComponent(currentAlgorithm);
  const template = getAlgorithmTemplate(currentAlgorithm);
  const badge = getStepTypeBadge(currentStepData?.type);

  // 3. Template-specific content padding
  // iterative-metrics: NO padding (dashboard fills edge-to-edge, uses container queries)
  // recursive-context: px-6 py-4 (call stack needs breathing room + scrolling)
  const contentClasses = "flex-1 overflow-hidden"
  return (
    <div
      id="panel-steps"
      className="w-96 bg-slate-800 rounded-xl shadow-2xl flex flex-col overflow-hidden select-none border border-slate-700"
    >
      {/* ================================================================
          UNIFIED HEADER (OUTSIDE #panel-steps-list)
          - Algorithm State title
          - Keyboard Hints button
          - Same for ALL algorithms (both iterative and recursive)
          - CRITICAL: This must be OUTSIDE #panel-steps-list per static mockup
          ================================================================ */}
      <div className="flex justify-between px-5 pt-5 items-center mb-4 flex-shrink-0">
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
          Algorithm State
        </h2>
        <button
          onClick={openModal}
          className="bg-slate-700 hover:bg-slate-600 text-white p-2 rounded-full shadow-lg transition-all"
          title="Keyboard shortcuts"
          aria-label="Show keyboard shortcuts"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect width="20" height="16" x="2" y="4" rx="2" ry="2"></rect>
            <path d="M6 8h.001"></path>
            <path d="M10 8h.001"></path>
            <path d="M14 8h.001"></path>
            <path d="M18 8h.001"></path>
            <path d="M8 12h.001"></path>
            <path d="M12 12h.001"></path>
            <path d="M16 12h.001"></path>
            <path d="M7 16h10"></path>
          </svg>
        </button>
      </div>

      {/* ================================================================
          ALGORITHM CONTENT - TOP 2/3 (flex-[2])
          #panel-steps-list: REQUIRED HTML landmark ID for auto-scroll
          
          Template-specific padding applied via contentClasses:
          - iterative-metrics: Dashboard fills edge-to-edge (no padding)
                              Uses container queries for responsive scaling
          - recursive-context: Call stack with px-6 py-4 breathing room
                               Scrollable content with custom scrollbar
          ================================================================ */}
      <div
        id="panel-steps-list"
        className="flex-[2] flex flex-col overflow-hidden"
      >
        <div className={contentClasses}>
          <ErrorBoundary>
            <StateComponent
              step={currentStepData}
              trace={trace}
              currentStep={currentStep}
              onIntervalHover={handleIntervalHover}
            />
          </ErrorBoundary>
        </div>
      </div>

      {/* ================================================================
          UNIFIED FOOTER - BOTTOM 1/3 (flex-[1])
          #panel-step-description: REQUIRED HTML landmark ID
          
          CRITICAL CHANGE (Phase 0):
          - Footer now renders for BOTH templates (no conditional)
          - Previous version only showed for recursive-context
          - New iterative template ALSO uses this footer section
          
          Content:
          - Step type badge (colored, with emoji if present)
          - Step description text
          - Scrollable if description is long
          ================================================================ */}
      <div
        id="panel-step-description"
        className="flex-[1] border-t border-slate-700 py-2 px-4 bg-gradient-to-br from-slate-700/60 to-slate-800/60 overflow-hidden flex flex-col"
      >
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <p className="text-white text-base font-medium leading-relaxed">
            <span
              className={`inline-flex items-center gap-1.5 px-2 py-0.5 mr-2 rounded-md text-xs font-bold ${badge.color} align-middle`}
            >
              {badge.icon && <span>{badge.icon}</span>}
              {badge.label}
            </span>
            {currentStepData?.description || "No description available"}
          </p>
        </div>
      </div>
    </div>
  );
};

StatePanel.propTypes = {
  // No props needed - all data consumed via contexts:
  // - useTrace() for trace data and currentAlgorithm
  // - useNavigation() for currentStepData and currentStep
  // - useVisualHighlight() for handleIntervalHover
};

export default StatePanel;