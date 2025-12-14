# Algorithm Visualization Platform

## Project Overview

An educational platform for visualizing algorithms with active learning features. Built on a **registry-based architecture** that makes adding new algorithms as simple as registering a class—no endpoint configuration required.

**Philosophy:** Backend does ALL the thinking, frontend does ALL the reacting.

**Status:** ✅ Platform Architecture Complete - 2 Algorithms Live (Interval Coverage, Binary Search)

---

## 🎯 Core Architecture Principles

### The Registry Pattern (⭐ Core Innovation)

**Critical Rule:** You do NOT modify `app.py` routing logic. Algorithms self-register and appear in the UI automatically.

**How It Works:**

```python
# backend/algorithms/your_algorithm.py
class YourAlgorithmTracer(AlgorithmTracer):
    def execute(self, input_data):
        # Your algorithm + trace generation
        return self._build_trace_result(result)

    def get_prediction_points(self):
        # Identify learning moments
        return [...]

# backend/algorithms/registry.py
registry.register(
    name='your-algorithm',
    tracer_class=YourAlgorithmTracer,
    display_name='Your Algorithm',
    description='What it does',
    example_inputs=[...]
)
```

**Result:** Algorithm automatically appears in UI dropdown. No app.py changes. No frontend routing changes. ✨

---

### Unified API Endpoint

**Single endpoint handles ALL algorithms:**

```bash
POST /api/trace/unified
{
  "algorithm": "binary-search",  # or "interval-coverage", "merge-sort", etc.
  "input": {
    "array": [1, 3, 5, 7, 9],
    "target": 5
  }
}
```

**Backend Routing:**

```python
# app.py - This handles ALL algorithms automatically
@app.route('/api/trace/unified', methods=['POST'])
def generate_trace_unified():
    algorithm_name = request.json['algorithm']
    algorithm_input = request.json['input']

    # Registry lookup (automatic)
    tracer_class = registry.get(algorithm_name)
    tracer = tracer_class()

    # Execute and return trace
    return jsonify(tracer.execute(algorithm_input))
```

---

### Dynamic Visualization Selection

**Backend declares visualization type; frontend selects component automatically:**

```python
# Backend declares visualization type
self.metadata = {
    'algorithm': 'binary-search',
    'visualization_type': 'array',  # ← Frontend reads this
    'visualization_config': {...}
}
```

```javascript
// Frontend dynamically selects component
import { getVisualizationComponent } from "./utils/visualizationRegistry";

const Component = getVisualizationComponent(
  trace.metadata.visualization_type // 'array' → ArrayView
);

return <Component step={step} config={config} />;
```

**Available Visualization Types:**

- `array` - For Binary Search, Sorting algorithms
- `timeline` - For Interval Coverage
- `graph` - Future: DFS, BFS, Dijkstra
- `tree` - Future: BST, Heap operations

---

## Project Structure

```
interval-viz-poc/
├── backend/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base_tracer.py          # ⭐ Abstract base class (CRITICAL)
│   │   ├── registry.py             # ⭐ Central algorithm registry
│   │   ├── interval_coverage.py    # Example algorithm
│   │   └── binary_search.py        # Example algorithm
│   ├── app.py                      # Flask API with unified routing
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AlgorithmSwitcher.jsx    # Dynamic algorithm selector
│   │   │   ├── ControlBar.jsx           # Navigation controls
│   │   │   ├── CompletionModal.jsx      # Success screen
│   │   │   ├── PredictionModal.jsx      # Interactive predictions
│   │   │   ├── KeyboardHints.jsx        # Shortcut guide
│   │   │   └── visualizations/          # ⭐ Reusable viz components
│   │   │       ├── ArrayView.jsx
│   │   │       ├── TimelineView.jsx
│   │   │       └── CallStackView.jsx
│   │   ├── hooks/                       # Business logic hooks
│   │   │   ├── useTraceLoader.js
│   │   │   ├── useTraceNavigation.js
│   │   │   ├── usePredictionMode.js
│   │   │   ├── useVisualHighlight.js
│   │   │   └── useKeyboardShortcuts.js
│   │   ├── utils/
│   │   │   └── visualizationRegistry.js # ⭐ Dynamic component selection
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
│
├── docs/
│   ├── TENANT_GUIDE.md                  # ⭐ Constitutional framework
│   └── compliance/                      # ⭐ Compliance checklists
│       ├── BACKEND_CHECKLIST.md
│       ├── FRONTEND_CHECKLIST.md
│       ├── QA_INTEGRATION_CHECKLIST.md
│       └── CHECKLIST_SYSTEM_OVERVIEW.md
│
└── README.md

⭐ = Critical files for understanding the architecture
```

