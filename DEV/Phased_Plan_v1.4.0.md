# Algorithm Visualization Platform: Multi-Algorithm Support

PS NOTES:
**IMPORTANT** - Use proper absolute path when asking user to copy and paste into fies:

```bash
pwd ~/Jupyter_Notebooks/interval-viz-poc/
# Project Absolute Path:
# /home/akbar/Jupyter_Notebooks/interval-viz-poc/
```

**IMPORTANT** - Use `pnpm`

---

## Requirements Analysis

**Current State**: POC with single hardcoded algorithm (Interval Coverage) using recursive execution on intervals with specific trace fields (`all_intervals`, `call_stack_state`)

**Core Goal**: Transform into extensible platform supporting 5-8 diverse algorithms (Binary Search, DFS, Merge Sort, etc.) without breaking "backend thinks, frontend reacts" philosophy

**Technical Constraints**:

- Python 3.11+ Flask backend, React frontend
- Solo dev + LLM workflow (20-40 sessions)
- Must preserve existing UX (prediction mode, visual highlighting, step descriptions)
- Current POC already has `base_tracer.py` (partially generic)

**Assumptions to Validate**:

1. Base tracer can define generic trace structure while allowing algorithm-specific visualization data
2. Frontend can dynamically render different visualization types without hardcoded components per algorithm
3. Prediction mode logic can generalize across algorithm types
4. Current interval-specific UI components can coexist with new algorithm components

---

## Strategic Approach

**Why This Phasing?**

Phase 0 is **mandatory design validation** - the trap is real. The current code logs `all_intervals` and `call_stack_state` which are interval-specific. We must prove the architecture works for Binary Search (arrays) and DFS (graphs) _on paper_ before writing code.

Phases 1-2 establish the foundation (registry + second algorithm proof), Phases 3-4 complete the infrastructure, Phase 5 adds 3-5 more algorithms rapidly.

**Main Risk Areas**:

1. **Overfitting to intervals** - Base class design fails for array/graph algorithms
2. **Frontend visualization coupling** - TimelineView hardcoded for intervals
3. **Prediction logic assumptions** - Current logic assumes EXAMINING_INTERVAL/DECISION_MADE pattern
4. **Data structure explosion** - Each algorithm needs different state serialization

**Validation Strategy**:

- Phase 0: Paper design + thought experiments (STOP if fails)
- Phase 1: Implement Binary Search as acid test (different data structure)
- Phase 2: Registry pattern proves scalability
- Phase 3+: Iterate based on validated patterns

---

## Phase 0: Architectural Design & Validation (3-5 hours, **CRITICAL**)

### Goal

**Prove on paper that a generic base class can support Interval Coverage, Binary Search, and DFS without hacks or base class modifications.**

### Success Criteria

- ✅ Base class contract defined with clear hook points
- ✅ Three thought experiments pass (Interval, Binary Search, DFS)
- ✅ Visualization data injection pattern documented
- ✅ No "special case" code in base class for specific algorithms

### Tasks

**0.1: Analyze Current `base_tracer.py` (1 hour)**

- Review existing `AlgorithmTracer` class
- Identify what's already generic (✓) vs. interval-specific (✗)
- Document method signatures and their assumptions

**Current Analysis**:

```python
# ALREADY GENERIC ✓
- execute() → abstract, no assumptions
- _add_step(type, data, description) → data is dict (flexible!)
- MAX_STEPS safety limit
- TraceStep dataclass structure

# NEEDS EXAMINATION
- get_prediction_points() → abstract, but example assumes EXAMINING_INTERVAL steps
- metadata structure → algorithm-specific fields expected?
```

**Key Decision**: The `data: dict` in `_add_step()` is our salvation! It's already flexible.

**0.2: Design Hook Pattern for Visualization Data (1.5 hours)**

Define how subclasses inject algorithm-specific visualization state into generic trace steps.

**Proposed Pattern** (to validate):

```python
# Base class provides the STRUCTURE
class AlgorithmTracer(ABC):
    @abstractmethod
    def _get_visualization_state(self) -> dict:
        """
        Hook: Subclass returns current visualization data.
        Called automatically by _add_step() to enrich trace.

        Examples:
        - IntervalTracer: {'all_intervals': [...], 'call_stack_state': [...]}
        - BinarySearchTracer: {'array': [...], 'left': int, 'right': int, 'mid': int}
        - DFSTracer: {'graph': {...}, 'visited': set, 'stack': [...]}
        """
        pass

    def _add_step(self, step_type: str, data: dict, description: str):
        # Automatically merge visualization state
        enriched_data = {
            **data,  # Algorithm-specific step data
            'visualization': self._get_visualization_state()  # Standardized key
        }
        self.trace.append(TraceStep(..., data=enriched_data, ...))
```

