# Workflow v2.1 Update Plan - Session Execution Guide

**Status:** Ready for Execution  
**Target Session:** Next session (immediately upon reading this document)  
**Estimated Time:** 30 minutes  
**Output Location:** `docs/compliance/`

---

## Context Summary

**Problem Identified:** Current workflow (v2.0) has ~50% false-approval rate for arithmetic errors in narrative review. Generic QA prompts miss mathematical errors that specialized audit catches.

**Solution:** Insert FAA (Forensic Arithmetic Audit) as blocking gate between Backend and QA.

**Implementation:** Minimal documentation updates (5 files, ~75 total lines added).

---

## Execution Order

### File 1: `docs/compliance/WORKFLOW.md`

**Why First:** Master document that establishes Stage 1.5 exists and defines the overall workflow.

**Changes:**
1. Update version to v2.1 in header
2. Add Stage 1.5 section between Stage 1 and Stage 2 (~30 lines)
3. Update Stage 2 intro to note FAA prerequisite (3 lines)
4. Update Stage 3 to mention narratives as supporting reference (10 lines)
5. Update workflow diagram showing FAA gate (5 lines)
6. Update "What Changed" section to include v2.1 changes (5 lines)

**Key Content for Stage 1.5:**
```markdown
## Stage 1.5: Forensic Arithmetic Audit (NEW - v2.1)

### Quality Gate: Mathematical Verification

**Timing:** After backend generates narratives, before QA review  
**Validator:** Backend developer using FAA_PERSONA.md  
**Purpose:** Catch arithmetic errors before human QA review

### How It Works

1. Backend developer completes narrative generation (Stage 1)
2. Developer submits narratives to FAA audit:
   - Uses FAA_PERSONA.md as review guide
   - Verifies every quantitative claim
   - Checks arithmetic correctness
3. FAA identifies any mathematical errors
4. Developer fixes errors and regenerates narratives
5. Process repeats until FAA passes

### FAA Validation Scope

**FAA ONLY validates:**
- ✅ Arithmetic correctness (e.g., "20 - 10 = 10" not "20")
- ✅ State transition math (e.g., "max_end updated from 660 → 720")
- ✅ Quantitative claims consistency (e.g., counts match operations)
- ✅ Visualization-text alignment (e.g., shown elements match claimed elements)

**FAA does NOT validate:**
- ❌ Pedagogical quality (QA handles this)
- ❌ Narrative completeness (QA handles this)
- ❌ Writing style or clarity (QA handles this)

### Decision Gate

- **✅ APPROVED** → Proceed to Stage 2 (QA Narrative Review)
- **❌ REJECTED** → Return to Stage 1 (Fix arithmetic, regenerate)

**Critical:** FAA is a BLOCKING gate. No narrative proceeds to QA with arithmetic errors.

### Why This Gate Exists

**Problem discovered:** Generic narrative review has ~50% false-approval rate for arithmetic errors. Specialized mathematical validation catches errors that pedagogical review misses.

**Evidence:** See project history for case study where 3 of 6 reviewers approved narratives with systematic arithmetic errors (claiming "20 elements remain" after "eliminating 10 from 20").
```

---

### File 2: `docs/compliance/BACKEND_CHECKLIST.md`

**Why Second:** References Stage 1.5 from WORKFLOW.md, establishes FAA requirement for backend developers.

**Changes:**
1. Update version to v2.1 in header (if needed)
2. In "Narrative Generation" section, add FAA audit requirement (3 lines)
3. Update "Workflow Integration" section to include FAA steps (7 lines)

**Specific Additions:**

**In "Narrative Generation (NEW in v2.0)" section:**
```markdown
- [ ] **Narrative passes FAA arithmetic audit**
  - Submit narratives to FAA review using FAA_PERSONA.md
  - Address all arithmetic errors flagged by FAA
  - Resubmit until FAA approves (blocking requirement)
```

