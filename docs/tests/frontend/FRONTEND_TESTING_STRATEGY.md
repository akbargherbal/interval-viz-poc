# Frontend Testing Strategy

**Project:** Algorithm Visualization Platform  
**Document Version:** 1.0  
**Date:** December 2024  
**Status:** 🔴 DRAFT - Awaiting Review

---

## Executive Summary

### Current State Assessment

The frontend has been **successfully refactored** according to the phased architecture plan. However, the test suite reflects the **proof-of-concept era** and is now critically misaligned with production reality:

**Test Coverage Analysis:**
- ✅ **5 Hook Tests**: Comprehensive, well-structured (useTraceLoader, useTraceNavigation, usePredictionMode, useVisualHighlight, useKeyboardShortcuts)
- ✅ **2 Utility Tests**: Registry tests working (stateRegistry, visualizationRegistry exists but not tested)
- ⚠️ **1 Component Test**: BinarySearchState only - **98% of UI untested**
- ❌ **Zero Integration Tests**: No App.jsx tests, no modal tests, no end-to-end workflows
- ❌ **Zero Compliance Tests**: Frontend Checklist requirements not validated

**Critical Gaps:**
1. **No LOCKED requirement validation** (modal IDs, keyboard shortcuts, overflow patterns)
2. **No registry integration tests** (dynamic component selection)
3. **No unified API endpoint tests** (algorithm switching, example loading)
4. **No prediction flow tests** (two-step confirmation, feedback display)
5. **No completion modal tests** (outcome-driven theming, algorithm-specific stats)

### Objective

Create a **compliance-driven, architecture-aligned testing strategy** that:
1. Validates LOCKED requirements (non-negotiable architectural contracts)
2. Tests registry-based dynamic behavior (core innovation)
3. Ensures backward compatibility during algorithm expansion
4. Complements backend testing (no duplication, clear boundaries)

### Success Criteria

By end of implementation:
- **100% LOCKED requirement coverage** (modal IDs, keyboard shortcuts, overflow)
- **95%+ hook coverage** (maintain current quality)
- **80%+ component coverage** (critical UI paths)
- **Zero obsolete tests** (legacy tests archived/removed)
- **Automated compliance checks** (Frontend Checklist items testable)

---

## Testing Philosophy

### Guiding Principles

#### 1. **Test What Matters Most**
   - **LOCKED requirements first** (architectural contracts)
   - **Registry behavior second** (dynamic component selection)
   - **User workflows third** (critical paths like prediction flow)
   - **Edge cases fourth** (error boundaries, null states)

#### 2. **Complement, Don't Duplicate Backend**
   - Backend tests API contracts → Frontend tests API consumption
   - Backend tests trace generation → Frontend tests trace rendering
   - Backend tests prediction point logic → Frontend tests prediction UI

#### 3. **Test Behavior, Not Implementation**
   - ✅ Test: "Prediction modal appears at step 5"
   - ❌ Test: "usePredictionMode sets showPrediction to true"
   - ✅ Test: "Modal has ID #prediction-modal"
   - ❌ Test: "Modal uses useState internally"

#### 4. **Prioritize Regression Prevention**
   - LOCKED requirements → Break builds if violated
   - CONSTRAINED requirements → Warn if exceeded
   - FREE zones → Optional coverage

---

## Test Architecture

### Test Pyramid (Frontend-Specific)

```
                    ▲
                   / \
                  /   \
                 /     \
                / E2E   \          5% - Manual user journeys
               /---------\         (See USER_JOURNEYS/*.md)
              /           \
             / Integration \       20% - Component interactions
            /---------------\      (Modals, registries, workflows)
           /                 \
          /   Component       \    30% - UI components
         /---------------------\   (Isolated rendering)
        /                       \
       /        Hooks &          \ 45% - Business logic
      /         Utilities         \(Current strength - maintain)
     /---------------------------\
```

**Distribution Rationale:**
- **45% Hooks/Utilities**: Already strong, maintain quality (5 hooks + utilities)
- **30% Components**: Massive gap - need 12 critical components tested
- **20% Integration**: Zero coverage - need modal flows, registry behavior
- **5% E2E**: Manual testing via user journey documentation

---

## Test Categories

### Category 1: LOCKED Requirements (CRITICAL - Priority 1)

**Definition:** Non-negotiable architectural contracts from Frontend Checklist.

**Test Coverage Required:** 100% automated + manual verification.

#### 1.1 Modal IDs (LOCKED)
```javascript
// tests/compliance/locked-modal-ids.test.jsx
describe('LOCKED: Modal IDs', () => {
  it('prediction modal MUST have ID #prediction-modal', () => {
    // Render PredictionModal
    const { container } = render(<PredictionModal {...mockProps} />);
    const modal = container.querySelector('#prediction-modal');
    expect(modal).toBeInTheDocument();
  });

  it('completion modal MUST have ID #completion-modal', () => {
    // Implementation remains to be seen - currently no ID!
    // This test will FAIL and expose the bug
  });
});
```

**Critical Finding:** CompletionModal is **missing its required ID**! This is a LOCKED requirement violation that tests would catch immediately.

#### 1.2 Keyboard Shortcuts (LOCKED)
```javascript
// tests/compliance/locked-keyboard-shortcuts.test.jsx
describe('LOCKED: Keyboard Shortcuts', () => {
  it('Arrow Right/Space MUST advance step', () => {...});
  it('Arrow Left MUST go to previous step', () => {...});
  it('R/Home MUST reset to start', () => {...});
  it('End MUST jump to end', () => {...});
  it('K/C/S MUST work in prediction modal', () => {...});
  it('Enter MUST submit prediction', () => {...});
  it('Escape MUST close completion modal', () => {...});
});
```

**Status:** Hook tests exist for useKeyboardShortcuts, but **no integration tests** verify they work in App context.