**Validation Questions**:

- Q: Does this work if Binary Search has no call stack?
- A: Yes! Binary Search's `_get_visualization_state()` returns `{'array': [...], 'pointers': {...}}` instead
- Q: What if DFS needs both adjacency list AND visited set?
- A: Both go in the returned dict under 'graph' and 'visited' keys
- Q: Frontend needs to know which visualization to render?
- A: Metadata includes `visualization_type: "timeline"|"array"|"graph"`

**0.3: Thought Experiment 1 - Binary Search (1 hour)**

**Scenario**: Implement Binary Search on sorted array

```python
class BinarySearchTracer(AlgorithmTracer):
    def __init__(self):
        super().__init__()
        self.array = []
        self.left = 0
        self.right = 0
        self.mid = None
        self.target = None

    def _get_visualization_state(self) -> dict:
        return {
            'array': [{'index': i, 'value': v, 'state': self._get_element_state(i)}
                      for i, v in enumerate(self.array)],
            'pointers': {
                'left': self.left,
                'right': self.right,
                'mid': self.mid,
                'target': self.target
            }
        }

    def _get_element_state(self, index):
        if index == self.mid:
            return 'examining'
        if index < self.left or index > self.right:
            return 'excluded'
        return 'active_range'

    def execute(self, input_data):
        self.array = input_data['array']
        self.target = input_data['target']
        self.left = 0
        self.right = len(self.array) - 1

        self._add_step(
            "INITIAL_STATE",
            {'target': self.target},
            f"Searching for {self.target} in sorted array"
        )

        while self.left <= self.right:
            self.mid = (self.left + self.right) // 2

            self._add_step(
                "CALCULATE_MID",
                {'mid_index': self.mid, 'mid_value': self.array[self.mid]},
                f"Check middle element: array[{self.mid}] = {self.array[self.mid]}"
            )

            if self.array[self.mid] == self.target:
                self._add_step(
                    "TARGET_FOUND",
                    {'index': self.mid},
                    f"✅ Found target at index {self.mid}"
                )
                return self._build_trace_result({'found': True, 'index': self.mid})
            # ... continue search
```

**Validation Results**:

- ✅ No modifications to base class needed
- ✅ `_get_visualization_state()` hook provides array-specific data
- ✅ Step types (CALCULATE_MID) are algorithm-specific, not hardcoded in base
- ✅ Metadata would include `visualization_type: "array"`

**0.4: Thought Experiment 2 - DFS on Graph (45 min)**

**Scenario**: Depth-First Search on graph

```python
class DFSTracer(AlgorithmTracer):
    def _get_visualization_state(self) -> dict:
        return {
            'graph': {
                'nodes': [{'id': n, 'state': self._get_node_state(n)}
                         for n in self.graph.nodes],
                'edges': self.graph.edges
            },
            'search_state': {
                'current': self.current_node,
                'visited': list(self.visited),
                'stack': list(self.stack)
            }
        }

    def execute(self, input_data):
        # Similar pattern - no base class changes needed
        self._add_step(
            "START_DFS",
            {'start_node': self.start},
            "Begin depth-first traversal"
        )
        # ... DFS logic
```

**Validation Results**:

- ✅ Works with graph structure instead of intervals/arrays
- ✅ Hook pattern flexible enough for visited sets + stacks
- ✅ No collision with Binary Search or Interval implementations

**0.5: Define Prediction Point Pattern (30 min)**

Current prediction logic assumes:

- Step type `EXAMINING_INTERVAL` triggers prediction
- Next step type `DECISION_MADE` provides answer

**Generalized Pattern**:

```python
def get_prediction_points(self) -> List[Dict]:
    """
    Subclass scans trace for prediction opportunities.
    Pattern: Find QUESTION steps, validate ANSWER exists.
    """
    predictions = []
    for i, step in enumerate(self.trace):
        if self._is_prediction_question(step):
            if i + 1 < len(self.trace):
                answer_step = self.trace[i + 1]
                predictions.append({
                    'step_index': i,
                    'question': self._format_question(step),
                    'choices': self._get_choices(step),
                    'correct_answer': self._extract_answer(answer_step)
                })
    return predictions

# Subclass implements these helpers
@abstractmethod
def _is_prediction_question(self, step) -> bool:
    pass

# IntervalTracer: checks step.type == "EXAMINING_INTERVAL"
# BinarySearchTracer: checks step.type == "COMPARE_MID"
```

### Deliverables

- [ ] Documented base class contract with hook methods
- [ ] Three passing thought experiments (written pseudo-code)
- [ ] Visualization data pattern specification
- [ ] Prediction pattern specification
- [ ] Decision: PROCEED to Phase 1 or STOP (architectural flaws detected)

