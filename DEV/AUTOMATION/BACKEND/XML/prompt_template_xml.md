# Backend Tracer Generation - User Prompt Template

## Task Definition

Generate Stage 1 Backend Artifacts (production-ready, single-shot) for the following algorithm:

**Target Algorithm:** `{{ALGORITHM_NAME}}`  
**Visualization Type:** `{{VISUALIZATION_TYPE}}`

---

## Context Materials

You have been provided with complete context in your system prompt and the following reference materials:

### A. Algorithm Specification
```json
{{ALGORITHM_SPECIFICATION_JSON}}
```

### B. Base Class Contract (Immutable)
*Inherit from this class. Do not modify it.*
```python
{{BASE_TRACER_CODE}}
```

### C. Compliance Checklist
*Your implementation must satisfy all LOCKED and CONSTRAINED requirements.*
```markdown
{{BACKEND_CHECKLIST_EXCERPT}}
```

### D. Visualization Contract
*Ensure `data.visualization` matches this structure exactly.*
```markdown
{{VISUALIZATION_CONTRACT}}
```

### E. Reference Implementation (Few-Shot Example)
*Follow the patterns demonstrated in this working tracer.*
```python
{{EXAMPLE_TRACER_CODE}}
```

---

## Core Operating Principles (Reminder)

### Universal Pedagogical Principles (ALL Algorithms)

1. **Operation Atomicity** - Unify logically-related operations in single steps
2. **State Display Efficiency** - Show each variable once per step (header OR body)
3. **Explicit Comparison Logic** - Show operands, operators, results: `X (value) op Y (value) → outcome`
4. **Term Definition Protocol** - Define jargon at first use or use descriptive language
5. **Data Structure Presentation** - Use ordered collections for narrative display; avoid unexplained ordering changes
6. **Result Field Traceability** - Every result field must have narrative trail showing when/why computed

### Algorithm-Specific Extensions

{{#if_graph_algorithm}}
**Graph Algorithm Requirements:**
- Apply all 6 universal principles PLUS graph-specific extensions
- Multi-element filtering: Show full collection, filter criteria, explicit comparisons, filtered result
- Traversal structure visibility: Stack/queue/priority queue with directional indicators
- Multi-variable state tables: Use markdown tables for distances, indegrees, previous pointers
- Multi-step result construction: Make tracking decisions explicit with purpose statements
- Conditional logic: Use IF/THEN/ELSE format for branches
- Edge operations: Show complete arithmetic for weighted graphs
- Graph topology: Markdown lists/tables (never ASCII art), show once in Step 0
{{/if_graph_algorithm}}

### Quality Gates (Self-Check Before Output)

- [ ] Atomicity: No fragmented operations across step boundaries
- [ ] Efficiency: No redundant state display (header AND body)
- [ ] Explicit Logic: All decisions show comparison data with values
- [ ] Terms: All jargon defined at/before first use
- [ ] Data Structures: No confusing unordered collection display
- [ ] Traceability: All result fields have narrative trail

---

## Required Deliverables

Generate exactly **three files** in XML format with CDATA sections:

### 1. Tracer Implementation
**Path:** `backend/algorithms/{{ALGORITHM_NAME_KEBAB}}_tracer.py`

**Requirements:**
- Inherit from `AlgorithmTracer` base class
- Implement all abstract methods: `execute()`, `get_prediction_points()`, `generate_narrative()`
- Use helper methods: `_add_step()`, `_build_trace_result()`
- Maximum 3 choices per prediction question
- Fail loudly (KeyError) if visualization data incomplete
- Complete implementation (no TODOs or placeholders)

### 2. Unit Tests
**Path:** `backend/algorithms/tests/test_{{ALGORITHM_NAME_KEBAB}}_tracer.py`

**Requirements:**
- Valid trace structure verification
- Visualization data completeness checks
- Edge case handling (empty input, single element, boundary conditions)
- Narrative generation tests (verify no KeyError exceptions)
- Prediction points validation (if applicable)

### 3. Algorithm Documentation
**Path:** `docs/algorithm-info/{{ALGORITHM_NAME_KEBAB}}.md`

**Requirements:**
- Educational overview: What it is, why it matters, how it works
- Complexity analysis (time/space)
- Common applications
- **Word count: 150-250 words**
- Focus on conceptual understanding (not code-heavy)
- Valid markdown formatting

---

## Narrative Generation Requirements

Your `generate_narrative()` implementation must:

### Structural Requirements
- Convert trace JSON to self-contained markdown explanation
- Include standardized "🎨 Frontend Visualization Hints" section with:
  - Primary Metrics to Emphasize
  - Visualization Priorities
  - Key JSON Paths
  - Algorithm-Specific Guidance

### Content Requirements
- Show ALL decision data with actual values
- Make comparisons explicit: `X (5) vs Y (3) → 5 > 3`
- Explain decision outcomes clearly
- Include result field traceability (all output fields must appear in narrative before final summary)
- Define algorithm-specific terms at first use

### Error Handling
- Fail loudly (raise KeyError) if visualization data incomplete
- This is by design—catches bugs during generation

### FAA Readiness
- All arithmetic must be correct (human audit happens after generation)
- Show calculations: `max(660, 720) = 720` not just "update to 720"
- No undefined variable references

---

## Output Format - XML with CDATA

**CRITICAL: Respond with ONLY valid XML. No preamble. No explanation. No markdown code blocks.**

Start immediately with:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
  <project_name>{{ALGORITHM_NAME_KEBAB}}</project_name>
  <description>Brief description of generated artifacts</description>
  <files>
    <file>
      <path>backend/algorithms/{{ALGORITHM_NAME_KEBAB}}_tracer.py</path>
      <content><![CDATA[
# Complete tracer implementation here
# No escaping needed inside CDATA
      ]]></content>
    </file>
    <file>
      <path>backend/algorithms/tests/test_{{ALGORITHM_NAME_KEBAB}}_tracer.py</path>
      <content><![CDATA[
# Complete test suite here
      ]]></content>
    </file>
    <file>
      <path>docs/algorithm-info/{{ALGORITHM_NAME_KEBAB}}.md</path>
      <content><![CDATA[
# Algorithm documentation here (150-250 words)
      ]]></content>
    </file>
  </files>
</project>
```

---

## Final Reminders

- **Single-shot execution** - This is your only chance; generate production-ready code
- **No iterative refinement** - Code must execute without errors on first generation
- **Pedagogical first** - Optimize for learner understanding, not code elegance
- **Fail loudly** - KeyErrors on missing data are better than incomplete narratives
- **Universal principles always apply** - Even for graph algorithms (extensions build on, not replace)
- **Complete implementations only** - No TODOs, no placeholders, no commented-out sections
- **XML output only** - No text before `<?xml` or after `</project>`

---

**Begin generation now. Output valid XML with complete, functional artifacts wrapped in CDATA sections.**