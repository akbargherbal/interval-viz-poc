// frontend/src/components/algorithm-states/SlidingWindowState.jsx

import React, { useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * SlidingWindowState - Iterative Metrics Template
 *
 * RHP Layout:
 * - Top 2/3: Metrics (Current Sum, Max Sum, Window Tracking)
 * - Bottom 1/3: Narrative
 *
 * Optimization:
 * - Compact vertical layout to prevent scrolling
 * - Highlights "New Max" updates
 * - Tracks "Best Window" indices
 */
const SlidingWindowState = ({ step, trace }) => {
  // Effect to hide the parent StatePanel's default description footer
  useEffect(() => {
    const parentFooter = document.getElementById('panel-step-description');
    if (parentFooter) {
      parentFooter.style.display = 'none';
    }
    return () => {
      if (parentFooter) parentFooter.style.display = '';
    };
  }, []);

  // Early return
  if (!step?.data?.visualization) {
    return <div className="text-slate-400 text-sm p-4">No state data available</div>;
  }

  const viz = step.data.visualization;
  const metrics = viz.metrics || {};
  const pointers = viz.pointers || {};

  // Data Extraction
  const currentSum = metrics.current_sum ?? '-';
  const maxSum = metrics.max_sum ?? '-';
  const k = metrics.k ?? '-';

  // Window Indices
  const currStart = pointers.window_start ?? '-';
  const currEnd = pointers.window_end ?? '-';

  // Best Window Calculation (derived)
  const bestStart = metrics.max_window_start ?? '-';
  let bestEnd = '-';
  if (bestStart !== '-' && k !== '-') {
    bestEnd = bestStart + k - 1;
  }

  // "New Max" Detection
  // We assume if current == max (and max > 0), it might be a new max.
  // Without previous step data, this is a best-effort visual cue.
  const isMax = currentSum !== '-' && maxSum !== '-' && currentSum === maxSum;

  // Step Type Coloring
  const getStepColor = (type) => {
    const t = type?.toUpperCase() || '';
    if (t.includes('MAX') || t.includes('UPDATE')) return 'bg-emerald-900/30 text-emerald-200 border-emerald-800';
    if (t.includes('SLIDE') || t.includes('MOVE')) return 'bg-blue-900/30 text-blue-200 border-blue-800';
    return 'bg-slate-700/20 text-slate-200 border-slate-700';
  };

  const stepType = step.type || 'STEP';
  const stepColorClass = getStepColor(stepType);

  return (
    <div className="h-full flex flex-col bg-slate-800">
      {/* ==========================================
          SECTION 1: Metrics (Top 2/3)
          ========================================== */}
      <div className="flex-[2] flex flex-col p-4 overflow-hidden relative border-b border-slate-700">

        {/* Row 1: Primary Metrics (Scoreboard) */}
        <div className="grid grid-cols-2 gap-3 mb-3 flex-1">
          {/* Current Sum */}
          <div className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-2 flex flex-col items-center justify-center relative">
            <span className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-1">
              Current Sum
            </span>
            <span className="text-cyan-300 text-4xl font-mono font-bold tracking-tighter drop-shadow-lg">
              {currentSum}
            </span>
            <div className="absolute top-2 right-2 text-[9px] text-slate-500 font-mono">
              k={k}
            </div>
          </div>

          {/* Max Sum */}
          <div className={`border rounded-lg p-2 flex flex-col items-center justify-center transition-colors duration-300 ${
            isMax
              ? 'bg-emerald-900/20 border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.1)]'
              : 'bg-slate-700/30 border-slate-600/50'
          }`}>
            <span className={`text-[10px] font-bold uppercase tracking-widest mb-1 ${
              isMax ? 'text-emerald-400' : 'text-slate-400'
            }`}>
              Max Sum
            </span>
            <span className="text-emerald-400 text-4xl font-mono font-bold tracking-tighter drop-shadow-lg">
              {maxSum}
            </span>
            {isMax && (
              <div className="absolute top-2 right-2">
                <span className="flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Row 2: Window Tracking (Compact Strip) */}
        <div className="bg-slate-900/40 rounded-lg border border-slate-700/50 p-2 mt-auto shrink-0">
          <div className="grid grid-cols-2 divide-x divide-slate-700/50">

            {/* Current Window */}
            <div className="px-3 flex flex-col items-center justify-center">
              <div className="text-[9px] text-slate-500 font-semibold uppercase mb-1">
                Current Window
              </div>
              <div className="flex items-center gap-2 font-mono text-sm font-bold text-slate-300">
                <span className="bg-slate-700 px-1.5 rounded text-blue-300">[{currStart}]</span>
                <span className="text-slate-600">to</span>
                <span className="bg-slate-700 px-1.5 rounded text-blue-300">[{currEnd}]</span>
              </div>
            </div>

            {/* Best Window */}
            <div className="px-3 flex flex-col items-center justify-center">
              <div className="text-[9px] text-slate-500 font-semibold uppercase mb-1">
                Best Window Found
              </div>
              <div className="flex items-center gap-2 font-mono text-sm font-bold text-slate-300">
                <span className="bg-slate-700 px-1.5 rounded text-emerald-300">[{bestStart}]</span>
                <span className="text-slate-600">to</span>
                <span className="bg-slate-700 px-1.5 rounded text-emerald-300">[{bestEnd}]</span>
              </div>
            </div>

          </div>
        </div>
      </div>

      {/* ==========================================
          SECTION 2: Narrative (Bottom 1/3)
          ========================================== */}
      <div className="flex-1 flex min-h-0">
        {/* Step Name */}
        <div className={`w-28 border-r flex items-center justify-center p-3 text-center shrink-0 ${stepColorClass}`}>
          <span className="text-xs font-bold leading-tight drop-shadow-md uppercase">
            {stepType.replace(/_/g, ' ')}
          </span>
        </div>

        {/* Description */}
        <div className="flex-1 p-4 flex items-center bg-slate-800 overflow-y-auto">
          <p className="text-slate-300 text-sm font-medium leading-relaxed">
            {step.description}
          </p>
        </div>
      </div>
    </div>
  );
};

SlidingWindowState.propTypes = {
  step: PropTypes.shape({
    type: PropTypes.string,
    description: PropTypes.string,
    data: PropTypes.shape({
      visualization: PropTypes.shape({
        metrics: PropTypes.object,
        pointers: PropTypes.object,
      }),
    }),
  }).isRequired,
  trace: PropTypes.object,
};

export default SlidingWindowState;