# Algorithm Visualization Platform

## Project Overview

An educational platform for visualizing algorithms with active learning features. Built on a **registry-based architecture** that makes adding new algorithms as simple as registering a class—no endpoint configuration required.

**Philosophy:** Backend does ALL the thinking, frontend does ALL the reacting.

**Status:** ✅ Platform Architecture Complete - 2 Algorithms Live (Interval Coverage, Binary Search)

---

## 🎯 What Makes This Platform Different?

### Traditional Approach (Rigid & Complex)

```python
# app.py - Must add endpoint for each algorithm
@app.route('/api/interval-coverage', methods=['POST'])
def interval_coverage_endpoint():
    # Algorithm-specific code
    pass

@app.route('/api/binary-search', methods=['POST'])
def binary_search_endpoint():
    # More algorithm-specific code
    pass

# And so on for every new algorithm...
```

```javascript
// Frontend - Must handle each algorithm explicitly
if (algorithm === 'binary-search') {
  return <ArrayView ... />
} else if (algorithm === 'interval-coverage') {
  return <TimelineView ... />
}
// Keep adding if-else chains...
```

### Our Approach (Extensible & Simple)

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

## Project Structure

```
interval-viz-poc/
├── backend/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── base_tracer.py          # ★ Abstract base class for all algorithms
│   │   ├── registry.py             # ★ Central algorithm registry
│   │   ├── interval_coverage.py    # Example: Interval Coverage algorithm
│   │   └── binary_search.py        # Example: Binary Search algorithm
│   ├── app.py                      # Flask API with unified routing
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AlgorithmSwitcher.jsx    # ★ Dynamic algorithm selector
│   │   │   ├── ControlBar.jsx           # Navigation controls
│   │   │   ├── CompletionModal.jsx      # Success screen with accuracy
│   │   │   ├── ErrorBoundary.jsx        # Error handling
│   │   │   ├── KeyboardHints.jsx        # Keyboard shortcuts display
│   │   │   ├── PredictionModal.jsx      # Interactive prediction prompts
│   │   │   └── visualizations/          # ★ Reusable visualization components
│   │   │       ├── ArrayView.jsx        # For array-based algorithms
│   │   │       ├── TimelineView.jsx     # For interval-based algorithms
│   │   │       ├── CallStackView.jsx    # For recursive algorithms
│   │   │       └── index.js
│   │   ├── hooks/                       # Custom React hooks
│   │   │   ├── useKeyboardShortcuts.js
│   │   │   ├── usePredictionMode.js
│   │   │   ├── useTraceLoader.js
│   │   │   ├── useTraceNavigation.js
│   │   │   └── useVisualHighlight.js
│   │   ├── utils/
│   │   │   ├── predictionUtils.js
│   │   │   ├── stepBadges.js
│   │   │   └── visualizationRegistry.js # ★ Dynamic visualization selection
│   │   ├── App.jsx                      # Main container
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── docs/
│   ├── TENANT_GUIDE.md                  # ★ Constitutional framework (LOCKED/CONSTRAINED/FREE)
│   ├── compliance/                      # ★ Compliance checklists
│   │   ├── BACKEND_CHECKLIST.md         # For backend developers
│   │   ├── FRONTEND_CHECKLIST.md        # For frontend developers
│   │   ├── QA_INTEGRATION_CHECKLIST.md  # For QA engineers
│   │   └── CHECKLIST_SYSTEM_OVERVIEW.md # System documentation
│   └── static_mockup/                   # Visual reference mockups
│       ├── algorithm_page_mockup.html
│       ├── prediction_modal_mockup.html
│       └── completion_modal_mockup.html
│
└── README.md

★ = New/key files for registry architecture
```

---

## Key Architecture Decisions

### 1. The Registry Pattern (★ Core Innovation)

**Decision:** Algorithms self-register with metadata; frontend discovers them dynamically.

**How It Works:**

```python
# backend/algorithms/registry.py
registry.register(
    name='binary-search',                      # Unique identifier
    tracer_class=BinarySearchTracer,           # Your algorithm class
    display_name='Binary Search',              # UI display name
    description='Search sorted array...',      # Brief description
    example_inputs=[...],                      # Example test cases
    input_schema={...}                         # Optional validation schema
)
```

**Benefits:**

- ✅ Add algorithm → It appears in UI automatically
- ✅ Zero changes to `app.py` routing logic
- ✅ Frontend gets algorithm list via `GET /api/algorithms`
- ✅ Consistent metadata structure enforced
- ✅ Example inputs bundled with algorithm

**Code Impact:** ~200 lines for registry system, eliminates 20+ lines per algorithm in `app.py`

---

### 2. Unified API Endpoint (★ Simplification)

**Decision:** Single `/api/trace/unified` endpoint routes to any registered algorithm.

**Old Approach (Deprecated):**

```bash
POST /api/trace                  # Interval Coverage only
POST /api/trace/binary-search    # Binary Search only
POST /api/trace/merge-sort       # Need to add endpoint...
POST /api/trace/dijkstra         # Need to add endpoint...
```

**New Approach:**

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

**Result:** One endpoint, infinite algorithms. 🚀

---

### 3. Dynamic Visualization Selection (★ Frontend Flexibility)

**Decision:** Algorithms declare their visualization type via metadata; frontend selects component dynamically.

**How It Works:**

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

**Visualization Registry:**

```javascript
// frontend/src/utils/visualizationRegistry.js
const VISUALIZATION_REGISTRY = {
  array: ArrayView, // For Binary Search, Sorting algorithms
  timeline: TimelineView, // For Interval Coverage
  graph: GraphView, // Future: DFS, BFS, Dijkstra
  tree: TreeView, // Future: BST, Heap operations
};
```

**Benefits:**

- ✅ Binary Search reuses `ArrayView` (zero new visualization code)
- ✅ Merge Sort, Quick Sort can reuse `ArrayView`
- ✅ Graph algorithms can share `GraphView`
- ✅ No if-else chains in frontend routing

---

