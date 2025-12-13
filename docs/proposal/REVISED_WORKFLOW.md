# Revised Workflow: Narrative-Driven Quality Gate Integration

**Version:** 2.0 (Session 33)  
**Status:** 🔄 DRAFT - Pending Approval  
**Changes From:** v1.0 Checklist System (Session 17)

---

## 📋 Executive Summary

### What Changed

**Version 1.0 (Current):**
```
[BE Implementation] → [BE Checklist] → [PR] → [FE Integration] → [FE Checklist] → [QA Tests] → [Done]
```

**Version 2.0 (Proposed):**
```
[BE Implementation] 
    ↓
[BE Self-Narrates] ← ⭐ NEW STEP
    ↓
[BE Checklist + Narrative] 
    ↓
[QA Reviews NARRATIVE ONLY] ← ⭐ CHANGED ROLE
    ↓
    ├─→ APPROVED → [FE Integration] → [FE Checklist] → [QA Integration Tests] → [Done]
    └─→ REJECTED → [BE Fixes] → [Loop back to Self-Narrate]
```

### Key Innovation

**QA becomes a NARRATIVE GATEKEEPER**, not a JSON validator.
- QA reviews **human-readable markdown**, not JSON
- QA has **no frontend knowledge required**
- Issues discovered **before FE integration** (saves round-trips)

---

## 🏗️ The Three-Stage Quality Gate

### Stage 1: Backend Implementation + Self-Narration

**Developer Actions:**

1. ✅ Implement algorithm tracer (inherits `AlgorithmTracer`)
2. ✅ Implement `generate_narrative()` method (NEW REQUIREMENT)
3. ✅ Run backend unit tests
4. ✅ Generate narratives for ALL example inputs
5. ✅ Self-review narratives:
   - Can I follow the algorithm logic?
   - Are all decisions explained with visible data?
   - Does temporal flow make sense?
   - Can I mentally visualize this?
6. ✅ Complete Backend Compliance Checklist (UPDATED)
7. ✅ Submit PR with:
   - Code
   - Backend checklist (signed off)
   - Generated narratives (all examples)

**Deliverables:**

```
backend/algorithms/my_algorithm.py
├── MyAlgorithmTracer class
│   ├── execute()
│   ├── get_prediction_points()
│   ├── _get_visualization_state()
│   └── generate_narrative()  ← NEW METHOD
│
docs/narratives/my_algorithm/
├── example_1_basic.md          ← Generated narrative
├── example_2_edge_case.md      ← Generated narrative
└── example_3_complex.md        ← Generated narrative
│
docs/compliance/
└── backend_checklist_my_algorithm.md  ← Completed checklist
```

**Time Estimate:** 2-3 hours (was 1.5-2 hours in v1.0)

---

### Stage 2: QA Narrative Review (NEW WORKFLOW)

**QA Engineer Role:**

⚠️ **CRITICAL:** QA does NOT look at JSON, code, or frontend.
✅ **ONLY INPUT:** Generated markdown narratives

**QA Reviews For:**

1. **Logical Completeness**
   - Can I follow the algorithm from start to finish?
   - Are all decision points explained?
   - Is the data supporting each decision visible?

2. **Temporal Coherence**
   - Does step N+1 logically follow from step N?
   - Are there narrative gaps or jumps?
   - Can I reconstruct the algorithm's flow?

3. **Mental Visualization**
   - Can I imagine what the visualization would show?
   - Are state changes clear?
   - Can I track what's happening without code?

4. **Decision Transparency**
   - For each decision (keep/discard, left/right, etc.):
     - Is the comparison data visible?
     - Is the decision logic clear?
     - Is the outcome explained?

**QA Does NOT Validate:**

