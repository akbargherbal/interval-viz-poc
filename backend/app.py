# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel, ValidationError, field_validator

from algorithms.interval_coverage import Interval, IntervalCoverageTracer
from algorithms.binary_search import BinarySearchTracer
from algorithms.registry import registry

app = Flask(__name__)
CORS(app)

# ============================================================================
# Pydantic Models for Input Validation (Legacy - kept for backward compat)
# ============================================================================

class IntervalInput(BaseModel):
    id: int
    start: int
    end: int
    color: str = 'blue'

    @field_validator('id')
    @classmethod
    def id_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('id must be a non-negative integer')
        return v

    @field_validator('end')
    @classmethod
    def end_must_be_greater_than_start(cls, v, info):
        if 'start' in info.data and v <= info.data['start']:
            raise ValueError(f'end ({v}) must be greater than start ({info.data["start"]})')
        return v


class IntervalTraceRequest(BaseModel):
    intervals: list[IntervalInput]


class BinarySearchRequest(BaseModel):
    array: list[int]
    target: int

    @field_validator('array')
    @classmethod
    def array_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('array cannot be empty')
        return v

    @field_validator('array')
    @classmethod
    def array_must_be_sorted(cls, v):
        if not all(v[i] <= v[i+1] for i in range(len(v)-1)):
            raise ValueError('array must be sorted in ascending order')
        return v


# ============================================================================
# NEW: Unified API Endpoints (Phase 2)
# ============================================================================

@app.route('/api/algorithms', methods=['GET'])
def list_algorithms():
    """
    Return list of all available algorithms with metadata.
    
    Frontend uses this to dynamically populate algorithm selector.
    
    Returns:
        JSON array of algorithm metadata:
        [
            {
                "name": "binary-search",
                "display_name": "Binary Search",
                "description": "Search sorted array...",
                "example_inputs": [...]
            },
            ...
        ]
    """
    try:
        algorithms = registry.list_algorithms()
        return jsonify(algorithms)
    except Exception as e:
        app.logger.error(f"Error listing algorithms: {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve algorithm list"}), 500