### Rollback Plan

**If** thought experiments reveal architectural flaws (e.g., Binary Search requires base class changes): **STOP implementation, redesign architecture**

---

## Phase 1: Prove Architecture with Binary Search (6-8 hours)

### Goal

**Implement Binary Search tracer to validate Phase 0 design actually works in code. This is the acid test.**

### Success Criteria

- ✅ Binary Search tracer implemented without modifying `base_tracer.py`
- ✅ Produces valid trace with array visualization data
- ✅ `/api/trace` endpoint works for both algorithms
- ✅ Frontend displays raw trace data (no visualization yet)

### Tasks

**1.1: Implement BinarySearchTracer (3 hours)**

```python
# backend/algorithms/binary_search.py
from .base_tracer import AlgorithmTracer

class BinarySearchTracer(AlgorithmTracer):
    def _get_visualization_state(self) -> dict:
        """Implementation details: Handle during coding session."""
        pass

    def execute(self, input_data) -> dict:
        """Implementation details: Handle during coding session."""
        pass

    def get_prediction_points(self) -> List[Dict]:
        """Implementation details: Handle during coding session."""
        pass
```

**Key Decision**: If this requires _any_ changes to `base_tracer.py` beyond adding optional helper methods, **STOP and reassess architecture**.

**1.2: Add Binary Search Endpoint (1 hour)**

```python
# backend/app.py
@app.route('/api/trace/binary-search', methods=['POST'])
def generate_binary_search_trace():
    """
    Input: {"array": [1,3,5,7,9], "target": 5}
    """
    pass
```

**1.3: Create Test Suite (2 hours)**

```python
# backend/tests/test_binary_search.py
def test_binary_search_tracer():
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [1,3,5,7,9], 'target': 5})

    assert result['result']['found'] == True
    assert result['metadata']['visualization_type'] == 'array'
    assert 'visualization' in result['trace']['steps'][0]['data']
```

**1.4: Verify Frontend Can Load Trace (1 hour)**

Modify `useTraceLoader` to call new endpoint, display raw JSON in console.

**Success Check**: Can we see array data and pointers in browser console? If yes, Phase 1 complete.

**1.5: Document Learnings (1 hour)**

- What worked as designed?
- What required adjustments?
- Are adjustments backward-compatible with Interval Coverage?

### Deliverables

- [ ] `binary_search.py` tracer implementation
- [ ] Binary Search endpoint in `app.py`
- [ ] Passing unit tests
- [ ] Raw trace visible in frontend
- [ ] Lessons learned document

### Rollback Plan

**If** Binary Search implementation requires breaking changes to `base_tracer.py`: Rollback to Phase 0, redesign hooks

---

## Phase 2: Algorithm Registry & Dynamic Routing (4-6 hours)

### Goal

**Create registry system so adding new algorithms requires zero changes to `app.py` or frontend loading logic.**

### Success Criteria

- ✅ Registry auto-discovers algorithm tracers
- ✅ Single `/api/trace` endpoint routes to correct algorithm
- ✅ Frontend selects algorithm via dropdown
- ✅ Adding new algorithm = create file + register, done

### Tasks

**2.1: Create Algorithm Registry (2 hours)**

```python
# backend/algorithms/registry.py
from typing import Dict, Type
from .base_tracer import AlgorithmTracer

class AlgorithmRegistry:
    def __init__(self):
        self._algorithms: Dict[str, Type[AlgorithmTracer]] = {}

    def register(self, name: str, tracer_class: Type[AlgorithmTracer]):
        """Register algorithm tracer."""
        pass

    def get(self, name: str) -> Type[AlgorithmTracer]:
        """Get tracer by name."""
        pass

    def list_algorithms(self) -> List[Dict]:
        """Return metadata for all algorithms."""
        pass

# Singleton instance
registry = AlgorithmRegistry()

# Auto-register existing algorithms
from .interval_coverage import IntervalCoverageTracer
from .binary_search import BinarySearchTracer

registry.register('interval-coverage', IntervalCoverageTracer)
registry.register('binary-search', BinarySearchTracer)
```

**2.2: Unified Trace Endpoint (1.5 hours)**

```python
# backend/app.py
@app.route('/api/trace', methods=['POST'])
def generate_trace():
    """
    Unified endpoint - routes to correct algorithm.
    Input: {"algorithm": "binary-search", "input": {...}}
    """
    algorithm_name = request.json.get('algorithm')
    tracer_class = registry.get(algorithm_name)
    tracer = tracer_class()
    result = tracer.execute(request.json.get('input'))
    return jsonify(result)

@app.route('/api/algorithms', methods=['GET'])
def list_algorithms():
    """Return available algorithms with metadata."""
    return jsonify(registry.list_algorithms())
```