---

## Compliance Framework (CRITICAL)

This platform follows a **three-tier requirement system** that defines what can and cannot be changed.

### Requirement Tiers

#### 1. LOCKED Requirements 🔒

**Cannot be changed without major version bump**

- **API Contracts**: Trace structure, metadata fields
- **Modal Behavior**: HTML IDs (`#prediction-modal`, `#completion-modal`), keyboard shortcuts, auto-scroll
- **Panel Layout**: Overflow pattern (MUST use `items-start` + `mx-auto`, NOT `items-center`)

#### 2. CONSTRAINED Requirements ⚠️

**Limited flexibility with defined bounds**

- **Visualization Data**: Array/timeline/graph patterns
- **Prediction Format**: ≤3 choices maximum
- **Step Type Categorization**: 7 defined types (DECISION, COVERAGE, etc.)

#### 3. FREE Zones ✅

**Full creative freedom**

- Internal algorithm implementation
- Performance optimizations
- Custom visualization styles (within overflow pattern)

---

### Three Compliance Checklists (CRITICAL)

All new algorithms MUST pass these checklists:

#### 1. Backend Compliance (`docs/compliance/BACKEND_CHECKLIST.md`)

**Validates:**

- ✅ Metadata structure (`algorithm`, `display_name`, `visualization_type`)
- ✅ Trace format (steps array, timestamps, descriptions)
- ✅ Visualization data contracts (use `state` string, not `visual_state` dict)
- ✅ Prediction points format (≤3 choices)
- ✅ Base class compliance (`AlgorithmTracer` inheritance)

**Critical Anti-Patterns:**

- ❌ Missing `display_name` field
- ❌ Using `visual_state` dict instead of `state` string
- ❌ >3 choices in prediction questions
- ❌ Hardcoding visualization logic in tracer

---

#### 2. Frontend Compliance (`docs/compliance/FRONTEND_CHECKLIST.md`)

**Validates:**

- ✅ Modal IDs: `#prediction-modal`, `#completion-modal` (LOCKED)
- ✅ Overflow pattern: `items-start` + `mx-auto` (NOT `items-center`)
- ✅ Keyboard shortcuts (←→ navigation, R reset, K/C/S prediction)
- ✅ Auto-scroll behavior in call stack
- ✅ Component interface (`step` and `config` props)

**Critical Overflow Pattern:**

```javascript
// ✅ CORRECT: Prevents left-side cutoff
<div className="h-full flex flex-col items-start overflow-auto py-4 px-6">
  <div className="mx-auto">
    {/* content centers but doesn't cut off */}
  </div>
</div>

// ❌ INCORRECT: Causes overflow cutoff on left side
<div className="h-full flex flex-col items-center overflow-auto">
  {/* content gets cut off */}
</div>
```

---

#### 3. QA & Integration (`docs/compliance/QA_INTEGRATION_CHECKLIST.md`)

**14 Test Suites:**

- Suite 1-6: LOCKED requirements (modals, IDs, keyboard, auto-scroll, overflow)
- Suite 7-10: CONSTRAINED requirements (backend contract, predictions)
- Suite 11-14: Integration tests (cross-algorithm, responsive, performance, regression)

**Workflow:** Backend checklist → Frontend checklist → QA checklist → Production ✅

---

## Base Tracer Abstraction (CRITICAL)

All algorithms MUST inherit from `AlgorithmTracer`:

```python
class AlgorithmTracer(ABC):
    @abstractmethod
    def execute(self, input_data: Any) -> dict:
        """
        Execute algorithm and return standardized result.

        REQUIRED FIELDS in metadata:
        - display_name: str (UI display name)
        - visualization_type: str ('array', 'timeline', 'graph', 'tree')

        Returns:
        {
            "result": <algorithm output>,
            "trace": {"steps": [...], "total_steps": N, "duration": T},
            "metadata": {
                "algorithm": "name",
                "display_name": "Display Name",      # REQUIRED
                "visualization_type": "array",       # REQUIRED
                "visualization_config": {...},
                "prediction_points": [...]           # Auto-generated
            }
        }
        """
        pass

    @abstractmethod
    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction moments for active learning.

        CRITICAL: Maximum 3 choices per question.

        Returns: [
            {
                "step_index": 5,
                "question": "Will we search left or right?",
                "choices": [  # ≤3 choices
                    {"id": "left", "label": "Search Left"},
                    {"id": "right", "label": "Search Right"}
                ],
                "hint": "Compare mid with target",
                "correct_answer": "right"
            }
        ]
        """
        pass
```

