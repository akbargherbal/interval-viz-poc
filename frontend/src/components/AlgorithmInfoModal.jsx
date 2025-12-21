import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { Loader, X, Info } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useTrace } from "../contexts/TraceContext";
import { useKeyboardHandler } from "../contexts/KeyboardContext";

const AlgorithmInfoModal = ({ isOpen, onClose }) => {
  const { currentAlgorithm, trace } = useTrace();
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const title = trace?.metadata?.display_name || "Algorithm Details";

  useEffect(() => {
    if (isOpen && currentAlgorithm) {
      setIsLoading(true);
      fetch(`/algorithm-info/${currentAlgorithm}.md`)
        .then((res) => {
          if (!res.ok) throw new Error("Failed to load info");
          return res.text();
        })
        .then((text) => setContent(text))
        .catch((err) => {
          console.error(err);
          setContent("# Error\nFailed to load algorithm information.");
        })
        .finally(() => setIsLoading(false));
    }
  }, [isOpen, currentAlgorithm]);

  // Close on Escape (Priority 10)
  useKeyboardHandler((event) => {
    if (isOpen && event.key === "Escape") {
      onClose();
      return true;
    }
    return false;
  }, 10);

  if (!isOpen) return null;

  return (
    <div
      id="algorithm-info-modal"
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="flex max-h-[80vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border-2 border-slate-600 bg-slate-800 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex flex-shrink-0 items-center justify-between border-b border-slate-700 bg-slate-800/50 p-5">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-blue-500/20 p-2">
              <Info className="h-6 w-6 text-blue-400" />
            </div>
            <h2 className="text-xl font-bold text-white">{title}</h2>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 transition-colors hover:bg-slate-700 hover:text-white"
            aria-label="Close modal"
          >
            <X size={24} />
          </button>
        </div>

        <div className="custom-scrollbar flex-1 overflow-y-auto p-6">
          {isLoading ? (
            <div className="flex h-40 flex-col items-center justify-center gap-3">
              <Loader className="animate-spin text-blue-400" size={32} />
              <p className="text-sm text-slate-400">Loading documentation...</p>
            </div>
          ) : (
            <div className="prose prose-invert prose-sm max-w-none">
              <ReactMarkdown
                components={{
                  code({ node, inline, className, children, ...props }) {
                    return (
                      <code className="inline rounded-sm bg-slate-700 px-1 py-0.5 font-mono text-xs text-blue-200">
                        {children}
                      </code>
                    );
                  },
                  h1: ({ children }) => (
                    <h1 className="mb-4 border-b border-slate-700 pb-2 text-2xl font-bold text-white">
                      {children}
                    </h1>
                  ),
                  h2: ({ children }) => (
                    <h2 className="mb-3 mt-6 flex items-center gap-2 text-lg font-bold text-white">
                      {children}
                    </h2>
                  ),
                  p: ({ children }) => (
                    <p className="mb-4 leading-relaxed text-slate-300">
                      {children}
                    </p>
                  ),
                  ul: ({ children }) => (
                    <ul className="mb-4 list-inside list-disc space-y-1 text-slate-300">
                      {children}
                    </ul>
                  ),
                  li: ({ children }) => <li className="ml-2">{children}</li>,
                }}
              >
                {content}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

AlgorithmInfoModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default AlgorithmInfoModal;