**2.3: Frontend Algorithm Selector (1.5 hours)**

```jsx
// New component: AlgorithmSelector.jsx
const AlgorithmSelector = ({ onSelect }) => {
  const [algorithms, setAlgorithms] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/algorithms`).then(/*...*/);
  }, []);

  return (
    <select onChange={(e) => onSelect(e.target.value)}>
      {algorithms.map((alg) => (
        <option value={alg.name}>{alg.display_name}</option>
      ))}
    </select>
  );
};
```

**2.4: Update Trace Loader (1 hour)**

Modify `useTraceLoader` to accept algorithm parameter.

### Deliverables

- [ ] `registry.py` with auto-discovery
- [ ] Unified `/api/trace` endpoint
- [ ] Algorithm list endpoint
- [ ] Frontend selector dropdown
- [ ] Both algorithms work through unified endpoint

### Rollback Plan

**If** registry adds >2 hours to adding new algorithms: Simplify to manual registration

---

## Phase 3: Visualization Component Registry (6-8 hours)

### Goal

**Create system where each algorithm declares its visualization component, frontend dynamically renders correct one.**

### Success Criteria

- ✅ Each algorithm's metadata specifies visualization type
- ✅ Frontend registry maps types to React components
- ✅ Array visualizer renders Binary Search correctly
- ✅ Timeline visualizer still renders Interval Coverage correctly

### Tasks

**3.1: Define Visualization Metadata Standard (1 hour)**

```python
# In binary_search.py
def execute(self, input_data):
    # ...
    self.metadata = {
        'algorithm': 'binary-search',
        'visualization_type': 'array',  # NEW
        'visualization_config': {       # NEW
            'element_renderer': 'number',
            'show_indices': True,
            'pointer_colors': {
                'left': 'blue',
                'right': 'red',
                'mid': 'yellow'
            }
        }
    }
```

**3.2: Create Array Visualization Component (3 hours)**

```jsx
// components/visualizations/ArrayView.jsx
const ArrayView = ({ step, highlightConfig }) => {
  const arrayData = step?.data?.visualization?.array || [];
  const pointers = step?.data?.visualization?.pointers || {};

  return (
    <div className="flex items-center gap-2">
      {arrayData.map((item, idx) => (
        <div key={idx} className={getElementClasses(item, pointers)}>
          {item.value}
        </div>
      ))}
    </div>
  );
};
```

**3.3: Create Visualization Registry (2 hours)**

```jsx
// utils/visualizationRegistry.js
import TimelineView from "../components/visualizations/TimelineView";
import ArrayView from "../components/visualizations/ArrayView";

const VISUALIZATION_REGISTRY = {
  timeline: TimelineView,
  array: ArrayView,
  // Future: 'graph', 'tree', 'matrix'
};

export const getVisualizationComponent = (type) => {
  return VISUALIZATION_REGISTRY[type] || TimelineView;
};
```

**3.4: Update App.jsx to Use Registry (1.5 hours)**

```jsx
const AlgorithmTracePlayer = () => {
  const { trace } = useTraceLoader();
  const vizType = trace?.metadata?.visualization_type || "timeline";
  const VisualizationComponent = getVisualizationComponent(vizType);

  return <VisualizationComponent step={currentStepData} />;
};
```

**3.5: Test Both Visualizations (30 min)**

- Load Interval Coverage → Timeline renders
- Load Binary Search → Array renders
- Switch between algorithms without page refresh

### Deliverables

- [ ] ArrayView component for Binary Search
- [ ] Visualization registry mapping
- [ ] App.jsx dynamically selects component
- [ ] Both algorithms render correctly

### Rollback Plan

**If** dynamic component selection causes >3 bugs: Fall back to if/else component selection

---

# Phase 3.5: UI Regression Prevention Addendum

**Added:** Session 6 (Post-Phase 3 Review)  
**Rationale:** Backend refactoring introduced UI regressions that broke PoC-era stability. This phase codifies design principles to prevent future violations.

---

## Problem Statement

During Phase 3 implementation, we introduced several UI regressions:

1. **Space Hierarchy Violation**: `AlgorithmSwitcher` consumed excessive vertical space, pushing Timeline/Stack views off-screen
2. **Missing Element IDs**: Zero landmark elements had HTML IDs, breaking:
   - Auto-scroll behavior (no `#step-current` target)
   - Testing/debugging workflows
   - Accessibility references
3. **Layout Overflow Issues**: `ArrayView` and right panel lacked proper overflow constraints
4. **Navigation Drift**: Control buttons scattered across header vs. integrated design

