# Implementation Specification: Narrative-Driven Quality Gate

**Session:** 33  
**Status:** 🔨 Ready for Implementation  
**Based On:** Revised Workflow v2.0 + Session 32 Decisions

---

## 📋 Implementation Decisions Summary

### Answers to the 6 Critical Questions

| # | Question | Decision | Rationale |
|---|----------|----------|-----------|
| 1 | Method location | **A - Abstract method** | Compiler-enforced, self-contained |
| 2 | Validation timing | **B - Post-execution hook** | Automatic, immediate feedback |
| 3 | Example coverage | **A - ALL examples** | Comprehensive, still practical |
| 4 | QA review depth | **A - Logical completeness** | No frontend knowledge needed |
| 5 | Length limits | **A - Hard limits (per-algo)** | Prevents QA time explosion |
| 6 | POC script fate | **B - Keep as example** | Reference for developers |

---

## 🏗️ Phase 1: Base Infrastructure Updates

### File 1: `backend/algorithms/base_tracer.py`

**Changes Required:**

#### 1. Add Abstract Method

```python
# Add to AlgorithmTracer class after get_prediction_points()

@abstractmethod
def generate_narrative(self, trace_result: dict) -> str:
    """
    Generate human-readable narrative from trace result.
    
    This method converts the algorithm's own JSON output into a coherent
    markdown narrative. If narrative generation fails (KeyError, missing data),
    it indicates the trace JSON is incomplete for visualization.
    
    The narrative is used by QA to validate logical completeness WITHOUT
    needing to look at JSON structure, code, or frontend implementation.
    
    Args:
        trace_result: Complete trace result dict with:
            - result: Algorithm output
            - trace: {steps: [...], total_steps: int, duration: float}
            - metadata: {algorithm, display_name, visualization_type, ...}
    
    Returns:
        str: Markdown-formatted narrative
        
    Raises:
        KeyError: If required visualization data is missing from steps
        
    Example Structure:
        # {Algorithm Name} - Execution Narrative
        
        **Input:** [summary]
        **Output:** [summary]
        **Total Steps:** {count}
        
        ## Step-by-Step Execution
        
        ### Step 1: {TYPE}
        > {description}
        
        [Detailed explanation using data from step.data.visualization]
        
        ### Step 2: {TYPE}
        ...
        
        ## Summary
        [Final results]
        
    Note:
        - Narrative must be readable WITHOUT seeing JSON or code
        - All decision points must have supporting data visible
        - State changes must be explained clearly
        - Temporal flow must be logical
    """
    pass
```

#### 2. Update `_build_trace_result()` with Validation Hook

```python
def _build_trace_result(self, algorithm_result: Any) -> dict:
    """
    Build the standardized trace result structure.
    
    UPDATED v2.0: Now includes automatic narrative generation and validation.
    If narrative generation fails, it indicates incomplete trace data.
    
    Args:
        algorithm_result: The algorithm's output
        
    Returns:
        dict: Standardized result with trace, metadata, and narrative
        
    Raises:
        RuntimeError: If narrative generation fails (incomplete data)
    """
    # Generate prediction points (existing)
    prediction_points = self.get_prediction_points()
    self.metadata["prediction_points"] = prediction_points
    
    # Build trace result (existing)
    trace_result = {
        "result": algorithm_result,
        "trace": {
            "steps": [asdict(s) for s in self.trace],
            "total_steps": len(self.trace),
            "duration": time.time() - self.start_time
        },
        "metadata": self.metadata
    }
    
    # 🔥 NEW: Auto-generate and validate narrative
    try:
        narrative = self.generate_narrative(trace_result)
        trace_result["metadata"]["narrative"] = narrative
        trace_result["metadata"]["narrative_valid"] = True
    except KeyError as e:
        # Missing required field in visualization data
        error_msg = (
            f"\n{'='*70}\n"
            f"NARRATIVE GENERATION FAILED\n"
            f"{'='*70}\n"
            f"Algorithm: {self.metadata.get('algorithm', 'unknown')}\n"
            f"Missing field: {e}\n\n"
            f"This indicates your trace JSON is incomplete.\n"
            f"The frontend would also fail to render this properly.\n\n"
            f"FIX: Add missing field to _get_visualization_state()\n"
            f"{'='*70}\n"
        )
        raise RuntimeError(error_msg) from e
    except Exception as e:
        # Other narrative generation error
        error_msg = (
            f"\n{'='*70}\n"
            f"NARRATIVE GENERATION ERROR\n"
            f"{'='*70}\n"
            f"Algorithm: {self.metadata.get('algorithm', 'unknown')}\n"
            f"Error: {type(e).__name__}: {e}\n\n"
            f"Check your generate_narrative() implementation.\n"
            f"{'='*70}\n"
        )
        raise RuntimeError(error_msg) from e
    
    return trace_result
```

