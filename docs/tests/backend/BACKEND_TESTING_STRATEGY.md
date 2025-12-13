# Backend Testing Strategy

**Algorithm Visualization Platform - Backend Testing**

**Document Version:** 1.0  
**Last Updated:** December 2024  
**Target Coverage:** ≥90%  
**Primary Framework:** pytest + pytest-cov

---

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Testing Stack](#testing-stack)
3. [Project Structure for Tests](#project-structure-for-tests)
4. [Coverage Requirements](#coverage-requirements)
5. [Unit Testing Strategy](#unit-testing-strategy)
6. [Test Data Strategy](#test-data-strategy)
7. [Testing Checklist by Component](#testing-checklist-by-component)
8. [Running Tests](#running-tests)
9. [CI/CD Integration](#cicd-integration)
10. [Common Testing Patterns](#common-testing-patterns)
11. [Appendix: Example Tests](#appendix-example-tests)

---

## Testing Philosophy

**Core Principle:** Backend does ALL the thinking, so backend tests must verify ALL the logic.

### What We Test

- ✅ **Algorithm Correctness:** Every algorithm produces correct results
- ✅ **Trace Completeness:** Every step is recorded with proper structure
- ✅ **Metadata Compliance:** Output matches frontend expectations
- ✅ **Edge Cases:** Empty inputs, single elements, maximum sizes
- ✅ **Error Handling:** Invalid inputs raise appropriate errors
- ✅ **Registry System:** Dynamic algorithm discovery works correctly
- ✅ **API Endpoints:** Request/response contracts are honored

### What We Don't Test (Yet)

- ❌ Performance benchmarks (not a priority in V1)
- ❌ Load testing (deferred to later phases)
- ❌ Frontend integration (separate testing strategy)
- ❌ Database operations (not applicable - stateless backend)

---

## Testing Stack

### Core Dependencies

```txt
# Add to requirements.txt

# Testing Framework
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0

# Test Utilities
pytest-xdist==3.5.0          # Parallel test execution
pytest-timeout==2.2.0         # Prevent hanging tests
pytest-clarity==1.0.1         # Better assertion messages

# Code Quality
flake8==6.1.0                # Linting
black==23.12.1               # Code formatting
mypy==1.7.1                  # Type checking
```

### Installation

```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # We'll create this
```

---

## Project Structure for Tests

```
backend/
├── algorithms/
│   ├── __init__.py
│   ├── base_tracer.py
│   ├── registry.py
│   ├── binary_search.py
│   ├── interval_coverage.py
│   └── tests/                          # NEW: Algorithm tests
│       ├── __init__.py
│       ├── conftest.py                 # Shared fixtures
│       ├── test_base_tracer.py         # Base class tests
│       ├── test_registry.py            # Registry tests
│       ├── test_binary_search.py       # Binary search tests
│       └── test_interval_coverage.py   # Interval coverage tests
│
├── tests/                              # NEW: API/Integration tests
│   ├── __init__.py
│   ├── conftest.py                     # App-level fixtures
│   ├── test_api_health.py
│   ├── test_api_algorithms.py
│   ├── test_api_trace_unified.py
│   └── test_api_legacy.py
│
├── app.py
├── requirements.txt
├── requirements-dev.txt                # NEW: Development dependencies
├── pytest.ini                          # NEW: Pytest configuration
└── .coveragerc                         # NEW: Coverage configuration
```

---

## Coverage Requirements

### Target Coverage: ≥90%

**Coverage Breakdown by Component:**

| Component | Target | Priority | Notes |
|-----------|--------|----------|-------|
| `base_tracer.py` | 95% | **CRITICAL** | Foundation for all algorithms |
| `registry.py` | 95% | **CRITICAL** | Core platform feature |
| `binary_search.py` | 90% | HIGH | Reference implementation |
| `interval_coverage.py` | 90% | HIGH | Original algorithm |
| `app.py` | 85% | MEDIUM | API layer (some paths hard to test) |

### Coverage Configuration

**File: `backend/.coveragerc`**

```ini
[run]
source = .
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*
    */.venv/*
    setup.py

[report]
precision = 2
show_missing = True
skip_covered = False

# Fail if coverage drops below 90%
fail_under = 90

exclude_lines =
    # Standard exclusions
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
    
[html]
directory = htmlcov

[xml]
output = coverage.xml
```

**File: `backend/pytest.ini`**

```ini
[pytest]
testpaths = algorithms/tests tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Pytest options
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=90
    --maxfail=5

# Markers for test categorization
markers =
    unit: Unit tests for individual components
    integration: Integration tests for API endpoints
    slow: Tests that take longer than 1 second
    edge_case: Edge case and boundary condition tests
    compliance: Tests verifying compliance with frontend contracts

# Timeout for individual tests (prevent hanging)
timeout = 10

# Better diffs for failed assertions
enable_assertion_pass_hook = True
```

---

## Unit Testing Strategy

### Testing Hierarchy

```
1. Base Class Tests (base_tracer.py)
   └─> 2. Registry Tests (registry.py)
        └─> 3. Algorithm Implementation Tests
             ├─> binary_search.py
             ├─> interval_coverage.py
             └─> [future algorithms]
                  └─> 4. API Endpoint Tests (app.py)
```

### Test Categories

#### 1. **Base Class Tests** (`test_base_tracer.py`)

**What to test:**
- Abstract methods raise NotImplementedError when not overridden
- `_add_step()` correctly increments step count
- `_add_step()` enforces MAX_STEPS limit
- `_get_visualization_state()` hook is called and merged correctly
- `_serialize_value()` handles infinity values
- `_build_trace_result()` produces correct structure
- Trace timing is recorded accurately

**Coverage Target:** 95%

#### 2. **Registry Tests** (`test_registry.py`)

**What to test:**
- Registration with valid tracer class succeeds
- Registration with invalid class raises ValueError
- Duplicate registration raises ValueError
- `get()` retrieves correct tracer class
- `get()` raises KeyError for unknown algorithm
- `list_algorithms()` returns all registered algorithms
- `get_metadata()` excludes tracer_class from output
- `is_registered()` and `__contains__` work correctly
- Auto-registration on module import works

**Coverage Target:** 95%

#### 3. **Algorithm Implementation Tests**

##### **Binary Search** (`test_binary_search.py`)

**What to test:**

*Correctness Tests:*
- Target found at various positions (start, middle, end)
- Target not found returns correct result
- Single element array (found and not found)
- Two element array (all cases)
- Large arrays work correctly

*Trace Tests:*
- All steps recorded with correct types
- INITIAL_STATE is first step
- CALCULATE_MID steps show correct mid calculation
- SEARCH_LEFT/SEARCH_RIGHT steps update pointers correctly
- TARGET_FOUND or TARGET_NOT_FOUND is final step
- Comparison count matches actual comparisons

*Visualization Tests:*
- Array elements have correct states (excluded, active_range, examining, found)
- Pointers (left, right, mid, target) are correct at each step
- Search space size decreases correctly
- Final state shows all elements as excluded (when not found)

*Prediction Tests:*
- Prediction points generated at CALCULATE_MID steps
- Correct answer matches actual decision
- Choices include all three options (found, search-left, search-right)
- Hints and explanations are present

*Edge Cases:*
- Empty array raises ValueError
- Unsorted array raises ValueError
- Array with duplicates (sorted) works correctly
- Target smaller than all elements
- Target larger than all elements

**Coverage Target:** 90%

##### **Interval Coverage** (`test_interval_coverage.py`)

**What to test:**

*Correctness Tests:*
- No overlapping intervals (all kept)
- Fully covered intervals (only largest kept)
- Partial coverage scenarios
- Single interval (kept)
- Multiple intervals with same start time
- Edge-to-edge intervals (not covered)

*Trace Tests:*
- INITIAL_STATE contains all intervals
- SORT_BEGIN and SORT_COMPLETE steps present
- Sorting order verified (start ASC, end DESC for ties)
- Recursive calls tracked with correct depth
- EXAMINING_INTERVAL for each interval
- DECISION_MADE follows each EXAMINING_INTERVAL
- MAX_END_UPDATE only when interval is kept
- CALL_RETURN for each call
- ALGORITHM_COMPLETE is final step

*Visualization Tests:*
- `all_intervals` includes all original intervals
- Interval states transition correctly (active → examining → covered/kept)
- Call stack state shows correct depth and current interval
- `max_end` values are serialized correctly (handle -inf)
- Call stack frames have required fields (id, is_active)

*Prediction Tests:*
- Prediction points at EXAMINING_INTERVAL steps
- Correct answer is "keep" or "covered"
- Question mentions interval bounds
- Hint references max_end comparison

*Edge Cases:*
- Single interval returns single interval
- Two identical intervals (one covered)
- Intervals exceeding MAX_INTERVALS raises ValueError
- Intervals with end <= start raise ValueError
- Empty interval list raises ValueError

**Coverage Target:** 90%

#### 4. **API Endpoint Tests** (`test_api_*.py`)

**What to test:**

*Health Endpoint:*
- Returns 200 status
- Returns correct algorithm count
- Lists available algorithms

*List Algorithms Endpoint:*
- Returns 200 status
- Returns array of algorithm metadata
- Each algorithm has required fields (name, display_name, description, example_inputs)

*Unified Trace Endpoint:*
- Valid algorithm + valid input returns 200 with trace
- Unknown algorithm returns 404 with helpful error
- Missing 'algorithm' field returns 400
- Missing 'input' field returns 400
- Invalid input returns 400 with validation details
- Algorithm-specific errors (unsorted array, etc.) return 400

*Legacy Endpoints:*
- `/api/trace` still works for interval coverage
- `/api/trace/binary-search` still works
- `/api/examples` returns interval examples
- `/api/examples/binary-search` returns binary search examples

**Coverage Target:** 85%

---

## Test Data Strategy

### Principle: **Practical, Not Overkill**

We use a **fixture-based approach** with **parameterized tests** for common scenarios, avoiding over-engineering.

### Fixture Organization

**File: `backend/algorithms/tests/conftest.py`**

```python
"""
Shared fixtures for algorithm tests.

Fixtures provide reusable test data without duplication.
Keep fixtures simple and focused.
"""

import pytest
from algorithms.base_tracer import AlgorithmTracer


# ============================================================================
# Mock Tracer for Base Class Testing
# ============================================================================

class MockTracer(AlgorithmTracer):
    """Minimal tracer implementation for testing base class."""
    
    def execute(self, input_data):
        self.metadata = {
            'algorithm': 'mock',
            'display_name': 'Mock Algorithm',
            'visualization_type': 'test'
        }
        return self._build_trace_result({'result': 'success'})
    
    def get_prediction_points(self):
        return []


@pytest.fixture
def mock_tracer():
    """Provide a basic tracer instance for testing."""
    return MockTracer()


# ============================================================================
# Binary Search Test Data
# ============================================================================

@pytest.fixture
def sorted_array_small():
    """Small sorted array for basic tests."""
    return [1, 3, 5, 7, 9]


@pytest.fixture
def sorted_array_large():
    """Large sorted array (100 elements)."""
    return list(range(0, 200, 2))  # [0, 2, 4, ..., 198]


@pytest.fixture
def binary_search_test_cases():
    """
    Parameterized test cases for binary search.
    
    Returns list of tuples: (array, target, expected_found, expected_index)
    """
    return [
        # Target found cases
        ([1, 3, 5, 7, 9], 5, True, 2),
        ([1, 3, 5, 7, 9], 1, True, 0),  # First element
        ([1, 3, 5, 7, 9], 9, True, 4),  # Last element
        ([42], 42, True, 0),  # Single element
        
        # Target not found cases
        ([1, 3, 5, 7, 9], 4, False, None),
        ([1, 3, 5, 7, 9], 0, False, None),  # Before first
        ([1, 3, 5, 7, 9], 10, False, None),  # After last
        ([42], 99, False, None),  # Single element miss
    ]


# ============================================================================
# Interval Coverage Test Data
# ============================================================================

@pytest.fixture
def basic_intervals():
    """Basic interval set from original example."""
    return [
        {'id': 1, 'start': 540, 'end': 660, 'color': 'blue'},
        {'id': 2, 'start': 600, 'end': 720, 'color': 'green'},
        {'id': 3, 'start': 540, 'end': 720, 'color': 'amber'},
        {'id': 4, 'start': 900, 'end': 960, 'color': 'purple'}
    ]


@pytest.fixture
def no_overlap_intervals():
    """Intervals with no overlap (all should be kept)."""
    return [
        {'id': 1, 'start': 100, 'end': 200, 'color': 'blue'},
        {'id': 2, 'start': 300, 'end': 400, 'color': 'green'},
        {'id': 3, 'start': 500, 'end': 600, 'color': 'amber'}
    ]


@pytest.fixture
def full_coverage_intervals():
    """One large interval covering all others."""
    return [
        {'id': 1, 'start': 100, 'end': 500, 'color': 'blue'},
        {'id': 2, 'start': 150, 'end': 250, 'color': 'green'},
        {'id': 3, 'start': 200, 'end': 300, 'color': 'amber'}
    ]


# ============================================================================
# API Test Fixtures
# ============================================================================

@pytest.fixture
def client():
    """Flask test client."""
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_binary_search_request():
    """Valid request for binary search endpoint."""
    return {
        'algorithm': 'binary-search',
        'input': {
            'array': [1, 3, 5, 7, 9],
            'target': 5
        }
    }


@pytest.fixture
def valid_interval_request(basic_intervals):
    """Valid request for interval coverage endpoint."""
    return {
        'algorithm': 'interval-coverage',
        'input': {
            'intervals': basic_intervals
        }
    }
```

### When to Use Fixtures vs. Inline Data

**Use Fixtures When:**
- ✅ Data is reused across multiple tests
- ✅ Data setup is complex or verbose
- ✅ You want to test the same algorithm with multiple inputs (parameterize)

**Use Inline Data When:**
- ✅ Test is testing a specific edge case unique to that test
- ✅ Data is trivial (e.g., empty list, single element)
- ✅ Inline data makes the test more readable

**Example:**

```python
# GOOD: Fixture for reused data
def test_binary_search_found(sorted_array_small):
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': sorted_array_small, 'target': 5})
    assert result['result']['found'] == True


# GOOD: Inline for edge case
def test_binary_search_empty_array():
    tracer = BinarySearchTracer()
    with pytest.raises(ValueError, match="cannot be empty"):
        tracer.execute({'array': [], 'target': 5})
```

### Parameterized Testing Pattern

Use `pytest.mark.parametrize` for testing multiple scenarios:

```python
@pytest.mark.parametrize("array,target,expected_found,expected_index", [
    ([1, 3, 5, 7, 9], 5, True, 2),
    ([1, 3, 5, 7, 9], 4, False, None),
    ([42], 42, True, 0),
])
def test_binary_search_scenarios(array, target, expected_found, expected_index):
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': array, 'target': target})
    
    assert result['result']['found'] == expected_found
    assert result['result']['index'] == expected_index
```

---

## Testing Checklist by Component

### ✅ Base Tracer (`test_base_tracer.py`)

- [ ] Test `_add_step()` increments step count correctly
- [ ] Test `_add_step()` raises RuntimeError when MAX_STEPS exceeded
- [ ] Test `_add_step()` calls `_get_visualization_state()` and merges result
- [ ] Test `_add_step()` handles empty visualization state (backward compat)
- [ ] Test `_serialize_value()` converts infinity to None
- [ ] Test `_serialize_value()` passes through normal values
- [ ] Test `_build_trace_result()` includes result, trace, and metadata
- [ ] Test `_build_trace_result()` calls `get_prediction_points()`
- [ ] Test `_build_trace_result()` adds prediction_points to metadata
- [ ] Test trace timing is recorded (start_time, duration)
- [ ] Test TraceStep dataclass serialization with asdict()

### ✅ Registry (`test_registry.py`)

- [ ] Test successful registration with valid AlgorithmTracer subclass
- [ ] Test registration fails with non-class argument
- [ ] Test registration fails with non-AlgorithmTracer class
- [ ] Test duplicate registration raises ValueError
- [ ] Test `get()` returns correct tracer class
- [ ] Test `get()` raises KeyError with helpful message for unknown algorithm
- [ ] Test `get_metadata()` returns metadata without tracer_class
- [ ] Test `get_metadata()` raises KeyError for unknown algorithm
- [ ] Test `list_algorithms()` returns all registered algorithms
- [ ] Test `list_algorithms()` excludes tracer_class from results
- [ ] Test `is_registered()` returns True for registered algorithms
- [ ] Test `is_registered()` returns False for unknown algorithms
- [ ] Test `__contains__` operator works (algorithm in registry)
- [ ] Test `__len__` returns correct count
- [ ] Test `count()` returns correct count
- [ ] Test auto-registration on module import (binary-search, interval-coverage)

### ✅ Binary Search (`test_binary_search.py`)

**Correctness:**
- [ ] Test target found at start of array
- [ ] Test target found in middle of array
- [ ] Test target found at end of array
- [ ] Test target not found (smaller than all elements)
- [ ] Test target not found (larger than all elements)
- [ ] Test target not found (between elements)
- [ ] Test single element array - target found
- [ ] Test single element array - target not found
- [ ] Test two element array - all cases
- [ ] Test large array (100+ elements)

**Trace Structure:**
- [ ] Test INITIAL_STATE is first step
- [ ] Test CALCULATE_MID steps present for each iteration
- [ ] Test SEARCH_LEFT or SEARCH_RIGHT follows CALCULATE_MID
- [ ] Test TARGET_FOUND is final step when found
- [ ] Test TARGET_NOT_FOUND is final step when not found
- [ ] Test comparison count is correct
- [ ] Test step count matches expected iterations

**Visualization State:**
- [ ] Test array elements have correct states at each step
- [ ] Test pointers (left, right, mid, target) are correct
- [ ] Test excluded elements outside search range
- [ ] Test active_range elements within [left, right]
- [ ] Test examining element is current mid
- [ ] Test found element marked correctly
- [ ] Test search_space_size decreases correctly

**Prediction Points:**
- [ ] Test prediction generated at each CALCULATE_MID step
- [ ] Test correct_answer matches next step type
- [ ] Test choices include all three options
- [ ] Test question mentions mid_value and target
- [ ] Test hint is present and helpful
- [ ] Test explanation provided

**Edge Cases & Errors:**
- [ ] Test empty array raises ValueError
- [ ] Test unsorted array raises ValueError
- [ ] Test non-dict input raises ValueError
- [ ] Test missing 'array' key raises ValueError
- [ ] Test missing 'target' key raises ValueError
- [ ] Test array with duplicates works correctly

**Metadata Compliance:**
- [ ] Test metadata has 'algorithm' field
- [ ] Test metadata has 'display_name' field
- [ ] Test metadata has 'visualization_type' = 'array'
- [ ] Test metadata has 'visualization_config'
- [ ] Test metadata has 'input_size'
- [ ] Test metadata has 'target_value'

### ✅ Interval Coverage (`test_interval_coverage.py`)

**Correctness:**
- [ ] Test no overlapping intervals (all kept)
- [ ] Test fully covered intervals (largest kept)
- [ ] Test partial coverage scenarios
- [ ] Test single interval (kept)
- [ ] Test two intervals - no overlap
- [ ] Test two intervals - partial overlap
- [ ] Test two intervals - full coverage
- [ ] Test intervals with same start time
- [ ] Test edge-to-edge intervals (touching but not covering)
- [ ] Test basic example from registry

**Trace Structure:**
- [ ] Test INITIAL_STATE is first step
- [ ] Test SORT_BEGIN step present
- [ ] Test SORT_COMPLETE step present
- [ ] Test sorting order correct (start ASC, end DESC ties)
- [ ] Test CALL_START for each recursive call
- [ ] Test EXAMINING_INTERVAL for each interval
- [ ] Test DECISION_MADE follows EXAMINING_INTERVAL
- [ ] Test MAX_END_UPDATE only when interval kept
- [ ] Test CALL_RETURN for each call
- [ ] Test ALGORITHM_COMPLETE is final step
- [ ] Test BASE_CASE when no intervals remaining

**Visualization State:**
- [ ] Test all_intervals includes all original intervals
- [ ] Test interval states: active, examining, covered, kept
- [ ] Test state transitions are correct
- [ ] Test call_stack_state has correct structure
- [ ] Test call stack frames have 'id' field (not 'call_id')
- [ ] Test call stack frames have 'is_active' field
- [ ] Test call stack depth is correct
- [ ] Test max_end serialization (-inf → null)

**Prediction Points:**
- [ ] Test predictions at EXAMINING_INTERVAL steps
- [ ] Test correct_answer is "keep" or "covered"
- [ ] Test question mentions interval bounds
- [ ] Test choices are ["keep", "covered"]
- [ ] Test hint references max_end comparison
- [ ] Test explanation provided

**Edge Cases & Errors:**
- [ ] Test single interval returns single interval
- [ ] Test empty interval list raises ValueError
- [ ] Test intervals exceeding MAX_INTERVALS raises ValueError
- [ ] Test interval with end <= start raises ValueError
- [ ] Test non-dict input raises ValueError
- [ ] Test missing 'intervals' key raises ValueError

**Metadata Compliance:**
- [ ] Test metadata has 'algorithm' field
- [ ] Test metadata has 'display_name' field
- [ ] Test metadata has 'visualization_type' = 'timeline'
- [ ] Test metadata has 'input_size'
- [ ] Test metadata has 'output_size'
- [ ] Test metadata has 'visualization_config'

### ✅ API Endpoints (`test_api_*.py`)

**Health Endpoint:**
- [ ] Test GET /api/health returns 200
- [ ] Test response has 'status' = 'healthy'
- [ ] Test response has 'algorithms_registered' count
- [ ] Test response has 'available_algorithms' list

**List Algorithms Endpoint:**
- [ ] Test GET /api/algorithms returns 200
- [ ] Test response is JSON array
- [ ] Test each algorithm has 'name', 'display_name', 'description'
- [ ] Test each algorithm has 'example_inputs'
- [ ] Test tracer_class is NOT in response

**Unified Trace Endpoint:**
- [ ] Test valid binary-search request returns 200
- [ ] Test valid interval-coverage request returns 200
- [ ] Test unknown algorithm returns 404
- [ ] Test missing 'algorithm' field returns 400
- [ ] Test missing 'input' field returns 400
- [ ] Test invalid input returns 400 with details
- [ ] Test unsorted array for binary-search returns 400
- [ ] Test empty array for binary-search returns 400
- [ ] Test response has 'result', 'trace', 'metadata'

**Legacy Endpoints:**
- [ ] Test POST /api/trace (interval coverage) still works
- [ ] Test POST /api/trace/binary-search still works
- [ ] Test GET /api/examples returns interval examples
- [ ] Test GET /api/examples/binary-search returns binary search examples
- [ ] Test legacy endpoints return same structure as unified

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest algorithms/tests/test_binary_search.py

# Run specific test function
pytest algorithms/tests/test_binary_search.py::test_binary_search_found

# Run tests matching pattern
pytest -k "binary_search"

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf

# Run in parallel (faster)
pytest -n auto
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Terminal coverage report with missing lines
pytest --cov=. --cov-report=term-missing

# XML coverage report (for CI/CD)
pytest --cov=. --cov-report=xml

# Check if coverage meets threshold (90%)
pytest --cov=. --cov-fail-under=90
```

### Test Organization

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only edge case tests
pytest -m edge_case

# Skip slow tests
pytest -m "not slow"
```

### Watch Mode (Development)

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw -- --cov=. --cov-report=term-missing
```

---

## CI/CD Integration

### GitHub Actions Workflow

**File: `.github/workflows/backend-tests.yml`**

```yaml
name: Backend Tests

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'backend/**'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        cd backend
        pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        cd backend
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Run type checking
      run: |
        cd backend
        mypy algorithms/ --ignore-missing-imports
    
    - name: Run tests with coverage
      run: |
        cd backend
        pytest --cov=. --cov-report=xml --cov-report=term-missing --cov-fail-under=90
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: backend/coverage.xml
        flags: backend
        name: backend-coverage
    
    - name: Comment coverage on PR
      if: github.event_name == 'pull_request'
      uses: py-cov-action/python-coverage-comment-action@v3
      with:
        GITHUB_TOKEN: ${{ github.token }}
        MINIMUM_GREEN: 90
        MINIMUM_ORANGE: 80
```

### Pre-commit Hooks

**File: `backend/.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=127']

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: bash -c 'cd backend && pytest --cov=. --cov-fail-under=90 -q'
        language: system
        pass_filenames: false
        always_run: true
```

---

## Common Testing Patterns

### Pattern 1: Testing Abstract Methods

```python
def test_abstract_methods_not_implemented():
    """Base class abstract methods raise NotImplementedError."""
    
    # Create an incomplete subclass
    class IncompleteTracer(AlgorithmTracer):
        pass  # Missing execute() and get_prediction_points()
    
    # Should not be able to instantiate
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        tracer = IncompleteTracer()
```

### Pattern 2: Testing MAX_STEPS Limit

```python
def test_max_steps_enforcement():
    """Tracer aborts when MAX_STEPS exceeded."""
    
    class InfiniteLoopTracer(AlgorithmTracer):
        def execute(self, input_data):
            # Try to add more steps than allowed
            for i in range(self.MAX_STEPS + 1):
                self._add_step("TEST", {}, f"Step {i}")
            return self._build_trace_result({})
        
        def get_prediction_points(self):
            return []
    
    tracer = InfiniteLoopTracer()
    
    with pytest.raises(RuntimeError, match="Exceeded maximum"):
        tracer.execute({})
```

### Pattern 3: Testing Trace Structure

```python
def test_trace_has_required_fields():
    """Trace result has all required top-level fields."""
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [1, 3, 5], 'target': 3})
    
    # Check top-level structure
    assert 'result' in result
    assert 'trace' in result
    assert 'metadata' in result
    
    # Check trace structure
    assert 'steps' in result['trace']
    assert 'total_steps' in result['trace']
    assert 'duration' in result['trace']
    
    # Check metadata structure
    assert 'algorithm' in result['metadata']
    assert 'display_name' in result['metadata']
    assert 'visualization_type' in result['metadata']
    assert 'prediction_points' in result['metadata']
```

### Pattern 4: Testing Visualization State

```python
def test_visualization_state_enrichment():
    """Each step is enriched with visualization state."""
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
    
    # Check that steps have visualization data
    for step in result['trace']['steps']:
        if step['type'] != 'INITIAL_STATE':  # Skip initial state
            assert 'visualization' in step['data']
            viz = step['data']['visualization']
            
            # Check required visualization fields
            assert 'array' in viz
            assert 'pointers' in viz
            assert 'search_space_size' in viz
            
            # Check array elements have required fields
            for element in viz['array']:
                assert 'index' in element
                assert 'value' in element
                assert 'state' in element
```

### Pattern 5: Testing Error Messages

```python
def test_error_message_clarity():
    """Error messages are helpful and specific."""
    tracer = BinarySearchTracer()
    
    # Test unsorted array
    with pytest.raises(ValueError) as exc_info:
        tracer.execute({'array': [5, 3, 1], 'target': 3})
    
    assert "sorted" in str(exc_info.value).lower()
    
    # Test empty array
    with pytest.raises(ValueError) as exc_info:
        tracer.execute({'array': [], 'target': 3})
    
    assert "empty" in str(exc_info.value).lower()
```

### Pattern 6: Testing API Responses

```python
def test_api_error_response_format(client):
    """API errors return consistent JSON structure."""
    
    # Unknown algorithm
    response = client.post('/api/trace/unified', json={
        'algorithm': 'nonexistent',
        'input': {}
    })
    
    assert response.status_code == 404
    data = response.get_json()
    
    assert 'error' in data
    assert 'available_algorithms' in data
    assert isinstance(data['available_algorithms'], list)
```

### Pattern 7: Parametrized Testing

```python
@pytest.mark.parametrize("intervals,expected_kept_count", [
    # No overlap - all kept
    ([
        {'id': 1, 'start': 100, 'end': 200, 'color': 'blue'},
        {'id': 2, 'start': 300, 'end': 400, 'color': 'green'}
    ], 2),
    
    # Full coverage - only largest kept
    ([
        {'id': 1, 'start': 100, 'end': 500, 'color': 'blue'},
        {'id': 2, 'start': 150, 'end': 250, 'color': 'green'}
    ], 1),
    
    # Single interval
    ([{'id': 1, 'start': 100, 'end': 200, 'color': 'blue'}], 1),
])
def test_interval_coverage_scenarios(intervals, expected_kept_count):
    """Test various interval coverage scenarios."""
    tracer = IntervalCoverageTracer()
    result = tracer.execute({'intervals': intervals})
    
    assert len(result['result']) == expected_kept_count
```

### Pattern 8: Testing Compliance Fields

```python
def test_metadata_compliance():
    """Metadata contains all required fields for frontend."""
    tracer = BinarySearchTracer()
    result = tracer.execute({'array': [1, 3, 5], 'target': 3})
    
    metadata = result['metadata']
    
    # Required fields
    required_fields = [
        'algorithm',
        'display_name',
        'visualization_type',
        'prediction_points'
    ]
    
    for field in required_fields:
        assert field in metadata, f"Missing required field: {field}"
    
    # Type checks
    assert isinstance(metadata['algorithm'], str)
    assert isinstance(metadata['display_name'], str)
    assert isinstance(metadata['visualization_type'], str)
    assert isinstance(metadata['prediction_points'], list)
```

---

## Appendix: Example Tests

### Example 1: Complete Base Tracer Test

**File: `backend/algorithms/tests/test_base_tracer.py`**

```python
"""
Tests for AlgorithmTracer base class.

Verifies that the base class provides correct functionality
for all algorithm implementations.
"""

import pytest
from algorithms.base_tracer import AlgorithmTracer, TraceStep


class MockTracer(AlgorithmTracer):
    """Minimal tracer for testing base class functionality."""
    
    def __init__(self):
        super().__init__()
        self.viz_state_called = False
    
    def execute(self, input_data):
        self.metadata = {
            'algorithm': 'mock',
            'display_name': 'Mock Algorithm',
            'visualization_type': 'test'
        }
        
        # Add some test steps
        self._add_step("INIT", {"value": 1}, "Initialize")
        self._add_step("PROCESS", {"value": 2}, "Process")
        
        return self._build_trace_result({'result': 'success'})
    
    def get_prediction_points(self):
        return [{'step_index': 0, 'question': 'Test?'}]
    
    def _get_visualization_state(self):
        self.viz_state_called = True
        return {'mock_state': 'test_value'}


class TestBaseTracer:
    """Test suite for AlgorithmTracer base class."""
    
    def test_initialization(self):
        """Tracer initializes with empty trace and zero step count."""
        tracer = MockTracer()
        
        assert tracer.trace == []
        assert tracer.step_count == 0
        assert tracer.metadata == {}
    
    def test_add_step_increments_count(self):
        """_add_step() increments step_count."""
        tracer = MockTracer()
        
        tracer._add_step("TEST", {}, "Test step")
        assert tracer.step_count == 1
        
        tracer._add_step("TEST", {}, "Test step 2")
        assert tracer.step_count == 2
    
    def test_add_step_creates_trace_step(self):
        """_add_step() creates TraceStep with correct fields."""
        tracer = MockTracer()
        tracer._add_step("TEST", {"key": "value"}, "Test description")
        
        step = tracer.trace[0]
        
        assert isinstance(step, TraceStep)
        assert step.step == 0
        assert step.type == "TEST"
        assert step.description == "Test description"
        assert "key" in step.data
    
    def test_add_step_calls_visualization_state(self):
        """_add_step() calls _get_visualization_state() and merges result."""
        tracer = MockTracer()
        tracer._add_step("TEST", {"original": "data"}, "Test")
        
        # Check that visualization state was called
        assert tracer.viz_state_called == True
        
        # Check that visualization state was merged
        step = tracer.trace[0]
        assert 'visualization' in step.data
        assert step.data['visualization']['mock_state'] == 'test_value'
        assert step.data['original'] == 'data'  # Original data preserved
    
    def test_max_steps_enforcement(self):
        """_add_step() raises RuntimeError when MAX_STEPS exceeded."""
        tracer = MockTracer()
        tracer.MAX_STEPS = 5  # Set low limit for testing
        
        # Add steps up to limit
        for i in range(5):
            tracer._add_step("TEST", {}, f"Step {i}")
        
        # Next step should raise error
        with pytest.raises(RuntimeError, match="Exceeded maximum"):
            tracer._add_step("TEST", {}, "Over limit")
    
    def test_serialize_value_handles_infinity(self):
        """_serialize_value() converts infinity to None."""
        tracer = MockTracer()
        
        assert tracer._serialize_value(float('-inf')) is None
        assert tracer._serialize_value(float('inf')) is None
        assert tracer._serialize_value(42) == 42
        assert tracer._serialize_value("test") == "test"
    
    def test_build_trace_result_structure(self):
        """_build_trace_result() returns correct structure."""
        tracer = MockTracer()
        result = tracer.execute({})
        
        # Check top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Check trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']
        
        assert result['trace']['total_steps'] == 2
        assert len(result['trace']['steps']) == 2
    
    def test_build_trace_result_includes_predictions(self):
        """_build_trace_result() adds prediction_points to metadata."""
        tracer = MockTracer()
        result = tracer.execute({})
        
        assert 'prediction_points' in result['metadata']
        assert len(result['metadata']['prediction_points']) == 1
    
    def test_abstract_methods_enforcement(self):
        """Cannot instantiate tracer without implementing abstract methods."""
        
        class IncompleteTracer(AlgorithmTracer):
            pass  # Missing execute() and get_prediction_points()
        
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteTracer()
```

### Example 2: Complete Binary Search Test

**File: `backend/algorithms/tests/test_binary_search.py`**

```python
"""
Tests for Binary Search algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, and prediction points.
"""

import pytest
from algorithms.binary_search import BinarySearchTracer


class TestBinarySearchCorrectness:
    """Test algorithm correctness - does it find the right answer?"""
    
    @pytest.mark.parametrize("array,target,expected_found,expected_index", [
        # Target found cases
        ([1, 3, 5, 7, 9], 5, True, 2),
        ([1, 3, 5, 7, 9], 1, True, 0),  # First element
        ([1, 3, 5, 7, 9], 9, True, 4),  # Last element
        ([1, 3, 5, 7, 9], 3, True, 1),
        ([1, 3, 5, 7, 9], 7, True, 3),
        ([42], 42, True, 0),  # Single element
        
        # Target not found cases
        ([1, 3, 5, 7, 9], 4, False, None),
        ([1, 3, 5, 7, 9], 0, False, None),  # Before first
        ([1, 3, 5, 7, 9], 10, False, None),  # After last
        ([42], 99, False, None),  # Single element miss
        ([1, 3], 2, False, None),  # Two elements
    ])
    def test_binary_search_scenarios(self, array, target, expected_found, expected_index):
        """Test binary search with various inputs."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        assert result['result']['found'] == expected_found
        assert result['result']['index'] == expected_index
    
    def test_large_array(self):
        """Test with large array (100 elements)."""
        array = list(range(0, 200, 2))  # [0, 2, 4, ..., 198]
        target = 100
        
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': array, 'target': target})
        
        assert result['result']['found'] == True
        assert result['result']['index'] == 50


class TestBinarySearchTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""
    
    def test_initial_state_first(self):
        """First step is INITIAL_STATE."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
    
    def test_target_found_final_step(self):
        """When target found, last step is TARGET_FOUND."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'TARGET_FOUND'
    
    def test_target_not_found_final_step(self):
        """When target not found, last step is TARGET_NOT_FOUND."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 4})
        
        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'TARGET_NOT_FOUND'
    
    def test_comparison_count_correct(self):
        """Comparison count matches actual comparisons."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 3})
        
        comparisons = result['result']['comparisons']
        
        # Count CALCULATE_MID steps (each leads to a comparison)
        mid_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        assert comparisons == len(mid_steps)


class TestBinarySearchVisualizationState:
    """Test visualization state - is frontend data correct?"""
    
    def test_array_elements_have_states(self):
        """Each array element has correct state."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        # Check a step in the middle (not initial)
        mid_step = result['trace']['steps'][2]
        
        assert 'visualization' in mid_step['data']
        viz = mid_step['data']['visualization']
        
        assert 'array' in viz
        for element in viz['array']:
            assert 'index' in element
            assert 'value' in element
            assert 'state' in element
            assert element['state'] in ['excluded', 'active_range', 'examining', 'found']
    
    def test_pointers_present(self):
        """Pointers (left, right, mid, target) are present."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        # Check CALCULATE_MID step
        calc_steps = [s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID']
        
        for step in calc_steps:
            viz = step['data']['visualization']
            pointers = viz['pointers']
            
            assert 'left' in pointers
            assert 'right' in pointers
            assert 'mid' in pointers
            assert 'target' in pointers
    
    def test_found_element_marked(self):
        """When target found, element is marked as 'found'."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        # Check TARGET_FOUND step
        found_step = [s for s in result['trace']['steps'] if s['type'] == 'TARGET_FOUND'][0]
        viz = found_step['data']['visualization']
        
        # Find element at index 2 (value 5)
        element = viz['array'][2]
        assert element['state'] == 'found'


class TestBinarySearchPredictionPoints:
    """Test prediction points - are learning moments identified?"""
    
    def test_predictions_at_calculate_mid(self):
        """Prediction generated at each CALCULATE_MID step."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        calc_mid_count = len([s for s in result['trace']['steps'] if s['type'] == 'CALCULATE_MID'])
        prediction_count = len(result['metadata']['prediction_points'])
        
        assert prediction_count == calc_mid_count
    
    def test_prediction_structure(self):
        """Each prediction has required fields."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 5})
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            assert 'step_index' in pred
            assert 'question' in pred
            assert 'choices' in pred
            assert 'hint' in pred
            assert 'correct_answer' in pred
            
            # Check choices structure
            assert len(pred['choices']) == 3
            for choice in pred['choices']:
                assert 'id' in choice
                assert 'label' in choice
    
    def test_correct_answer_matches_decision(self):
        """Correct answer matches actual algorithm decision."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5, 7, 9], 'target': 7})
        
        predictions = result['metadata']['prediction_points']
        steps = result['trace']['steps']
        
        for pred in predictions:
            step_index = pred['step_index']
            correct_answer = pred['correct_answer']
            
            # Next step after prediction should match answer
            next_step = steps[step_index + 1]
            
            if correct_answer == 'found':
                assert next_step['type'] == 'TARGET_FOUND'
            elif correct_answer == 'search-left':
                assert next_step['type'] == 'SEARCH_LEFT'
            elif correct_answer == 'search-right':
                assert next_step['type'] == 'SEARCH_RIGHT'


class TestBinarySearchEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_array_raises_error(self):
        """Empty array raises ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'array': [], 'target': 5})
    
    def test_unsorted_array_raises_error(self):
        """Unsorted array raises ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="sorted"):
            tracer.execute({'array': [5, 3, 1], 'target': 3})
    
    def test_missing_array_key_raises_error(self):
        """Missing 'array' key raises ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="array"):
            tracer.execute({'target': 5})
    
    def test_missing_target_key_raises_error(self):
        """Missing 'target' key raises ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="target"):
            tracer.execute({'array': [1, 3, 5]})
    
    def test_non_dict_input_raises_error(self):
        """Non-dictionary input raises ValueError."""
        tracer = BinarySearchTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute([1, 3, 5])


class TestBinarySearchMetadata:
    """Test metadata compliance with frontend requirements."""
    
    def test_required_metadata_fields(self):
        """Metadata has all required fields."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        metadata = result['metadata']
        
        assert metadata['algorithm'] == 'binary-search'
        assert metadata['display_name'] == 'Binary Search'
        assert metadata['visualization_type'] == 'array'
        assert 'visualization_config' in metadata
        assert 'prediction_points' in metadata
    
    def test_visualization_config_structure(self):
        """visualization_config has expected fields."""
        tracer = BinarySearchTracer()
        result = tracer.execute({'array': [1, 3, 5], 'target': 3})
        
        config = result['metadata']['visualization_config']
        
        assert 'element_renderer' in config
        assert 'show_indices' in config
        assert 'pointer_colors' in config
```

---

## Summary

This testing strategy provides:

1. **Clear Coverage Targets:** ≥90% overall, with component-specific targets
2. **Practical Test Organization:** Fixtures for reuse, inline data for edge cases
3. **Comprehensive Checklists:** Component-by-component testing requirements
4. **Real Examples:** Complete test files demonstrating best practices
5. **CI/CD Integration:** Ready-to-use GitHub Actions workflow
6. **Common Patterns:** Reusable testing patterns for consistency

**Next Steps:**

1. Create `requirements-dev.txt` with testing dependencies
2. Set up `pytest.ini` and `.coveragerc` configuration files
3. Create `algorithms/tests/` directory with `conftest.py`
4. Implement tests component by component (base_tracer → registry → algorithms → API)
5. Run tests and iterate until ≥90% coverage achieved
6. Set up CI/CD pipeline
7. Document any edge cases or limitations discovered during testing

---

**Document Status:** ✅ Ready for Implementation  
**Estimated Implementation Time:** 3-5 sessions (15-25 hours)  
**Priority:** HIGH - Testing is critical before adding more algorithms
