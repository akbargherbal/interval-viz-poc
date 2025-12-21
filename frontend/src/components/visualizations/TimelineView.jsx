import React from "react";
import PropTypes from "prop-types";
import { getIntervalColor } from "../../constants/intervalColors";

// EXTRACTED CONSTANTS (Phase 3.2)
const TIMELINE_CONFIG = {
  MIN_VAL: 500,
  MAX_VAL: 1000,
  // Helper to convert value to percentage (0-100)
  toPercent: (val) => ((val - 500) / (1000 - 500)) * 100,
};

/**
 * TimelineView - Interval Coverage Visualization
 *
 * Refactored Phase 3:
 * - Removed magic numbers (4, 0.92, 48)
 * - Used CSS variables for padding
 * - Used Flexbox for vertical stacking (removed absolute top calculation)
 * - Extracted static configuration
 */
const TimelineView = ({ step, highlightedIntervalId, onIntervalHover }) => {
  const allIntervals =
    step?.data?.visualization?.all_intervals || step?.data?.all_intervals || [];
  const maxEnd = step?.data?.visualization?.max_end ?? step?.data?.max_end;

  const hasHighlight = highlightedIntervalId !== null;

  return (
    <div className="relative flex h-full flex-col pb-4">
      {/* Timeline Container */}
      <div
        className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden rounded-lg bg-slate-900/50"
        style={{
          paddingLeft: "var(--timeline-padding-x)",
          paddingRight: "var(--timeline-padding-x)",
          paddingTop: "2rem", // top-4
          paddingBottom: "2rem", // bottom-8 space for axis
        }}
      >
        {/* Axis Line (Bottom) */}
        <div className="absolute bottom-6 left-0 right-0 mx-[var(--timeline-padding-x)] h-0.5 bg-slate-600"></div>

        {/* Axis Labels */}
        <div className="absolute bottom-1 left-[var(--timeline-padding-x)] -translate-x-1/2 transform text-xs text-slate-400">
          {TIMELINE_CONFIG.MIN_VAL}
        </div>
        <div className="absolute bottom-1 left-1/2 -translate-x-1/2 transform text-xs text-slate-400">
          750
        </div>
        <div className="absolute bottom-1 right-[var(--timeline-padding-x)] translate-x-1/2 transform text-xs text-slate-400">
          {TIMELINE_CONFIG.MAX_VAL}
        </div>

        {/* Max End Line */}
        {maxEnd !== undefined && maxEnd !== null && (
          <div
            className="absolute bottom-6 top-4 z-10 w-0.5 bg-cyan-400 transition-all duration-300"
            style={{ left: `${TIMELINE_CONFIG.toPercent(maxEnd)}%` }}
          >
            <div className="absolute -left-10 -top-3 whitespace-nowrap rounded bg-teal-400 px-2 py-1 text-xs font-bold text-black drop-shadow-sm">
              max_end: {maxEnd}
            </div>
          </div>
        )}

        {/* Intervals Stack (Flex Column) */}
        <div className="relative z-0 flex w-full flex-col gap-[var(--timeline-row-gap)]">
          {allIntervals.map((interval, idx) => {
            if (
              !interval ||
              typeof interval.start !== "number" ||
              typeof interval.end !== "number"
            ) {
              return null;
            }

            const left = TIMELINE_CONFIG.toPercent(interval.start);
            const width = TIMELINE_CONFIG.toPercent(interval.end) - left;
            const colors = getIntervalColor(interval.color);

            const state = interval.state || "active";
            const isExamining = state === "examining";
            const isCovered = state === "covered";
            const isKept = state === "kept";

            const isHighlighted = interval.id === highlightedIntervalId;
            const isDimmed = hasHighlight && !isHighlighted;

            let additionalClasses = "transition-all duration-300";

            if (isHighlighted) {
              additionalClasses +=
                " ring-2 ring-yellow-400 z-30 shadow-[0_0_12px_4px_rgba(250,204,21,0.3)]";
            } else if (isDimmed) {
              additionalClasses += " opacity-40";
            } else if (isExamining) {
              additionalClasses +=
                " border-4 border-yellow-300 scale-105 shadow-[0_0_15px_5px_rgba(234,179,8,0.6)] z-20";
            }

            if (isCovered) {
              additionalClasses +=
                " opacity-30 grayscale line-through bg-gray-800/50";
            }

            if (isKept && !isHighlighted) {
              additionalClasses += " shadow-lg shadow-emerald-500/50";
            }

            return (
              <div
                key={interval.id || idx}
                className="relative h-10 w-full flex-shrink-0"
              >
                <div
                  className={`absolute h-full ${colors.bg} rounded border-2 ${colors.border} flex items-center justify-center text-sm font-bold text-white ${additionalClasses}`}
                  style={{
                    left: `${left}%`,
                    width: `${width}%`,
                  }}
                  onMouseEnter={() => onIntervalHover?.(interval.id)}
                  onMouseLeave={() => onIntervalHover?.(null)}
                >
                  {interval.start}-{interval.end}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-4 flex flex-wrap items-center justify-center gap-4 text-xs">
        <div className="flex items-center gap-2">
          <div className="h-3 w-8 rounded bg-cyan-400"></div>
          <span className="text-slate-400">max_end line</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-8 rounded bg-yellow-400 ring-2 ring-yellow-400"></div>
          <span className="text-slate-400">highlighted</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-8 rounded border-2 border-yellow-300 bg-yellow-400"></div>
          <span className="text-slate-400">examining</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-3 w-8 rounded bg-slate-500 line-through opacity-30 grayscale"></div>
          <span className="text-slate-400">covered (skipped)</span>
        </div>
      </div>
    </div>
  );
};

TimelineView.propTypes = {
  step: PropTypes.shape({
    data: PropTypes.shape({
      all_intervals: PropTypes.arrayOf(PropTypes.object),
      max_end: PropTypes.number,
      visualization: PropTypes.shape({
        all_intervals: PropTypes.arrayOf(PropTypes.object),
        max_end: PropTypes.number,
      }),
    }),
  }),
  highlightedIntervalId: PropTypes.number,
  onIntervalHover: PropTypes.func.isRequired,
};

export default React.memo(TimelineView);
