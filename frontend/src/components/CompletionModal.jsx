import React from "react";
import { RotateCcw } from "lucide-react";
import { getAccuracyFeedback } from "../utils/predictionUtils";
import { getIntervalColor } from "../constants/intervalColors";
import { useTrace } from "../contexts/TraceContext";

/**
 * Get outcome-driven modal theme based on algorithm result
 */
const getOutcomeTheme = (trace) => {
  const result = trace?.result || {};
  const algorithm = trace?.metadata?.algorithm || "unknown";

  if (algorithm === "binary-search") {
    if (result.found === true) {
      return {
        border: "border-emerald-500",
        icon: "bg-emerald-500",
        iconPath: "M5 13l4 4L19 7",
        title: "Target Found!",
        subtitle: "Binary search completed successfully.",
      };
    } else if (result.found === false) {
      return {
        border: "border-red-500",
        icon: "bg-red-500",
        iconPath: "M6 18L18 6M6 6l12 12",
        title: "Target Not Found",
        subtitle: "Binary search completed.",
      };
    }
  }

  return {
    border: "border-blue-500",
    icon: "bg-blue-500",
    iconPath: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
    title: "Algorithm Complete!",
    subtitle:
      algorithm === "interval-coverage"
        ? "Interval coverage finished."
        : "Execution finished.",
  };
};