**In "Workflow Integration (v2.0)" section - update step numbers:**
```markdown
**Stage 1: Backend Implementation**

1. ✅ Implement tracer class
2. ✅ Implement `generate_narrative()` method
3. ✅ Run unit tests
4. ✅ Generate narratives for ALL registered examples
5. ✅ **Submit narratives to FAA audit (using FAA_PERSONA.md)**
6. ✅ **Fix arithmetic errors, regenerate until FAA passes**
7. ✅ Self-review narratives (use checklist above)
8. ✅ Complete this checklist
9. ✅ Submit PR with code + FAA-approved narratives + checklist

**Next Stage:** QA Narrative Review (see QA_INTEGRATION_CHECKLIST.md)
```

---

### File 3: `docs/compliance/FAA.md` (NEW FILE)

**Why Third:** Tool referenced by BACKEND_CHECKLIST.md. Backend developers need this to perform audit.

**Content:** Create new file containing:

```markdown
# Forensic Arithmetic Auditor (FAA) Guide

**Version:** 1.0  
**Authority:** WORKFLOW.md v2.1 - Stage 1.5  
**Purpose:** Mathematical verification of algorithm narratives  
**For:** Backend developers conducting self-audit before QA submission

---

## What is FAA?

FAA (Forensic Arithmetic Auditor) is a specialized review persona that focuses exclusively on mathematical correctness in algorithm narratives. It catches arithmetic errors that generic narrative reviews miss.

**Core Principle:** Every number is guilty until proven innocent through independent calculation.

---

## When to Use FAA

**Timing:** After generating narratives, before submitting to QA  
**Frequency:** Every narrative, every time  
**Blocking:** Yes - narratives cannot proceed to QA with arithmetic errors

---

## FAA Persona

### Core Identity

You do NOT evaluate:
- Writing quality or clarity
- Pedagogical effectiveness
- Narrative flow or structure
- Completeness of explanations

You ONLY evaluate:
- Arithmetic correctness of quantitative claims
- Mathematical consistency of state transitions
- Alignment between visualizations and numeric claims
- Logical coherence of computational steps

### Operational Mindset

**Trust nothing.** Every number is guilty until proven innocent through independent calculation.

When reviewing documentation:
1. Build an internal state-tracking model as you read
2. Extract every quantitative claim
3. Verify each claim against your model using arithmetic
4. Flag discrepancies with specific evidence
5. One arithmetic error = immediate rejection

---

## Verification Protocol

For each step containing quantitative claims:

**Extract:**
- Initial count/state
- Operation performed
- Claimed result

**Calculate:**
- Expected result using basic arithmetic
- Compare expected vs. claimed

**Document:**
- If match: Update internal model, continue
- If mismatch: Flag error with calculation proof

---

## Error Detection Focus

Hunt for these specific patterns:

1. **Copy-paste errors**: Same number appearing after different eliminations
   - Example: "Eliminated 10 elements... Search space: 20 elements" (should be 10)

2. **Stale state**: Previous step's count incorrectly carried forward
   - Example: Step 2 shows "10 remaining", Step 4 shows "10 remaining" after eliminating 6

3. **Visualization mismatches**: Text claims differ from what's shown
   - Example: Text says "eliminated [0-9]" but visualization shows indices 0-8

4. **Off-by-one errors**: Incorrect index arithmetic
   - Example: Range [10, 13] claimed as 3 elements (should be 4)

5. **State propagation failures**: Variables not updating correctly
   - Example: "max_end updated to 720" but next step shows "max_end=660"

---

## Output Format

### When Errors Found

```
❌ ARITHMETIC ERROR DETECTED

Location: [Step X, section/line reference]
Claimed: "[exact quote from narrative]"
Context: Started with [A], eliminated/changed [B]
Expected: A - B = [C]
Claimed: [D]
Verification: C ≠ D

Evidence: [show your calculation work]
Severity: CRITICAL
```

### When No Errors Found

```
✅ ARITHMETIC VERIFICATION COMPLETE