**Built-in Methods:**

- `_add_step(type, data, description)` - Record trace steps
- `_build_trace_result(result)` - Format standardized output
- `_get_visualization_state()` - Optional: Auto-enrich steps

**Safety Limits:**

- `MAX_STEPS = 10,000` - Prevents infinite loops
- Automatic error handling

---

## API Documentation (CRITICAL)

### Primary Endpoints

#### `GET /api/algorithms`

**Purpose:** Discover all available algorithms with metadata.

**Response:**

```json
[
  {
    "name": "binary-search",
    "display_name": "Binary Search",
    "description": "Search sorted array in O(log n) time",
    "example_inputs": [
      {
        "name": "Basic Search - Target Found",
        "input": {"array": [1, 3, 5, 7, 9], "target": 5}
      }
    ],
    "input_schema": {...}
  }
]
```

---

#### `POST /api/trace/unified`

**Purpose:** Generate trace for any registered algorithm.

**Request:**

```json
{
  "algorithm": "binary-search",
  "input": {
    "array": [1, 3, 5, 7, 9, 11, 13, 15],
    "target": 7
  }
}
```

**Response:**

```json
{
  "result": {
    "found": true,
    "index": 3,
    "comparisons": 3
  },
  "trace": {
    "steps": [
      {
        "step": 0,
        "type": "INITIAL_STATE",
        "timestamp": 0.001,
        "data": {
          "target": 7,
          "array_size": 8,
          "visualization": {
            "array": [
              {"index": 0, "value": 1, "state": "active_range"},
              ...
            ],
            "pointers": {"left": 0, "right": 7, "mid": null, "target": 7}
          }
        },
        "description": "🔍 Searching for 7 in sorted array of 8 elements"
      }
    ],
    "total_steps": 12,
    "duration": 0.023
  },
  "metadata": {
    "algorithm": "binary-search",
    "display_name": "Binary Search",           # REQUIRED
    "visualization_type": "array",             # REQUIRED
    "visualization_config": {...},
    "prediction_points": [...],
    "input_size": 8
  }
}
```

**Error Response (400):**

```json
{
  "error": "Unknown algorithm: 'merge-sort'",
  "available_algorithms": ["binary-search", "interval-coverage"]
}
```

---

#### `GET /api/health`

**Purpose:** Health check with registry info.

**Response:**

```json
{
  "status": "healthy",
  "service": "algorithm-trace-backend",
  "algorithms_registered": 2,
  "available_algorithms": ["binary-search", "interval-coverage"]
}
```

---

## Adding a New Algorithm (CRITICAL WORKFLOW)

**Time Investment:** 1-2 hours total

### Step 1: Implement AlgorithmTracer (30-45 min)

```python
# backend/algorithms/merge_sort.py
from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer

class MergeSortTracer(AlgorithmTracer):
    def __init__(self):
        super().__init__()
        self.array = []

    def execute(self, input_data: Any) -> dict:
        # Validate input
        self.array = input_data.get('array', [])
        if not self.array:
            raise ValueError("Array cannot be empty")

        # CRITICAL: Set required metadata fields
        self.metadata = {
            'algorithm': 'merge-sort',
            'display_name': 'Merge Sort',              # ← REQUIRED
            'visualization_type': 'array',             # ← REQUIRED
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True
            }
        }

        # Initial state
        self._add_step(
            "INITIAL_STATE",
            {'array': self.array.copy()},
            f"🔢 Starting merge sort on array of {len(self.array)} elements"
        )

        # Run algorithm with trace generation
        sorted_array = self._merge_sort_recursive(self.array, 0, len(self.array) - 1)

        # Final state
        self._add_step(
            "ALGORITHM_COMPLETE",
            {'sorted_array': sorted_array},
            "✅ Array sorted!"
        )

        # CRITICAL: Use _build_trace_result()
        return self._build_trace_result(sorted_array)

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """CRITICAL: Maximum 3 choices per question"""
        predictions = []
        for i, step in enumerate(self.trace):
            if step.type == "MERGE_DECISION":
                predictions.append({
                    'step_index': i,
                    'question': "Which element should be merged next?",
                    'choices': [  # ≤3 choices
                        {'id': 'left', 'label': 'Left subarray element'},
                        {'id': 'right', 'label': 'Right subarray element'}
                    ],
                    'correct_answer': 'left'
                })
        return predictions

    def _merge_sort_recursive(self, arr, left, right):
        # Implementation with _add_step() calls
        pass
```

