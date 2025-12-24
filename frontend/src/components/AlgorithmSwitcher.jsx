import React, { useState, useRef, useEffect } from "react";
import { Search, ChevronDown } from "lucide-react";
import { useTrace } from "../contexts/TraceContext";
import { useKeyboardHandler } from "../contexts/KeyboardContext";

const AlgorithmSwitcher = () => {
  const {
    currentAlgorithm,
    availableAlgorithms,
    switchAlgorithm: onAlgorithmSwitch,
    loading,
  } = useTrace();

  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Get display name for current algorithm
  const currentAlgorithmDisplay =
    availableAlgorithms.find((alg) => alg.name === currentAlgorithm)
      ?.display_name || currentAlgorithm;

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  // Close dropdown on Escape key (Priority 5)
  useKeyboardHandler((event) => {
    if (isOpen && event.key === "Escape") {
      setIsOpen(false);
      return true; // Consume event
    }
    return false;
  }, 5);

  const handleAlgorithmSelect = (algorithmName) => {
    if (algorithmName !== currentAlgorithm && !loading) {
      onAlgorithmSwitch(algorithmName);
      setIsOpen(false);
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        onClick={() => !loading && setIsOpen(!isOpen)}
        disabled={loading}
        className="group flex items-center gap-2 rounded-lg bg-slate-700 px-3 py-1.5 transition-colors hover:bg-slate-600 disabled:cursor-not-allowed disabled:bg-slate-800"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        {/* Algorithm Icon */}
        <Search className="h-4 w-4 text-blue-400" />

        {/* Algorithm Name */}
        <span className="text-sm font-medium text-white">
          {currentAlgorithmDisplay}
        </span>

        {/* Dropdown Arrow */}
        <ChevronDown
          className={`h-4 w-4 text-slate-400 transition-all group-hover:text-white ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          className="animate-in fade-in slide-in-from-top-2 absolute left-0 top-full z-50 mt-2 w-64 rounded-lg border border-slate-600 bg-slate-700 shadow-xl duration-100"
          role="menu"
        >
          <div className="p-2">
            {/* Header */}
            <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
              Select Algorithm
            </div>

            {/* Algorithm List */}
            {availableAlgorithms.length === 0 ? (
              <div className="px-3 py-2 text-sm text-slate-400">
                No algorithms available
              </div>
            ) : (
              <div className="space-y-1">
                {availableAlgorithms.map((algorithm) => {
                  const isCurrent = algorithm.name === currentAlgorithm;
                  return (
                    <button
                      key={algorithm.name}
                      onClick={() => handleAlgorithmSelect(algorithm.name)}
                      disabled={isCurrent}
                      className={`w-full rounded-md px-3 py-2 text-left text-sm font-medium transition-colors ${
                        isCurrent
                          ? "cursor-default bg-blue-600 text-white"
                          : "text-slate-200 hover:bg-slate-600"
                      }`}
                      role="menuitem"
                    >
                      <div className="flex items-center gap-2">
                        <Search className="h-4 w-4 flex-shrink-0" />
                        <div className="min-w-0 flex-1">
                          <div className="truncate">
                            {algorithm.display_name}
                          </div>
                          {algorithm.description && (
                            <div className="mt-0.5 truncate text-xs text-slate-400">
                              {algorithm.description}
                            </div>
                          )}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AlgorithmSwitcher;
