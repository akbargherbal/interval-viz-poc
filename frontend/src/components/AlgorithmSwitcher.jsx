import React from "react";

/**
 * Algorithm switcher with registry support.
 * 
 * Phase 2: Now supports both:
 * 1. Registry-based algorithms (fetched from backend)
 * 2. Hardcoded algorithms (fallback if registry unavailable)
 * 
 * This allows for dynamic algorithm loading while maintaining
 * backward compatibility during transition period.
 */
const AlgorithmSwitcher = ({
  currentAlgorithm,
  availableAlgorithms = [], // From registry
  onLoadIntervalExample,
  onLoadBinarySearchExample,
}) => {
  // Fallback: Hardcoded algorithms if registry not available
  const hardcodedAlgorithms = [
    {
      name: "interval-coverage",
      display_name: "Interval Coverage",
      color: "blue",
      handler: onLoadIntervalExample,
    },
    {
      name: "binary-search",
      display_name: "Binary Search",
      color: "green",
      handler: onLoadBinarySearchExample,
    },
  ];

  // Map registry algorithms to button configs
  const registryButtons = availableAlgorithms.map((alg) => ({
    name: alg.name,
    display_name: alg.display_name,
    color: alg.name === "binary-search" ? "green" : "blue",
    handler:
      alg.name === "binary-search"
        ? onLoadBinarySearchExample
        : onLoadIntervalExample,
  }));

  // Use registry if available, otherwise use hardcoded
  const algorithmButtons =
    registryButtons.length > 0 ? registryButtons : hardcodedAlgorithms;

  const getButtonClasses = (algorithmName) => {
    const isActive = currentAlgorithm === algorithmName;
    const colorClasses = {
      blue: isActive
        ? "bg-blue-600 text-white"
        : "bg-gray-700 text-gray-300 hover:bg-gray-600",
      green: isActive
        ? "bg-green-600 text-white"
        : "bg-gray-700 text-gray-300 hover:bg-gray-600",
    };

    const color =
      algorithmButtons.find((alg) => alg.name === algorithmName)?.color ||
      "blue";

    return `px-4 py-2 rounded-lg text-sm font-medium transition-colors ${colorClasses[color]}`;
  };

  return (
    <div className="bg-gray-800 border-b border-gray-700 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4">
          <span className="text-gray-400 text-sm font-medium">
            {availableAlgorithms.length > 0
              ? "Select Algorithm:"
              : "Test Algorithm:"}
          </span>

          {algorithmButtons.map((alg) => (
            <button
              key={alg.name}
              onClick={alg.handler}
              className={getButtonClasses(alg.name)}
              title={
                availableAlgorithms.find((a) => a.name === alg.name)
                  ?.description || ""
              }
            >
              {alg.display_name}
            </button>
          ))}

          <div className="flex-1" />

          <div className="text-xs text-gray-500 flex items-center gap-2">
            <span>Current:</span>
            <span className="font-mono text-gray-400">{currentAlgorithm}</span>
            {availableAlgorithms.length > 0 && (
              <span className="ml-2 px-2 py-0.5 bg-green-900/30 text-green-400 rounded text-xs">
                Registry: {availableAlgorithms.length}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlgorithmSwitcher;