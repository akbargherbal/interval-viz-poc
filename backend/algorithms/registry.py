"""
Algorithm Registry for automatic discovery and routing.

This registry system allows adding new algorithms without modifying
app.py or frontend components. Each algorithm tracer registers itself
with metadata that drives the frontend UI and routing logic.

Phase 2: Dynamic algorithm discovery and unified routing
"""

import os
from pathlib import Path
from typing import Dict, Type, List, Any, Optional
from .base_tracer import AlgorithmTracer
import inspect


class AlgorithmRegistry:
    """
    Central registry for algorithm tracers.

    Provides:
    - Algorithm registration with metadata
    - Retrieval by algorithm name
    - List all available algorithms with metadata
    - Validation of tracer implementations
    """

    def __init__(self):
        """Initialize empty registry."""
        self._algorithms: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        tracer_class: Type[AlgorithmTracer],
        display_name: str,
        description: str,
        example_inputs: List[Dict[str, Any]],
        input_schema: Optional[Dict[str, Any]] = None,
    ):
        """
        Register an algorithm tracer with metadata.

        Args:
            name: Unique identifier (e.g., 'binary-search', 'interval-coverage')
            tracer_class: Class inheriting from AlgorithmTracer
            display_name: Human-readable name for UI (e.g., 'Binary Search')
            description: Brief explanation of the algorithm
            example_inputs: List of example input dictionaries for quick testing
            input_schema: Optional JSON schema for input validation

        Raises:
            ValueError: If name already registered or tracer_class invalid
        """
        # Validate tracer class
        if not inspect.isclass(tracer_class):
            raise ValueError(f"tracer_class must be a class, got {type(tracer_class)}")

        if not issubclass(tracer_class, AlgorithmTracer):
            raise ValueError(
                f"{tracer_class.__name__} must inherit from AlgorithmTracer"
            )

        # Check for duplicate registration
        if name in self._algorithms:
            raise ValueError(f"Algorithm '{name}' is already registered")

        # Store algorithm metadata
        self._algorithms[name] = {
            "name": name,
            "tracer_class": tracer_class,
            "display_name": display_name,
            "description": description,
            "example_inputs": example_inputs,
            "input_schema": input_schema,
        }

    def get(self, name: str) -> Type[AlgorithmTracer]:
        """
        Retrieve tracer class by algorithm name.

        Args:
            name: Algorithm identifier

        Returns:
            Tracer class for instantiation

        Raises:
            KeyError: If algorithm not found
        """
        if name not in self._algorithms:
            available = ", ".join(self._algorithms.keys())
            raise KeyError(
                f"Algorithm '{name}' not found. "
                f"Available algorithms: {available}"
            )

        return self._algorithms[name]["tracer_class"]

    def get_metadata(self, name: str) -> Dict[str, Any]:
        """
        Get complete metadata for an algorithm (excluding tracer_class).

        Args:
            name: Algorithm identifier

        Returns:
            Dictionary with display_name, description, example_inputs, etc.

        Raises:
            KeyError: If algorithm not found
        """
        if name not in self._algorithms:
            raise KeyError(f"Algorithm '{name}' not found")

        # Return copy without tracer_class (not JSON-serializable)
        metadata = self._algorithms[name].copy()
        del metadata["tracer_class"]
        return metadata

    def get_info(self, algorithm_name: str) -> str:
        """
        Retrieve algorithm information markdown.

        Args:
            algorithm_name: Algorithm identifier (e.g., 'binary-search')

        Returns:
            str: Markdown content

        Raises:
            ValueError: If algorithm not registered or info file missing
        """
        if algorithm_name not in self._algorithms:
            raise ValueError(
                f"Unknown algorithm: '{algorithm_name}'. "
                f"Available: {list(self._algorithms.keys())}"
            )

        # Construct path to info file relative to this file's location
        # backend/algorithms/registry.py -> backend/ -> interval-viz-poc/
        base_dir = Path(__file__).parent.parent.parent
        info_path = base_dir / "docs" / "algorithm-info" / f"{algorithm_name}.md"

        if not info_path.exists():
            raise ValueError(
                f"Algorithm info file not found: {info_path}. "
                f"Create docs/algorithm-info/{algorithm_name}.md"
            )

        return info_path.read_text(encoding="utf-8")

    def list_algorithms(self) -> List[Dict[str, Any]]:
        """
        Return list of all registered algorithms with metadata.

        Returns:
            List of algorithm metadata dictionaries (without tracer_class)
            Suitable for JSON serialization to frontend.

        Example:
            [
                {
                    'name': 'binary-search',
                    'display_name': 'Binary Search',
                    'description': 'Search sorted array in O(log n) time',
                    'example_inputs': [...]
                },
                ...
            ]
        """
        return [self.get_metadata(name) for name in self._algorithms.keys()]

    def is_registered(self, name: str) -> bool:
        """Check if algorithm is registered."""
        return name in self._algorithms

    def count(self) -> int:
        """Return number of registered algorithms."""
        return len(self._algorithms)

    def __contains__(self, name: str) -> bool:
        """Support 'name in registry' syntax."""
        return self.is_registered(name)

    def __len__(self) -> int:
        """Support len(registry) syntax."""
        return self.count()


# =============================================================================
# Singleton Registry Instance
# =============================================================================

# Create global registry instance
registry = AlgorithmRegistry()


# =============================================================================
# Algorithm Registrations
# =============================================================================


def register_algorithms():
    """
    Register all available algorithm tracers.

    This function is called once during module import to populate
    the registry. Adding a new algorithm only requires adding a
    registration call here.
    """

    # Import algorithm tracers
    from .interval_coverage import IntervalCoverageTracer
    from .binary_search import BinarySearchTracer
    from .two_pointer import TwoPointerTracer
    from .sliding_window import SlidingWindowTracer
    from .merge_sort import MergeSortTracer
    from .depth_first_search_tracer import DepthFirstSearchTracer
    from .boyer_moore_voting_tracer import BoyerMooreVotingTracer
    from .breadth_first_search_tracer import BreadthFirstSearchTracer
    from .bubble_sort_tracer import BubbleSortTracer
    from .container_with_most_water_tracer import ContainerWithMostWaterTracer
    from .dijkstras_algorithm_tracer import DijkstrasAlgorithmTracer
    from .dutch_national_flag_tracer import DutchNationalFlagTracer
    from .insertion_sort_tracer import InsertionSortTracer
    from .kadanes_algorithm_tracer import KadanesAlgorithmTracer
    from .longest_increasing_subsequence_tracer import LongestIncreasingSubsequenceTracer
    from .meeting_rooms_tracer import MeetingRoomsTracer
    from .merge_intervals_tracer import MergeIntervalsTracer
    from .quick_sort_tracer import QuickSortTracer
    from .topological_sort_tracer import TopologicalSortTracer

    # -------------------------------------------------------------------------
    # Interval Coverage (PoC Algorithm - Now Refactored!)
    # -------------------------------------------------------------------------
    if not registry.is_registered("interval-coverage"):
        registry.register(
            name="interval-coverage",
            tracer_class=IntervalCoverageTracer,
            display_name="Interval Coverage",
            description="Remove intervals that are completely covered by other intervals using a greedy recursive strategy",
            example_inputs=[
                {
                    "name": "Basic Example - 4 Intervals",
                    "input": {
                        "intervals": [
                            {"id": 1, "start": 540, "end": 660, "color": "blue"},
                            {"id": 2, "start": 600, "end": 720, "color": "green"},
                            {"id": 3, "start": 540, "end": 720, "color": "amber"},
                            {"id": 4, "start": 900, "end": 960, "color": "purple"},
                        ]
                    },
                },
                {
                    "name": "No Overlap - All Kept",
                    "input": {
                        "intervals": [
                            {"id": 1, "start": 100, "end": 200, "color": "blue"},
                            {"id": 2, "start": 300, "end": 400, "color": "green"},
                            {"id": 3, "start": 500, "end": 600, "color": "amber"},
                        ]
                    },
                },
                {
                    "name": "Full Coverage - Only One Kept",
                    "input": {
                        "intervals": [
                            {"id": 1, "start": 100, "end": 500, "color": "blue"},
                            {"id": 2, "start": 150, "end": 250, "color": "green"},
                            {"id": 3, "start": 200, "end": 300, "color": "amber"},
                            {"id": 4, "start": 350, "end": 450, "color": "purple"},
                        ]
                    },
                },
                {
                    "name": "Complex Case - 6 Intervals",
                    "input": {
                        "intervals": [
                            {"id": 1, "start": 0, "end": 300, "color": "blue"},
                            {"id": 2, "start": 100, "end": 200, "color": "green"},
                            {"id": 3, "start": 250, "end": 500, "color": "amber"},
                            {"id": 4, "start": 150, "end": 350, "color": "purple"},
                            {"id": 5, "start": 600, "end": 700, "color": "red"},
                            {"id": 6, "start": 650, "end": 800, "color": "orange"},
                        ]
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["intervals"],
                "properties": {
                    "intervals": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id", "start", "end", "color"],
                            "properties": {
                                "id": {"type": "integer"},
                                "start": {"type": "integer"},
                                "end": {"type": "integer"},
                                "color": {"type": "string"},
                            },
                        },
                        "minItems": 1,
                        "maxItems": 100,
                        "description": "List of time intervals to analyze",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Binary Search
    # -------------------------------------------------------------------------
    if not registry.is_registered("binary-search"):
        registry.register(
            name="binary-search",
            tracer_class=BinarySearchTracer,
            display_name="Binary Search",
            description="Search for a target value in a sorted array using divide-and-conquer strategy (O(log n) time complexity)",
            example_inputs=[
                {
                    "name": "Basic Search - Target Found",
                    "input": {
                        "array": [
                            4,
                            11,
                            12,
                            14,
                            22,
                            23,
                            33,
                            34,
                            39,
                            48,
                            51,
                            59,
                            63,
                            69,
                            70,
                            71,
                            74,
                            79,
                        ],
                        "target": 59,
                    },
                },
                {
                    "name": "Basic Search - Target Not Found",
                    "input": {"array": [1, 3, 5, 7, 9, 11, 13, 15], "target": 6},
                },
                {
                    "name": "Large Array",
                    "input": {
                        "array": list(range(1, 101, 2)),  # [1, 3, 5, ..., 99]
                        "target": 51,
                    },
                },
                {
                    "name": "Single Element - Found",
                    "input": {"array": [42], "target": 42},
                },
                {
                    "name": "Target at Start",
                    "input": {"array": [10, 20, 30, 40, 50], "target": 10},
                },
                {
                    "name": "Target at End",
                    "input": {"array": [10, 20, 30, 40, 50], "target": 50},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array", "target"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "description": "Sorted array of integers",
                    },
                    "target": {"type": "integer", "description": "Value to search for"},
                },
            },
        )

    # -------------------------------------------------------------------------
    # Two Pointer Pattern
    # -------------------------------------------------------------------------
    if not registry.is_registered("two-pointer"):
        registry.register(
            name="two-pointer",
            tracer_class=TwoPointerTracer,
            display_name="Two Pointer Pattern",
            description="Remove duplicates from a sorted array in-place using a slow and fast pointer technique.",
            example_inputs=[
                {
                    "name": "Basic Duplicates",
                    "input": {
                        "array": [0, 1, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 8, 8, 9]
                    },
                },
                {"name": "All Unique", "input": {"array": [1, 2, 3, 4, 5]}},
                {"name": "All Duplicates", "input": {"array": [1, 1, 1, 1, 1]}},
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Sorted array of integers, may contain duplicates",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Sliding Window Pattern
    # -------------------------------------------------------------------------
    if not registry.is_registered("sliding-window"):
        registry.register(
            name="sliding-window",
            tracer_class=SlidingWindowTracer,
            display_name="Sliding Window Pattern",
            description="Find maximum sum subarray of a fixed size k",
            example_inputs=[
                {
                    "name": "Basic",
                    "input": {"array": [1, 5, 1, 3, 2, 5, 1, 6, 7, 0, 5], "k": 3},
                },
                {
                    "name": "Increasing Trend",
                    "input": {"array": [1, 2, 3, 4, 5, 6], "k": 3},
                },
                {
                    "name": "Decreasing Trend",
                    "input": {"array": [6, 5, 4, 3, 2, 1], "k": 4},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array", "k"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Array of integers",
                    },
                    "k": {
                        "type": "integer",
                        "description": "The size of the sliding window",
                    },
                },
            },
        )

    # -------------------------------------------------------------------------
    # Merge Sort
    # -------------------------------------------------------------------------
    if not registry.is_registered("merge-sort"):
        registry.register(
            name="merge-sort",
            tracer_class=MergeSortTracer,
            display_name="Merge Sort",
            description="Recursive divide-and-conquer sorting algorithm with O(n log n) guaranteed time complexity",
            example_inputs=[
                {
                    "name": "Basic - 8 Elements",
                    "input": {"array": [38, 27, 43, 3, 9, 82, 10, 5]},
                },
                {
                    "name": "Already Sorted",
                    "input": {"array": [1, 2, 3, 4, 5, 6, 7, 8]},
                },
                {
                    "name": "Reverse Sorted",
                    "input": {"array": [8, 7, 6, 5, 4, 3, 2, 1]},
                },
                {
                    "name": "With Duplicates",
                    "input": {"array": [5, 2, 8, 2, 9, 1, 5, 5]},
                },
                {"name": "Small Array", "input": {"array": [3, 1, 4, 1, 5]}},
                {
                    "name": "Larger Array - 12 Elements",
                    "input": {
                        "array": [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 33, 17]
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 1,
                        "maxItems": 12,
                        "description": "Array of numbers to sort (8-12 elements recommended)",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Depth-First Search (Iterative) - REPLACED VERSION
    # -------------------------------------------------------------------------
    if not registry.is_registered("depth-first-search"):
        registry.register(
            name="depth-first-search",
            tracer_class=DepthFirstSearchTracer,
            display_name="Depth-First Search (Iterative)",
            description="Graph traversal algorithm that explores as far as possible along each branch before backtracking using an iterative approach",
            example_inputs=[
                {
                    "name": "Basic 5-Node Graph",
                    "input": {
                        "nodes": ["A", "B", "C", "D", "E"],
                        "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")],
                        "start_node": "A",
                    },
                },
                {
                    "name": "Linear Chain",
                    "input": {
                        "nodes": ["A", "B", "C", "D"],
                        "edges": [("A", "B"), ("B", "C"), ("C", "D")],
                        "start_node": "A",
                    },
                },
                {
                    "name": "Disconnected Components",
                    "input": {
                        "nodes": ["A", "B", "C", "D", "E"],
                        "edges": [("A", "B"), ("C", "D")],
                        "start_node": "A",
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["nodes", "edges", "start_node"],
                "properties": {
                    "nodes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of node identifiers",
                    },
                    "edges": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "description": "List of edges as [from, to] pairs (undirected)",
                    },
                    "start_node": {
                        "type": "string",
                        "description": "Node to start traversal from",
                    },
                },
            },
        )

    # -------------------------------------------------------------------------
    # Boyer-Moore Voting
    # -------------------------------------------------------------------------
    if not registry.is_registered("boyer-moore-voting"):
        registry.register(
            name="boyer-moore-voting",
            tracer_class=BoyerMooreVotingTracer,
            display_name="Boyer-Moore Voting",
            description="Find majority element (appears > n/2 times) in O(n) time and O(1) space",
            example_inputs=[
                {
                    "name": "Basic - Majority Exists",
                    "input": {"array": [2, 2, 1, 1, 1, 2, 2]},
                },
                {
                    "name": "No Majority",
                    "input": {"array": [1, 2, 3, 1, 2, 3, 1]},
                },
                {
                    "name": "All Same",
                    "input": {"array": [5, 5, 5, 5, 5]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 100,
                        "description": "List of integers to find majority element in",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Breadth-First Search
    # -------------------------------------------------------------------------
    if not registry.is_registered("breadth-first-search"):
        registry.register(
            name="breadth-first-search",
            tracer_class=BreadthFirstSearchTracer,
            display_name="Breadth-First Search",
            description="Graph traversal algorithm that explores neighbors at current depth before moving to next level",
            example_inputs=[
                {
                    "name": "Basic Connected Graph",
                    "input": {
                        "nodes": ["A", "B", "C", "D", "E", "F"],
                        "edges": [
                            ("A", "B"),
                            ("A", "C"),
                            ("B", "D"),
                            ("B", "E"),
                            ("C", "F"),
                        ],
                        "start_node": "A",
                    },
                },
                {
                    "name": "Disconnected Graph",
                    "input": {
                        "nodes": ["A", "B", "C", "D"],
                        "edges": [("A", "B"), ("C", "D")],
                        "start_node": "A",
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["nodes", "edges", "start_node"],
                "properties": {
                    "nodes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of node identifiers",
                    },
                    "edges": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "description": "List of edges as [from, to] pairs",
                    },
                    "start_node": {
                        "type": "string",
                        "description": "Node to start traversal from",
                    },
                },
            },
        )

    # -------------------------------------------------------------------------
    # Bubble Sort
    # -------------------------------------------------------------------------
    if not registry.is_registered("bubble-sort"):
        registry.register(
            name="bubble-sort",
            tracer_class=BubbleSortTracer,
            display_name="Bubble Sort",
            description="Simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them",
            example_inputs=[
                {
                    "name": "Basic Unsorted",
                    "input": {"array": [64, 34, 25, 12, 22, 11, 90]},
                },
                {
                    "name": "Already Sorted",
                    "input": {"array": [1, 2, 3, 4, 5]},
                },
                {
                    "name": "Reverse Sorted",
                    "input": {"array": [5, 4, 3, 2, 1]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of integers to sort",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Container With Most Water
    # -------------------------------------------------------------------------
    if not registry.is_registered("container-with-most-water"):
        registry.register(
            name="container-with-most-water",
            tracer_class=ContainerWithMostWaterTracer,
            display_name="Container With Most Water",
            description="Find two lines that together with the x-axis form a container, such that the container contains the most water",
            example_inputs=[
                {
                    "name": "Basic Example",
                    "input": {"heights": [1, 8, 6, 2, 5, 4, 8, 3, 7]},
                },
                {
                    "name": "Increasing Heights",
                    "input": {"heights": [1, 2, 3, 4, 5]},
                },
                {
                    "name": "Decreasing Heights",
                    "input": {"heights": [5, 4, 3, 2, 1]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["heights"],
                "properties": {
                    "heights": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 0},
                        "minItems": 2,
                        "maxItems": 20,
                        "description": "List of non-negative integers representing heights",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Dijkstra's Algorithm
    # -------------------------------------------------------------------------
    if not registry.is_registered("dijkstras-algorithm"):
        registry.register(
            name="dijkstras-algorithm",
            tracer_class=DijkstrasAlgorithmTracer,
            display_name="Dijkstra's Algorithm",
            description="Find shortest paths from a starting node to all other nodes in a weighted graph",
            example_inputs=[
                {
                    "name": "Basic Weighted Graph",
                    "input": {
                        "nodes": ["A", "B", "C", "D", "E"],
                        "edges": [
                            ["A", "B", 4],
                            ["A", "C", 2],
                            ["B", "C", 1],
                            ["B", "D", 5],
                            ["C", "D", 8],
                            ["C", "E", 10],
                            ["D", "E", 2],
                        ],
                        "start_node": "A",
                    },
                },
                {
                    "name": "Simple Triangle",
                    "input": {
                        "nodes": ["X", "Y", "Z"],
                        "edges": [["X", "Y", 5], ["Y", "Z", 3], ["X", "Z", 10]],
                        "start_node": "X",
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["nodes", "edges", "start_node"],
                "properties": {
                    "nodes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of node identifiers",
                    },
                    "edges": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"oneOf": [{"type": "string"}, {"type": "integer"}]},
                            "minItems": 3,
                            "maxItems": 3,
                            "description": "[from, to, weight]",
                        },
                        "description": "List of edges with weights",
                    },
                    "start_node": {
                        "type": "string",
                        "description": "Node to start traversal from",
                    },
                },
            },
        )

    # -------------------------------------------------------------------------
    # Dutch National Flag
    # -------------------------------------------------------------------------
    if not registry.is_registered("dutch-national-flag"):
        registry.register(
            name="dutch-national-flag",
            tracer_class=DutchNationalFlagTracer,
            display_name="Sort Colors (Dutch National Flag)",
            description="Sort an array of 0s, 1s, and 2s in linear time and constant space",
            example_inputs=[
                {
                    "name": "Mixed Colors",
                    "input": {"array": [2, 0, 2, 1, 1, 0]},
                },
                {
                    "name": "Reverse Sorted",
                    "input": {"array": [2, 2, 1, 1, 0, 0]},
                },
                {
                    "name": "Sorted",
                    "input": {"array": [0, 0, 1, 1, 2, 2]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer", "enum": [0, 1, 2]},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "Array containing only 0s, 1s, and 2s",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Insertion Sort
    # -------------------------------------------------------------------------
    if not registry.is_registered("insertion-sort"):
        registry.register(
            name="insertion-sort",
            tracer_class=InsertionSortTracer,
            display_name="Insertion Sort",
            description="Builds the final sorted array one item at a time",
            example_inputs=[
                {
                    "name": "Basic Unsorted",
                    "input": {"array": [12, 11, 13, 5, 6]},
                },
                {
                    "name": "Reverse Sorted",
                    "input": {"array": [5, 4, 3, 2, 1]},
                },
                {
                    "name": "Nearly Sorted",
                    "input": {"array": [2, 1, 3, 4, 5]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of integers to sort",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Kadane's Algorithm
    # -------------------------------------------------------------------------
    if not registry.is_registered("kadanes-algorithm"):
        registry.register(
            name="kadanes-algorithm",
            tracer_class=KadanesAlgorithmTracer,
            display_name="Kadane's Algorithm",
            description="Find the contiguous subarray within a one-dimensional array of numbers which has the largest sum",
            example_inputs=[
                {
                    "name": "Mixed Values",
                    "input": {"array": [-2, 1, -3, 4, -1, 2, 1, -5, 4]},
                },
                {
                    "name": "All Negative",
                    "input": {"array": [-5, -2, -9, -1, -4]},
                },
                {
                    "name": "All Positive",
                    "input": {"array": [1, 2, 3, 4, 5]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of integers",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Longest Increasing Subsequence
    # -------------------------------------------------------------------------
    if not registry.is_registered("longest-increasing-subsequence"):
        registry.register(
            name="longest-increasing-subsequence",
            tracer_class=LongestIncreasingSubsequenceTracer,
            display_name="Longest Increasing Subsequence (Patience Sorting)",
            description="Find the length of the longest subsequence of a given sequence such that all elements of the subsequence are sorted in increasing order",
            example_inputs=[
                {
                    "name": "Basic Example",
                    "input": {"array": [10, 9, 2, 5, 3, 7, 101, 18]},
                },
                {
                    "name": "Already Sorted",
                    "input": {"array": [1, 2, 3, 4, 5]},
                },
                {
                    "name": "Reverse Sorted",
                    "input": {"array": [5, 4, 3, 2, 1]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of integers",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Meeting Rooms II
    # -------------------------------------------------------------------------
    if not registry.is_registered("meeting-rooms"):
        registry.register(
            name="meeting-rooms",
            tracer_class=MeetingRoomsTracer,
            display_name="Meeting Rooms II",
            description="Find the minimum number of conference rooms required for a given set of meetings",
            example_inputs=[
                {
                    "name": "Basic Overlap",
                    "input": {
                        "intervals": [[0, 30], [5, 10], [15, 20]],
                    },
                },
                {
                    "name": "Nested Meetings",
                    "input": {
                        "intervals": [[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]],
                    },
                },
                {
                    "name": "No Overlap",
                    "input": {
                        "intervals": [[7, 10], [2, 4]],
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["intervals"],
                "properties": {
                    "intervals": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of [start, end] time intervals",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Merge Intervals
    # -------------------------------------------------------------------------
    if not registry.is_registered("merge-intervals"):
        registry.register(
            name="merge-intervals",
            tracer_class=MergeIntervalsTracer,
            display_name="Merge Intervals",
            description="Merge all overlapping intervals",
            example_inputs=[
                {
                    "name": "Basic Overlap",
                    "input": {
                        "intervals": [[1, 3], [2, 6], [8, 10], [15, 18]],
                    },
                },
                {
                    "name": "Merge All",
                    "input": {
                        "intervals": [[1, 4], [4, 5]],
                    },
                },
                {
                    "name": "No Overlap",
                    "input": {
                        "intervals": [[1, 2], [3, 4], [5, 6]],
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["intervals"],
                "properties": {
                    "intervals": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of [start, end] time intervals",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Quick Sort
    # -------------------------------------------------------------------------
    if not registry.is_registered("quick-sort"):
        registry.register(
            name="quick-sort",
            tracer_class=QuickSortTracer,
            display_name="Quick Sort",
            description="Divide-and-conquer sorting algorithm that uses partitioning",
            example_inputs=[
                {
                    "name": "Basic Unsorted",
                    "input": {"array": [10, 7, 8, 9, 1, 5]},
                },
                {
                    "name": "Already Sorted",
                    "input": {"array": [1, 2, 3, 4, 5]},
                },
                {
                    "name": "Reverse Sorted",
                    "input": {"array": [5, 4, 3, 2, 1]},
                },
            ],
            input_schema={
                "type": "object",
                "required": ["array"],
                "properties": {
                    "array": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 1,
                        "maxItems": 20,
                        "description": "List of integers to sort",
                    }
                },
            },
        )

    # -------------------------------------------------------------------------
    # Topological Sort
    # -------------------------------------------------------------------------
    if not registry.is_registered("topological-sort"):
        registry.register(
            name="topological-sort",
            tracer_class=TopologicalSortTracer,
            display_name="Topological Sort (Kahn's Algorithm)",
            description="Linear ordering of vertices in a directed graph such that for every directed edge u -> v, vertex u comes before v",
            example_inputs=[
                {
                    "name": "Basic DAG",
                    "input": {
                        "nodes": ["A", "B", "C", "D", "E"],
                        "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["D", "E"]],
                    },
                },
                {
                    "name": "Disconnected Components",
                    "input": {
                        "nodes": ["A", "B", "C", "D"],
                        "edges": [["A", "B"], ["C", "D"]],
                    },
                },
                {
                    "name": "Cycle Detection",
                    "input": {
                        "nodes": ["A", "B", "C"],
                        "edges": [["A", "B"], ["B", "C"], ["C", "A"]],
                    },
                },
            ],
            input_schema={
                "type": "object",
                "required": ["nodes", "edges"],
                "properties": {
                    "nodes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "maxItems": 10,
                        "description": "List of node identifiers",
                    },
                    "edges": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "description": "List of directed edges [from, to]",
                    },
                },
            },
        )


# Auto-register algorithms on module import
# Added idempotency checks to prevent re-registration during hot-reloading
if not registry.is_registered("binary-search"):
    register_algorithms()


# =============================================================================
# Convenience Functions
# =============================================================================


def get_algorithm_names() -> List[str]:
    """Get list of all registered algorithm names."""
    return list(registry._algorithms.keys())


def get_algorithm(name: str) -> Type[AlgorithmTracer]:
    """Alias for registry.get() for convenience."""
    return registry.get(name)