These violations undermined the core PoC achievement: **stable, consistent UI where students don't have to do anything except watch the Stack and Timeline**.

---

## Core Design Principles (Non-Negotiable)

### 1. **Space Hierarchy**

**Rule:** The Timeline (visualization) and Stack (steps/state) are **PRIMARY UI elements**. All other components must accommodate them, never the reverse.

**Rationale:** These are the core educational elements. A student watching an algorithm trace should see:

- The data structure being operated on (Timeline/Array/Graph)
- The execution context (Call Stack/Algorithm State)
- The current step description

Everything else (controls, algorithm switchers, mode toggles) is **secondary**.

**Implementation:**

```jsx
// ✅ CORRECT: Compact header, maximum viewport for primary content
<div id="app-header" className="px-4 py-3"> {/* ~50px total */}
  {/* Algorithm info + switcher + controls */}
</div>
<div className="flex-1"> {/* Remaining viewport */}
  <div id="panel-visualization">{/* Timeline/Array */}</div>
  <div id="panel-steps">{/* Stack/State */}</div>
</div>

// ❌ WRONG: Bloated switcher, cramped visualization
<div className="p-4 border-b-2"> {/* ~80px+ */}
  <AlgorithmSwitcher /> {/* Takes too much space */}
</div>
<div className="flex-1"> {/* Squished */}
  {/* Visualization cramped */}
</div>
```

---

### 2. **HTML IDs for Landmark Elements**

**Rule:** Major UI landmarks MUST have semantic HTML IDs for:

- Direct DOM access (testing, debugging)
- Auto-scroll targets
- Accessibility (ARIA labels, screen readers)

**Rationale:** While React encourages `useRef()` for dynamic interactions, IDs provide:

- **Debugging speed**: `document.getElementById('panel-visualization')` in console
- **Test stability**: Selectors like `#step-current` don't break on class changes
- **Accessibility**: WCAG guidelines recommend ID references for complex UIs

**Required IDs:**

```jsx
// Application structure
#app-root           // <div> Top-level app container
#app-header         // <div> Main header bar

// Content panels
#panel-visualization  // <div> Main visualization area (Timeline/Array/Graph)
#panel-steps          // <div> Right panel container
#panel-steps-list     // <div> Scrollable steps/stack list
#panel-step-description // <div> Current step description

// Dynamic elements (added by components)
#step-current         // <div> Currently executing step (auto-scroll target)
```

**When to use IDs vs useRef():**

| Use Case                    | Solution                        | Example                                          |
| --------------------------- | ------------------------------- | ------------------------------------------------ |
| Auto-scroll to current step | `useRef()` + `scrollIntoView()` | `activeCallRef.current.scrollIntoView()`         |
| Test targeting              | HTML ID                         | `cy.get('#panel-steps-list')`                    |
| Accessibility labels        | HTML ID                         | `<button aria-describedby="step-description">`   |
| Console debugging           | HTML ID                         | `document.getElementById('panel-visualization')` |
| Class-based styling         | Tailwind classes                | `className="bg-slate-800"`                       |

---

### 3. **Overflow and Scroll Behavior**

**Rule:** Visualization and steps panels MUST handle overflow gracefully. Never sacrifice viewport space for "perfect centering."

**Implementation:**

```jsx
// ✅ CORRECT: Overflow scrolls, content always accessible
<div id="panel-visualization" className="flex-1 flex flex-col overflow-hidden">
  <div className="flex-1 overflow-auto p-6">
    {/* Content scrolls within container */}
  </div>
</div>

// ❌ WRONG: Flex centering causes cutoff
<div className="flex-1 flex items-center justify-center">
  {/* Content can overflow viewport */}
</div>
```

**Critical Auto-Scroll:**

- The `#step-current` element (in CallStackView or equivalent) MUST scroll into view on step change
- Use `scrollIntoView({ behavior: 'smooth', block: 'center' })` for optimal UX
- This is **mandatory** for recursive algorithms where the stack grows beyond viewport

---

### 4. **Compact, Integrated Controls**

**Rule:** Controls (algorithm switcher, mode toggle, navigation buttons) should be **compact and header-integrated**, not scattered or bloated.

**Reference:** See `CONCEPT_static_mockup.html` for the original compact design.

**Before (Session 5 - Bloated):**

```jsx
<div className="bg-gray-800 border-b border-gray-700 p-4">
  {" "}
  {/* 80px+ */}
  <div className="max-w-7xl mx-auto">
    <span>Select Algorithm:</span>
    {/* Large buttons, excessive padding */}
  </div>
</div>
```

**After (Session 6 - Compact):**