❌ Whether JSON structure is correct (Backend Checklist handles this)
❌ Whether frontend can render it (Integration Tests handle this)
❌ Whether coordinates/scales are correct (That's rendering detail)
❌ Performance or optimization (That's Integration Tests)

**QA Checklist (Narrative Review):**

```markdown
# QA Narrative Review: [Algorithm Name]

## Example 1: [Example Name]

### Logical Completeness
- [ ] Can follow algorithm logic start-to-finish
- [ ] All decision points explained
- [ ] No undefined references (e.g., "compare with X" but X not shown)

### Temporal Coherence
- [ ] Steps flow logically
- [ ] No narrative gaps
- [ ] Can reconstruct execution order

### Mental Visualization
- [ ] Can imagine the visualization
- [ ] State changes are clear
- [ ] Tracking is possible without code

### Decision Transparency
- [ ] Every decision has supporting data
- [ ] Comparison logic visible
- [ ] Outcomes explained

### Overall Assessment
- [ ] APPROVED - Narrative is complete and clear
- [ ] NEEDS REVISION - Issues documented below

### Issues Found:
[List specific issues with step numbers]

## Example 2: [Example Name]
[Repeat checklist]

## Final Decision:
- [ ] ✅ APPROVED - All examples pass, ready for FE integration
- [ ] ⚠️ MINOR ISSUES - Approved with notes
- [ ] ❌ REJECTED - Backend must fix and resubmit
```

**QA Feedback Format:**

```markdown
## Rejection Example:

❌ REJECTED - Interval Coverage Example 1

**Issue 1: Missing Decision Context (Step 5)**
- Narrative says: "Compare interval end (720) with max_end"
- Problem: What IS max_end at this step? Not visible.
- Impact: Cannot follow decision logic

**Issue 2: Temporal Gap (Steps 8-9)**
- Step 8: "Examining interval [900, 960]"
- Step 9: "Returning with 2 intervals kept"
- Problem: What happened to interval [900, 960]? Was it kept?

**Recommendation:**
Add max_end value to Step 5 narrative.
Add explicit decision for interval [900, 960] before Step 9.
```

**Time Estimate:** 15-20 minutes per algorithm (all examples)

---

### Stage 3: Frontend Integration (If QA Approved)

**Frontend Developer Actions:**

1. ✅ Receive:
   - Backend code (QA-approved)
   - Narratives (QA-approved as complete)
2. ✅ Create/select visualization component
3. ✅ Register in visualization registry
4. ✅ Complete Frontend Checklist
5. ✅ Submit PR

**Changed Expectations:**

- Frontend should NOT discover missing data (QA caught it)
- Frontend focuses on "how to render" not "what to render"
- Narratives serve as **reference documentation**

**Time Estimate:** 1-2 hours (unchanged from v1.0)

---

### Stage 4: Integration Testing (Final Validation)

**QA Engineer Actions:**

1. ✅ Run automated integration test suite (Suites 1-14)
2. ✅ Visual comparison to mockups
3. ✅ Cross-algorithm regression tests
4. ✅ Complete QA Integration Checklist

**Note:** This stage should have ZERO "missing data" bugs (narrative review caught them)

**Time Estimate:** 30-45 minutes (unchanged from v1.0)

---

## 📊 Updated Backend Checklist (v2.0)

### NEW SECTION: Narrative Generation

**Added to LOCKED REQUIREMENTS:**

```markdown
### Narrative Generation (NEW - v2.0)

- [ ] **Implements `generate_narrative(trace_result: dict) -> str`**
      - Abstract method in AlgorithmTracer base class
      - Converts own trace JSON → markdown
      
- [ ] **Narrative generated for ALL example inputs**
      - Each registered example has corresponding .md file
      - Files saved in `docs/narratives/[algorithm-name]/`
      
- [ ] **Narrative generation does NOT fail**
      - No KeyError exceptions
      - No missing field references
      - Fails loudly if data incomplete
      
- [ ] **Self-review completed**
      - [ ] Can follow algorithm logic from narrative alone
      - [ ] All decisions have supporting data visible
      - [ ] Temporal flow makes sense
      - [ ] Mental visualization possible
```

**Updated ANTI-PATTERNS:**

```markdown
### Narrative Anti-Patterns

- [ ] ✅ **NOT referencing undefined variables in narrative**
      Example ❌: "Compare with max_end" (but max_end not shown)
      Example ✅: "Compare 720 with max_end (660)"

- [ ] ✅ **NOT skipping decision outcomes**
      Example ❌: "Examining interval... [next step unrelated]"
      Example ✅: "Examining interval... → KEPT (extends coverage)"

- [ ] ✅ **NOT using centralized narrative generator**
      Each algorithm narrates ITSELF (no shared generator)
```

---

## 📊 Updated QA Checklist (v2.0)

### NEW SECTION: Pre-Integration Narrative Review

**Added BEFORE Integration Tests:**

```markdown
## Stage 1: Narrative Review (NEW - v2.0)

**Input:** Generated markdown narratives ONLY (no code, no JSON)

### For Each Example Input:

#### Logical Completeness
- [ ] Algorithm logic is followable start-to-finish
- [ ] All decision points are explained
- [ ] No undefined variable references
- [ ] Data supporting decisions is visible

#### Temporal Coherence  
- [ ] Steps flow logically from N to N+1
- [ ] No narrative gaps or jumps
- [ ] Execution order can be reconstructed
- [ ] State transitions are clear

#### Mental Visualization
- [ ] Can imagine what visualization would show
- [ ] State changes are clear enough to track
- [ ] No need to consult code or JSON

#### Decision Transparency
- [ ] Every decision (keep/discard, left/right) has:
  - [ ] Comparison data visible
  - [ ] Decision logic clear
  - [ ] Outcome explained

### Overall Narrative Assessment:

- [ ] ✅ APPROVED - All examples pass, ready for FE integration
- [ ] ⚠️ MINOR ISSUES - Approved with documentation notes
- [ ] ❌ REJECTED - Backend must fix and resubmit narratives

**If REJECTED:** Document specific issues with step numbers and resubmit to backend.

---

## Stage 2: Integration Tests (Existing - v1.0)

[... existing integration test suites 1-14 ...]
```

---

## 🔄 Feedback Loops

### When Narrative Review Finds Issues

**Scenario 1: Missing Decision Context**

```
QA: "Step 5 says 'compare with max_end' but doesn't show max_end value"

Backend Action:
1. Check _get_visualization_state() - is max_end included?
2. Update visualization state to include max_end
3. Regenerate narrative
4. Verify narrative now shows: "Compare 720 with max_end (660)"
5. Resubmit
```

**Scenario 2: Temporal Gap**

```
QA: "Steps 8-9 jump from examining interval to returning - what happened?"

Backend Action:
1. Check if missing _add_step() call
2. Add explicit decision step
3. Regenerate narrative
4. Verify gap is filled
5. Resubmit
```

**Scenario 3: Unclear Decision Logic**

```
QA: "Narrative says 'interval is covered' but doesn't explain why"

Backend Action:
1. Update step description to include reasoning
2. Or add comparison data to visualization state
3. Regenerate narrative
4. Verify logic is now clear
5. Resubmit
```

### When Integration Tests Find Issues (After Narrative Approved)

**This should be RARE** - it means:

1. Narrative was clear (logical completeness ✓)
2. But rendering failed (visualization implementation ✗)

**Example:**

```
Narrative: "Compare 720 with max_end (660)"  ← Clear, QA approved
Frontend: max_end line doesn't render       ← Frontend bug, not backend

Action: Frontend fixes rendering, backend JSON is correct
```

---

## 🎯 Success Metrics (Updated for v2.0)

### Efficiency Metrics

| Metric | v1.0 Target | v2.0 Target | Change |
|--------|-------------|-------------|--------|
| Time to add algorithm | 5 hours | 5.5 hours | +0.5h (narrative) |
| Backend round-trips | 2-3 | 0-1 | **-70%** |
| Frontend "missing data" bugs | 3-5 | 0-1 | **-80%** |
| QA narrative review time | N/A | 15-20 min | New |
| QA integration test time | 30-45 min | 30-45 min | Unchanged |

### Quality Metrics

| Metric | v1.0 | v2.0 | Change |
|--------|------|------|--------|
| Issues found in narrative review | 0% | 60-70% | **Earlier detection** |
| Issues found in FE integration | 60-70% | 10-20% | **Fewer surprises** |
| Issues found in QA integration | 30-40% | 20-30% | **Cleaner handoffs** |

### Confidence Metrics

- **Backend:** "I know my JSON is complete before FE touches it"
- **QA:** "I can validate completeness without frontend knowledge"
- **Frontend:** "I trust the JSON is complete when I receive it"

---

## 🚀 Migration Path: v1.0 → v2.0

### Phase 1: Update Base Infrastructure (Session 33)

**Tasks:**

1. ✅ Update `base_tracer.py`:
   - Add abstract `generate_narrative()` method
   - Add narrative validation in `_build_trace_result()`
   
2. ✅ Update Backend Checklist:
   - Add Narrative Generation section
   - Add narrative anti-patterns
   
3. ✅ Update QA Checklist:
   - Add Pre-Integration Narrative Review section
   - Add QA narrative review template

4. ✅ Create `docs/narratives/` directory structure

**Time:** 1-2 hours

---

### Phase 2: Retrofit Existing Algorithms (Session 34)

**Tasks:**

1. ✅ Implement `generate_narrative()` for Interval Coverage
2. ✅ Implement `generate_narrative()` for Binary Search
3. ✅ Generate narratives for all example inputs
4. ✅ QA reviews narratives (pilot test)
5. ✅ Fix any issues found
6. ✅ Document lessons learned

**Time:** 3-4 hours

**Success Criteria:**

- Both algorithms have complete narratives
- QA can review narratives in <20 minutes each
- Zero "missing data" issues in narratives

---

### Phase 3: Establish New Workflow (Session 35+)

**Tasks:**

1. ✅ Update PROPOSAL.md with final architecture
2. ✅ Update CHECKLIST_SYSTEM_OVERVIEW.md (this document)
3. ✅ Create developer guide: "How to Implement generate_narrative()"
4. ✅ Create QA guide: "How to Review Narratives"
5. ✅ Archive `narrative_generator_poc.py` as example

**Time:** 2-3 hours

---

## 📚 Supporting Documents (To Be Created)

### 1. Developer Guide: Implementing generate_narrative()

**Location:** `docs/guides/NARRATIVE_IMPLEMENTATION_GUIDE.md`

**Contents:**
- Step-by-step tutorial
- Pattern examples (array, timeline, graph)
- Common mistakes and fixes
- Reference to POC script (archived example)

---

### 2. QA Guide: Reviewing Narratives

**Location:** `docs/guides/NARRATIVE_REVIEW_GUIDE.md`

**Contents:**
- What to look for (4 criteria)
- What NOT to look for
- Example approvals and rejections
- Feedback templates

---

### 3. Narrative Examples Library

**Location:** `docs/narratives/examples/`

**Contents:**
- `good_example_binary_search.md` - Approved narrative
- `bad_example_missing_context.md` - Rejected (with issues highlighted)
- `bad_example_temporal_gap.md` - Rejected (with issues highlighted)

---

## ❓ FAQ (Updated for v2.0)

### Q: Why add narrative generation? Isn't JSON enough?

**A:** JSON is machine-readable, narrative is human-readable. If you can't explain your JSON in plain English, the JSON is probably incomplete. Narrative forces you to consume your own output as a story.

---

### Q: How long does it take to implement generate_narrative()?

**A:** 30-45 minutes for simple algorithms, up to 1 hour for complex ones. It's mostly string formatting - the hard part is realizing what's missing from your JSON (which is the point!).

---

### Q: What if my narrative is 2000 lines long?

**A:** Your algorithm is too complex for educational visualization. Simplify inputs or reject the algorithm. QA review should take <20 minutes, which implies ~500-line narratives max.

---

### Q: Can I use the POC script to generate narratives?

**A:** No. The POC script has hardcoded if/elif chains that don't scale. Each algorithm must narrate itself. See the POC script as an **example** only (archived in `docs/examples/`).

---

### Q: What if QA approves narrative but frontend still breaks?

**A:** That's a **frontend rendering issue**, not a backend data issue. The narrative proved the data is logically complete. Frontend needs to fix how they're using the data.

---

### Q: Do narratives get versioned?

**A:** Yes. When you update an algorithm, regenerate narratives. If logic changes, QA re-reviews. If only optimization changes, no re-review needed.

---

## ✅ Approval Checklist for v2.0 Workflow

**Before adopting this workflow:**

- [ ] Team agrees with 3-stage gate (BE → QA → FE)
- [ ] QA capacity allows 15-20 min per algorithm review
- [ ] Backend developers accept narrative implementation time
- [ ] All documentation updates planned (guides, checklists)
- [ ] Phase 1-3 migration path approved
- [ ] Success metrics defined and measurable

---

## 🎯 Next Session Agenda (34)

**If this workflow is approved:**

1. **Implement Phase 1** (1-2 hours)
   - Update `base_tracer.py`
   - Update checklists
   - Create directory structure

2. **Pilot Phase 2** (2-3 hours)
   - Retrofit Binary Search with `generate_narrative()`
   - Generate narratives for all 6 examples
   - QA reviews narratives (time it!)
   - Fix any issues
   - Document findings

3. **Evaluate** (30 minutes)
   - Did QA find issues in narratives?
   - How long did review take?
   - Would this have caught real bugs?
   - Adjust workflow if needed

**Total:** 4-6 hours (one session)

---

**Document Status:** 🔄 DRAFT - Awaiting Approval  
**Next Step:** Review with team, approve/modify workflow, proceed to Phase 1

---

**End of Revised Workflow Document**
