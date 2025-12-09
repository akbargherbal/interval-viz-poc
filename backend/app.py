# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel, ValidationError, field_validator

from algorithms.interval_coverage import Interval, IntervalCoverageTracer

app = Flask(__name__)
CORS(app)

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

class TraceRequest(BaseModel):
    intervals: list[IntervalInput]


@app.route('/api/trace', methods=['POST'])
def generate_trace():
    """
    Accept intervals, return complete trace.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        validated_request = TraceRequest(**data)
        
        intervals = [Interval(**i.dict()) for i in validated_request.intervals]

        tracer = IntervalCoverageTracer()
        result = tracer.remove_covered_intervals(intervals)
        
        return jsonify(result)
    
    except ValidationError as e:
        # --- MODIFIED: Manually build a clean, serializable error list ---
        # This prevents the non-serializable ValueError from reaching jsonify.
        clean_errors = [
            {
                "loc": err.get("loc"),
                "msg": err.get("msg"),
                "type": err.get("type")
            }
            for err in e.errors(include_context=False) # Exclude context which may contain the ValueError
        ]
        return jsonify({
            "error": "Invalid input data",
            "details": clean_errors
        }), 400
        # --- END MODIFIED ---
    
    except (ValueError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({"error": "An unexpected server error occurred."}), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Provide pre-defined example inputs (NOT traces - just inputs!)"""
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


@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "algorithm-trace-backend",
        "available_algorithms": ["interval-coverage"]
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Algorithm Trace Backend Starting...")
    print("=" * 60)
    print("📍 Running on: http://localhost:5000")
    print("📊 Available endpoints:")
    print("   POST /api/trace      - Generate algorithm trace")
    print("   GET  /api/examples   - Get example inputs")
    print("   GET  /api/health     - Health check")
    print("=" * 60)
    print()
    
    app.run(debug=True, port=5000)