#### 1.3 Overflow Pattern (LOCKED)
```javascript
// tests/compliance/locked-overflow-pattern.test.jsx
describe('LOCKED: Overflow Pattern', () => {
  it('visualization panel MUST use items-start + mx-auto', () => {
    render(<App />);
    const panel = screen.getByTestId('panel-visualization');
    
    // Check parent has items-start
    expect(panel).toHaveClass('items-start');
    
    // Check child wrapper has mx-auto
    const wrapper = panel.querySelector('.mx-auto');
    expect(wrapper).toBeInTheDocument();
  });

  it('MUST NOT use items-center on overflow container', () => {
    // Anti-pattern detection
  });
});
```

**Status:** Zero tests. This pattern was **manually fixed** in refactoring but has no automated protection.

#### 1.4 Narrative Generation (LOCKED - v2.0+)
**Scope:** Backend responsibility. Frontend displays `step.description` from narrative.

**Frontend Test:** Verify description field is rendered (not empty).

---

### Category 2: Registry Behavior (CRITICAL - Priority 2)

**Definition:** Dynamic component selection - core architectural innovation.

#### 2.1 Visualization Registry
```javascript
// tests/integration/visualization-registry.test.jsx
describe('Visualization Registry Integration', () => {
  it('selects ArrayView for binary-search algorithm', async () => {
    // Mock API to return binary-search trace
    render(<App />);
    await switchToAlgorithm('binary-search');
    
    // Verify ArrayView is rendered (not TimelineView)
    expect(screen.getByTestId('array-view')).toBeInTheDocument();
  });

  it('selects TimelineView for interval-coverage algorithm', async () => {
    render(<App />);
    await switchToAlgorithm('interval-coverage');
    
    expect(screen.getByTestId('timeline-view')).toBeInTheDocument();
  });

  it('falls back to TimelineView for unknown type', () => {
    // Mock trace with invalid visualization_type
    const invalidTrace = {
      metadata: { visualization_type: 'unknown-type' }
    };
    
    // Should log warning and use TimelineView
    expect(getVisualizationComponent('unknown-type')).toBe(TimelineView);
  });
});
```

**Status:** Utility tests exist, but **no integration tests** verify it works in App.

#### 2.2 State Registry
```javascript
// tests/integration/state-registry.test.jsx
describe('State Registry Integration', () => {
  it('selects BinarySearchState for binary-search algorithm', async () => {
    render(<App />);
    await switchToAlgorithm('binary-search');
    
    // Verify BinarySearchState is rendered
    expect(screen.getByText('Pointers')).toBeInTheDocument();
  });

  it('selects IntervalCoverageState for interval-coverage', async () => {
    render(<App />);
    
    // Default algorithm should show call stack
    expect(screen.getByText('Call Stack')).toBeInTheDocument();
  });

  it('renders fallback component for unknown algorithm', () => {
    // Should not crash, show generic message
  });
});
```

**Status:** Unit tests exist, **no integration tests**.

---

### Category 3: Component Tests (HIGH - Priority 3)

**Definition:** Isolated component rendering and behavior.

#### 3.1 Modals (CRITICAL)

##### PredictionModal
```javascript
describe('PredictionModal', () => {
  // Structure
  it('renders with ID #prediction-modal', () => {...});
  it('displays question from predictionData', () => {...});
  it('displays hint if provided', () => {...});
  it('renders dynamic number of choice buttons (1-3)', () => {...});
  
  // Interaction
  it('highlights selected choice', () => {...});
  it('enables Submit button only when choice selected', () => {...});
  it('shows feedback after submission', () => {...});
  it('auto-advances after 2.5 seconds', () => {...});
  
  // Keyboard shortcuts
  it('selects choice with derived shortcut (K/C)', () => {...});
  it('submits with Enter key', () => {...});
  it('skips with S key', () => {...});
  
  // Semantic colors
  it('uses emerald for positive choices (Found, Keep)', () => {...});
  it('uses orange for negative choices (Covered)', () => {...});
  it('uses blue for left/backward choices', () => {...});
  it('uses red for right/forward choices', () => {...});
});
```

**Status:** ❌ Zero tests. **98% of prediction flow untested**.

##### CompletionModal
```javascript
describe('CompletionModal', () => {
  // LOCKED requirement - MISSING!
  it('MUST have ID #completion-modal', () => {
    // THIS WILL FAIL - bug caught by tests!
  });
  
  // Structure
  it('only renders on last step', () => {...});
  it('displays outcome-driven theme (found vs not found)', () => {...});
  
  // Algorithm-specific stats
  it('shows binary search stats (comparisons, result)', () => {...});
  it('shows interval coverage stats (kept, removed)', () => {...});
  it('shows prediction accuracy if predictions made', () => {...});
  
  // Animation
  it('fades in with 500ms transition', () => {...});
  it('scales from 95% to 100%', () => {...});
  
  // Keyboard shortcuts
  it('closes with Escape key', () => {...});
});
```

**Status:** ❌ Zero tests. **Critical LOCKED requirement violation undetected**.

#### 3.2 AlgorithmSwitcher
```javascript
describe('AlgorithmSwitcher', () => {
  it('displays current algorithm name', () => {...});
  it('opens dropdown on click', () => {...});
  it('lists all available algorithms from registry', () => {...});
  it('highlights current algorithm in dropdown', () => {...});
  it('calls onAlgorithmSwitch when selecting algorithm', () => {...});
  it('closes on click outside', () => {...});
  it('closes on Escape key', () => {...});
  it('disables during loading', () => {...});
});
```

**Status:** ❌ Zero tests. **Core navigation untested**.

#### 3.3 ControlBar
```javascript
describe('ControlBar', () => {
  it('disables Prev button at step 0', () => {...});
  it('disables Next button at last step', () => {...});
  it('shows step progress (X of Y)', () => {...});
  it('calls onPrev when clicking Previous', () => {...});
  it('calls onNext when clicking Next', () => {...});
  it('calls onReset when clicking Reset', () => {...});
});
```

**Status:** ❌ Zero tests.

#### 3.4 KeyboardHints
```javascript
describe('KeyboardHints', () => {
  it('displays shortcut guide', () => {...});
  it('lists navigation shortcuts (arrows, space)', () => {...});
  it('lists reset shortcuts (R, Home)', () => {...});
  it('lists prediction shortcuts (K, C, S)', () => {...});
});
```