### 4. Base Tracer Abstraction

**Decision:** All algorithms inherit from `AlgorithmTracer` for consistency.

**Required Methods:**

```python
class AlgorithmTracer(ABC):
    @abstractmethod
    def execute(self, input_data: Any) -> dict:
        """
        Execute algorithm and return standardized result:
        {
            "result": <algorithm output>,
            "trace": {"steps": [...], "total_steps": N, "duration": T},
            "metadata": {
                "algorithm": "name",
                "display_name": "Display Name",  # Required
                "visualization_type": "array",   # Required
                "visualization_config": {...},
                "prediction_points": [...]       # Auto-generated
            }
        }
        """
        pass

    @abstractmethod
    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction moments for active learning.
        Returns: [
            {
                "step_index": 5,
                "question": "Will we search left or right?",
                "choices": [
                    {"id": "left", "label": "Search Left"},
                    {"id": "right", "label": "Search Right"}
                ],
                "hint": "Compare mid with target",
                "correct_answer": "right"
            },
            ...
        ]
        """
        pass
```

**Optional Hook:**

```python
def _get_visualization_state(self) -> dict:
    """
    Automatically enrich each trace step with visualization data.
    Called by _add_step() to inject current state.
    """
    return {
        'array': [...],      # Current array state
        'pointers': {...},   # Left, right, mid pointers
        ...
    }
```

**Benefits:**

- ✅ Enforces consistent trace structure
- ✅ Automatic prediction point generation
- ✅ Built-in step recording with `_add_step()`
- ✅ Safety limits (MAX_STEPS = 10,000 prevents infinite loops)
- ✅ Standardized error handling

---

### 5. Backend-Generated Traces (Retained from POC)

**Decision:** Backend generates complete execution trace upfront.

**Benefits:**

- ✅ Frontend has zero algorithm logic
- ✅ Traces are deterministic and replayable
- ✅ Easier debugging (backend bugs vs UI bugs)
- ✅ Backend can be unit tested independently
- ✅ Supports prediction mode without re-execution

**Trade-offs:**

- ⚠️ Larger initial payload (~30-50KB for typical inputs)
- ⚠️ Backend must anticipate visualization needs

---

### 6. Prediction Mode for Active Learning (Retained)

**Decision:** Interactive prediction layer transforms passive observation into active engagement.

**How It Works:**

1. Algorithm identifies decision points via `get_prediction_points()`
2. Frontend pauses at these points and shows modal
3. Student predicts outcome before seeing answer
4. Immediate feedback with accuracy tracking

**Example (Binary Search):**

```python
def get_prediction_points(self):
    predictions = []
    for i, step in enumerate(self.trace):
        if step.type == "CALCULATE_MID":
            next_step = self.trace[i + 1]
            predictions.append({
                'step_index': i,
                'question': f"Compare mid ({mid_value}) with target ({target}). What's next?",
                'choices': [
                    {'id': 'found', 'label': 'Found!'},
                    {'id': 'search-left', 'label': 'Search Left'},
                    {'id': 'search-right', 'label': 'Search Right'}
                ],
                'correct_answer': 'search-right'  # From next_step.type
            })
    return predictions
```

**Pedagogical Impact:**

- 🎯 Forces active thinking at critical moments
- ✅ Provides immediate reinforcement
- 📊 Tracks accuracy for self-assessment
- 🔄 Mirrors real problem-solving (predict → verify → learn)

---

### 7. Component Extraction & Hooks (Architecture Evolution)

**Decision:** Split monolithic `App.jsx` into specialized hooks and components.

**Original:** 570-line `App.jsx` with mixed concerns

**Current Architecture:**

- **Hooks (Business Logic):**

  - `useTraceLoader` - Fetch traces from backend
  - `useTraceNavigation` - Step controls (next/prev/reset)
  - `usePredictionMode` - Prediction state management
  - `useVisualHighlight` - Visual highlighting for Interval Coverage
  - `useKeyboardShortcuts` - Keyboard navigation

- **Components (UI):**
  - `AlgorithmSwitcher` - Dropdown selector
  - `ControlBar` - Navigation buttons
  - `PredictionModal` - Prediction prompts
  - `CompletionModal` - Success screen
  - `KeyboardHints` - Shortcut guide
  - Visualization components (ArrayView, TimelineView, CallStackView)

**Benefits:**

- ✅ Easier to maintain and debug
- ✅ Reusable hooks across components
- ✅ Clear separation of concerns
- ✅ Enables independent testing

---

## API Documentation

### Primary Endpoints (Use These)

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
        "input": {
          "array": [1, 3, 5, 7, 9],
          "target": 5
        }
      }
    ],
    "input_schema": {...}
  },
  {
    "name": "interval-coverage",
    "display_name": "Interval Coverage",
    "description": "Remove covered intervals using greedy strategy",
    "example_inputs": [...]
  }
]
```

**Use Case:** Populate algorithm selector dropdown in UI.

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
              {"index": 1, "value": 3, "state": "active_range"},
              ...
            ],
            "pointers": {"left": 0, "right": 7, "mid": null, "target": 7}
          }
        },
        "description": "🔍 Searching for 7 in sorted array of 8 elements"
      },
      ...
    ],
    "total_steps": 12,
    "duration": 0.023
  },
  "metadata": {
    "algorithm": "binary-search",
    "display_name": "Binary Search",
    "visualization_type": "array",
    "visualization_config": {
      "element_renderer": "number",
      "show_indices": true
    },
    "prediction_points": [
      {
        "step_index": 1,
        "question": "Compare mid (3) with target (7). What's next?",
        "choices": [
          {"id": "found", "label": "Found!"},
          {"id": "search-left", "label": "Search Left"},
          {"id": "search-right", "label": "Search Right"}
        ],
        "correct_answer": "search-right"
      }
    ],
    "input_size": 8,
    "target_value": 7
  }
}
```

**Error Response (400 Bad Request):**

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

### Legacy Endpoints (Deprecated)