#### 3. Add Complexity Limits (Optional per Algorithm)

```python
# Add to AlgorithmTracer class attributes
MAX_STEPS = 10000  # Existing safety limit
MAX_NARRATIVE_LINES = 2000  # New: Narrative length limit

def _add_step(self, step_type: str, data: dict, description: str):
    """
    Record a step in the algorithm execution.
    
    UPDATED v2.0: Now checks both MAX_STEPS and MAX_NARRATIVE_LINES.
    """
    if self.step_count >= self.MAX_STEPS:
        raise RuntimeError(
            f"Trace generation aborted: Exceeded maximum of {self.MAX_STEPS} steps. "
            "The input may be too complex or causing an infinite loop."
        )
    
    # ... existing code ...
```

---

### File 2: `backend/algorithms/registry.py`

**Changes Required:**

#### Add Optional Complexity Limits

```python
def register(
    self,
    name: str,
    tracer_class: Type[AlgorithmTracer],
    display_name: str,
    description: str,
    example_inputs: List[Dict[str, Any]],
    input_schema: Optional[Dict[str, Any]] = None,
    max_steps: Optional[int] = None,  # NEW
    max_narrative_lines: Optional[int] = None  # NEW
):
    """
    Register an algorithm tracer with metadata.
    
    Args:
        [... existing args ...]
        max_steps: Optional override for MAX_STEPS limit
        max_narrative_lines: Optional narrative length limit
    """
    # ... existing validation ...
    
    # Store algorithm metadata
    self._algorithms[name] = {
        'name': name,
        'tracer_class': tracer_class,
        'display_name': display_name,
        'description': description,
        'example_inputs': example_inputs,
        'input_schema': input_schema,
        'max_steps': max_steps,  # NEW
        'max_narrative_lines': max_narrative_lines  # NEW
    }
```

---

### File 3: Documentation Updates

#### A. `docs/compliance/BACKEND_CHECKLIST.md`

**Add NEW SECTION after "Inheritance & Base Class":**

```markdown
### Narrative Generation (NEW - v2.0)

- [ ] **Implements `generate_narrative(trace_result: dict) -> str`**
      - Required abstract method in AlgorithmTracer
      - Converts own trace JSON → markdown
      - Fails loudly (KeyError) if data missing
      
- [ ] **Narrative generated for ALL example inputs**
      - Run: `python generate_all_narratives.py my-algorithm`
      - Files saved in `docs/narratives/my-algorithm/`
      - One .md file per example input
      
- [ ] **Narrative generation does NOT fail**
      - No KeyError exceptions when generating
      - No missing field references
      - No undefined variable references
      
- [ ] **Self-review completed**
      - [ ] Can follow algorithm logic from narrative alone
      - [ ] All decisions have supporting data visible
      - [ ] Temporal flow makes sense (step N → N+1 logical)
      - [ ] Mental visualization possible
      - [ ] No references to undefined variables

### Narrative Quality Checks

- [ ] **Decision transparency**
      - Every "compare X with Y" shows values of X and Y
      - Every "keep/discard" decision has reasoning
      - Every state change is explained
      
- [ ] **Temporal coherence**
      - No narrative gaps (missing steps)
      - Progression is logical
      - Can reconstruct execution order
      
- [ ] **Length reasonable**
      - Narrative ≤ 500 lines per example (guideline)
      - QA review should take ≤ 5 minutes per example
      - If longer, consider simplifying example inputs
```

**Add to ANTI-PATTERNS:**