**Status:** ❌ Zero tests.

#### 3.5 Visualization Components

##### ArrayView
```javascript
describe('ArrayView', () => {
  it('renders array elements from visualization data', () => {...});
  it('highlights elements by state (active, compared, found)', () => {...});
  it('displays pointers (left, right, mid)', () => {...});
  it('handles empty array gracefully', () => {...});
  it('applies overflow pattern (items-start + mx-auto)', () => {...});
});
```

**Status:** ❌ Zero tests. **Used by binary-search but untested**.

##### TimelineView
```javascript
describe('TimelineView', () => {
  it('renders intervals from visualization data', () => {...});
  it('highlights hovered interval', () => {...});
  it('shows kept vs covered intervals', () => {...});
  it('calls onIntervalHover callback', () => {...});
  it('applies overflow pattern', () => {...});
});
```

**Status:** ❌ Zero tests. **Core interval coverage visualization untested**.

#### 3.6 State Components

##### BinarySearchState
```javascript
describe('BinarySearchState', () => {
  // EXISTING TESTS - Keep and maintain
  it('renders pointers section when pointers data is present', () => {...});
  it('renders search progress section', () => {...});
  it('calculates progress bar width correctly', () => {...});
  // ... 8 existing tests
});
```

**Status:** ✅ **8 tests exist**. Maintain quality.

##### IntervalCoverageState
```javascript
describe('IntervalCoverageState', () => {
  it('renders call stack with active call highlighted', () => {...});
  it('auto-scrolls to active call', () => {...});
  it('handles empty call stack', () => {...});
  it('calls onIntervalHover on interval hover', () => {...});
  it('formats intervals correctly (start, end)', () => {...});
});
```

**Status:** ❌ Zero tests. **Default algorithm state untested**.

---

### Category 4: Integration Tests (HIGH - Priority 4)

**Definition:** Multi-component workflows and state synchronization.

#### 4.1 Algorithm Switching Flow
```javascript
describe('Algorithm Switching Integration', () => {
  it('loads binary-search with first example on switch', async () => {
    render(<App />);
    
    // Start with interval-coverage (default)
    expect(screen.getByText('Interval Coverage')).toBeInTheDocument();
    
    // Switch to binary-search
    await userEvent.click(screen.getByRole('button', { name: /binary search/i }));
    
    // Verify:
    // 1. Trace loaded from backend
    // 2. ArrayView displayed
    // 3. BinarySearchState displayed
    // 4. Step counter reset to 0
    // 5. Prediction stats reset
  });

  it('maintains prediction mode toggle across algorithm switch', async () => {
    // Enable prediction mode
    // Switch algorithm
    // Verify prediction mode still enabled
  });

  it('resets step to 0 when switching algorithms', async () => {
    // Navigate to step 5 in current algorithm
    // Switch algorithm
    // Verify currentStep === 0
  });
});
```

#### 4.2 Prediction Flow Integration
```javascript
describe('Prediction Flow Integration', () => {
  it('blocks navigation during prediction modal', async () => {
    // Enable prediction mode
    // Navigate to prediction point
    // Verify modal appears
    // Try to click Next button → Should not advance
    // Try arrow key → Should not advance
    // Submit prediction → Should advance
  });

  it('tracks accuracy across multiple predictions', async () => {
    // Answer first prediction correctly
    // Answer second prediction incorrectly
    // Answer third prediction correctly
    // Jump to end
    // Verify completion modal shows 66% accuracy
  });

  it('resets prediction stats on Reset button', async () => {
    // Make 3 predictions
    // Click Reset
    // Navigate to end
    // Verify completion modal shows 0 answered
  });
});
```

#### 4.3 Unified API Integration
```javascript
describe('Unified API Endpoint Integration', () => {
  it('fetches available algorithms on mount', async () => {
    const mockAlgorithms = [
      { name: 'binary-search', display_name: 'Binary Search' },
      { name: 'interval-coverage', display_name: 'Interval Coverage' }
    ];
    
    global.fetch = jest.fn()
      .mockResolvedValueOnce({ ok: true, json: async () => mockAlgorithms })
      .mockResolvedValueOnce({ ok: true, json: async () => mockTrace });
    
    render(<App />);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/algorithms')
      );
    });
  });

  it('uses unified endpoint for registry algorithms', async () => {
    // Mock: /algorithms returns ['binary-search', 'interval-coverage']
    // Mock: Switch to binary-search
    // Verify: POST /trace/unified with {algorithm: 'binary-search', input: {...}}
  });

  it('falls back to legacy endpoint for interval-coverage', async () => {
    // Handle race condition where registry hasn't loaded
    // Verify: POST /trace (legacy) still works
  });
});
```

---

### Category 5: Hook Tests (MAINTAIN - Priority 5)

**Status:** ✅ Comprehensive coverage already exists.

**Strategy:** Maintain existing quality, add tests for new features only.

#### Existing Coverage
1. **useTraceLoader** (46 tests) - ✅ Excellent
2. **useTraceNavigation** (15 tests) - ✅ Good
3. **usePredictionMode** (15 tests) - ⚠️ **Needs update** (now uses activePrediction)
4. **useVisualHighlight** (12 tests) - ✅ Excellent
5. **useKeyboardShortcuts** (15 tests) - ✅ Excellent

**Total:** 103 hook tests - **This is a strength, maintain it**.

#### Update Required: usePredictionMode
```javascript
// CURRENT TEST (obsolete):
it('should call handlePredictionAnswer with isCorrect boolean', () => {
  act(() => {
    result.current.handlePredictionAnswer(true); // ❌ Old API
  });
});

// NEW TEST (post-refactoring):
it('should call handlePredictionAnswer with userAnswer', () => {
  act(() => {
    result.current.handlePredictionAnswer('keep'); // ✅ New API
  });
});

it('returns activePrediction object at prediction points', () => {
  // PHASE 4 update - activePrediction replaces step/nextStep props
  const { result } = renderHook(() => usePredictionMode(trace, 1, mockNext));
  
  expect(result.current.activePrediction).toMatchObject({
    question: expect.any(String),
    choices: expect.any(Array),
    correct_answer: expect.any(String),
    step_index: 1
  });
});
```