```jsx
<div id="app-header" className="bg-slate-800 px-4 py-3">
  {" "}
  {/* ~50px */}
  <div className="flex items-center justify-between">
    <div className="flex items-center gap-4">
      {/* Algo info + compact pills */}
    </div>
    <div className="flex items-center gap-2">
      {/* Mode toggle + controls */}
    </div>
  </div>
</div>
```

---

## Implementation Checklist (Every Phase)

Before merging any UI changes, verify:

- [ ] **Space Test**: Do Timeline + Stack occupy ≥85% of viewport height?
- [ ] **ID Audit**: Are all 6 required IDs present (`#app-root`, `#app-header`, `#panel-visualization`, `#panel-steps`, `#panel-steps-list`, `#panel-step-description`)?
- [ ] **Scroll Test**: Does auto-scroll to `#step-current` work? (Test with 10+ step trace)
- [ ] **Overflow Test**: Does ArrayView handle 20+ element arrays without cutoff?
- [ ] **Regression Test**: Load Interval Coverage trace. Does it look identical to PoC?
- [ ] **Control Compactness**: Is header ≤60px tall?

---

## Rollback Trigger

**If** any phase introduces UI regressions that violate these principles:

1. **STOP implementation** of current phase
2. **Create regression fix branch**
3. **Restore PoC-era behavior** using static mockup as reference
4. **Document root cause** (e.g., "Flex centering broke overflow handling")
5. **Resume phase** only after regression fixed and tested

---

## Visual Regression Testing (Future Enhancement)

Consider adding Percy or Chromatic for automated visual regression detection:

```javascript
// Example: Cypress + Percy
describe("UI Regression Suite", () => {
  it("Timeline View - Interval Coverage", () => {
    cy.visit("/");
    cy.get("#panel-visualization").percySnapshot("Interval Coverage - Step 1");
  });

  it("Array View - Binary Search", () => {
    cy.get("button").contains("Binary Search").click();
    cy.get("#panel-visualization").percySnapshot("Binary Search - Step 1");
  });
});
```

---

## Session 6 Fixes Applied

| Issue                     | Fix                                           | Files Modified  |
| ------------------------- | --------------------------------------------- | --------------- |
| Bloated AlgorithmSwitcher | Compacted into header, removed excess padding | `App.jsx`       |
| Missing IDs               | Added 6 required landmark IDs                 | `App.jsx`       |
| ArrayView cutoff          | Changed flex centering to overflow-auto       | `ArrayView.jsx` |
| Right panel scroll        | Added proper overflow constraints             | `App.jsx`       |

**Result:** UI now matches PoC-era stability. Timeline/Stack remain primary focus.

---

## Best Practices Summary

### DO ✅

- Keep header ≤60px tall
- Use IDs for landmark elements
- Implement auto-scroll for `#step-current`
- Test with 20+ step traces to verify scrolling
- Reference `CONCEPT_static_mockup.html` for layout decisions

### DON'T ❌

- Let secondary UI elements (switchers, controls) dominate viewport
- Remove IDs "because React doesn't need them"
- Use flex centering without overflow handling
- Break PoC-era features (Stack auto-scroll, Timeline highlighting)
- Ignore the static mockup's design principles

---

## Next Steps

With UI stability restored:

1. ✅ **Session 6 Complete**: UI regressions fixed
2. 🎯 **Next Session**: Resume Phase 4 (Generalize Prediction Mode)
3. 📋 **Future**: Consider visual regression testing setup

**The PoC's stability is now codified. Protect it vigilantly.**

---

## Phase 4: Generalize Prediction Mode (5-7 hours)

### Goal

**Make prediction mode work for any algorithm that defines prediction points.**

### Success Criteria

- ✅ PredictionModal renders algorithm-agnostic questions
- ✅ Binary Search predictions work (compare mid to target)
- ✅ Interval Coverage predictions still work
- ✅ Prediction accuracy tracked per algorithm

### Tasks

**4.1: Enhance Prediction Metadata (1.5 hours)**

```python
# In BinarySearchTracer
def get_prediction_points(self) -> List[Dict]:
    predictions = []
    for i, step in enumerate(self.trace):
        if step.type == "CALCULATE_MID":
            predictions.append({
                'step_index': i,
                'question': f"Will we search left or right of mid={step.data['mid_value']}?",
                'choices': ['search-left', 'search-right', 'found'],
                'hint': f"Compare mid ({step.data['mid_value']}) with target",
                'correct_answer': self._determine_answer(step, self.trace[i+1])
            })
    return predictions
```

**4.2: Generalize PredictionModal (2 hours)**