---

### Step 2: Register in Registry (5 min)

```python
# backend/algorithms/registry.py

def register_algorithms():
    from .merge_sort import MergeSortTracer

    registry.register(
        name='merge-sort',                    # Unique ID (kebab-case)
        tracer_class=MergeSortTracer,
        display_name='Merge Sort',
        description='Divide-and-conquer sorting with O(n log n) complexity',
        example_inputs=[
            {
                'name': 'Basic Sort',
                'input': {'array': [5, 2, 8, 1, 9, 3]}
            }
        ]
    )
```

**That's it for backend!** No app.py changes needed. ✨

---

### Step 3: Backend Compliance Checklist (10 min)

Complete `docs/compliance/BACKEND_CHECKLIST.md`:

**Critical Checks:**

- [ ] Metadata has `algorithm`, `display_name`, `visualization_type`
- [ ] Trace structure matches contract
- [ ] Visualization state uses `state` (string), not `visual_state` (dict)
- [ ] Prediction points have ≤3 choices
- [ ] Inherits from `AlgorithmTracer`
- [ ] Uses `_add_step()` and `_build_trace_result()`

**Rule:** If >3 items fail, stop and fix before proceeding.

---

### Step 4: Create/Reuse Visualization (0-30 min)

**Option A: Reuse (0 min)** - Recommended for array-based algorithms

```python
self.metadata = {
    'visualization_type': 'array',  # Reuses ArrayView automatically
}
```

**Option B: New Component (30 min)** - For custom visualizations

```javascript
// frontend/src/components/visualizations/GraphView.jsx
const GraphView = ({ step, config = {} }) => {
  const visualization = step?.data?.visualization;

  return (
    // CRITICAL: Use items-start + mx-auto pattern
    <div className="h-full flex flex-col items-start overflow-auto py-4 px-6">
      <div className="mx-auto">{/* Your visualization */}</div>
    </div>
  );
};
```

---

### Step 5: Register Visualization (5 min, if new)

```javascript
// frontend/src/utils/visualizationRegistry.js
import GraphView from "../components/visualizations/GraphView";

const VISUALIZATION_REGISTRY = {
  array: ArrayView,
  timeline: TimelineView,
  graph: GraphView, // ← Add new component
};
```

---

### Step 6: Frontend & QA Checklists (15 min)

**Frontend Checklist (`docs/compliance/FRONTEND_CHECKLIST.md`):**

- [ ] Overflow pattern: `items-start` + `mx-auto` (NOT `items-center`)
- [ ] Modal IDs: `#prediction-modal`, `#completion-modal`
- [ ] Keyboard shortcuts work
- [ ] Component receives `step` and `config` props

**QA Checklist (`docs/compliance/QA_INTEGRATION_CHECKLIST.md`):**

- [ ] All 14 test suites pass
- [ ] No regressions in existing algorithms
- [ ] Overflow testing with 20+ elements

---

## Component Architecture

### Business Logic Hooks

- **`useTraceLoader`** - Fetch algorithm list and traces
- **`useTraceNavigation`** - Step controls (next/prev/reset)
- **`usePredictionMode`** - Prediction state management
- **`useVisualHighlight`** - Visual highlighting (Interval Coverage)
- **`useKeyboardShortcuts`** - Keyboard navigation

### UI Components

- **`AlgorithmSwitcher`** - Algorithm dropdown selector
- **`ControlBar`** - Navigation buttons
- **`PredictionModal`** - Interactive prediction prompts (ID: `#prediction-modal`)
- **`CompletionModal`** - Success screen with stats (ID: `#completion-modal`)
- **`KeyboardHints`** - Shortcut guide
- **Visualizations**: `ArrayView`, `TimelineView`, `CallStackView`

---

## Prediction Mode (Active Learning)

**Transform passive observation into active engagement.**

### How It Works

1. Algorithm identifies decision points via `get_prediction_points()`
2. Frontend pauses at these points
3. Student predicts outcome before seeing answer
4. Immediate feedback with accuracy tracking

### Example: Binary Search