These endpoints still work for backward compatibility but should not be used for new integrations.

⚠️ **Use `/api/trace/unified` instead**

- `POST /api/trace` - Interval Coverage (legacy)
- `POST /api/trace/binary-search` - Binary Search (legacy)
- `GET /api/examples` - Interval Coverage examples (legacy)
- `GET /api/examples/binary-search` - Binary Search examples (legacy)

---

## Compliance & Standards

This platform follows the **Tenant Guide** (`docs/TENANT_GUIDE.md`), which defines a three-tier requirement system:

### Requirement Tiers

1. **LOCKED Requirements** ⛔ - Cannot be changed without major version bump

   - API contracts (trace structure, metadata fields)
   - Modal behavior (HTML IDs, keyboard shortcuts, auto-scroll)
   - Panel layout patterns

2. **CONSTRAINED Requirements** ⚠️ - Limited flexibility with defined bounds

   - Visualization data patterns (array/timeline/graph)
   - Prediction format (≤3 choices)
   - Step type categorization

3. **FREE Zones** ✅ - Full creative freedom
   - Internal algorithm implementation
   - Performance optimizations
   - Custom visualization styles

### Compliance Checklists

All new algorithms must pass three compliance checklists:

#### 1. Backend Compliance (`docs/compliance/BACKEND_CHECKLIST.md`)

**For:** Backend Python developers implementing algorithm tracers

**Validates:**

- ✅ Metadata structure (`algorithm`, `display_name`, `visualization_type`)
- ✅ Trace format (steps array, timestamps, descriptions)
- ✅ Visualization data contracts (state strings, pointer objects)
- ✅ Prediction points format
- ✅ Base class compliance (`AlgorithmTracer` inheritance)

**Anti-Patterns Caught:**

- ❌ Missing `display_name` field
- ❌ Using `visual_state` dict instead of `state` string
- ❌ >3 choices in prediction questions
- ❌ Hardcoding visualization logic in tracer

---

#### 2. Frontend UI/UX Compliance (`docs/compliance/FRONTEND_CHECKLIST.md`)

**For:** Frontend React developers implementing UI components

**Validates:**

- ✅ Modal standards (IDs: `#prediction-modal`, `#completion-modal`)
- ✅ Panel layout (items-start + mx-auto overflow pattern)
- ✅ Keyboard shortcuts (←→ navigation, R reset, K/C/S prediction)
- ✅ Auto-scroll behavior in call stack
- ✅ Visualization component interface

**Anti-Patterns Caught:**

- ❌ Using `items-center` (causes overflow cutoff)
- ❌ Missing auto-scroll on active element
- ❌ Non-standard modal IDs
- ❌ Breaking keyboard shortcuts

---

#### 3. QA & Integration (`docs/compliance/QA_INTEGRATION_CHECKLIST.md`)

**For:** QA engineers, integration testers, CI/CD pipelines

**Validates:**

- ✅ All 14 test suites pass (modals, layout, keyboard, responsive, etc.)
- ✅ Cross-algorithm compatibility
- ✅ No regressions in existing algorithms
- ✅ Performance benchmarks met

**Test Coverage:**

- Suite 1-6: LOCKED requirements (modals, IDs, keyboard, auto-scroll, overflow)
- Suite 7-10: CONSTRAINED requirements (backend contract, prediction, completion)
- Suite 11-14: Integration tests (cross-algorithm, responsive, performance, regression)

---

### Why Compliance Matters

✅ **Consistency** - All algorithms look and feel the same
✅ **Quality** - Prevents architectural drift and bugs
✅ **Speed** - Clear standards accelerate development
✅ **Automation** - Enables LLM-driven development with guardrails
✅ **Maintainability** - Future developers know exactly what's expected

**Workflow:** Backend checklist → Frontend checklist → QA checklist → Production ✅

See `docs/compliance/CHECKLIST_SYSTEM_OVERVIEW.md` for detailed workflow and integration with LLM-assisted development.

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (or pnpm)
- pip and npm/pnpm

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py
```

Backend will run on `http://localhost:5000`

**You should see:**

```
🚀 Algorithm Trace Backend Starting...
📍 Running on: http://localhost:5000
📊 Registered Algorithms: 2
   - interval-coverage: Interval Coverage
   - binary-search: Binary Search

📡 Available endpoints:
   GET  /api/algorithms               - List all algorithms (NEW)
   POST /api/trace/unified            - Unified trace endpoint (NEW)
   ...
```

---

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
# or if using pnpm:
pnpm install

# Run frontend
npm start
# or:
pnpm start
```

Frontend will run on `http://localhost:3000`

**Features Available:**

- ✅ Algorithm selector dropdown (top-left)
- ✅ Step-by-step navigation (arrow keys or buttons)
- ✅ Prediction mode toggle (⏳ Predict / ⚡ Watch)
- ✅ Keyboard shortcuts (press keyboard icon to see)
- ✅ Visual highlighting and hover effects
- ✅ Completion modal with accuracy statistics

---

## Contributing: Adding a New Algorithm

### Overview

Adding a new algorithm requires **6 steps** and takes approximately **1-2 hours** including testing and compliance validation.

**The Golden Rule:** You do NOT modify `app.py` routing logic. The registry handles everything automatically.

---

### Step 1: Inherit from `AlgorithmTracer`

Create your algorithm file in `backend/algorithms/`:

```python
# backend/algorithms/merge_sort.py
from typing import Any, List, Dict
from .base_tracer import AlgorithmTracer

class MergeSortTracer(AlgorithmTracer):
    """
    Merge Sort algorithm with complete trace generation.
    """

    def __init__(self):
        super().__init__()
        self.array = []

    def execute(self, input_data: Any) -> dict:
        """
        Execute merge sort and generate trace.

        Args:
            input_data: {"array": [5, 2, 8, 1, 9]}

        Returns:
            Standardized trace result
        """
        # Validate input
        self.array = input_data.get('array', [])
        if not self.array:
            raise ValueError("Array cannot be empty")

        # Set metadata (REQUIRED FIELDS)
        self.metadata = {
            'algorithm': 'merge-sort',
            'display_name': 'Merge Sort',              # ← Required
            'visualization_type': 'array',             # ← Required
            'visualization_config': {
                'element_renderer': 'number',
                'show_indices': True
            },
            'input_size': len(self.array)
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
            f"✅ Array sorted! {len(self.array)} elements in order."
        )

        # Return standardized result
        return self._build_trace_result(sorted_array)

    def _get_visualization_state(self) -> dict:
        """
        Optional: Automatically enrich steps with visualization data.
        """
        return {
            'array': [
                {'index': i, 'value': v, 'state': self._get_element_state(i)}
                for i, v in enumerate(self.array)
            ]
        }

    def get_prediction_points(self) -> List[Dict[str, Any]]:
        """
        Identify prediction moments for active learning.
        """
        predictions = []

        for i, step in enumerate(self.trace):
            if step.type == "MERGE_DECISION":
                # Create prediction question
                predictions.append({
                    'step_index': i,
                    'question': "Which element should be merged next?",
                    'choices': [
                        {'id': 'left', 'label': 'Left subarray element'},
                        {'id': 'right', 'label': 'Right subarray element'}
                    ],
                    'hint': 'Compare the current elements from both subarrays',
                    'correct_answer': 'left'  # Determine from next step
                })

        return predictions

    def _merge_sort_recursive(self, arr, left, right):
        """Your algorithm implementation with _add_step() calls"""
        # ... implementation with trace generation ...
        pass
```

**Key Requirements:**

- ✅ Inherit from `AlgorithmTracer`
- ✅ Implement `execute(input_data)` → Returns standardized dict
- ✅ Implement `get_prediction_points()` → Returns prediction list
- ✅ Set `metadata['display_name']` (required field)
- ✅ Set `metadata['visualization_type']` (required field)
- ✅ Use `_add_step()` for trace generation
- ✅ Return `self._build_trace_result(your_result)`

---

### Step 2: Register in Registry

Add registration to `backend/algorithms/registry.py`:

```python
# backend/algorithms/registry.py

def register_algorithms():
    """Register all available algorithm tracers."""

    # Import your algorithm
    from .merge_sort import MergeSortTracer

    # ... existing registrations ...

    # Add your registration
    registry.register(
        name='merge-sort',                    # Unique ID (kebab-case)
        tracer_class=MergeSortTracer,         # Your class
        display_name='Merge Sort',            # UI display name
        description='Divide-and-conquer sorting algorithm with O(n log n) time complexity',
        example_inputs=[
            {
                'name': 'Basic Sort - Random Order',
                'input': {
                    'array': [5, 2, 8, 1, 9, 3]
                }
            },
            {
                'name': 'Already Sorted',
                'input': {
                    'array': [1, 2, 3, 4, 5]
                }
            },
            {
                'name': 'Reverse Order',
                'input': {
                    'array': [9, 7, 5, 3, 1]
                }
            }
        ],
        input_schema={                        # Optional but recommended
            'type': 'object',
            'required': ['array'],
            'properties': {
                'array': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'minItems': 1,
                    'maxItems': 100
                }
            }
        }
    )
```

**That's it for backend!** No changes to `app.py` needed. The unified endpoint automatically routes to your algorithm. ✨

---

### Step 3: Run Backend Compliance Checklist

Complete `docs/compliance/BACKEND_CHECKLIST.md` to validate your implementation.

**Critical Checks:**

- [ ] Metadata has `algorithm`, `display_name`, `visualization_type`
- [ ] Trace structure matches contract (steps array, timestamps, descriptions)
- [ ] Visualization state uses `state` (string), not `visual_state` (dict)
- [ ] Prediction points have ≤3 choices
- [ ] Inherits from `AlgorithmTracer`
- [ ] Uses `_add_step()` for trace generation
- [ ] Returns `self._build_trace_result()`

**If >3 checklist items fail:** Stop and fix issues before proceeding to frontend.

---

### Step 4: Create or Reuse Visualization Component

**Option A: Reuse Existing Component** (Recommended)

If your algorithm is array-based (sorting, searching):

```python
# In your tracer's execute() method
self.metadata = {
    'visualization_type': 'array',  # Reuses ArrayView component
    ...
}
```

**Result:** Zero frontend code needed! ArrayView handles it automatically.

**Option B: Create New Visualization Component**

For custom visualizations (graphs, trees, matrices):

```javascript
// frontend/src/components/visualizations/GraphView.jsx
import React from "react";

const GraphView = ({ step, config = {} }) => {
  const visualization = step?.data?.visualization;

  if (!visualization || !visualization.graph) {
    return <div>No graph data available</div>;
  }

  const { nodes, edges } = visualization.graph;

  return (
    <div className="h-full flex flex-col items-start overflow-auto py-4 px-6">
      <div className="mx-auto">
        {/* Your graph visualization */}
        {nodes.map((node) => (
          <div key={node.id} className={getNodeClasses(node.state)}>
            {node.label}
          </div>
        ))}
      </div>
    </div>
  );
};

export default GraphView;
```

**Important:** Follow the overflow pattern:

```javascript
// CORRECT: items-start on outer, mx-auto on inner
<div className="... items-start overflow-auto">
  <div className="mx-auto">
    {/* content */}
  </div>
</div>

// INCORRECT: items-center causes overflow cutoff
<div className="... items-center overflow-auto"> ❌
```

---

### Step 5: Register Visualization (If New)

```javascript
// frontend/src/utils/visualizationRegistry.js
import GraphView from "../components/visualizations/GraphView";

const VISUALIZATION_REGISTRY = {
  array: ArrayView,
  timeline: TimelineView,
  graph: GraphView, // ← Add your new component
  // ...
};
```

---

### Step 6: Run Frontend & QA Compliance Checklists

#### Frontend Checklist (`docs/compliance/FRONTEND_CHECKLIST.md`)

**Critical Checks:**

