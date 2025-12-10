#!/bin/bash
# Test script for Phase 2 registry backend changes
# Run this from: /home/akbar/Jupyter_Notebooks/interval-viz-poc/

echo "=========================================="
echo "Phase 2: Testing Registry Backend"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://localhost:5000"

echo "Prerequisites: Flask backend must be running on port 5000"
echo "Start it with: cd backend && python app.py"
echo ""
read -p "Press Enter when backend is running..."
echo ""

# Test 1: GET /api/algorithms
echo "=========================================="
echo "Test 1: GET /api/algorithms"
echo "=========================================="
echo "Expected: JSON array with 2 algorithms"
echo ""
curl -s "${API_URL}/api/algorithms" | python -m json.tool
echo ""

# Test 2: POST /api/trace/unified - Binary Search
echo "=========================================="
echo "Test 2: POST /api/trace/unified (Binary Search)"
echo "=========================================="
echo "Expected: Complete trace with array visualization"
echo ""
curl -s -X POST "${API_URL}/api/trace/unified" \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "binary-search",
    "input": {
      "array": [1, 3, 5, 7, 9],
      "target": 5
    }
  }' | python -m json.tool | head -n 50
echo "... (truncated)"
echo ""

# Test 3: POST /api/trace/unified - Interval Coverage
echo "=========================================="
echo "Test 3: POST /api/trace/unified (Interval Coverage)"
echo "=========================================="
echo "Expected: Complete trace with interval visualization"
echo ""
curl -s -X POST "${API_URL}/api/trace/unified" \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "interval-coverage",
    "input": {
      "intervals": [
        {"id": 1, "start": 100, "end": 200, "color": "blue"},
        {"id": 2, "start": 150, "end": 250, "color": "green"}
      ]
    }
  }' | python -m json.tool | head -n 50
echo "... (truncated)"
echo ""

# Test 4: Error handling - Unknown algorithm
echo "=========================================="
echo "Test 4: Error Handling - Unknown Algorithm"
echo "=========================================="
echo "Expected: 404 error with available algorithms list"
echo ""
curl -s -X POST "${API_URL}/api/trace/unified" \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "nonexistent-algorithm",
    "input": {}
  }' | python -m json.tool
echo ""

# Test 5: Error handling - Missing algorithm field
echo "=========================================="
echo "Test 5: Error Handling - Missing Algorithm Field"
echo "=========================================="
echo "Expected: 400 error with message about missing 'algorithm'"
echo ""
curl -s -X POST "${API_URL}/api/trace/unified" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"array": [1, 2, 3], "target": 2}
  }' | python -m json.tool
echo ""

# Test 6: Backward compatibility - Legacy endpoints still work
echo "=========================================="
echo "Test 6: Backward Compatibility - Legacy /api/trace"
echo "=========================================="
echo "Expected: Interval coverage trace (same as before)"
echo ""
curl -s -X POST "${API_URL}/api/trace" \
  -H "Content-Type: application/json" \
  -d '{
    "intervals": [
      {"id": 1, "start": 100, "end": 200, "color": "blue"}
    ]
  }' | python -m json.tool | head -n 30
echo "... (truncated)"
echo ""

# Test 7: Health check shows registry info
echo "=========================================="
echo "Test 7: Health Check with Registry Info"
echo "=========================================="
echo "Expected: Status + registered algorithm count"
echo ""
curl -s "${API_URL}/api/health" | python -m json.tool
echo ""

echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - New endpoints: /api/algorithms, /api/trace/unified"
echo "  - Legacy endpoints: Still functional"
echo "  - Registry: Auto-discovers algorithms"
echo ""
echo "Next: Update frontend to use unified endpoint"