---

### Category 6: Utility Tests (MAINTAIN - Priority 6)

#### Existing Coverage
1. **stateRegistry** (6 tests) - ✅ Excellent
2. **visualizationRegistry** - ❌ **No tests** (but simple, low priority)
3. **predictionUtils** - ❌ **No tests** (2 functions, should test)
4. **stepBadges** - ❌ **No tests** (7 badge types, should test)

#### New Tests Required

##### predictionUtils
```javascript
describe('predictionUtils', () => {
  describe('getAccuracyFeedback', () => {
    it('returns "Excellent" for 90-100%', () => {
      expect(getAccuracyFeedback(95)).toMatchObject({
        message: 'Excellent work!',
        color: 'emerald'
      });
    });
    
    it('returns "Great" for 70-89%', () => {...});
    it('returns "Good start" for 50-69%', () => {...});
    it('returns "Keep practicing" for <50%', () => {...});
  });

  describe('formatPredictionStats', () => {
    it('calculates accuracy percentage', () => {
      const stats = formatPredictionStats({ total: 10, correct: 7 });
      expect(stats.accuracy).toBe(70);
    });
    
    it('handles zero total gracefully', () => {
      const stats = formatPredictionStats({ total: 0, correct: 0 });
      expect(stats.accuracy).toBe(0);
    });
  });
});
```

##### stepBadges
```javascript
describe('stepBadges', () => {
  it('returns correct badge for INITIAL_STATE', () => {
    expect(getStepTypeBadge('INITIAL_STATE')).toMatchObject({
      label: expect.stringContaining('Start'),
      color: expect.stringContaining('blue')
    });
  });
  
  // Test all 7 badge types
  it('returns correct badge for DECISION', () => {...});
  it('returns correct badge for COVERAGE', () => {...});
  it('returns correct badge for EXAMINING_INTERVAL', () => {...});
  // ... etc
  
  it('returns default badge for unknown type', () => {
    expect(getStepTypeBadge('UNKNOWN_TYPE')).toMatchObject({
      label: 'Step',
      color: expect.any(String)
    });
  });
});
```

---

### Category 7: Error Boundary Tests (MEDIUM - Priority 7)

```javascript
describe('ErrorBoundary', () => {
  it('catches rendering errors in children', () => {
    const ThrowError = () => { throw new Error('Test error'); };
    
    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );
    
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
  });

  it('displays error message to user', () => {...});
  it('logs error to console', () => {...});
  it('allows app to continue functioning', () => {...});
});
```

---

## Test Organization Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── AlgorithmSwitcher.test.jsx          # NEW
│   │   ├── CompletionModal.test.jsx            # NEW - CRITICAL
│   │   ├── ControlBar.test.jsx                 # NEW
│   │   ├── ErrorBoundary.test.jsx              # NEW
│   │   ├── KeyboardHints.test.jsx              # NEW
│   │   ├── PredictionModal.test.jsx            # NEW - CRITICAL
│   │   ├── algorithm-states/
│   │   │   ├── BinarySearchState.test.jsx      # ✅ EXISTS - Keep
│   │   │   └── IntervalCoverageState.test.jsx  # NEW
│   │   └── visualizations/
│   │       ├── ArrayView.test.jsx              # NEW
│   │       └── TimelineView.test.jsx           # NEW
│   ├── hooks/
│   │   └── __tests__/
│   │       ├── useKeyboardShortcuts.test.js    # ✅ EXISTS - Keep
│   │       ├── usePredictionMode.test.js       # ✅ EXISTS - Update
│   │       ├── useTraceLoader.test.js          # ✅ EXISTS - Update
│   │       ├── useTraceNavigation.test.js      # ✅ EXISTS - Keep
│   │       └── useVisualHighlight.test.js      # ✅ EXISTS - Keep
│   ├── utils/
│   │   ├── predictionUtils.test.js             # NEW
│   │   ├── stateRegistry.test.js               # ✅ EXISTS - Keep
│   │   ├── stepBadges.test.js                  # NEW
│   │   └── visualizationRegistry.test.js       # NEW (optional)
│   └── __tests__/                              # NEW - Integration tests
│       ├── integration/
│       │   ├── algorithm-switching.test.jsx
│       │   ├── prediction-flow.test.jsx
│       │   ├── state-registry.test.jsx
│       │   ├── unified-api.test.jsx
│       │   └── visualization-registry.test.jsx
│       └── compliance/                         # NEW - CRITICAL
│           ├── locked-keyboard-shortcuts.test.jsx
│           ├── locked-modal-ids.test.jsx
│           └── locked-overflow-pattern.test.jsx
└── tests/                                       # ARCHIVE obsolete tests here
    └── archive/
        └── poc-era/
            └── <old tests from proof-of-concept>
```

---

## Testing Tools & Configuration

### Current Setup (Verified)
- ✅ Jest (via react-scripts)
- ✅ React Testing Library 16.3.0
- ✅ @testing-library/jest-dom 6.9.1
- ✅ @testing-library/user-event 14.6.1
- ✅ setupTests.js configured

### Additional Tools Needed
```json
// package.json additions
{
  "devDependencies": {
    "@testing-library/react-hooks": "^8.0.1",  // Already have renderHook from RTL
    "jest-axe": "^8.0.0",                       // Accessibility testing
    "msw": "^2.0.0"                             // Mock Service Worker for API mocking
  },
  "scripts": {
    "test": "react-scripts test",
    "test:coverage": "react-scripts test --coverage --watchAll=false",
    "test:compliance": "react-scripts test --testPathPattern=compliance --watchAll=false",
    "test:integration": "react-scripts test --testPathPattern=integration --watchAll=false",
    "test:ci": "CI=true pnpm test:coverage && pnpm test:compliance"
  }
}
```

### Mock Service Worker Setup
```javascript
// src/mocks/handlers.js
import { http, HttpResponse } from 'msw';

