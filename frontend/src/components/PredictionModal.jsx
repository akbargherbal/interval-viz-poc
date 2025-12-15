import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';

const PredictionModal = ({
    predictionData,
    onAnswer,
    onSkip,
    isOpen = true // Default to true as parent conditionally renders
}) => {
    const [selectedChoiceId, setSelectedChoiceId] = useState(null);

    // Destructure data with safety checks
    const { question, choices = [] } = predictionData || {};

    // Map choices to include UI properties if missing
    const mappedChoices = choices.map((choice, index) => {
        // Default styling based on index
        const defaultColors = [
            'bg-blue-600 hover:bg-blue-500',
            'bg-purple-600 hover:bg-purple-500',
            'bg-emerald-600 hover:bg-emerald-500'
        ];
        
        // Default shortcuts
        const defaultShortcuts = ['k', 'c', 't']; // k=keep/1, c=cover/2, t=third

        return {
            ...choice,
            // Use provided ID or index as fallback
            id: choice.id || `choice-${index}`,
            // Use provided styling or default
            className: choice.className || defaultColors[index % defaultColors.length],
            // Use provided shortcut or default
            shortcut: choice.shortcut || defaultShortcuts[index % defaultShortcuts.length]
        };
    });

    const handleSubmit = useCallback(() => {
        if (selectedChoiceId) {
            onAnswer(selectedChoiceId);
        }
    }, [selectedChoiceId, onAnswer]);

    // Handle keyboard shortcuts locally
    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e) => {
            const key = e.key.toLowerCase();

            // Skip if typing in inputs
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            // Choice selection shortcuts
            mappedChoices.forEach(choice => {
                if (choice.shortcut && key === choice.shortcut.toLowerCase()) {
                    setSelectedChoiceId(choice.id);
                }
            });

            // Action shortcuts
            if (key === 'enter') {
                e.preventDefault();
                handleSubmit();
            } else if (key === 's' || key === 'escape') {
                e.preventDefault();
                onSkip();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, mappedChoices, handleSubmit, onSkip]);

    if (!isOpen) return null;

    return (
        <div
            id="prediction-modal"
            className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
            <div className="bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-w-lg w-full p-6 text-white">
                <h2 className="text-2xl font-bold mb-6">{question}</h2>

                <div className={`grid grid-cols-${Math.min(mappedChoices.length, 3)} gap-3 mb-6`}>
                    {mappedChoices.map((choice) => (
                        <button
                            key={choice.id}
                            onClick={() => setSelectedChoiceId(choice.id)}
                            className={`p-4 rounded-lg text-white font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-800
                                ${choice.className}
                                ${
                                    selectedChoiceId === choice.id
                                        ? 'scale-105 ring-2 ring-white shadow-xl z-10'
                                        : 'opacity-80 hover:opacity-100 hover:scale-[1.02]'
                                }
                                ${selectedChoiceId && selectedChoiceId !== choice.id ? 'opacity-40' : ''}
                            `}
                        >
                            <div className="text-base">{choice.label}</div>
                            {choice.shortcut && (
                                <div className="text-xs opacity-75 mt-1 uppercase">
                                    Press [{choice.shortcut}]
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
                        onClick={handleSubmit}
                        disabled={!selectedChoiceId}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded-md font-semibold disabled:bg-slate-600 disabled:cursor-not-allowed transition-colors"
                    >
                        Submit (Enter)
                    </button>
                </div>
            </div>
        </div>
    );
};

PredictionModal.propTypes = {
    predictionData: PropTypes.shape({
        question: PropTypes.string,
        choices: PropTypes.arrayOf(PropTypes.shape({
            id: PropTypes.string,
            label: PropTypes.string,
            className: PropTypes.string,
            shortcut: PropTypes.string,
        }))
    }),
    onAnswer: PropTypes.func.isRequired,
    onSkip: PropTypes.func.isRequired,
    isOpen: PropTypes.bool
};

export default PredictionModal;