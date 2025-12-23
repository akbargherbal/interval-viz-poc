# Backend Tracer Generation - User Prompt Template v2.5

## Task Definition

Generate **Stage 1 Backend Artifacts** (production-ready, single-shot) for the following algorithm:

**Target Algorithm:** `{{ALGORITHM_NAME}}`  
**Visualization Type:** `{{VISUALIZATION_TYPE}}`

---

## Context Materials

You have complete context in your system prompt and the following reference materials:

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
*Satisfy all ARCHITECTURAL CONSTRAINTS and LOCKED requirements. Apply Universal Principles + extensions.*
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

## Generation Instructions

### Implementation Requirements

1. **Inherit from `AlgorithmTracer`** and implement 3 required abstract methods:
   - `execute(input_data)` - Algorithm logic + trace recording via `_add_step()`
   - `get_prediction_points()` - Prediction moments (≤3 choices per question)
   - `generate_narrative(trace_result)` - Convert trace to markdown (fail loudly if data incomplete)

2. **Use base class helpers**:
   - `_add_step(type, data, description)` - Records all steps (enforces MAX_STEPS=10,000)
   - `_build_trace_result(result)` - Constructs final output (auto-generates prediction_points)
   - Optionally override `_get_visualization_state()` for automatic enrichment

3. **Follow checklist**:
   - Apply 6 Universal Pedagogical Principles to narrative
   - Apply algorithm-specific extensions (graph algorithms have 7 additional patterns)
   - Include "🎨 Frontend Visualization Hints" section (LOCKED requirement)
   - Ensure result field traceability (all output fields mentioned before final summary)

### Narrative Quality Standards

Your `generate_narrative()` implementation must produce markdown that demonstrates:

- **Explicit Logic**: All decisions show operands, operator, result: `X (value) op Y (value) → outcome`
- **Arithmetic Correctness**: Show calculations: `max(660, 720) = 720` not just "update to 720"
- **Term Definitions**: Define jargon at first use or use descriptive language
- **Result Traceability**: Three-part pattern for each result field (purpose → update → application)
- **Graph-Specific** (if applicable):
  - Graph topology shown once in Step 0 (markdown lists/tables, no ASCII art)
  - Multi-element filtering: full collection → criteria → explicit comparisons → result
  - Traversal structures with directional indicators: `[A, B, C] ← C on top`
  - Multi-variable state tables (markdown tables for 3+ variables per node)
  - Edge weight calculations shown explicitly

### Self-Check Before Output

Verify your `generate_narrative()` CODE will produce output passing these checks:

1. Can readers follow logic step-by-step? (Atomicity)
2. Is state displayed efficiently? (No redundancy)
3. Are comparisons backed by visible data? (Explicit Logic)
4. Are terms defined? (Term Definition)
5. Could unordered collections cause confusion? (Data Structure)
6. Can readers predict all result fields? (Traceability)

---

## Required Deliverables

Generate exactly **three files** in XML format with CDATA sections:

### 1. Tracer Implementation
**Path:** `backend/algorithms/{{ALGORITHM_NAME_KEBAB}}_tracer.py`

**Must include:**
- Complete class inheriting from `AlgorithmTracer`
- All 3 abstract methods implemented
- `_add_step()` for ALL trace recording
- `_build_trace_result()` for final output
- No TODOs or placeholders

### 2. Unit Tests
**Path:** `backend/algorithms/tests/test_{{ALGORITHM_NAME_KEBAB}}_tracer.py`

**Must include:**
- Valid trace structure verification
- Visualization data completeness checks
- Edge case handling (empty input, single element, boundary conditions)
- Narrative generation tests (verify `generate_narrative()` executes without KeyError exceptions)
- Prediction points validation (if applicable)

### 3. Algorithm Documentation
**Path:** `docs/algorithm-info/{{ALGORITHM_NAME_KEBAB}}.md`

**Must include:**
- Focus on WHY algorithm exists (conceptual understanding)
- What it is, why it matters, where used, complexity, applications
- **Word count: 150-250 words** (strictly enforced)
- No code-heavy content
- Valid markdown formatting

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

### XML Rules (Unchanged)

1. Start immediately with `<?xml version="1.0" encoding="UTF-8"?>`
2. Wrap ALL code/content in `<![CDATA[...]]>` sections
3. No escaping needed inside CDATA—quotes, newlines, special chars are all safe
4. Order files: tracer implementation → tests → documentation
5. No text outside XML—no explanations, no preamble, no markdown blocks
6. Complete implementations only—no TODOs, no placeholders

---

## Critical Reminders

- **Single-shot execution** - Generate production-ready CODE on first attempt
- **Pedagogical first** - Your `generate_narrative()` code should optimize for learner understanding
- **Fail loudly** - Code should raise KeyErrors on missing data (better than incomplete narratives when executed)
- **Universal principles always apply** - Your narrative generation code must follow all 6 principles
- **FAA-ready code** - Your `generate_narrative()` must show arithmetic correctly when executed (human audit in Stage 1.5)
- **Complete implementations only** - No TODOs, no placeholders, no commented-out sections
- **XML output only** - No text before `<?xml` or after `</project>`

---

**Begin generation now. Output valid XML with complete, functional artifacts wrapped in CDATA sections.**