Claims verified: [N]
Errors found: 0

Spot checks performed:
- Step X: [calculation] ✅
- Step Y: [calculation] ✅
- Step Z: [calculation] ✅

Conclusion: All mathematical claims verified correct.
Status: APPROVED for QA review
```

---

## FAA Audit Process (Step-by-Step)

### Step 1: Prepare

- Open narrative file
- Open blank document for audit notes
- Clear your mind of assumptions

### Step 2: Build State Model

As you read each step:
- Track all numeric variables (counts, indices, pointers)
- Note starting values
- Calculate expected values after operations

### Step 3: Verify Each Claim

For every quantitative statement:
- Extract the claim
- Calculate what it should be
- Compare claimed vs. expected
- Document any mismatch

### Step 4: Document Findings

**If errors found:**
- List each error with location
- Show your calculation
- Quote exact text
- Mark narrative as REJECTED

**If no errors:**
- Document spot checks performed
- Mark narrative as APPROVED

### Step 5: Report

**For REJECTED narratives:**
- Return to backend developer with specific errors
- Developer fixes and regenerates
- Re-audit updated narrative

**For APPROVED narratives:**
- Document approval in audit log
- Narrative proceeds to QA review

---

## Example Audit

### Narrative Excerpt

```
Step 2: Narrow Search Space
Eliminated left half: indices [0, 9]
Eliminated 10 elements from search

Remaining Search Space:
Search space reduced to 20 elements
```

### FAA Analysis

```
❌ ARITHMETIC ERROR DETECTED

Location: Step 2, "Remaining Search Space" section
Claimed: "Search space reduced to 20 elements"

Context:
- Started with: 20 elements (indices 0-19)
- Eliminated: indices [0, 9] = 10 elements
- Operation: 20 - 10 = ?

Expected: 10 elements
Claimed: 20 elements

Verification: 20 - 10 = 10, not 20

Evidence: After eliminating 10 elements from a 20-element array, 
10 elements remain. The claimed "20 elements" is a stale state 
error (original count not updated).

Severity: CRITICAL
Action: REJECT - Backend must fix and regenerate
```

---

## Common Mistakes to Avoid

### DON'T: Approve "close enough"
```
❌ "20 elements vs 10 elements - minor difference, approve anyway"
✅ "20 ≠ 10, REJECT"
```

### DON'T: Evaluate pedagogy
```
❌ "This explanation could be clearer"
✅ Only flag if arithmetic is wrong
```

### DON'T: Skip calculations
```
❌ "Looks right at a glance"
✅ Verify with calculator every time
```

### DO: Show your work
```
✅ "Started: 20, Eliminated: 10, Expected: 20-10=10, Claimed: 20, MISMATCH"
```

---

## FAA Scope Boundaries

### IN SCOPE (FAA validates)

- ✅ Arithmetic: 20 - 10 = 10
- ✅ Counts: "3 intervals kept" matches list of 3 intervals
- ✅ State transitions: max_end updates from 660 to 720
- ✅ Index ranges: [10, 13] = 4 elements
- ✅ Visualization alignment: Text matches shown elements

### OUT OF SCOPE (QA validates)

- ❌ Logical completeness: "Is the algorithm flow clear?"
- ❌ Temporal coherence: "Do steps flow logically?"
- ❌ Mental visualization: "Can I imagine this?"
- ❌ Decision transparency: "Are decisions well-explained?"

**When in doubt:** Can I verify this with a calculator? 
- If YES → FAA scope
- If NO → QA scope

---

## Success Metrics

**You succeed when:**
- You catch arithmetic errors before QA sees them
- You provide specific, actionable error reports
- Backend can fix issues quickly based on your feedback

**You fail when:**
- You approve narratives with arithmetic errors
- QA or integration testing catches math errors you missed
- You evaluate things outside arithmetic scope

---

## Audit Checklist

Use this for each narrative:

- [ ] Built internal state model while reading
- [ ] Verified every quantitative claim
- [ ] Checked all arithmetic operations
- [ ] Validated state transitions
- [ ] Compared visualizations to text claims
- [ ] Documented all errors found (if any)
- [ ] Marked narrative APPROVED or REJECTED
- [ ] Provided specific evidence for rejections

---

## Quick Reference Card

**What to verify:**
- Counts after additions/subtractions
- Index ranges and their element counts
- State variable updates
- Visualization-text alignment

**How to verify:**
- Extract: Initial value, operation, claimed result
- Calculate: Expected result independently
- Compare: Expected vs. claimed
- Flag if mismatch

**Output:**
- APPROVED: All math checks out
- REJECTED: Specific errors with evidence

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Session [X] | Initial FAA guide created for v2.1 workflow |

---

**Remember:** One arithmetic error = narrative rejected. Mathematical correctness is non-negotiable.
```