- [ ] Overflow pattern: `items-start` + `mx-auto` (not `items-center`)
- [ ] Modal IDs: `#prediction-modal`, `#completion-modal`
- [ ] Keyboard shortcuts work (←→ navigation, R reset)
- [ ] Auto-scroll to active element in call stack
- [ ] Component receives `step` and `config` props

#### QA Checklist (`docs/compliance/QA_INTEGRATION_CHECKLIST.md`)

**Test Suites:**

- [ ] Suite 1-6: LOCKED requirements (modals, IDs, keyboard, overflow)
- [ ] Suite 7-10: CONSTRAINED requirements (backend contract, predictions)
- [ ] Suite 11: Cross-algorithm compatibility (no regressions)
- [ ] Suite 12: Responsive testing (3 viewport sizes)
- [ ] Suite 13: Performance benchmarks (<100ms trace gen)
- [ ] Suite 14: Regression testing (existing algorithms still work)

---

### Result: Algorithm Is Live! 🎉

**What happens next:**

1. ✅ Restart backend → Algorithm appears in registry
2. ✅ Refresh frontend → Algorithm appears in dropdown
3. ✅ Select from dropdown → Examples load automatically
4. ✅ Click example → Trace generates and visualizes
5. ✅ Enable prediction mode → Interactive questions appear
6. ✅ Complete trace → Accuracy statistics shown

**Time investment:**

- Step 1-2 (Backend): 30-45 minutes
- Step 3 (Backend Checklist): 10 minutes
- Step 4-5 (Frontend): 0-30 minutes (0 if reusing, 30 if new component)
- Step 6 (Compliance): 15 minutes
- **Total: 1-2 hours** ⏱️

---

## Algorithm Gallery

| Algorithm             | Visualization | Status     | Prediction Points        | Complexity |
| --------------------- | ------------- | ---------- | ------------------------ | ---------- |
| **Interval Coverage** | Timeline      | ✅ Live    | Keep/Covered decisions   | Greedy     |
| **Binary Search**     | Array         | ✅ Live    | Search direction choices | O(log n)   |
| Merge Sort            | Array         | 🔄 Planned | Merge decisions          | O(n log n) |
| Quick Sort            | Array         | 🔄 Planned | Pivot selection          | O(n log n) |
| Depth-First Search    | Graph         | 🔄 Planned | Next node selection      | O(V+E)     |
| Dijkstra's Algorithm  | Graph         | 🔄 Planned | Path selection           | O(E log V) |

**Legend:**

- ✅ Live - Available in production
- 🔄 Planned - Architecture supports, implementation pending
- 🎯 In Progress - Currently being developed

---

## Active Learning Features

### 🎯 Prediction Mode

Transform passive observation into active engagement by predicting algorithm decisions before they're revealed.

**How It Works:**

1. **Enable Prediction Mode** - Click "⏳ Predict" button (top-right)
2. **Algorithm Pauses** - At decision points identified by `get_prediction_points()`
3. **Make Prediction** - Choose from 2-3 options
4. **Immediate Feedback** - See if you're correct with explanation
5. **Track Accuracy** - Real-time percentage displayed
6. **Completion Stats** - Final accuracy with encouraging feedback

**Example: Binary Search**

```
Question: "Compare mid (7) with target (9). What's next?"

Choices:
  • Found! (7 == 9)
  • Search Left (7 > 9)
  • Search Right (7 < 9)  ← Correct!

Explanation: "7 < 9, so target must be in right half (larger values)"
```

**Example: Interval Coverage**

```
Question: "Will interval (600, 720) be kept or covered?"

Choices:
  • Keep this interval  ← Correct!
  • Covered by previous

Explanation: "✅ KEEP: end=720 > max_end=660 — this interval extends coverage"
```

**Keyboard Shortcuts:**

- `K` - Predict first option (often "KEEP" or "LEFT")
- `C` - Predict second option (often "COVERED" or "RIGHT")
- `S` - Skip question
- `Enter` - Submit answer

**Pedagogical Impact:**

- 🎯 Forces active thinking at critical moments
- ✅ Provides immediate reinforcement of correct understanding
- 📊 Identifies gaps in comprehension through accuracy metrics
- 🔄 Mirrors real problem-solving: predict → verify → learn
- 🏆 Gamification element increases engagement

**Accuracy Feedback:**

- 90-100%: "🎉 Excellent! You've mastered this algorithm!"
- 70-89%: "👍 Great job! You have a solid understanding."
- 50-69%: "📚 Good effort! Review the patterns for better accuracy."
- <50%: "💪 Keep practicing! Focus on understanding each decision."

---

### 🔗 Visual Bridge Between Views

**Problem Solved:** Students struggle to mentally map abstract recursion (call stack) to concrete intervals (timeline).

**Solution:** Automatic highlighting creates direct visual connection.

**Features:**

- **Auto-highlight** - Active call stack entry glows on timeline with yellow ring
- **Dimming effect** - Non-active intervals fade to 40% opacity for focus
- **Hover sync** - Hover over any call stack entry to highlight its interval
- **Smooth transitions** - 300ms GPU-accelerated animations (60fps)
- **Smart priority** - Hover overrides automatic highlighting for exploration

**Visual Indicators:**

- 🟡 **Yellow ring + glow** - Currently highlighted interval
- 🟡 **Yellow border** - Interval being examined by algorithm
- 🔵 **Cyan line** - max_end coverage tracker
- ⚫ **Dimmed (40%)** - Intervals not currently relevant

**Code Implementation:**

```javascript
// App.jsx - Pass highlight props to TimelineView
<TimelineView
  step={step}
  highlightedIntervalId={effectiveHighlight} // Auto or hover
  onIntervalHover={handleIntervalHover} // Bidirectional sync
/>
```

**Pedagogical Impact:**

- ✅ Reduces cognitive load (no manual mapping needed)
- ✅ Makes recursion concrete (see which interval each call processes)
- ✅ Enables exploration without committing to step changes
- ✅ Guides attention to relevant information
- ✅ Students learn faster with less frustration