```python
def get_prediction_points(self):
    predictions = []
    for i, step in enumerate(self.trace):
        if step.type == "CALCULATE_MID":
            predictions.append({
                'step_index': i,
                'question': f"Compare mid ({mid}) with target ({target}). What's next?",
                'choices': [  # ≤3 choices (CONSTRAINED)
                    {'id': 'found', 'label': 'Found!'},
                    {'id': 'search-left', 'label': 'Search Left'},
                    {'id': 'search-right', 'label': 'Search Right'}
                ],
                'correct_answer': 'search-right'
            })
    return predictions
```

### Keyboard Shortcuts (LOCKED)

| Keys           | Action                | Context             |
| -------------- | --------------------- | ------------------- |
| `→` or `Space` | Next step             | During navigation   |
| `←`            | Previous step         | During navigation   |
| `R` or `Home`  | Reset to start        | Anytime             |
| `End`          | Jump to end           | During navigation   |
| `K`            | Predict first option  | In prediction modal |
| `C`            | Predict second option | In prediction modal |
| `S`            | Skip question         | In prediction modal |
| `Enter`        | Submit answer         | In prediction modal |
| `Esc`          | Close modal           | In completion modal |

### Accuracy Feedback Tiers

- **90-100%**: "🎉 Excellent! You've mastered this algorithm!"
- **70-89%**: "👍 Great job! You have a solid understanding."
- **50-69%**: "📚 Good effort! Review the patterns for better accuracy."
- **<50%**: "💪 Keep practicing! Focus on understanding each decision."

---

## Environment Configuration

### Backend

```bash
# Required
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend-domain.com

# Optional
MAX_INTERVALS=100
MAX_STEPS=10000
```

### Frontend

```bash
# .env.development
REACT_APP_API_URL=http://localhost:5000/api

# .env.production
REACT_APP_API_URL=https://api.your-domain.com/api
```

---

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Expected Output:**

```
🚀 Algorithm Trace Backend Starting...
📍 Running on: http://localhost:5000
📊 Registered Algorithms: 2
   - interval-coverage: Interval Coverage
   - binary-search: Binary Search
```

### Frontend

```bash
cd frontend
npm install  # or: pnpm install
npm start    # or: pnpm start
```

Frontend runs on `http://localhost:3000`

---

## Testing

### Backend Testing

```bash
# Discovery endpoint
curl http://localhost:5000/api/algorithms | jq

# Unified endpoint - Binary Search
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "binary-search", "input": {"array": [1,3,5,7,9], "target": 5}}' | jq

# Error handling - Unknown algorithm
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{"algorithm": "unknown", "input": {}}' | jq
```

### Frontend Testing (Manual)

**Critical Tests:**

1. **Algorithm Discovery** - Dropdown shows all algorithms
2. **Visualization Types** - ArrayView (Binary Search), TimelineView (Interval Coverage)
3. **Overflow Handling** - Test with 20+ elements, verify no left-side cutoff
4. **Prediction Mode** - Enable, make predictions, check accuracy tracking
5. **Keyboard Shortcuts** - Test ←→ navigation, R reset, K/C/S prediction
6. **Modal IDs** - Verify `#prediction-modal`, `#completion-modal` exist
7. **Responsive** - Test 3 viewport sizes (desktop, tablet, mobile)

---

## Current Algorithms

| Algorithm             | Visualization | Status  | Prediction Points        |
| --------------------- | ------------- | ------- | ------------------------ |
| **Interval Coverage** | Timeline      | ✅ Live | Keep/Covered decisions   |
| **Binary Search**     | Array         | ✅ Live | Search direction choices |

---

## Deployment

### Backend (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Environment Variables:**

- `FLASK_ENV=production`
- `CORS_ORIGINS=https://your-frontend-domain.com`

### Frontend (Production)

```bash
npm run build  # Output: ./build/
```

**Deployment Options:** Vercel, Netlify, AWS S3+CloudFront, GitHub Pages

**Required:** `REACT_APP_API_URL=https://api.your-domain.com/api`

---

## Support

- **GitHub Issues:** Open with [Bug], [Feature], or [Question] tag
- **Documentation:**
  - `docs/TENANT_GUIDE.md` - Constitutional framework
  - `docs/compliance/` - Compliance checklists
  - `docs/compliance/CHECKLIST_SYSTEM_OVERVIEW.md` - Workflow guide

---

## License

MIT License

---

**Status:** ✅ Platform Architecture Complete - Ready for Algorithm Expansion

**Next Steps:** Add 3rd algorithm to validate scalability

---