```markdown
### Narrative Anti-Patterns (v2.0)

- [ ] ✅ **NOT referencing undefined variables**
      ❌ BAD: "Compare with max_end" (value not shown)
      ✅ GOOD: "Compare 720 with max_end (660)"

- [ ] ✅ **NOT skipping decision outcomes**
      ❌ BAD: "Examining interval [900, 960]... [next: Return]"
      ✅ GOOD: "Examining interval [900, 960] → KEPT (extends coverage)"

- [ ] ✅ **NOT using centralized narrative generator**
      ❌ BAD: Global function with if/elif for step types
      ✅ GOOD: Each algorithm's generate_narrative() method

- [ ] ✅ **NOT generating narratives with missing context**
      ❌ BAD: Narrative has gaps, but "looks okay"
      ✅ GOOD: Narrative reads like complete documentation
```

#### B. `docs/compliance/QA_INTEGRATION_CHECKLIST.md`

**Add NEW SECTION at the very beginning (before "Pre-Integration Checklist"):**

```markdown
## 🎯 Stage 0: Narrative Review (NEW - v2.0)

**When:** BEFORE frontend integration  
**Input:** Generated markdown narratives ONLY (no code, no JSON, no frontend)  
**Time:** 15-20 minutes per algorithm (all examples)

### Review Process

For each example input narrative:

#### 1. Logical Completeness

- [ ] Can follow algorithm logic from start to finish
- [ ] All decision points are explained
- [ ] No undefined variable references
- [ ] Data supporting each decision is visible

**Example PASS:**
```
✅ Step 5: Compare interval end (720) with max_end (660)
   → 720 > 660, so KEEP interval (extends coverage)