const CompletionModal = ({
  isOpen,
  step,
  onReset,
  onClose,
  predictionStats,
}) => {
  const { trace } = useTrace();

  console.log("CompletionModal re-rendered", { isOpen });

  if (!isOpen) {
    return null;
  }

  const theme = getOutcomeTheme(trace);
  const algorithm = trace?.metadata?.algorithm || "unknown";
  const isIntervalCoverage = algorithm === "interval-coverage";
  const isBinarySearch = algorithm === "binary-search";

  const accuracy =
    predictionStats?.total > 0
      ? Math.round((predictionStats.correct / predictionStats.total) * 100)
      : null;
  const feedback = accuracy !== null ? getAccuracyFeedback(accuracy) : null;

  const renderAlgorithmResults = () => {
    if (isIntervalCoverage) {
      return renderIntervalCoverageResults();
    } else if (isBinarySearch) {
      return renderBinarySearchResults();
    } else {
      return renderGenericResults();
    }
  };

  const renderIntervalCoverageResults = () => {
    const inputSize = trace?.metadata?.input_size || 0;
    const keptCount = step?.data?.kept_count || 0;
    const removedCount = step?.data?.removed_count || 0;
    const result = step?.data?.result || [];

    return (
      <>
        <div className="mb-3 rounded-lg bg-slate-900/50 p-3">
          <div className="grid grid-cols-3 gap-2 text-center">
            <div>
              <div className="text-xs uppercase tracking-wide text-slate-400">
                Initial
              </div>
              <div className="text-xl font-bold text-white">{inputSize}</div>
            </div>
            <div className="border-l border-slate-700">
              <div className="text-xs uppercase tracking-wide text-slate-400">
                Kept
              </div>
              <div className="text-xl font-bold text-emerald-400">
                {keptCount}
              </div>
            </div>
            <div className="border-l border-slate-700">
              <div className="text-xs uppercase tracking-wide text-slate-400">
                Removed
              </div>
              <div className="text-xl font-bold text-red-400">
                {removedCount}
              </div>
            </div>
          </div>
        </div>
        <div className="mb-4 rounded-lg bg-slate-900/50 p-3">
          <div className="mb-2 flex items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-wide text-slate-300">
              Final Result:
            </span>
          </div>
          {result.length === 0 ? (
            <div className="py-2 text-center text-xs italic text-slate-500">
              No intervals remaining
            </div>
          ) : (
            <div className="flex flex-wrap gap-1.5">
              {result.slice(0, 7).map((interval, idx) => {
                if (
                  !interval ||
                  typeof interval.start !== "number" ||
                  typeof interval.end !== "number"
                )
                  return null;
                const colors = getIntervalColor(interval.color);
                return (
                  <div
                    key={interval.id || idx}
                    className={`${colors.bg} ${colors.text} whitespace-nowrap rounded px-1.5 py-0.5 text-xs font-bold`}
                  >
                    ({interval.start}, {interval.end})
                  </div>
                );
              })}
              {result.length > 7 && (
                <div className="rounded bg-gray-500 px-1.5 py-0.5 text-xs font-bold text-white">
                  +{result.length - 7} more
                </div>
              )}
            </div>
          )}
        </div>
      </>
    );
  };

  const renderBinarySearchResults = () => {
    const result = trace?.result || {};
    const comparisons = result.comparisons || 0;
    const arraySize = trace?.metadata?.input_size || 0;

    return (
      <div className="mb-3 rounded-lg bg-slate-900/50 p-3">
        <div className="grid grid-cols-3 gap-2 text-center">
          <div>
            <div className="text-xs uppercase tracking-wide text-slate-400">
              Array Size
            </div>
            <div className="text-xl font-bold text-white">{arraySize}</div>
          </div>
          <div className="border-l border-slate-700">
            <div className="text-xs uppercase tracking-wide text-slate-400">
              Comparisons
            </div>
            <div className="text-xl font-bold text-blue-400">{comparisons}</div>
          </div>
          <div className="border-l border-slate-700">
            <div className="text-xs uppercase tracking-wide text-slate-400">
              Result
            </div>
            <div
              className={`text-xl font-bold ${result.found ? "text-emerald-400" : "text-red-400"}`}
            >
              {result.found ? "✓ Found" : "✗ Missing"}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderGenericResults = () => (
    <div className="mb-3 rounded-lg bg-slate-900/50 p-3">
      <div className="py-2 text-center text-sm text-slate-300">
        Execution finished successfully.
      </div>
    </div>
  );

  return (
    <div
      className={`fixed inset-0 z-50 flex select-none items-center justify-center bg-black/70 p-4 backdrop-blur-sm transition-opacity duration-500 ${isOpen ? "opacity-100" : "opacity-0"}`}
    >
      <div
        className={`rounded-2xl border-2 bg-slate-800 shadow-2xl ${theme.border} w-full max-w-lg p-5 transition-all duration-500 ${isOpen ? "scale-100 opacity-100" : "scale-95 opacity-0"}`}
      >
        <div className="mb-4 flex items-center gap-4">
          <div
            className={`inline-flex h-12 w-12 flex-shrink-0 items-center justify-center ${theme.icon} rounded-full`}
          >
            <svg
              className="h-7 w-7 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d={theme.iconPath}
              />
            </svg>
          </div>
          <div>
            <h2 className="text-2xl font-bold leading-tight text-white">
              {theme.title}
            </h2>
            <p className="text-sm text-slate-400">{theme.subtitle}</p>
          </div>
        </div>
        {renderAlgorithmResults()}
        {predictionStats?.total > 0 && (
          <div className="mb-4 flex items-center justify-between rounded-lg border border-blue-500/30 bg-slate-900/50 p-3">
            <div>
              <h3 className="text-sm font-bold text-white">
                Prediction Accuracy
              </h3>
              <div
                className={`mt-0.5 text-xs ${feedback.color === "emerald" ? "text-emerald-300" : feedback.color === "amber" ? "text-amber-300" : "text-red-300"}`}
              >
                {feedback.message}
              </div>
            </div>
            <div className="text-right">
              <div
                className={`text-2xl font-bold leading-none ${feedback.color === "emerald" ? "text-emerald-400" : feedback.color === "amber" ? "text-amber-400" : "text-red-400"}`}
              >
                {accuracy}%
              </div>
              <div className="text-xs text-slate-400">
                ({predictionStats.correct}/{predictionStats.total})
              </div>
            </div>
          </div>
        )}
        {predictionStats?.total === 0 && (
          <div className="mb-2 py-2 text-center text-xs italic text-slate-500">
            Prediction mode was not used.
          </div>
        )}
        <div className="grid grid-cols-2 gap-3 border-t border-slate-700 pt-3">
          <button
            onClick={onClose}
            className="rounded-lg bg-slate-600 px-4 py-2 font-semibold text-white transition-colors hover:bg-slate-500"
          >
            Close
          </button>
          <button
            onClick={onReset}
            className="flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 font-bold text-white transition-colors hover:bg-blue-500"
          >
            <RotateCcw size={16} />
            Start Over
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompletionModal;
