import React from 'react';
import PropTypes from 'prop-types';
import { Loader } from 'lucide-react';
// Assuming react-markdown is installed for rendering markdown content.
import ReactMarkdown from 'react-markdown';

const AlgorithmInfoModal = ({ isOpen, onClose, title, children, isLoading }) => {
    if (!isOpen) return null;

    return (
        <div
            id="algorithm-info-modal"
            className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={onClose}
        >
            <div
                className="bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] flex flex-col"
                onClick={(e) => e.stopPropagation()}
            >
                <div className="flex justify-between items-center p-4 border-b border-slate-700 flex-shrink-0">
                    <h2 className="text-xl font-bold text-white">{title || 'Algorithm Details'}</h2>
                    <button
                        onClick={onClose}
                        className="text-slate-400 hover:text-white"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M6 18L18 6M6 6l12 12"
                            />
                        </svg>
                    </button>
                </div>
                <div className="p-6 overflow-y-auto flex-1">
                    {isLoading ? (
                        <div className="flex items-center justify-center h-full">
                            <Loader className="animate-spin text-blue-400" size={32} />
                        </div>
                    ) : (
                        <div className="prose prose-invert prose-sm max-w-none">
                            <ReactMarkdown
                                components={{
                                    code({node, inline, className, children, ...props}) {
                                        // FIX: Ensure code tags are always inline.
                                        return <code className="inline bg-slate-700 rounded-sm px-1 py-0.5 font-mono text-xs">{children}</code>
                                    }
                                }}
                            >
                                {children}
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
    title: PropTypes.string.isRequired,
    children: PropTypes.string.isRequired, // Content is now expected as a markdown string
    isLoading: PropTypes.bool,
};

export default AlgorithmInfoModal;