@app.route('/api/trace/unified', methods=['POST'])
def generate_trace_unified():
    """
    Unified trace generation endpoint - routes to correct algorithm.
    
    Input format:
        {
            "algorithm": "binary-search" | "interval-coverage",
            "input": { ... algorithm-specific input ... }
        }
    
    Output: Standard trace result from algorithm tracer
    
    This endpoint replaces algorithm-specific endpoints and enables
    adding new algorithms without modifying app.py.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Extract algorithm name and input
        algorithm_name = data.get('algorithm')
        algorithm_input = data.get('input')
        
        if not algorithm_name:
            return jsonify({
                "error": "Missing required field: 'algorithm'",
                "available_algorithms": [alg['name'] for alg in registry.list_algorithms()]
            }), 400
        
        if not algorithm_input:
            return jsonify({"error": "Missing required field: 'input'"}), 400
        
        # Check if algorithm exists
        if algorithm_name not in registry:
            available = [alg['name'] for alg in registry.list_algorithms()]
            return jsonify({
                "error": f"Unknown algorithm: '{algorithm_name}'",
                "available_algorithms": available
            }), 404
        
        # Get tracer class and instantiate
        tracer_class = registry.get(algorithm_name)
        tracer = tracer_class()
        
        # Execute algorithm with input
        # Note: Algorithm-specific validation happens in tracer.execute()
        result = tracer.execute(algorithm_input)
        
        return jsonify(result)
    
    except ValueError as e:
        # Algorithm-specific validation errors
        return jsonify({"error": str(e)}), 400
    
    except RuntimeError as e:
        # Algorithm execution errors (e.g., max steps exceeded)
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        app.logger.error(f"Unexpected error in unified trace endpoint: {e}", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred"}), 500


# ============================================================================
# LEGACY API Endpoints (Kept for Backward Compatibility)
# ============================================================================

@app.route('/api/trace', methods=['POST'])
def generate_trace():
    """
    LEGACY ENDPOINT: Interval Coverage algorithm.
    Kept for backward compatibility with existing frontend.

    Accept intervals, return complete trace.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        validated_request = IntervalTraceRequest(**data)
        intervals = [Interval(**i.model_dump()) for i in validated_request.intervals]

        tracer = IntervalCoverageTracer()
        result = tracer.remove_covered_intervals(intervals)

        return jsonify(result)

    except ValidationError as e:
        clean_errors = [
            {
                "loc": err.get("loc"),
                "msg": err.get("msg"),
                "type": err.get("type")
            }
            for err in e.errors(include_context=False)
        ]
        return jsonify({
            "error": "Invalid input data",
            "details": clean_errors
        }), 400

    except (ValueError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred."}), 500


@app.route('/api/trace/binary-search', methods=['POST'])
def generate_binary_search_trace():
    """
    LEGACY ENDPOINT: Binary Search algorithm trace generation.
    Kept for backward compatibility.

    Input: {"array": [1, 3, 5, 7, 9], "target": 5}
    Output: Complete trace with visualization data
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        validated_request = BinarySearchRequest(**data)

        tracer = BinarySearchTracer()
        result = tracer.execute({
            'array': validated_request.array,
            'target': validated_request.target
        })

        return jsonify(result)

    except ValidationError as e:
        clean_errors = [
            {
                "loc": err.get("loc"),
                "msg": err.get("msg"),
                "type": err.get("type")
            }
            for err in e.errors(include_context=False)
        ]
        return jsonify({
            "error": "Invalid input data",
            "details": clean_errors
        }), 400

    except (ValueError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred."}), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """
    LEGACY ENDPOINT: Provide interval coverage examples.
    
    FUTURE: This will be replaced by registry-based example retrieval.
    """
    examples = [
        {
            "name": "Basic Example",
            "intervals": [
                {"id": 1, "start": 540, "end": 660, "color": "blue"},
                {"id": 2, "start": 600, "end": 720, "color": "green"},
                {"id": 3, "start": 540, "end": 720, "color": "amber"},
                {"id": 4, "start": 900, "end": 960, "color": "purple"}
            ]
        },
        {
            "name": "All Disjoint",
            "intervals": [
                {"id": 1, "start": 100, "end": 200, "color": "blue"},
                {"id": 2, "start": 300, "end": 400, "color": "green"},
                {"id": 3, "start": 500, "end": 600, "color": "amber"}
            ]
        },
        {
            "name": "All Covered",
            "intervals": [
                {"id": 1, "start": 100, "end": 500, "color": "amber"},
                {"id": 2, "start": 150, "end": 200, "color": "blue"},
                {"id": 3, "start": 250, "end": 350, "color": "green"}
            ]
        }
    ]
    return jsonify(examples)


@app.route('/api/examples/binary-search', methods=['GET'])
def get_binary_search_examples():
    """
    LEGACY ENDPOINT: Provide binary search examples.
    
    FUTURE: This will be replaced by registry-based example retrieval.
    """
    examples = [
        {
            "name": "Basic Search - Target Found",
            "array": [1, 3, 5, 7, 9, 11, 13, 15],
            "target": 7
        },
        {
            "name": "Basic Search - Target Not Found",
            "array": [1, 3, 5, 7, 9, 11, 13, 15],
            "target": 6
        },
        {
            "name": "Large Array",
            "array": list(range(1, 101, 2)),  # [1, 3, 5, ..., 99]
            "target": 51
        },
        {
            "name": "Single Element - Found",
            "array": [42],
            "target": 42
        },
        {
            "name": "Target at Start",
            "array": [10, 20, 30, 40, 50],
            "target": 10
        },
        {
            "name": "Target at End",
            "array": [10, 20, 30, 40, 50],
            "target": 50
        }
    ]
    return jsonify(examples)


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Now includes dynamic algorithm count from registry.
    """
    return jsonify({
        "status": "healthy",
        "service": "algorithm-trace-backend",
        "algorithms_registered": len(registry),
        "available_algorithms": [alg['name'] for alg in registry.list_algorithms()]
    })


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Algorithm Trace Backend Starting...")
    print("=" * 60)
    print("📍 Running on: http://localhost:5000")
    print(f"📊 Registered Algorithms: {len(registry)}")
    for alg in registry.list_algorithms():
        print(f"   - {alg['name']}: {alg['display_name']}")
    print()
    print("📡 Available endpoints:")
    print("   GET  /api/algorithms               - List all algorithms (NEW)")
    print("   POST /api/trace/unified            - Unified trace endpoint (NEW)")
    print("   POST /api/trace                    - Interval Coverage (legacy)")
    print("   POST /api/trace/binary-search      - Binary Search (legacy)")
    print("   GET  /api/examples                 - Interval examples (legacy)")
    print("   GET  /api/examples/binary-search   - Binary Search examples (legacy)")
    print("   GET  /api/health                   - Health check")
    print("=" * 60)
    print()

    app.run(debug=True, port=5000)