```jsx
// components/PredictionModal.jsx
const PredictionModal = ({ predictionPoint, onAnswer }) => {
  // predictionPoint now has algorithm-agnostic structure
  const { question, choices, hint } = predictionPoint;

  return (
    <div>
      <h2>{question}</h2>
      {choices.map((choice) => (
        <button onClick={() => onAnswer(choice)}>{choice}</button>
      ))}
      {hint && <p>{hint}</p>}
    </div>
  );
};
```

**4.3: Update Prediction Detection (1.5 hours)**

```jsx
// hooks/usePredictionMode.js
useEffect(() => {
  const predictions = trace?.metadata?.prediction_points || [];
  const matchingPrediction = predictions.find(
    (p) => p.step_index === currentStep
  );
  setActivePrediction(matchingPrediction);
}, [currentStep, trace]);
```

**4.4: Test Predictions Across Algorithms (1 hour)**

- Interval Coverage: KEEP vs COVERED predictions
- Binary Search: LEFT vs RIGHT vs FOUND predictions
- Verify accuracy statistics tracked separately

**4.5: Add Keyboard Shortcuts Per Algorithm (1 hour)**

Allow algorithms to define custom prediction shortcuts:

```python
metadata = {
    'prediction_shortcuts': {
        'search-left': 'L',
        'search-right': 'R',
        'found': 'F'
    }
}
```

### Deliverables

- [ ] Generalized prediction point format
- [ ] Algorithm-agnostic PredictionModal
- [ ] Binary Search predictions working
- [ ] Per-algorithm accuracy tracking

### Rollback Plan

**If** generalizing predictions breaks Interval Coverage: Keep algorithm-specific prediction modals

---

## Phase 5: Add 3-5 More Algorithms (12-20 hours, 3-5 hours each)

### Goal

**Prove scalability by rapidly adding diverse algorithms using established patterns.**

### Success Criteria

- ✅ Each new algorithm takes <5 hours to add
- ✅ No modifications to base infrastructure
- ✅ All algorithms have working visualizations and predictions

### Algorithms to Add (Choose 3-5)

**5.1: Merge Sort (4 hours)**

- Visualization: Array with merge animations
- Prediction: Which subarray will merge next?
- Data structure: Array + recursion

**5.2: Depth-First Search (5 hours)**

- Visualization: Graph with nodes/edges
- Prediction: Which node visited next?
- Data structure: Graph (adjacency list)

**5.3: Dijkstra's Algorithm (6 hours)**

- Visualization: Weighted graph
- Prediction: Which node's distance updated next?
- Data structure: Graph + priority queue

**5.4: Quick Sort (4 hours)**

- Visualization: Array with pivot highlighting
- Prediction: Where will pivot end up?
- Data structure: Array + partitioning

**5.5: Breadth-First Search (4 hours)**

- Visualization: Graph with level-by-level coloring
- Prediction: Next node in queue?
- Data structure: Graph + queue

### Per-Algorithm Tasks (Template)

**Phase 5.X: [Algorithm Name] (est. time)**

1. **Implement Tracer** (2 hours)

   - Inherit from `AlgorithmTracer`
   - Implement `_get_visualization_state()`
   - Implement `execute()`
   - Define step types

2. **Create Visualization Component** (1.5 hours)

   - New component or extend existing
   - Register in visualization registry

3. **Define Prediction Points** (1 hour)

   - Implement `get_prediction_points()`
   - Test predictions

4. **Test & Polish** (30 min)
   - Unit tests
   - Visual QA

### Deliverables

- [ ] 3-5 new algorithm tracers
- [ ] Corresponding visualization components
- [ ] Working predictions for each
- [ ] Updated documentation

### Rollback Plan

**If** any algorithm takes >8 hours: Stop, reassess pattern complexity, simplify infrastructure

---

## Decision Tree & Stop Conditions

```
START
  ↓
PHASE 0: Architectural Design
  ├─ Thought experiments pass → PHASE 1
  ├─ Minor design issues → Iterate design (max 2 iterations)
  └─ Major architectural flaws → STOP & REDESIGN

PHASE 1: Binary Search Proof
  ├─ No base class changes needed → PHASE 2
  ├─ Minor base class additions (helpers) → Document & PHASE 2
  └─ Breaking changes required → STOP, return to PHASE 0

PHASE 2: Registry System
  ├─ Works cleanly → PHASE 3
  ├─ Registry adds >2 hours per algorithm → Simplify & retry
  └─ Registry causes coupling → STOP, use manual routing

PHASE 3: Visualization Registry
  ├─ Dynamic rendering works → PHASE 4
  ├─ 1-2 component bugs → Fix & continue
  └─ >3 rendering bugs → STOP, use if/else selection

PHASE 4: Generalized Predictions
  ├─ Works across algorithms → PHASE 5
  ├─ Breaks existing predictions → Rollback, keep algorithm-specific
  └─ >5 hours to generalize → STOP, phase optional

PHASE 5: Scale to 5-8 Algorithms
  ├─ Each <5 hours → SUCCESS
  ├─ 1-2 algorithms take 6-8 hours → Acceptable
  └─ Any algorithm >8 hours → STOP, simplify patterns
```