export const handlers = [
  // GET /api/algorithms
  http.get('*/api/algorithms', () => {
    return HttpResponse.json([
      {
        name: 'binary-search',
        display_name: 'Binary Search',
        description: 'Search sorted array',
        example_inputs: [
          { name: 'Basic', input: { array: [1, 3, 5], target: 3 } }
        ]
      },
      {
        name: 'interval-coverage',
        display_name: 'Interval Coverage',
        description: 'Minimize interval set',
        example_inputs: [
          { name: 'Basic', input: { intervals: [...] } }
        ]
      }
    ]);
  }),

  // POST /api/trace/unified
  http.post('*/api/trace/unified', async ({ request }) => {
    const body = await request.json();
    const { algorithm } = body;
    
    if (algorithm === 'binary-search') {
      return HttpResponse.json(mockBinarySearchTrace);
    } else if (algorithm === 'interval-coverage') {
      return HttpResponse.json(mockIntervalCoverageTrace);
    }
    
    return HttpResponse.json(
      { error: 'Unknown algorithm' },
      { status: 400 }
    );
  })
];

// src/mocks/browser.js
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);

// src/setupTests.js (update)
import '@testing-library/jest-dom';
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

## Test Data Management

### Centralized Test Fixtures

```javascript
// src/__tests__/fixtures/traces.js
export const mockBinarySearchTrace = {
  result: { found: true, index: 2, comparisons: 2 },
  trace: {
    steps: [
      {
        step: 0,
        type: 'INITIAL_STATE',
        description: 'Searching for 5',
        data: {
          visualization: {
            array: [
              { index: 0, value: 1, state: 'active_range' },
              { index: 1, value: 3, state: 'active_range' },
              { index: 2, value: 5, state: 'active_range' }
            ],
            pointers: { left: 0, right: 2, mid: null, target: 5 }
          }
        }
      },
      // ... more steps
    ],
    total_steps: 5,
    duration: 0.01
  },
  metadata: {
    algorithm: 'binary-search',
    display_name: 'Binary Search',
    visualization_type: 'array',
    visualization_config: { show_indices: true },
    prediction_points: [
      {
        step_index: 1,
        question: 'Compare mid (3) with target (5). What next?',
        choices: [
          { id: 'found', label: 'Found! (3 == 5)' },
          { id: 'search-left', label: 'Search Left' },
          { id: 'search-right', label: 'Search Right' }
        ],
        correct_answer: 'search-right',
        hint: 'Is 3 less than, equal to, or greater than 5?',
        explanation: '3 < 5, so search right half'
      }
    ]
  }
};

export const mockIntervalCoverageTrace = {
  // Similar structure for interval coverage
};

// src/__tests__/fixtures/predictions.js
export const mockPredictionData = {
  step_index: 1,
  question: 'Will this interval be kept or covered?',
  choices: [
    { id: 'keep', label: 'Keep this interval' },
    { id: 'covered', label: 'Covered by previous' }
  ],
  correct_answer: 'keep',
  hint: 'Compare interval.end with max_end',
  explanation: 'end (660) > max_end (600), so keep'
};
```

---

## Coverage Targets

### Overall Target: 85% Coverage

**Breakdown by Category:**

| Category            | Lines | Functions | Branches | Current | Target | Priority |
|---------------------|-------|-----------|----------|---------|--------|----------|
| Hooks               | 95%   | 98%       | 90%      | ~95%    | 95%    | Maintain |
| Components          | 80%   | 85%       | 75%      | ~10%    | 80%    | HIGH     |
| Utilities           | 90%   | 95%       | 85%      | ~60%    | 90%    | MEDIUM   |
| Integration         | 75%   | 80%       | 70%      | 0%      | 75%    | HIGH     |
| **Overall**         | 85%   | 88%       | 80%      | ~50%    | 85%    | -        |

**Coverage Exclusions:**
- Mock files (`__mocks__/`)
- Test fixtures (`__tests__/fixtures/`)
- Index files (`index.js` - just exports)
- Development utilities (if any)

### Critical Path Coverage (Must be 100%)

1. ✅ Modal rendering (IDs, structure)
2. ✅ Keyboard shortcuts (all 7+ shortcuts)
3. ✅ Overflow pattern (visual regression)
4. ✅ Registry selection (visualization + state)
5. ✅ Prediction flow (modal → feedback → advance)
6. ✅ Algorithm switching (API → state → UI)

---

## Compliance Validation

### Automated Checks (CI/CD Integration)

```bash
#!/bin/bash
# scripts/check-compliance.sh

echo "🔍 Running Frontend Compliance Checks..."

# 1. LOCKED Requirements
echo "1️⃣ Validating LOCKED requirements..."
pnpm test:compliance --testNamePattern="LOCKED" --bail
if [ $? -ne 0 ]; then
  echo "❌ LOCKED requirements violated - BUILD FAILED"
  exit 1
fi

# 2. Coverage Thresholds
echo "2️⃣ Checking coverage thresholds..."
pnpm test:coverage --coverageThreshold='{
  "global": {
    "lines": 85,
    "functions": 88,
    "branches": 80
  }
}'

# 3. Integration Tests
echo "3️⃣ Running integration tests..."
pnpm test:integration --bail

echo "✅ All compliance checks passed!"
```

### Manual Checklist Mapping

**Frontend Checklist → Test Coverage:**