---

### File 4: `docs/compliance/QA_INTEGRATION_CHECKLIST.md`

**Why Fourth:** Assumes FAA already passed (established in previous files).

**Changes:**
1. Add FAA prerequisite block to Phase 1 intro (5 lines)
2. Add line to "What QA does NOT review" (1 line)
3. Add note to review criteria about arithmetic (1 line)

**Specific Additions:**

**In "Phase 1: Narrative Review" section:**
```markdown
## Phase 1: Narrative Review (NEW in v2.0)

**Timing:** AFTER backend implementation, BEFORE frontend integration  
**Input:** FAA-approved narratives in `docs/narratives/[algorithm-name]/*.md`
**Purpose:** Validate logical completeness and pedagogical quality

**PREREQUISITE:**
- ✅ **Narratives have passed FAA arithmetic audit**
- ✅ All quantitative claims verified correct
- ✅ QA focuses on logical flow and completeness (NOT arithmetic)

### What QA Reviews

**ONLY the narratives in `docs/narratives/[algorithm-name]/*.md`**

QA does NOT look at:

- ❌ Backend code
- ❌ JSON trace structure
- ❌ Frontend components
- ❌ Visual rendering
- ❌ Arithmetic correctness (FAA already validated)
```

**In "Review Criteria" intro:**
```markdown
### Review Criteria

**NOTE:** Arithmetic correctness already validated by FAA. Focus on:
- Can I understand the algorithm logic?
- Are decisions explained clearly?
- Does the flow make sense?

For each example narrative:
```

---

### File 5: `docs/compliance/FRONTEND_CHECKLIST.md`

**Why Fifth:** Receives FAA+QA approved output, lowest dependency.

**Changes:**
1. Add FAA audit line to pre-integration validation (1 line)
2. Add narratives availability line (1 line)
3. Add optional "Using Narratives" section (~20 lines)

**Specific Additions:**

**In "Pre-Integration Validation" section:**
```markdown
## Pre-Integration Validation

**Before starting frontend work:**

- [ ] **QA narrative review PASSED** - Narratives approved for logical completeness
- [ ] **FAA audit completed** - Arithmetic correctness verified
- [ ] **Backend JSON contract validated** - Narrative confirmed data completeness
- [ ] **FAA-approved narratives available** - Located in `docs/narratives/[algorithm-name]/`
- [ ] **Trust the JSON** - Frontend focuses on "how to render" not "what to render"
```

**Add new section after "Pre-Integration Validation":**
```markdown
## Using Narratives as Reference (Optional but Recommended)

**Narratives are your "script":**
- **JSON is the fuel** (drives your React engine) ← PRIMARY
- **Markdown narratives provide context** (accelerates understanding) ← SUPPORTING

### When to Reference Narratives

- ✅ Understanding algorithm intent ("Why does this step happen?")
- ✅ Debugging visualization ("What should step 5 look like?")
- ✅ Verifying decision logic ("Is my rendering showing the right comparison?")
- ✅ Onboarding to new algorithm ("How does this work?")

### What Narratives Are NOT

- ❌ UI specifications (you have creative freedom - see mockups)
- ❌ Layout requirements (mockups govern visual standards)
- ❌ Binding constraints (JSON is the contract)
- ❌ Implementation instructions (you decide HOW to visualize)

### The Director Analogy

Think of it like theater production:
- **JSON** = Musical score (precise technical notation)
- **Narrative** = Director's notes (context, intent, interpretation)
- **Frontend** = Performance (you bring it to life on stage)

The score tells you exactly what notes to play. The director's notes help you understand why those notes were chosen and what emotion to convey. But you're the performer - you decide the staging, lighting, movements, and presentation.

**Remember:** Narratives describe WHAT the algorithm does. You decide HOW to visualize it. Your creative freedom is protected by WORKFLOW.md's three-tier system (LOCKED/CONSTRAINED/FREE).
```

---

## Execution Checklist

When executing next session, follow this exact sequence:

1. [ ] Open `docs/compliance/WORKFLOW.md`
   - [ ] Add Stage 1.5 section
   - [ ] Update Stage 2 intro
   - [ ] Update Stage 3 intro
   - [ ] Update workflow diagram
   - [ ] Save file

2. [ ] Open `docs/compliance/BACKEND_CHECKLIST.md`
   - [ ] Add FAA audit requirement to narrative section
   - [ ] Update workflow integration steps
   - [ ] Save file

3. [ ] Create `docs/compliance/FAA.md`
   - [ ] Copy full FAA guide content from this plan
   - [ ] Save file

4. [ ] Open `docs/compliance/QA_INTEGRATION_CHECKLIST.md`
   - [ ] Add FAA prerequisite block
   - [ ] Add arithmetic exclusion to "What QA does NOT review"
   - [ ] Add note to review criteria
   - [ ] Save file

5. [ ] Open `docs/compliance/FRONTEND_CHECKLIST.md`
   - [ ] Update pre-integration validation
   - [ ] Add "Using Narratives" section
   - [ ] Save file

6. [ ] Verification
   - [ ] All 5 files updated/created
   - [ ] Cross-reference links work
   - [ ] Version numbers updated where needed
   - [ ] No contradictions between documents

---

## Post-Execution Verification

After completing all edits, verify:

1. **Dependency chain correct:**
   - WORKFLOW.md establishes Stage 1.5
   - BACKEND_CHECKLIST.md references Stage 1.5
   - FAA.md is referenced by BACKEND_CHECKLIST.md
   - QA_INTEGRATION_CHECKLIST.md assumes FAA passed
   - FRONTEND_CHECKLIST.md receives FAA+QA approved output

2. **No contradictions:**
   - All documents agree on FAA scope (arithmetic only)
   - All documents agree on QA scope (logic/pedagogy)
   - All documents agree narratives are supporting (not binding) for FE

3. **Completeness:**
   - Backend knows to run FAA audit
   - QA knows arithmetic already validated
   - Frontend knows narratives available as reference

---

## Success Criteria

**You'll know the update is complete when:**

- ✅ 5 files updated/created in `docs/compliance/`
- ✅ Stage 1.5 (FAA gate) exists in workflow
- ✅ Backend checklist requires FAA audit
- ✅ FAA.md provides clear audit guide
- ✅ QA checklist assumes FAA passed
- ✅ Frontend checklist mentions narrative availability
- ✅ All cross-references valid
- ✅ Total additions: ~75 lines across 5 files
- ✅ No verbose bloat - lean, actionable updates only

---

## Time Estimate

- WORKFLOW.md: 10 minutes
- BACKEND_CHECKLIST.md: 5 minutes
- FAA.md: 5 minutes (copy from this plan)
- QA_INTEGRATION_CHECKLIST.md: 5 minutes
- FRONTEND_CHECKLIST.md: 5 minutes
- **Total: ~30 minutes**

---

**Upon reading this document next session, proceed directly to File 1 (WORKFLOW.md) and execute in order.**
