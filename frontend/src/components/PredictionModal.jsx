import React from 'react';
import PropTypes from 'prop-types';

const PredictionModal = ({
    isOpen,
    question,
    choices,
    onSelect,
    onSkip,
    selectedChoice,
    onSubmit,
}) => {
    if (!isOpen) return null;

    return (
        <div
            id="prediction-modal"
            className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
            <div className="bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-w-lg w-full p-6 text-white">
                <h2 className="text-2xl font-bold mb-6">{question}</h2>

                <div className={`grid grid-cols-${choices.length} gap-3 mb-6`}>
                    {choices.map((choice) => (
                        <button
                            key={choice.id}
                            onClick={() => onSelect(choice.id)}
                            className={`p-4 rounded-lg text-white font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-800
                                ${choice.className}
                                ${
                                    selectedChoice === choice.id
                                        ? 'scale-105 ring-2 ring-blue-400 shadow-xl'
                                        : 'opacity-60 hover:opacity-100'
                                }
                                ${selectedChoice && selectedChoice !== choice.id ? 'opacity-40' : ''}
                            `}
                        >
                            <div className="text-base">{choice.label}</div>
                            {choice.shortcut && (
                                <div className="text-xs opacity-75 mt-1">
                                    Press [{choice.shortcut.toUpperCase()}]
                                </div>
                            )}
                        </button>
                    ))}
                </div>

                <div className="flex justify-between items-center pt-4 border-t border-slate-700">
                    <button
                        onClick={onSkip}
                        className="text-sm text-slate-400 hover:text-white transition-colors"
                    >
                        Skip Question (S)
                    </button>
                    <button
                        onClick={onSubmit}
                        disabled={!selectedChoice}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded-md font-semibold disabled:bg-slate-600 disabled:cursor-not-allowed"
                    >
                        Submit (Enter)
                    </button>
                </div>
            </div>
        </div>
    );
};

PredictionModal.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    question: PropTypes.string.isRequired,
    choices: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            className: PropTypes.string.isRequired,
            shortcut: PropTypes.string,
        })
    ).isRequired,
    onSelect: PropTypes.func.isRequired,
    onSkip: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
    selectedChoice: PropTypes.string,
};

export default PredictionModal;