```

**Example FAIL:**
```
❌ Step 5: Compare interval end with max_end
   → [What is max_end value? Can't follow logic]
```

#### 2. Temporal Coherence

- [ ] Steps flow logically from N to N+1
- [ ] No narrative gaps or unexplained jumps
- [ ] Can reconstruct execution order
- [ ] State transitions are clear

**Example PASS:**
```
✅ Step 7: Examining interval [900, 960]
   Step 8: Decision → KEPT (max_end was 720, interval ends at 960)
   Step 9: Update max_end from 720 → 960
```

**Example FAIL:**
```
❌ Step 7: Examining interval [900, 960]
   Step 9: Returning with 2 intervals kept
   [Where's the decision for interval [900, 960]?]
```

#### 3. Mental Visualization

- [ ] Can imagine what the visualization would show
- [ ] State changes clear enough to track mentally
- [ ] No need to consult code or JSON to understand

**Example PASS:**
```
✅ "Array state: [1, 3, 5, 7, 9]
    Left pointer at index 0 (value 1)
    Right pointer at index 4 (value 9)
    Mid pointer at index 2 (value 5)"
```

**Example FAIL:**
```
❌ "Update pointers"
   [Which pointers? To what values?]
```

#### 4. Decision Transparency

- [ ] Every decision (keep/discard, left/right, etc.) has:
  - [ ] Comparison data visible
  - [ ] Decision logic clear
  - [ ] Outcome explained

**Example PASS:**
```
✅ "Mid value (5) < target (7)
    → Search right half
    → Eliminate left 3 elements"
```

**Example FAIL:**
```
❌ "Search right half"
   [Why? What was compared?]
```

### Review Outcome

For EACH example:

- [ ] ✅ **PASS** - Narrative is complete and clear
- [ ] ⚠️ **MINOR ISSUES** - Approved with notes (document below)
- [ ] ❌ **FAIL** - Reject, backend must fix (document below)

### Overall Algorithm Assessment

- [ ] ✅ **APPROVED** - All examples PASS or have only MINOR ISSUES
  - Ready for frontend integration
  - Narratives saved as reference documentation
  
- [ ] ❌ **REJECTED** - One or more examples FAIL
  - Document issues below
  - Return to backend for fixes
  - Resubmit narratives after fixes

### Issues Found

**If REJECTED, document specific issues:**

```markdown
## Algorithm: [Name]

### Example 1: [Name] - REJECTED

**Issue 1: [Category] at Step [N]**
- Problem: [Specific issue]
- Impact: [Why this breaks understanding]
- Fix needed: [What backend should add/change]

**Issue 2: [Category] at Steps [N-M]**
...

### Example 2: [Name] - PASS
[No issues]

### Example 3: [Name] - MINOR ISSUES
[List non-blocking observations]
```

### Review Template Example

```markdown
# QA Narrative Review: Binary Search

## Example 1: Basic Search - Target Found

### Checklist
- [x] Logical completeness - ✅ PASS
- [x] Temporal coherence - ✅ PASS  
- [x] Mental visualization - ✅ PASS
- [x] Decision transparency - ✅ PASS

### Outcome: ✅ PASS

---

## Example 2: Target Not Found

### Checklist
- [x] Logical completeness - ✅ PASS
- [x] Temporal coherence - ❌ FAIL
- [ ] Mental visualization - ⚠️ MINOR
- [x] Decision transparency - ✅ PASS

### Outcome: ❌ FAIL

**Issue 1: Temporal Gap (Steps 5-6)**
- Problem: Step 5 calculates mid=3, Step 6 returns "not found"
- Impact: Missing decision/comparison that eliminated element
- Fix: Add step showing "mid value (7) == target (7) → FOUND"

---

## Overall: ❌ REJECTED
Example 2 must be fixed and resubmitted.
```

### What QA Does NOT Review

❌ JSON structure (Backend Checklist handles this)  
❌ Frontend rendering (Integration Tests handle this)  
❌ Coordinate calculations (That's rendering detail)  
❌ Performance (That's Integration Tests)  
❌ Code quality (That's Code Review)

### Time Guidelines

- **Per example:** 3-5 minutes
- **Per algorithm (6 examples):** 15-20 minutes max
- **If review exceeds 20 min:** Algorithm too complex, recommend simplification

---

## [Continue with existing Pre-Integration Checklist...]
```

#### C. Update `docs/compliance/CHECKLIST_SYSTEM_OVERVIEW.md`

**Update the workflow diagram:**

```markdown
## How They Work Together (v2.0)

```
 ___________________________________________________________
|                       TENANT GUIDE                       |
|                   (Constitutional Framework)             |
|__________________________________________________________|
                          |
            +-------------+-------------+-----------------+
            |                           |                 |
            v                           v                 v
  +---------------------+   +---------------------+   +---------------------+
  |     Backend         |   |   QA Narrative      |   |    Frontend         |
  |     Checklist       |   |      Review         |   |    Checklist        |
  |     + Narrative     |   |     (NEW v2.0)      |   |                     |
  |---------------------|   |---------------------|   |---------------------|
  | [x] Metadata        |   | [x] Logical         |   | [x] Modals          |
  | [x] Trace           |   | [x] Temporal        |   | [x] Panels          |
  | [x] Narrative ⭐    |   | [x] Visualization   |   | [x] IDs             |
  +---------------------+   | [x] Decisions       |   +---------------------+
            |               +---------------------+              |
            |                       |                            |
            +----------+------------+                            |
                       ↓                                         ↓
              +------------------+              +-------------------------+
              |  QA APPROVED     |─────────────→|  Frontend Integration   |
              |  (Narrative OK)  |              |  (Trusts complete JSON) |
              +------------------+              +-------------------------+
                                                           |
                                                           ↓
                                                +---------------------+
                                                |   QA Integration    |
                                                |   Tests (Suites 1-14)|
                                                +---------------------+
                                                           |
                                                           ↓
                                                    ✅ PRODUCTION
```

---

## 🎯 Phase 2: Pilot Implementation (Binary Search)

### Step-by-Step Guide

#### 1. Implement `generate_narrative()` in Binary Search

**File:** `backend/algorithms/binary_search.py`

**Add method after `_get_prediction_explanation()`:**

```python
def generate_narrative(self, trace_result: dict) -> str:
    """
    Generate human-readable narrative for Binary Search execution.
    
    Converts trace JSON into markdown documentation that QA can review
    for logical completeness without needing frontend knowledge.
    """
    lines = []
    
    # Header
    algorithm = trace_result['metadata']['display_name']
    lines.append(f"# {algorithm} - Execution Narrative\n")
    
    # Input summary
    array_size = trace_result['metadata']['input_size']
    target = trace_result['metadata']['target_value']
    lines.append(f"**Input:** Array of {array_size} elements")
    lines.append(f"**Target:** {target}")
    
    # Result summary
    result = trace_result['result']
    if result['found']:
        lines.append(f"**Result:** ✅ Found at index {result['index']}")
    else:
        lines.append(f"**Result:** ❌ Not found")
    lines.append(f"**Comparisons:** {result['comparisons']}")
    
    lines.append(f"**Total Steps:** {trace_result['trace']['total_steps']}")
    lines.append(f"**Duration:** {trace_result['trace']['duration']:.4f}s\n")
    
    lines.append("---\n")
    lines.append("## Step-by-Step Execution\n")
    
    # Process each step
    steps = trace_result['trace']['steps']
    
    for step in steps:
        step_num = step['step']
        step_type = step['type']
        description = step['description']
        data = step['data']
        
        lines.append(f"### Step {step_num + 1}: {step_type}\n")
        lines.append(f"> {description}\n")
        
        # Generate step-specific narrative
        step_narrative = self._generate_step_narrative(step_type, data)
        if step_narrative:
            lines.append(step_narrative)
        
        lines.append("")  # Blank line between steps
    
    # Summary
    lines.append("---\n")
    lines.append("## Summary\n")
    if result['found']:
        lines.append(f"Target **{target}** was found at index **{result['index']}** "
                    f"after **{result['comparisons']}** comparisons.\n")
    else:
        lines.append(f"Target **{target}** was not found in the array "
                    f"after **{result['comparisons']}** comparisons.\n")
    
    return "\n".join(lines)

def _generate_step_narrative(self, step_type: str, data: dict) -> str:
    """
    Generate narrative for a specific step type.
    
    This method intentionally accesses fields that MUST be present
    for complete visualization. If a field is missing, KeyError is
    raised, which indicates incomplete JSON.
    """
    if step_type == "INITIAL_STATE":
        target = data['target']
        array_size = data['array_size']
        search_range = data['search_range']
        
        return (
            f"Starting binary search:\n"
            f"- Target value: **{target}**\n"
            f"- Array size: **{array_size}** elements\n"
            f"- Initial search range: **{search_range}**\n"
        )
    
    elif step_type == "CALCULATE_MID":
        # 🔥 CRITICAL: Accessing visualization state
        # If these fields are missing, narrative generation fails
        viz = data['visualization']  # Will KeyError if missing!
        
        mid_index = data['mid_index']
        mid_value = data['mid_value']
        left = data['left']
        right = data['right']
        calculation = data['calculation']
        
        # Access array state to show context
        array = viz['array']  # Will KeyError if missing!
        pointers = viz['pointers']  # Will KeyError if missing!
        
        return (
            f"**Calculate middle index:**\n"
            f"- Calculation: `{calculation}`\n"
            f"- Mid index: **{mid_index}** (value: **{mid_value}**)\n"
            f"- Search range: [{left}, {right}]\n"
            f"- Search space size: **{viz['search_space_size']}** elements\n"
        )
    
    elif step_type == "TARGET_FOUND":
        index = data['index']
        value = data['value']
        comparisons = data['comparisons']
        
        return (
            f"✅ **Target found!**\n"
            f"- Index: **{index}**\n"
            f"- Value: **{value}**\n"
            f"- Total comparisons: **{comparisons}**\n"
        )
    
    elif step_type == "SEARCH_LEFT":
        comparison = data['comparison']
        old_right = data['old_right']
        new_right = data['new_right']
        eliminated = data['eliminated_elements']
        
        return (
            f"⬅️ **Search left half:**\n"
            f"- Comparison: {comparison}\n"
            f"- Update right pointer: {old_right} → **{new_right}**\n"
            f"- Eliminated: **{eliminated}** elements from right side\n"
        )
    
    elif step_type == "SEARCH_RIGHT":
        comparison = data['comparison']
        old_left = data['old_left']
        new_left = data['new_left']
        eliminated = data['eliminated_elements']
        
        return (
            f"➡️ **Search right half:**\n"
            f"- Comparison: {comparison}\n"
            f"- Update left pointer: {old_left} → **{new_left}**\n"
            f"- Eliminated: **{eliminated}** elements from left side\n"
        )
    
    elif step_type == "TARGET_NOT_FOUND":
        comparisons = data['comparisons']
        
        return (
            f"❌ **Target not found:**\n"
            f"- Search space exhausted\n"
            f"- Total comparisons: **{comparisons}**\n"
        )
    
    return f"_(Step type: {step_type})_"
```

#### 2. Generate Narratives for All Examples

**Create utility script:** `backend/scripts/generate_narratives.py`

```python
#!/usr/bin/env python3
"""
Generate narratives for all example inputs of an algorithm.

Usage:
    python generate_narratives.py binary-search
    python generate_narratives.py interval-coverage
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from algorithms.registry import registry


def generate_all_narratives(algorithm_name: str):
    """Generate narratives for all examples of an algorithm."""
    
    # Get algorithm metadata
    metadata = registry.get_metadata(algorithm_name)
    tracer_class = registry.get(algorithm_name)
    
    print(f"Generating narratives for: {metadata['display_name']}")
    print(f"Examples: {len(metadata['example_inputs'])}\n")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent.parent / "docs" / "narratives" / algorithm_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate narrative for each example
    for i, example in enumerate(metadata['example_inputs'], 1):
        example_name = example['name']
        example_input = example['input']
        
        print(f"[{i}/{len(metadata['example_inputs'])}] {example_name}")
        
        # Execute algorithm
        tracer = tracer_class()
        try:
            trace_result = tracer.execute(example_input)
            
            # Extract narrative
            narrative = trace_result['metadata']['narrative']
            
            # Save to file
            filename = f"example_{i}_{example_name.lower().replace(' ', '_')}.md"
            output_file = output_dir / filename
            
            with open(output_file, 'w') as f:
                f.write(narrative)
            
            print(f"   ✅ Saved: {output_file}")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            return False
    
    print(f"\n✅ All narratives generated successfully!")
    print(f"📁 Output directory: {output_dir}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_narratives.py <algorithm-name>")
        print("\nAvailable algorithms:")
        for algo in registry.list_algorithms():
            print(f"  - {algo['name']}")
        sys.exit(1)
    
    algorithm_name = sys.argv[1]
    
    if not registry.is_registered(algorithm_name):
        print(f"Error: Algorithm '{algorithm_name}' not found")
        print("\nAvailable algorithms:")
        for algo in registry.list_algorithms():
            print(f"  - {algo['name']}")
        sys.exit(1)
    
    success = generate_all_narratives(algorithm_name)
    sys.exit(0 if success else 1)
```

#### 3. QA Reviews Narratives

**Process:**

1. ✅ QA receives only the `.md` files (no code, no JSON)
2. ✅ QA reviews using narrative review checklist
3. ✅ QA documents time taken
4. ✅ QA documents issues found (if any)
5. ✅ QA approves or rejects

**Expected Outcome:**

- If Binary Search is already complete → QA approves in <20 min
- If any issues found → QA documents, backend fixes, regenerates

---

## 📊 Success Metrics for Pilot

### Before Implementation (Current State)

- Narrative validation: **None**
- QA review time: **N/A**
- Backend-FE round-trips: **2-3 per algorithm**
- "Missing data" bugs: **3-5 per algorithm**

### After Pilot (Binary Search)

**Target Metrics:**

- ✅ Narrative generation: **< 1 hour implementation**
- ✅ QA review time: **< 20 minutes for 6 examples**
- ✅ Issues found in narrative: **0-2** (proves JSON complete)
- ✅ Issues found in FE integration: **0** (narrative validated completeness)

**If Pilot Succeeds:**

- Roll out to Interval Coverage
- Update all documentation
- Establish as standard workflow

**If Pilot Fails:**

- Document what broke
- Adjust workflow
- Try again with simplified approach

---

## 🚀 Next Actions

### Session 33 (Current)

1. ✅ Review this implementation spec
2. ✅ Approve/modify approach
3. ✅ Decide: Implement now or next session?

### Session 34 (Proposed)

1. ✅ Implement Phase 1 (base infrastructure)
2. ✅ Pilot Phase 2 (Binary Search)
3. ✅ QA reviews narratives
4. ✅ Document findings
5. ✅ Adjust workflow if needed

---

**End of Implementation Specification**
