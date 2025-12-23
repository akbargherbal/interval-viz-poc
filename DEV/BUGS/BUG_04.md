# Debug Context: 76 Test Failures Investigation

**Date:** January 2025
**Status:** 🛑 Blocked by 76 test failures
**Scope:** Backend Algorithm Tracers

## 🚨 Executive Summary

A recent `pytest` run revealed 76 failures across multiple algorithm tracers. An investigation has categorized these into 5 distinct root causes ranging from `NoneType` crashes to state precedence mismatches.

**Key Findings:**

1. **Boyer-Moore & Merge Intervals:** Crashing due to `NoneType` comparisons (instance state vs. trace data).
2. **BFS & Insertion Sort:** State mismatches (Active "visiting" state vs. Passive "visited" state).
3. **LIS:** Missing binary search steps due to loop condition.
4. **Narrative Generation:** Formatting mismatches (Markdown vs. Plain Text expectations).
5. **Kadane & Container:** Arithmetic assertion failures in tests.

---

## 🔍 Root Cause Analysis

### 1. NoneType Crashes (Critical)

**Symptoms:** `TypeError: '<' not supported between instances of 'int' and 'NoneType'`

- **Boyer-Moore (`boyer_moore_voting_tracer.py`):**
  - _Cause:_ In `_get_element_state`, the code checks `if index < self.current_index` during the `VERIFYING` phase. However, `self.current_index` is explicitly set to `None` during the `PHASE_TRANSITION` step, causing a crash when `_add_step` triggers a visualization update.
- **Merge Intervals (`merge_intervals_tracer.py`):**
  - _Cause:_ `generate_narrative` attempts to access `self.current_index` (live instance variable).
  - _Context:_ `generate_narrative` runs _after_ execution completes. The live instance variables are reset/null. The method must access data from `trace_result['trace']['steps']` instead.

### 2. State Precedence Mismatches

**Symptoms:** `AssertionError: assert 'visiting' == 'visited'`

- **BFS (`breadth_first_search_tracer.py`):**
  - _Cause:_ Visualization logic prioritizes the active state (`visiting`) over the set membership (`visited`).
  - _Analysis:_ The code is pedagogically correct (showing "visiting" is more informative), but the test expects the passive "visited" state.
- **Insertion Sort (`insertion_sort_tracer.py`):**
  - _Cause:_ Prioritizes `comparing` state over `sorted` state for elements within the sorted boundary.

### 3. LIS Missing Steps

**Symptoms:** `assert 0 > 0` (Binary search steps list is empty)

- **LIS (`longest_increasing_subsequence_tracer.py`):**
  - _Cause:_ The binary search loop uses `while left < right`.
  - _Impact:_ If the search range is small (e.g., 1 element), the loop body never executes, and the `BINARY_SEARCH` trace step is never recorded.

### 4. Narrative Formatting

**Symptoms:** `AssertionError` on string containment

- **General:** Tests expect plain strings (e.g., `"Start Node: A"`) but the tracers are correctly generating Markdown (e.g., `"**Start Node:** A"`).

---

## 🛠️ Action Plan for Next Session

### Step 1: Fix NoneType Safety (High Priority)

1.  **Boyer-Moore:** Modify `_get_element_state` to check `if self.current_index is not None` before comparison.
2.  **Merge Intervals:** Refactor `generate_narrative` to remove all references to `self.*` state variables. Use `step['data']` exclusively.

### Step 2: Fix LIS Logic

1.  **LIS Tracer:** Update binary search loop to ensure at least one comparison is recorded, or adjust the loop condition to `while left <= right` with appropriate break logic.

### Step 3: Reconcile State Logic

1.  **BFS & Insertion Sort:** **Do not downgrade the code.** The "active" states (`visiting`, `comparing`) are better for visualization.
2.  **Action:** Update the _tests_ (`test_breadth_first_search_tracer.py`, `test_insertion_sort_tracer.py`) to accept the active states.

### Step 4: Update Narrative Tests

1.  **Action:** Update test strings to match the actual Markdown output (add `**` bold markers where necessary).

### Step 5: Verify Arithmetic Logic

1.  **Kadane & Container:** Review `test_kadanes_algorithm_tracer.py` and `test_container_with_most_water_tracer.py`.
2.  **Action:** Verify if the test input data matches the expected output. If the algorithm logic is FAA-verified, update the test expectations.

---

## 📂 Relevant Files

- `backend/algorithms/boyer_moore_voting_tracer.py`
- `backend/algorithms/merge_intervals_tracer.py`
- `backend/algorithms/breadth_first_search_tracer.py`
- `backend/algorithms/longest_increasing_subsequence_tracer.py`
- `backend/algorithms/tests/` (all corresponding test files)