### Explicit Stop Conditions

**STOP if:**

1. **Phase 0 fails validation** - Thought experiments reveal architectural impossibility
2. **Phase 1 requires breaking changes** - Base tracer needs algorithm-specific code
3. **Registry adds >2 hours per algorithm** - Pattern too complex
4. **Visualization registry causes >3 rendering bugs** - Dynamic loading too brittle
5. **Any Phase 5 algorithm takes >8 hours** - Patterns not actually reusable
6. **Combined time for Phases 0-4 exceeds 30 hours** - Overhead too high
7. **Existing features break** - Interval Coverage stops working during refactor

**Red Flags** (investigate but don't stop immediately):

- Binary Search trace >2x size of Interval Coverage trace
- Frontend rerender performance drops >50ms
- Base tracer grows >300 lines
- More than 3 visualization components needed per algorithm

---

## Risk Mitigation Summary

| Risk                                   | Likelihood | Impact   | Mitigation                                        |
| -------------------------------------- | ---------- | -------- | ------------------------------------------------- |
| Base class overfitted to intervals     | High       | Critical | Phase 0 mandatory design validation before coding |
| Frontend hardcoded for Timeline        | Medium     | High     | Phase 3 registry + component abstraction          |
| Prediction logic too interval-specific | Medium     | Medium   | Phase 4 metadata-driven predictions               |
| Registry pattern over-engineered       | Medium     | Medium   | Phase 2 includes simplification rollback          |
| New algorithms take >8 hours each      | Low        | High     | Phase 5 uses validated patterns, stop if exceeds  |
| Performance degradation                | Low        | Medium   | Profile after Phase 3, optimize if needed         |
| Existing POC breaks                    | Low        | Critical | Git commits per phase, rollback plan each phase   |

---

## Success Metrics

### Minimum Viable Success (Timeline: 25-35 hours across 8-12 sessions)

- ✅ Base architecture validated (Phase 0)
- ✅ 2 working algorithms (Interval + Binary Search)
- ✅ Dynamic visualization rendering
- ✅ Algorithm registry functional
- ✅ Predictions work for both algorithms

### Stretch Goals (If ahead of schedule)

- Add 3 more algorithms (DFS, Merge Sort, Quick Sort)
- Graph visualization component
- Algorithm comparison mode
- Performance profiling dashboard

---

## Scope Boundaries

### In Scope

- ✅ 5-8 distinct algorithms (Interval, Binary, DFS, Sorting)
- ✅ Dynamic visualization component selection
- ✅ Generalized prediction mode
- ✅ Algorithm registry and routing
- ✅ Existing UX features preserved (highlighting, keyboard shortcuts)

### Out of Scope

- ❌ User-created custom algorithms
- ❌ LLM-generated explanations
- ❌ Side-by-side algorithm comparison
- ❌ Advanced graph animations (force-directed layouts)
- ❌ Multi-step undo/redo
- ❌ Algorithm performance analytics (time/space complexity tracking)
- ❌ Mobile-optimized touch controls

---

## Next Steps

1. **Read and approve this plan** - Ensure Phase 0 approach makes sense
2. **Phase 0 Start** - Begin architectural design document (no coding!)
3. **Phase 0 Validation** - Run thought experiments, get explicit GO/NO-GO
4. **Phase 1 or Redesign** - Either implement Binary Search or return to drawing board

---

## Implementation Notes

**Technologies Requiring Research**:

- React dynamic component rendering (`React.lazy` for visualization components?)
- Python plugin/registry patterns (importlib for auto-discovery?)

**Potential Blockers**:

- Frontend component registry might need React Context for global access
- Graph visualization library selection (D3.js? Cytoscape.js?)
- Large traces (DFS on 100-node graph) might need pagination

**Recommended Starting Point**:
Create `docs/phase0_architecture.md` with:

1. Base class contract specification
2. Three thought experiment pseudo-code implementations
3. Explicit GO/NO-GO decision before any code changes

---

## Questions Before Starting

**None** - The plan is self-contained. Phase 0 will surface any ambiguities through thought experiments. If the design can't handle Binary Search on paper, we'll know immediately.

**Critical Success Factor**: Do NOT proceed past Phase 0 unless all three thought experiments prove the architecture is sound. This is your protection against the "overfitting trap."
