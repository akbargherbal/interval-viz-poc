# backend/algorithms/base_tracer.py
"""
Base class for algorithm tracers in the educational visualization platform.

This abstract base class defines the common interface and utilities that all
algorithm implementations must follow to generate traces compatible with the
frontend visualization system.

Philosophy: Backend does ALL the thinking, frontend does ALL the reacting.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict
from dataclasses import dataclass, asdict
import time


@dataclass
class TraceStep:
    """
    A single step in the algorithm execution trace.
    
    This structure is shared across all algorithms to ensure consistent
    visualization on the frontend.
    """
    step: int
    type: str
    timestamp: float
    data: dict
    description: str


class AlgorithmTracer(ABC):
    """
    Abstract base class for algorithm trace generation.
    
    All algorithm implementations inherit from this class and implement:
    - execute(): Main algorithm entry point
    - get_prediction_points(): Educational prediction moments
    
    The base class provides:
    - Trace step recording with _add_step()
    - Safety limits (MAX_STEPS to prevent infinite loops)
    - Common serialization utilities
    - Consistent metadata structure
    """
    
    MAX_STEPS = 10000
    
    def __init__(self):
        """Initialize tracer with empty trace and reset counters."""
        self.trace = []
        self.step_count = 0
        self.start_time = time.time()
        self.metadata = {}
    
    @abstractmethod
    def execute(self, input_data: Any) -> dict:
        """
        Execute the algorithm and generate complete trace.
        
        This method must be implemented by each algorithm to:
        1. Validate input
        2. Execute algorithm with trace generation
        3. Return standardized result structure
        
        Args:
            input_data: Algorithm-specific input (intervals, arrays, graphs, etc.)
        
        Returns:
            dict: {
                "result": <algorithm output>,
                "trace": {
                    "steps": [list of TraceStep dicts],
                    "total_steps": int,
                    "duration": float
                },
                "metadata": {
                    "algorithm": str,
                    "visualization_type": str,  # NEW: for frontend registry
                    "prediction_points": [...]  # NEW: for prediction mode
                    ... other algorithm-specific metadata
                }
            }
        """
        pass
    
    @abstractmethod
    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction moments in the trace for active learning.
        
        Returns a list of prediction opportunities where students should
        pause and predict the algorithm's next decision.
        
        Returns:
            list: [
                {
                    "step_index": int,           # Which step to pause at
                    "question": str,             # Question to ask student
                    "choices": [str, ...],       # Possible answers
                    "hint": str,                 # Optional hint
                    "correct_answer": str        # For validation (optional)
                },
                ...
            ]
        
        Example for interval coverage:
            {
                "step_index": 5,
                "question": "Will this interval be kept or covered?",
                "choices": ["keep", "covered"],
                "hint": "Compare interval.end with max_end"
            }
        """
        pass
    
    def _add_step(self, step_type: str, data: dict, description: str):
        """
        Record a step in the algorithm execution.
        
        This is the core trace generation method used by algorithm implementations.
        It enforces the MAX_STEPS limit and creates a standardized TraceStep.
        
        Args:
            step_type: Category of step (e.g., "EXAMINING_INTERVAL", "DECISION_MADE")
            data: Step-specific data (must be JSON-serializable)
            description: Human-readable explanation of what's happening
        
        Raises:
            RuntimeError: If MAX_STEPS exceeded (prevents infinite loops)
        """
        if self.step_count >= self.MAX_STEPS:
            raise RuntimeError(
                f"Trace generation aborted: Exceeded maximum of {self.MAX_STEPS} steps. "
                "The input may be too complex or causing an infinite loop."
            )
        
        self.trace.append(TraceStep(
            step=self.step_count,
            type=step_type,
            timestamp=time.time() - self.start_time,
            data=data,
            description=description
        ))
        self.step_count += 1
    
    def _serialize_value(self, value):
        """
        Convert Python values to JSON-safe values.
        
        Handles special cases like infinity that don't serialize to JSON.
        
        Args:
            value: Any Python value
        
        Returns:
            JSON-serializable value (or None for inf/-inf)
        """
        if value == float('-inf'):
            return None
        if value == float('inf'):
            return None
        return value
    
    def _build_trace_result(self, algorithm_result: Any) -> dict:
        """
        Build the standardized trace result structure.
        
        This helper ensures all algorithms return consistent structure.
        
        Args:
            algorithm_result: The algorithm's output (kept intervals, sorted array, etc.)
        
        Returns:
            dict: Standardized result with trace and metadata
        """
        # Generate prediction points after trace is complete
        prediction_points = self.get_prediction_points()
        
        # Add prediction points to metadata
        self.metadata["prediction_points"] = prediction_points
        
        return {
            "result": algorithm_result,
            "trace": {
                "steps": [asdict(s) for s in self.trace],
                "total_steps": len(self.trace),
                "duration": time.time() - self.start_time
            },
            "metadata": self.metadata
        }