---

### 📚 Enhanced Step Descriptions

**Problem Solved:** Mechanical descriptions ("Decision: KEEP") don't teach WHY decisions are made.

**Solution:** Educational descriptions explain the greedy strategy, not just mechanics.

**Step Type Badges** (7 Categories):

- ⚖️ **DECISION** (green) - Keep/covered decisions
- 📊 **COVERAGE** (cyan) - max_end updates
- 🔍 **EXAMINE** (yellow) - Interval comparisons
- 🔄 **RECURSION** (blue) - Recursive calls
- 🎯 **BASE CASE** (purple) - Termination conditions
- 📊 **SORT** (orange) - Sorting steps
- 🎬 **STATE** (pink) - Algorithm state changes

**Enhanced Descriptions:**

Before (Mechanical):

```
"Decision: KEEP"
"max_end updated to 720"
```

After (Educational):

```
"✅ KEEP: end=720 > max_end=660 — this interval extends our coverage,
so we must keep it to ensure complete interval coverage."

"Coverage extended: max_end updated from 660 → 720
(now we can skip any intervals ending ≤ 720)"
```

**Implementation:**

```python
# backend/algorithms/interval_coverage.py
if is_covered:
    explanation = (
        f"❌ COVERED: end={current.end} ≤ max_end={max_end} "
        f"— an earlier interval already covers this range, so we can skip it safely."
    )
else:
    explanation = (
        f"✅ KEEP: end={current.end} > max_end={max_end} "
        f"— this interval extends our coverage, so we must keep it."
    )

self._add_step("DECISION_MADE", {...}, explanation)
```

**Pedagogical Impact:**

- ✅ Students learn WHY decisions are made, not just WHAT
- ✅ Greedy strategy is explicit (not inferred)
- ✅ Reduces confusion with clear step categorization
- ✅ Works synergistically with prediction mode
- ✅ Color-coded badges help orient students in execution flow

---

## Keyboard Shortcuts

Master efficient navigation with these shortcuts:

| Keys           | Action                | Context             |
| -------------- | --------------------- | ------------------- |
| `→` or `Space` | Next step             | During navigation   |
| `←`            | Previous step         | During navigation   |
| `R` or `Home`  | Reset to start        | Anytime             |
| `End`          | Jump to end           | During navigation   |
| `Esc`          | Close modal           | In completion modal |
| `K`            | Predict first option  | In prediction modal |
| `C`            | Predict second option | In prediction modal |
| `S`            | Skip question         | In prediction modal |
| `Enter`        | Submit answer         | In prediction modal |

**Tip:** Click the keyboard icon (bottom-right) to see shortcuts anytime.

**Implementation:** Handled by `useKeyboardShortcuts` hook with modal awareness (shortcuts disabled when modals are open except for modal-specific shortcuts).

---

## Environment Configuration

The application uses environment variables for deployment flexibility:

**Development** (`.env.development`):

```bash
REACT_APP_API_URL=http://localhost:5000/api
```

**Production** (`.env.production`):

```bash
REACT_APP_API_URL=https://your-backend-domain.com/api
```

**Local Overrides** (create `.env.development.local` if needed):

```bash
REACT_APP_API_URL=http://localhost:9999/api
```

**Usage in Code:**

```javascript
// frontend/src/hooks/useTraceLoader.js
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000/api";
```

---

## Testing

### Backend Testing

```bash
cd backend
python app.py
```

**Test with curl:**

```bash
# Test discovery endpoint
curl http://localhost:5000/api/algorithms | jq

# Test unified endpoint - Binary Search
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "binary-search",
    "input": {
      "array": [1, 3, 5, 7, 9],
      "target": 5
    }
  }' | jq

# Test unified endpoint - Interval Coverage
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "interval-coverage",
    "input": {
      "intervals": [
        {"id": 1, "start": 540, "end": 660, "color": "blue"},
        {"id": 2, "start": 600, "end": 720, "color": "green"}
      ]
    }
  }' | jq

# Test error handling - Unknown algorithm
curl -X POST http://localhost:5000/api/trace/unified \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "unknown-algorithm",
    "input": {}
  }' | jq
# Should return 404 with available algorithms list
```

---

### Frontend Testing

#### 1. **Algorithm Discovery & Switching**

- Start both backend and frontend
- Open browser to `http://localhost:3000`
- Click algorithm dropdown (top-left, next to title)
- Verify both "Interval Coverage" and "Binary Search" appear
- Switch between algorithms
- Verify UI updates correctly for each algorithm

#### 2. **Binary Search Visualization**

- Select "Binary Search" from dropdown
- Click one of the example inputs
- Verify ArrayView displays with:
  - Target indicator at top
  - Array elements in grid layout (wraps to multiple rows)
  - Pointers (L, R, M) below elements
  - State legend at bottom
- Navigate steps and verify:
  - Active range (blue), examining (yellow), excluded (gray) states
  - Pointers update correctly
  - Search space counter decreases

#### 3. **Interval Coverage Visualization**

- Select "Interval Coverage" from dropdown
- Click an example input
- Verify TimelineView displays with:
  - Intervals on horizontal timeline
  - Call stack in right panel
  - Visual highlighting when hovering call stack
- Test hover effect:
  - Hover over call stack entry
  - Verify corresponding interval highlights on timeline
  - Verify other intervals dim to 40%

#### 4. **Prediction Mode**

- Enable prediction mode (click "⏳ Predict" button)
- Navigate to a decision point
- Verify modal appears with:
  - Question about next decision
  - 2-3 choice buttons
  - Skip button
- Make prediction:
  - Click a choice (or press K/C)
  - Verify immediate feedback (✅ correct or ❌ incorrect)
  - Verify explanation appears
- Check accuracy tracking:
  - Make several predictions
  - Verify percentage updates in header
  - Complete trace and verify completion modal shows final stats

#### 5. **Keyboard Shortcuts**

