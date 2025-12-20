/**
 * State Component Registry
 *
 * Maps algorithm names to their corresponding state components (RIGHT panel).
 * Mirrors the pattern from visualizationRegistry.js but for algorithm-specific state displays.
 *
 * Phase 5: Updated imports to use algorithm-states directory.
 * Bug Fix (Dec 19, 2025): Added template metadata to support conditional footer rendering.
 */
import BinarySearchState from "../components/algorithm-states/BinarySearchState";
import IntervalCoverageState from "../components/algorithm-states/IntervalCoverageState";
import SlidingWindowState from "../components/algorithm-states/SlidingWindowState";
import TwoPointerState from "../components/algorithm-states/TwoPointerState";
import MergeSortState from "../components/algorithm-states/MergeSortState";

/**
 * Fallback component for algorithms without a registered state component
 */
const DefaultStateComponent = ({ step }) => {
  return (
    <div className="text-slate-400 text-sm">
      <p className="mb-2">Algorithm state display not configured.</p>
      <p className="text-xs">
        Algorithm: {step?.metadata?.algorithm || "unknown"}
      </p>
    </div>
  );
};

/**
 * Registry mapping algorithm names to state components with metadata
 *
 * @typedef {Object} AlgorithmConfig
 * @property {React.Component} component - The state component to render
 * @property {string} template - Template type: 'iterative-metrics' | 'recursive-context'
 */
const STATE_REGISTRY = {
  "binary-search": {
    component: BinarySearchState,
    template: "recursive-context", // FIXED: Binary Search uses traditional layout
  },
  "interval-coverage": {
    component: IntervalCoverageState,
    template: "recursive-context",
  },
  "sliding-window": {
    component: SlidingWindowState,
    template: "iterative-metrics",
  },
  "two-pointer": {
    component: TwoPointerState,
    template: "iterative-metrics",
  },
  "merge-sort": {
    component: MergeSortState,
    template: "recursive-context",
  },
};

/**
 * Get the state component for a given algorithm
 *
 * @param {string} algorithmName - The algorithm identifier (e.g., 'binary-search')
 * @returns {React.Component} The state component for this algorithm, or DefaultStateComponent
 *
 * @example
 * const StateComponent = getStateComponent('binary-search');
 * <StateComponent step={step} trace={trace} />
 */
export const getStateComponent = (algorithmName) => {
  if (!algorithmName) {
    console.warn("getStateComponent called with null/undefined algorithmName");
    return DefaultStateComponent;
  }

  const config = STATE_REGISTRY[algorithmName];
  if (!config) {
    console.warn(
      `No state component registered for algorithm: ${algorithmName}`
    );
    return DefaultStateComponent;
  }

  return config.component;
};

/**
 * Get the template type for a given algorithm
 *
 * @param {string} algorithmName - The algorithm identifier
 * @returns {string} Template type ('iterative-metrics' | 'recursive-context')
 *
 * @example
 * const template = getAlgorithmTemplate('binary-search');
 * // Returns: 'recursive-context'
 */
export const getAlgorithmTemplate = (algorithmName) => {
  if (!algorithmName) {
    return "recursive-context"; // Default fallback
  }

  const config = STATE_REGISTRY[algorithmName];
  return config?.template || "recursive-context";
};

/**
 * Check if an algorithm has a registered state component
 *
 * @param {string} algorithmName - The algorithm identifier
 * @returns {boolean} True if a state component is registered
 */
export const isStateComponentRegistered = (algorithmName) => {
  return algorithmName && algorithmName in STATE_REGISTRY;
};

/**
 * Get list of all algorithms with registered state components
 *
 * @returns {string[]} Array of algorithm names
 */
export const getRegisteredAlgorithms = () => {
  return Object.keys(STATE_REGISTRY);
};
