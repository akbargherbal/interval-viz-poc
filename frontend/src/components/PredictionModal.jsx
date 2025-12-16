import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';

const PredictionModal = ({
    predictionData,
    onAnswer,
    onSkip,
    isOpen = true
}) => {
    const [selectedChoiceId, setSelectedChoiceId] = useState(null);

    // Destructure data with safety checks
    const { question, choices = [], hint } = predictionData || {};

    // Map choices to include UI properties if missing
    const mappedChoices = choices.map((choice, index) => {
        // Default styling based on index if no specific class provided
        // We try to infer semantic meaning from labels if possible, otherwise cycle colors
        let colorClass = 'bg-slate-600 hover:bg-slate-500'; // Fallback
        
        const labelLower = (choice.label || '').toLowerCase();
        const idLower = (choice.id || '').toLowerCase();
        
        // Semantic color mapping based on mockup guidelines
        if (labelLower.includes('found') || labelLower.includes('keep') || labelLower.includes('yes') || idLower === 'found') {
            colorClass = 'bg-emerald-600 hover:bg-emerald-500';
        } else if (labelLower.includes('covered') || labelLower.includes('discard') || labelLower.includes('no') || idLower.includes('covered')) {
            colorClass = 'bg-orange-600 hover:bg-orange-500';
        } else if (labelLower.includes('left') || labelLower.includes('back') || labelLower.includes('prev')) {
            colorClass = 'bg-blue-600 hover:bg-blue-500';
        } else if (labelLower.includes('right') || labelLower.includes('next')) {
            colorClass = 'bg-red-600 hover:bg-red-500';
        } else {
            // Fallback cycle for generic choices
            const defaultColors = [
                'bg-blue-600 hover:bg-blue-500',
                'bg-purple-600 hover:bg-purple-500',
                'bg-emerald-600 hover:bg-emerald-500'
            ];
            colorClass = defaultColors[index % defaultColors.length];
        }
        
        // Default shortcuts
        const defaultShortcuts = ['1', '2', '3']; 

        return {
            ...choice,
            id: choice.id || `choice-${index}`,
            className: choice.className || colorClass,
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
                // Check explicit shortcut or numeric fallback
                if (
                    (choice.shortcut && key === choice.shortcut.toLowerCase()) ||
                    (key === (mappedChoices.indexOf(choice) + 1).toString())
                ) {
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
            {/* LOCKED: max-w-lg (512px), p-6, NO height constraint */}
            <div className="bg-slate-800 border-2 border-slate-600 rounded-2xl shadow-2xl max-w-lg w-full p-6 text-white select-none">
                
                {/* Header Section */}
                <div className="mb-6">
                    <h2 className="text-2xl font-bold text-white mb-2 leading-tight">{question}</h2>
                    {/* Optional: Could add step info here if passed via props */}
                </div>

                {/* Hint Box (Visual Standard) */}
                {hint && (
                    <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-4 mb-6">
                        <p className="text-blue-300 text-sm">
                            💡 <strong>Hint:</strong> {hint}
                        </p>
                    </div>
                )}

                {/* Choices Grid */}
                <div className={`grid ${mappedChoices.length > 2 ? 'grid-cols-3' : 'grid-cols-2'} gap-3 mb-6`}>
                    {mappedChoices.map((choice) => {
                        const isSelected = selectedChoiceId === choice.id;
                        const isOthersSelected = selectedChoiceId && !isSelected;
                        
                        // Extract base color for ring (simplified logic)
                        let ringColor = 'ring-blue-400';
                        if (choice.className.includes('emerald')) ringColor = 'ring-emerald-400';
                        else if (choice.className.includes('orange')) ringColor = 'ring-orange-400';
                        else if (choice.className.includes('red')) ringColor = 'ring-red-400';
                        else if (choice.className.includes('purple')) ringColor = 'ring-purple-400';

                        return (
                            <button
                                key={choice.id}
                                onClick={() => setSelectedChoiceId(choice.id)}
                                className={`
                                    py-4 px-3 rounded-lg text-white font-semibold transition-all duration-200 
                                    flex flex-col items-center justify-center text-center
                                    focus:outline-none
                                    ${choice.className}
                                    ${isSelected 
                                        ? `scale-105 ring-2 ${ringColor} shadow-xl z-10` 
                                        : 'hover:scale-105 shadow-lg'
                                    }
                                    ${isOthersSelected ? 'opacity-60' : 'opacity-100'}
                                `}
                            >
                                <div className="text-sm mb-1">{choice.label}</div>
                                <div className="text-xs opacity-75 uppercase font-mono">
                                    Press {choice.shortcut}
                                </div>
                            </button>
                        );
                    })}
                </div>

                {/* Actions - Two-Step Confirmation */}
                <div className="flex justify-between items-center pt-4 border-t border-slate-700">
                    <button
                        onClick={onSkip}
                        className="text-slate-400 hover:text-slate-300 text-sm transition-colors"
                    >
                        Skip (Press S)
                    </button>
                    <button
                        onClick={handleSubmit}
                        disabled={!selectedChoiceId}
                        className={`
                            px-6 py-2 rounded-lg font-semibold transition-all shadow-lg
                            ${selectedChoiceId 
                                ? 'bg-blue-600 hover:bg-blue-500 text-white animate-pulse hover:scale-105' 
                                : 'bg-blue-600 text-white opacity-50 cursor-not-allowed'
                            }
                        `}
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
        hint: PropTypes.string,
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