- Test navigation: → (next), ← (prev), R (reset), End (jump)
- Test prediction shortcuts: K, C, S
- Click keyboard icon (bottom-right) to verify hints display
- Verify shortcuts work across both algorithms

#### 6. **Overflow Handling** (Critical!)

- Test with large arrays (20+ elements)
- Verify content doesn't get cut off on left side
- Scroll vertically to see all content
- Verify no horizontal scrollbar appears

#### 7. **Error Handling**

- Stop backend: `Ctrl+C` in backend terminal
- Refresh frontend
- Verify error screen appears with "Backend Not Available"
- Click "Retry Connection" button
- Restart backend
- Verify connection restores

#### 8. **Responsive Testing**

- Test on 3 viewport sizes:
  - Desktop (1920x1080)
  - Tablet (768x1024)
  - Mobile (375x667)
- Verify layouts adapt appropriately
- Verify no content overflow or cutoff

---

## Performance Metrics

| Metric                    | Target  | Current Status                    |
| ------------------------- | ------- | --------------------------------- |
| Backend trace generation  | <100ms  | ✅ ~20-50ms                       |
| JSON payload size         | <100KB  | ✅ ~30-50KB                       |
| Frontend render time      | 60fps   | ✅ Smooth, GPU-accelerated        |
| Algorithm registration    | <1 hour | ✅ ~30-45 minutes                 |
| Component reuse rate      | 80%+    | ✅ Binary Search reuses ArrayView |
| Prediction modal response | <50ms   | ✅ Instant                        |
| Registry lookup time      | <1ms    | ✅ O(1) dictionary lookup         |
| Frontend hot reload       | <2s     | ✅ Fast development iteration     |

---

## Deployment

### Backend (Production)

```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or use Flask directly (not recommended for production)
FLASK_ENV=production python app.py
```

**Environment Variables:**

- `FLASK_ENV=production`
- `CORS_ORIGINS=https://your-frontend-domain.com`
- `MAX_INTERVALS=100` (optional)
- `MAX_STEPS=10000` (optional)

**Health Check Endpoint:** `GET /api/health`

---

### Frontend (Production)

```bash
# Build for production
npm run build
# or:
pnpm build

# Output: ./build/ directory with static files
```

**Deployment Options:**

- **Vercel:** Connect GitHub repo, auto-deploys on push
- **Netlify:** Drag-and-drop `build/` folder
- **AWS S3 + CloudFront:** Static hosting with CDN
- **GitHub Pages:** Free hosting for public repos

**Required Environment Variable:**

```bash
REACT_APP_API_URL=https://api.your-domain.com/api
```

**Build Command:** `npm run build`
**Publish Directory:** `build`

---

## Roadmap

### ✅ Completed (Current Version)

**Platform Architecture:**

- ✅ Registry-based algorithm system
- ✅ Unified API endpoint (`/api/trace/unified`)
- ✅ Dynamic visualization selection
- ✅ Base tracer abstraction (`AlgorithmTracer`)
- ✅ Compliance framework (3 checklists + Tenant Guide)
- ✅ Component extraction (7+ components, 5 hooks)

**Algorithms:**

- ✅ Interval Coverage (Timeline visualization)
- ✅ Binary Search (Array visualization)

**Active Learning:**

- ✅ Prediction mode with accuracy tracking
- ✅ Visual highlighting and hover effects
- ✅ Enhanced step descriptions
- ✅ Keyboard shortcuts

**Quality:**

- ✅ Error boundaries and safe data access
- ✅ Backend input validation with Pydantic
- ✅ Overflow pattern (no content cutoff)
- ✅ Responsive design

---

### 🔄 Next Phase (V2.0)

**New Algorithms (Reusing Existing Visualizations):**

- [ ] Merge Sort (array visualization)
- [ ] Quick Sort (array visualization)
- [ ] Insertion Sort (array visualization)

**New Visualization Types:**

- [ ] Graph visualization component (for DFS, BFS, Dijkstra)
- [ ] Tree visualization component (for BST, Heap)
- [ ] Matrix visualization component (for Dynamic Programming)

**Platform Enhancements:**

- [ ] Algorithm comparison mode (side-by-side execution)
- [ ] Custom input editor (create your own test cases)
- [ ] Shareable URLs (save trace state, generate link)
- [ ] Export trace as PDF/slides for presentations

**Educational Features:**

- [ ] Difficulty levels (beginner/intermediate/advanced examples)
- [ ] Learning path recommendations
- [ ] Progress tracking across sessions
- [ ] Certificate generation for mastery

---

### 🎯 Future (V3.0+)

**Advanced Algorithms:**

- [ ] Depth-First Search (graph visualization)
- [ ] Breadth-First Search (graph visualization)
- [ ] Dijkstra's Algorithm (graph visualization)
- [ ] Dynamic Programming examples (matrix visualization)
- [ ] Backtracking algorithms (tree visualization)

**Developer Tools:**

- [ ] LLM-driven algorithm generation with auto-compliance
- [ ] Algorithm testing framework (pytest + React Testing Library)
- [ ] Performance profiling dashboard
- [ ] CI/CD pipeline with automated compliance checks

**Platform Features:**

- [ ] Multi-language support (Python, Java, C++, JavaScript)
- [ ] Collaborative mode (multiple users, shared traces)
- [ ] Annotation system (add notes to specific steps)
- [ ] Dark/light theme toggle
- [ ] Accessibility improvements (ARIA labels, screen reader support)

---

## Architecture Overview

### Data Flow: From User Click to Visualization

**FRONTEND (React)**

1. **User Interaction Layer**

   - `AlgorithmSwitcher` component
     - Displays dropdown with available algorithms
     - Fetches algorithm list via `useTraceLoader` hook

2. **Data Loading Layer** (`useTraceLoader` hook)

   - Fetches `GET /api/algorithms` (discovery)
   - Loads example inputs for selected algorithm
   - Sends `POST /api/trace/unified` with:
     ```json
     {
       "algorithm": "binary-search",
       "input": {"array": [...], "target": 7}
     }
     ```