| Checklist Item                          | Test Category          | Automation Level |
|-----------------------------------------|------------------------|------------------|
| Modal IDs (#prediction-modal, etc.)     | Compliance/LOCKED      | 100% Automated   |
| Keyboard shortcuts (7+ shortcuts)       | Compliance/LOCKED      | 100% Automated   |
| Overflow pattern (items-start)          | Compliance/LOCKED      | 100% Automated   |
| Component props (step, config)          | Component Tests        | 100% Automated   |
| Auto-scroll behavior                    | Integration Tests      | 50% Automated    |
| Responsive design (3 viewports)         | Manual                 | 0% Automated     |
| Registry-based rendering                | Integration Tests      | 100% Automated   |
| Prediction modal behavior               | Component + Integration| 100% Automated   |
| Completion modal outcome themes         | Component Tests        | 100% Automated   |

**Manual Testing Required:**
- Visual regression (screenshot comparison)
- Responsive breakpoints (3 viewport sizes)
- Browser compatibility (Chrome, Firefox, Safari)
- Accessibility (screen readers, keyboard-only navigation)

---

## Migration Strategy: Legacy Tests

### Phase 1: Audit (1-2 hours)
```bash
# Run all existing tests to identify obsolete ones
pnpm test --listTests

# Categorize each test file:
# ✅ Keep (still valid)
# 🔄 Update (needs refactoring)
# ❌ Archive (obsolete)
```

### Phase 2: Archive (30 min)
```bash
# Create archive directory
mkdir -p tests/archive/poc-era

# Move obsolete tests (DO NOT DELETE - historical reference)
# Example: If useTraceLoader tests were for old single-algorithm API:
# mv src/hooks/__tests__/useTraceLoader.legacy.test.js tests/archive/poc-era/

# Update package.json to exclude archived tests:
{
  "jest": {
    "testPathIgnorePatterns": [
      "/node_modules/",
      "/tests/archive/"
    ]
  }
}
```

### Phase 3: Update (2-3 hours)

**Example: Updating useTraceLoader tests**

```javascript
// BEFORE (POC era - single algorithm, hardcoded example):
it('should load example trace on mount', async () => {
  const { result } = renderHook(() => useTraceLoader());
  
  await waitFor(() => {
    expect(result.current.loading).toBe(false);
  });
  
  expect(fetch).toHaveBeenCalledWith(
    'http://localhost:5000/api/trace',
    expect.objectContaining({
      body: JSON.stringify({ 
        intervals: HARDCODED_INTERVALS  // ❌ Frontend-generated data
      })
    })
  );
});

// AFTER (Registry era - multiple algorithms, backend examples):
it('should load first algorithm from registry on mount', async () => {
  // Mock: /api/algorithms returns registry
  global.fetch
    .mockResolvedValueOnce({
      ok: true,
      json: async () => [
        { 
          name: 'interval-coverage',
          example_inputs: [
            { input: { intervals: [...] } }  // ✅ Backend-provided
          ]
        }
      ]
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => mockTrace
    });
  
  const { result } = renderHook(() => useTraceLoader());
  
  await waitFor(() => {
    expect(result.current.loading).toBe(false);
  });
  
  // Verify: Called /algorithms, then /trace/unified
  expect(fetch).toHaveBeenCalledWith(
    expect.stringContaining('/algorithms')
  );
  expect(fetch).toHaveBeenCalledWith(
    expect.stringContaining('/trace/unified'),
    expect.objectContaining({
      body: JSON.stringify({
        algorithm: 'interval-coverage',
        input: { intervals: [...] }  // ✅ From backend example
      })
    })
  );
});
```

### Phase 4: Verify (30 min)
```bash
# Run all tests to ensure no regressions
pnpm test --coverage

# Verify coverage hasn't decreased
# Target: Maintain or improve current ~50% → 85%
```

---

## Implementation Plan Reference

**This strategy feeds into a phased implementation plan:**

### Suggested Phasing (To be detailed in separate PHASED_PLAN.md):

1. **Phase 1: LOCKED Requirements** (1 week)
   - Modal IDs
   - Keyboard shortcuts
   - Overflow pattern
   - **Goal:** 100% LOCKED coverage, CI/CD integration

2. **Phase 2: Critical Modals** (1 week)
   - PredictionModal tests
   - CompletionModal tests (fix missing ID first!)
   - **Goal:** Full prediction flow coverage

3. **Phase 3: Registry Integration** (1 week)
   - Visualization registry integration tests
   - State registry integration tests
   - Algorithm switching tests
   - **Goal:** Dynamic behavior validated

4. **Phase 4: Component Coverage** (2 weeks)
   - AlgorithmSwitcher, ControlBar, KeyboardHints
   - ArrayView, TimelineView
   - IntervalCoverageState
   - **Goal:** 80%+ component coverage

5. **Phase 5: Utilities & Polish** (3 days)
   - predictionUtils, stepBadges tests
   - Update usePredictionMode tests
   - Legacy test migration
   - **Goal:** 85%+ overall coverage

6. **Phase 6: Documentation & Maintenance** (2 days)
   - Test documentation
   - Coverage reports
   - CI/CD refinement

**Total Estimated Effort:** 5-6 weeks (1 developer)

---

## Risk Assessment

### High-Risk Areas (Test First)

1. **Modal IDs Missing** (LOCKED violation)
   - **Risk:** CompletionModal has no ID
   - **Impact:** LOCKED requirement violated, keyboard shortcuts may not work
   - **Mitigation:** Add test first (will fail), then fix code

2. **Overflow Pattern Regression**
   - **Risk:** Easy to accidentally use `items-center` again
   - **Impact:** UI cutoff on large visualizations
   - **Mitigation:** Automated visual regression test

3. **Registry Fallback Behavior**
   - **Risk:** Unknown algorithms crash instead of falling back
   - **Impact:** App unusable for new algorithms
   - **Mitigation:** Integration tests with invalid data

4. **Prediction Flow State Sync**
   - **Risk:** Prediction stats not reset on algorithm switch
   - **Impact:** Incorrect accuracy percentages
   - **Mitigation:** Integration test covering full workflow

### Medium-Risk Areas

5. **API Endpoint Race Conditions**
   - **Risk:** Algorithm switch before registry loads
   - **Impact:** Fallback to legacy endpoint
   - **Mitigation:** Mock timing issues in tests

6. **Keyboard Shortcut Conflicts**
   - **Risk:** Modal shortcuts interfere with navigation
   - **Impact:** Poor UX
   - **Mitigation:** Integration test with modal open

### Low-Risk Areas (Test Last)

7. **Visual Aesthetics** (semantic colors, animations)
8. **Accessibility** (screen reader support)
9. **Performance** (render optimization)

---

## Success Metrics

### Quantitative Metrics

| Metric                          | Current | Target | Timeline  |
|---------------------------------|---------|--------|-----------|
| Overall Test Coverage           | ~50%    | 85%    | 6 weeks   |
| LOCKED Requirement Coverage     | 0%      | 100%   | Week 1    |
| Component Test Coverage         | ~10%    | 80%    | Week 4    |
| Integration Test Coverage       | 0%      | 75%    | Week 3    |
| Test Execution Time             | ~5s     | <30s   | Week 6    |
| CI/CD Pass Rate                 | N/A     | >95%   | Week 1    |

### Qualitative Metrics

- ✅ **Zero obsolete tests** in main test suite
- ✅ **Compliance checklist automatable** (90%+ items)
- ✅ **Regression confidence** (safe to refactor)
- ✅ **Onboarding clarity** (new devs understand test structure)
- ✅ **Documentation completeness** (every test category explained)

---

## Maintenance & Evolution

### Ongoing Practices

1. **New Algorithm Checklist:**
   ```
   When adding a new algorithm:
   ☐ Add example inputs to backend registry
   ☐ Create state component tests (if new component)
   ☐ Add integration test for algorithm switching
   ☐ Verify registry selection works
   ☐ Test prediction points (if applicable)
   ☐ Run full compliance suite
   ```

2. **Test Review Criteria:**
   - LOCKED tests: Peer review required before merge
   - Component tests: Review for coverage completeness
   - Integration tests: Verify no backend duplication
   - Hook tests: Check for proper mocking

3. **Coverage Monitoring:**
   ```bash
   # Weekly coverage report
   pnpm test:coverage --coverageReporters=html
   open coverage/index.html
   
   # Flag regression if coverage drops >2%
   ```

4. **Test Debt Management:**
   - Quarterly audit of test relevance
   - Archive obsolete tests (don't delete)
   - Update tests for new features within same PR
   - Document test debt in GitHub Issues

### Anti-Patterns to Avoid

❌ **Testing Implementation Details**
```javascript
// BAD - tests internal state
it('sets showPrediction to true', () => {
  const { result } = renderHook(() => usePredictionMode(...));
  expect(result.current.showPrediction).toBe(true);
});

// GOOD - tests behavior
it('displays prediction modal at step 1', () => {
  render(<App />);
  clickNext();
  expect(screen.getByRole('dialog')).toBeInTheDocument();
});
```

❌ **Duplicating Backend Tests**
```javascript
// BAD - backend already tests this
it('trace has correct metadata structure', () => {
  const trace = await loadTrace('binary-search');
  expect(trace.metadata.algorithm).toBe('binary-search');
});

// GOOD - test frontend consumption
it('displays algorithm name from metadata', () => {
  render(<App trace={mockTrace} />);
  expect(screen.getByText('Binary Search')).toBeInTheDocument();
});
```

❌ **Testing Library Code**
```javascript
// BAD - testing React itself
it('useState updates state', () => {
  const [count, setCount] = useState(0);
  setCount(1);
  expect(count).toBe(1);
});

// GOOD - test your component logic
it('increments counter on button click', () => {
  render(<Counter />);
  userEvent.click(screen.getByRole('button'));
  expect(screen.getByText('1')).toBeInTheDocument();
});
```

---

## Appendix A: Test Examples

### Example 1: LOCKED Modal ID Test (Compliance)

```javascript
// src/__tests__/compliance/locked-modal-ids.test.jsx
import { render, screen } from '@testing-library/react';
import PredictionModal from '../../components/PredictionModal';
import CompletionModal from '../../components/CompletionModal';
import { mockPredictionData, mockTrace } from '../fixtures';

describe('LOCKED: Modal IDs', () => {
  describe('PredictionModal', () => {
    it('MUST have ID #prediction-modal', () => {
      const { container } = render(
        <PredictionModal
          predictionData={mockPredictionData}
          onAnswer={jest.fn()}
          onSkip={jest.fn()}
        />
      );

      const modal = container.querySelector('#prediction-modal');
      expect(modal).toBeInTheDocument();
      expect(modal.tagName).toBe('DIV'); // Root element
    });

    it('modal ID MUST be on root element, not nested', () => {
      const { container } = render(
        <PredictionModal
          predictionData={mockPredictionData}
          onAnswer={jest.fn()}
          onSkip={jest.fn()}
        />
      );

      // Verify ID is on the outermost element
      const modal = container.querySelector('#prediction-modal');
      expect(modal.parentElement).toBe(container);
    });
  });

  describe('CompletionModal', () => {
    it('MUST have ID #completion-modal', () => {
      // THIS TEST WILL FAIL - exposing bug!
      const mockStep = {
        type: 'ALGORITHM_COMPLETE',
        step: 5,
        data: {}
      };

      const { container } = render(
        <CompletionModal
          trace={mockTrace}
          step={mockStep}
          onReset={jest.fn()}
          predictionStats={{ total: 5, correct: 4 }}
        />
      );

      const modal = container.querySelector('#completion-modal');
      expect(modal).toBeInTheDocument(); // ❌ FAILS - ID missing
    });
  });
});
```

### Example 2: Registry Integration Test

```javascript
// src/__tests__/integration/visualization-registry.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../App';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';
import { mockBinarySearchTrace, mockIntervalCoverageTrace } from '../fixtures/traces';

describe('Visualization Registry Integration', () => {
  it('dynamically selects ArrayView when switching to binary-search', async () => {
    // Mock: Start with interval-coverage
    server.use(
      http.get('*/api/algorithms', () => {
        return HttpResponse.json([
          { 
            name: 'interval-coverage',
            display_name: 'Interval Coverage',
            example_inputs: [{ input: { intervals: [] } }]
          },
          { 
            name: 'binary-search',
            display_name: 'Binary Search',
            example_inputs: [{ input: { array: [1, 3, 5], target: 3 } }]
          }
        ]);
      }),
      http.post('*/api/trace/unified', async ({ request }) => {
        const body = await request.json();
        if (body.algorithm === 'interval-coverage') {
          return HttpResponse.json(mockIntervalCoverageTrace);
        } else {
          return HttpResponse.json(mockBinarySearchTrace);
        }
      })
    );

    render(<App />);

    // Wait for initial load (interval-coverage)
    await waitFor(() => {
      expect(screen.getByText('Interval Coverage')).toBeInTheDocument();
    });

    // Verify TimelineView is rendered (data-testid or specific content)
    expect(screen.getByTestId('timeline-view')).toBeInTheDocument();

    // Switch to binary-search
    const algorithmButton = screen.getByRole('button', { name: /interval coverage/i });
    await userEvent.click(algorithmButton);

    const binarySearchOption = screen.getByRole('menuitem', { name: /binary search/i });
    await userEvent.click(binarySearchOption);

    // Wait for trace to load
    await waitFor(() => {
      expect(screen.getByText('Binary Search')).toBeInTheDocument();
    });

    // Verify ArrayView is now rendered (TimelineView gone)
    expect(screen.queryByTestId('timeline-view')).not.toBeInTheDocument();
    expect(screen.getByTestId('array-view')).toBeInTheDocument();
  });

  it('maintains visualization config from metadata', async () => {
    // Test that visualization_config is passed correctly
    // Binary Search: { show_indices: true }
    // Should see index labels in ArrayView
  });
});
```

### Example 3: Prediction Flow Integration Test

```javascript
// src/__tests__/integration/prediction-flow.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../App';
import { mockBinarySearchTrace } from '../fixtures/traces';

describe('Prediction Flow Integration', () => {
  beforeEach(() => {
    // Setup mock with prediction points
    global.fetch = jest.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            name: 'binary-search',
            display_name: 'Binary Search',
            example_inputs: [{ input: { array: [1, 3, 5, 7, 9], target: 5 } }]
          }
        ]
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockBinarySearchTrace
      });
  });

  it('blocks navigation during prediction modal', async () => {
    render(<App />);

    // Wait for load
    await waitFor(() => {
      expect(screen.getByText('Binary Search')).toBeInTheDocument();
    });

    // Enable prediction mode
    const predictionToggle = screen.getByRole('button', { name: /predict/i });
    await userEvent.click(predictionToggle);

    // Navigate to prediction point (step 1 in mockBinarySearchTrace)
    const nextButton = screen.getByRole('button', { name: /next/i });
    await userEvent.click(nextButton);

    // Prediction modal should appear
    const modal = screen.getByRole('dialog');
    expect(modal).toBeInTheDocument();

    // Try to advance with Next button → Should not work
    await userEvent.click(nextButton);
    expect(screen.getByText(/step 2 of/i)).toBeInTheDocument(); // Still at step 2
    expect(modal).toBeInTheDocument(); // Modal still open

    // Try to advance with keyboard → Should not work
    await userEvent.keyboard('{ArrowRight}');
    expect(screen.getByText(/step 2 of/i)).toBeInTheDocument(); // Still at step 2

    // Submit prediction → Should advance
    const submitButton = screen.getByRole('button', { name: /submit/i });
    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument(); // Modal closed
      expect(screen.getByText(/step 3 of/i)).toBeInTheDocument(); // Advanced
    });
  });

  it('tracks accuracy across multiple predictions', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Binary Search')).toBeInTheDocument();
    });

    // Enable prediction mode
    await userEvent.click(screen.getByRole('button', { name: /predict/i }));

    // Answer first prediction correctly
    await userEvent.click(screen.getByRole('button', { name: /next/i }));
    await userEvent.click(screen.getByRole('button', { name: /search right/i }));
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    // Navigate to end (triggering completion modal)
    const endButton = screen.getByRole('button', { name: /end/i });
    await userEvent.click(endButton);

    // Completion modal should show accuracy
    await waitFor(() => {
      expect(screen.getByText(/prediction accuracy/i)).toBeInTheDocument();
      expect(screen.getByText('100%')).toBeInTheDocument(); // 1/1 correct
    });
  });
});
```

---

## Appendix B: Coverage Configuration

```javascript
// package.json - Jest configuration
{
  "jest": {
    "collectCoverageFrom": [
      "src/**/*.{js,jsx}",
      "!src/index.js",
      "!src/setupTests.js",
      "!src/**/*.test.{js,jsx}",
      "!src/**/__tests__/**",
      "!src/**/__mocks__/**",
      "!src/**/index.js"
    ],
    "coverageThreshold": {
      "global": {
        "lines": 85,
        "functions": 88,
        "branches": 80,
        "statements": 85
      }
    },
    "coverageReporters": [
      "text",
      "text-summary",
      "html",
      "lcov"
    ]
  }
}
```

---

## Appendix C: CI/CD Integration

```yaml
# .github/workflows/frontend-tests.yml
name: Frontend Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main, develop]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
          
      - name: Install dependencies
        working-directory: frontend
        run: pnpm install --frozen-lockfile
        
      - name: Run LOCKED compliance tests (CRITICAL)
        working-directory: frontend
        run: pnpm test:compliance
        
      - name: Run all tests with coverage
        working-directory: frontend
        run: pnpm test:coverage
        
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          directory: ./frontend/coverage
          flags: frontend
          fail_ci_if_error: true
          
      - name: Check coverage thresholds
        working-directory: frontend
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if (( $(echo "$COVERAGE < 85" | bc -l) )); then
            echo "❌ Coverage $COVERAGE% is below threshold 85%"
            exit 1
          fi
          echo "✅ Coverage $COVERAGE% meets threshold"
```

---

## Document Control

**Version History:**

| Version | Date       | Author | Changes                        |
|---------|------------|--------|--------------------------------|
| 1.0     | 2024-12-14 | Claude | Initial strategy document      |

**Review Status:**
- [ ] Technical Review (Lead Developer)
- [ ] Compliance Review (QA Team)
- [ ] Approval (Project Manager)

**Next Steps:**
1. Review and approve this strategy
2. Create detailed FRONTEND_TEST_PLAN.md with phased implementation
3. Begin Phase 1: LOCKED Requirements (Week 1)

---

**END OF STRATEGY DOCUMENT**