3. **Trace Processing Layer**

   - Receives trace response:
     ```json
     {
       "result": {...},
       "trace": {"steps": [...]},
       "metadata": {
         "visualization_type": "array",  ← KEY: Determines component
         "prediction_points": [...]
       }
     }
     ```

4. **Dynamic Visualization Selection**

   - `visualizationRegistry.js`
   - Reads `metadata.visualization_type`
   - Returns appropriate component:
     - `"array"` → `ArrayView` (Binary Search, Merge Sort)
     - `"timeline"` → `TimelineView` (Interval Coverage)
     - `"graph"` → `GraphView` (DFS, BFS) [future]
     - `"tree"` → `TreeView` (BST, Heap) [future]

5. **Visualization Components**
   - `ArrayView` - For array-based algorithms
   - `TimelineView` - For interval-based algorithms
   - `CallStackView` - For recursive call visualization
   - Each component receives: `step` (current state) + `config` (rendering hints)

---

**HTTP REQUEST** (Frontend → Backend)

```
POST /api/trace/unified
Content-Type: application/json

{
  "algorithm": "binary-search",
  "input": {"array": [1, 3, 5, 7], "target": 5}
}
```

---

**BACKEND (Flask + Python)**

1. **Unified Endpoint** (`/api/trace/unified`)

   ```python
   def generate_trace_unified():
       algorithm = request.json['algorithm']      # "binary-search"
       algorithm_input = request.json['input']    # {"array": [...], ...}

       # Registry lookup (automatic routing)
       tracer_class = registry.get(algorithm)     # Returns BinarySearchTracer

       # Instantiate and execute
       tracer = tracer_class()
       return tracer.execute(algorithm_input)
   ```

2. **Algorithm Registry** (`backend/algorithms/registry.py`)

   - Central registry mapping algorithm names to classes:
     ```python
     registry = {
         'binary-search': BinarySearchTracer,
         'interval-coverage': IntervalCoverageTracer,
         'merge-sort': MergeSortTracer,
         ...
     }
     ```
   - Populated via `registry.register()` calls
   - No manual routing in `app.py` needed!

3. **Algorithm Implementations**

   - `BinarySearchTracer` (array-based)
   - `IntervalCoverageTracer` (timeline-based)
   - `MergeSortTracer` (array-based) [future]
   - `DFSTracer` (graph-based) [future]

4. **Abstract Base Class** (`AlgorithmTracer`)
   - All algorithms inherit from this
   - Provides:
     - `execute(input)` → Returns standardized trace
     - `get_prediction_points()` → Returns learning moments
     - `_add_step(type, data, desc)` → Records trace steps
     - `_build_trace_result(result)` → Formats output
     - `_get_visualization_state()` → Optional auto-enrichment

---

### Key Architecture Principles

**1. Registry Pattern**

- Add algorithm → Automatic UI discovery
- Zero changes to `app.py` routing logic
- Zero changes to frontend component selection

**2. Unified Routing**

- One endpoint handles all algorithms: `/api/trace/unified`
- Backend routes based on `algorithm` field in request
- Eliminates need for algorithm-specific endpoints

**3. Dynamic Visualization**

- Backend declares visualization type in metadata
- Frontend selects component dynamically
- Component reuse: Binary Search + Merge Sort both use `ArrayView`

**4. Base Class Abstraction**

- Consistent trace structure across all algorithms
- Enforced metadata fields (`algorithm`, `display_name`, `visualization_type`)
- Built-in safety limits (MAX_STEPS prevents infinite loops)

**5. Separation of Concerns**

- **Backend:** ALL the thinking (algorithm logic, trace generation)
- **Frontend:** ALL the reacting (visualization, interaction, navigation)
- No algorithm logic in frontend code

---

## Questions This Project Answers

1. ✅ Can backend generate complete traces efficiently? (Yes - 20-50ms)
2. ✅ Is the JSON payload reasonable size? (Yes - 30-50KB)
3. ✅ Can frontend display traces without algorithmic logic? (Yes - pure visualization)
4. ✅ Is this approach scalable to other algorithms? (Yes - registry handles it)
5. ✅ Can visualization components be reused? (Yes - Binary Search reuses ArrayView)
6. ✅ Does adding algorithms require app.py changes? (No - registry auto-routes)
7. ✅ Can prediction mode work across algorithms? (Yes - base class provides interface)
8. ✅ Is the compliance system effective? (Yes - catches issues before production)
9. ✅ Can the platform be extended by non-experts? (Yes - checklists guide implementation)
10. ✅ Does it improve learning outcomes? (User engagement metrics show promise)

---

## Support

For issues, questions, or contributions:

- **GitHub Issues:** Open an issue with [Bug], [Feature], or [Question] tag
- **Documentation:**
  - Tenant Guide: `docs/TENANT_GUIDE.md`
  - Compliance Checklists: `docs/compliance/`
  - Static Mockups: `docs/static_mockup/`
- **Contributing:** See "Contributing: Adding a New Algorithm" section above
- **Compliance Questions:** Reference `docs/compliance/CHECKLIST_SYSTEM_OVERVIEW.md`

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

**Built with:**

- **Backend:** Python 3.11, Flask, Pydantic
- **Frontend:** React 18, Tailwind CSS
- **Architecture:** Registry pattern, Base class abstraction
- **Philosophy:** Backend does ALL the thinking, Frontend does ALL the reacting

**Development Time:**

- Platform architecture: 5 sessions (~15 hours)
- First algorithm (Interval Coverage): 3 sessions (~10 hours)
- Second algorithm (Binary Search): 1 session (~2 hours) ← **This shows the power of the registry system!**
- Compliance framework: 1 session (~3 hours)

**Total:** ~30 hours from concept to production-ready platform with 2 algorithms and full compliance system.

---

**Status:** ✅ Platform Architecture Complete - Ready for Algorithm Expansion

**Next Steps:** Add 3rd algorithm to validate scalability, then focus on graph/tree visualizations for next algorithm category.

---

_Last Updated: December 2024_
