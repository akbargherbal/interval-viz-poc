# Frontend Code Investigation Tasks

## Purpose

This document outlines potential code quality issues that require investigation and verification. Each item describes a suspected problem pattern with questions to guide your analysis. **Do not assume these issues exist** - investigate first, then determine if action is needed.

---

## Investigation 1: Single Responsibility Violation in App.jsx

**Suspicion**: The main App component may be handling too many unrelated concerns.

**File**: `src/App.jsx` (340 lines)

### Questions to Investigate

1. **Responsibility Audit**:

   - What are the distinct responsibilities this component handles?
   - Count: How many `useState` declarations? How many `useEffect` blocks?
   - Does it mix UI layout definition with business logic?
   - Can you identify sections that could be tested independently?

2. **Coupling Analysis**:

   - If you needed to change the visual layout (flex to grid, reorder panels), how many lines would you need to modify?
   - If you needed to test the prediction logic in isolation, is that currently possible?
   - What happens if you need to add a new modal or panel?

3. **Change Impact**:
   - Pick a recent feature addition or bug fix in this file
   - How many unrelated areas of code did you need to understand to make the change?
   - Did you worry about breaking something unrelated?

### Investigation Criteria

**Red Flags** (investigate deeper if true):

- Component handles >3 distinct concerns (layout + data + events + modals + ...)
- Changes to visual structure require understanding business logic
- Cannot test individual features without mocking entire component
- File grows with every new feature addition

**Green Flags** (acceptable if true):

- Clear separation between orchestration and implementation
- Visual changes don't affect logic and vice versa
- Easy to test individual behaviors

### Deliverable

Document your findings:

- List of distinct responsibilities found
- Assessment: Is this component doing too much?
- If yes: Propose what should be extracted (don't implement yet)

---

## Investigation 2: Re-render Performance Concerns

**Suspicion**: Handler functions may be causing unnecessary re-renders in child components.

**File**: `src/App.jsx` (handler definitions section)

### Questions to Investigate

1. **Handler Definition Patterns**:

   - Identify all function definitions passed as props to child components
   - Are these functions defined inline in the component body?
   - Are any wrapped in `useCallback`?

2. **Child Component Impact**:

   - Identify components that receive these handlers as props:
     - `ControlBar`
     - `PredictionModal`
     - `CompletionModal`
     - Algorithm state components
   - Are any of these wrapped with `React.memo`?

3. **Performance Testing**:

   - Add console.log statements to child component render functions
   - Navigate through a trace quickly (spam arrow keys)
   - Question: Do child components re-render when they shouldn't?
   - Try wrapping a handler in `useCallback` - does re-render frequency decrease?

4. **Severity Assessment**:
   - Test with a large trace (100+ steps)
   - Does the UI feel sluggish during navigation?
   - Use React DevTools Profiler: How many components re-render per navigation action?

### Investigation Criteria

**Red Flags**:

- Child components re-render on every parent render regardless of prop changes
- UI feels sluggish with larger traces
- React DevTools shows cascading re-renders
- Handlers are plain functions (not memoized) passed to memoized children

**Green Flags**:

- Child components only re-render when their props actually change
- UI remains snappy with large traces
- Minimal re-renders in DevTools profiler

### Deliverable

- Performance profile results (before any changes)
- List of handlers that should be memoized (if any)
- Quantified impact: "Component X re-renders Y times per navigation"

---

## Investigation 3: Keyboard Shortcut Conflicts

**Suspicion**: Global keyboard listeners may conflict with each other or trigger in inappropriate contexts.

**Files to Examine**:

- `src/components/algorithm-states/TwoPointerState.jsx`
- `src/hooks/useKeyboardShortcuts.js`
- Any other files that add `window.addEventListener("keydown", ...)`

### Questions to Investigate

1. **Listener Inventory**:

   - Search codebase for `addEventListener("keydown"` - how many locations?
   - Create a table of all keyboard shortcuts:
     | Key | Component | Purpose | Modal-aware? |
     |-----|-----------|---------|--------------|
     | ... | ... | ... | ... |

2. **Conflict Testing**:

   - Open the prediction modal
   - Press each shortcut key
   - Question: Do shortcuts trigger when they shouldn't?
   - Try typing in a future text input - do shortcuts still fire?

3. **Race Condition Risk**:

   - If component A and component B both listen for key "P"
   - Are there execution order guarantees?
   - What happens if both components are mounted?

4. **Edge Cases**:
   - Open a modal, press arrow keys - does navigation still occur?
   - If modal has text input, type normal text - do shortcuts interfere?
   - Rapidly press multiple shortcut keys - any unexpected behavior?

### Investigation Criteria

**Red Flags**:

- Multiple components listening for the same key
- Shortcuts trigger when modals are open
- No centralized coordination of keyboard events
- Shortcuts fire during text input

**Green Flags**:

- Single source of truth for keyboard handling
- Shortcuts disabled when modals open
- No reported user complaints about unexpected keyboard behavior

### Deliverable

- Complete keyboard shortcut inventory
- List of conflicts or edge cases found
- Test results: "Pressing X when Y causes Z unexpected behavior"
- Recommendation: Does this need centralization?

---

## Investigation 4: Prop Drilling Depth Analysis

**Suspicion**: Shared data may be passed through multiple component levels unnecessarily.

**Starting Point**: `src/App.jsx` (where props are passed to children)

### Questions to Investigate

1. **Data Flow Mapping**:

   - Pick key data: `trace`, `step`, `metadata`, `highlight`
   - Trace where these props flow:
     ```
     App.jsx
       → [Component A]
         → [Component B]
           → [Component C]
     ```
   - What's the maximum depth for any prop?

2. **Usage Analysis**:

   - For each intermediate component in the chain:
     - Does it USE the data itself?
     - Or does it just pass it to children?
   - Count: How many components are "pass-through only"?

3. **Change Impact Test**:

   - Imagine adding a new piece of trace data that all visualizations need
   - How many component files would need modification?
   - How many component signatures would change?

4. **Coupling Assessment**:
   - Can you add a new algorithm state component without modifying App.jsx?
   - What if that new component needs access to `trace` or `step`?

### Investigation Criteria

**Red Flags**:

- Props passed through 3+ levels
- Multiple "pass-through only" components
- Adding new data requires modifying many files
- Component signatures polluted with props they don't use

**Green Flags**:

- Most components access only the props they need
- Adding new consumers doesn't require changing intermediate components
- Shallow prop passing (1-2 levels max)

### Deliverable

- Data flow diagram for key props
- Count of pass-through components
- Assessment: "Adding new shared data would require modifying X files"
- Recommendation: Would Context API help?

---

## Investigation 5: CSS Positioning Fragility

**Suspicion**: Visualization positioning may break when layout styles are modified.

**File**: `src/components/visualizations/TimelineView.jsx`

### Questions to Investigate

1. **Code Inspection**:

   - Look for inline style calculations involving percentages
   - Are there hardcoded numbers like `0.92`, `4`, `96`?
   - Do comments mention "padding compensation" or similar?

2. **Calculation Dependency**:

   - Identify what parent container styles these calculations assume
   - Does positioning math depend on specific padding values?
   - What happens if parent padding changes?

3. **Break Test**:

   - Change parent container padding from `p-4` to `p-6`
   - Does visualization alignment break?
   - Try changing from `px` to `rem` units
   - Does anything break?

4. **Similar Patterns**:
   - Search other visualization files for similar percentage math
   - Are there magic numbers in `ArrayView.jsx`, `IntervalView.jsx`?

### Investigation Criteria

**Red Flags**:

- Hardcoded multipliers (0.92, 0.88, etc.) in positioning
- Positioning breaks when container padding changes
- Comments explaining "this accounts for padding"
- Position calculations that reverse-engineer parent styles

**Green Flags**:

- Pure percentage calculations
- Positioning independent of parent padding
- Clean separation of concerns (content vs. positioning)

### Deliverable

- List of magic numbers found with their locations
- Break test results
- Screenshot comparisons: before/after padding change
- Severity: "Visual breaks catastrophically" vs "Minor misalignment"

---

## Investigation 6: Render Optimization Opportunities

**Suspicion**: Some objects may be unnecessarily recreated on every render.

**File**: `src/components/visualizations/ArrayView.jsx` (and similar)

### Questions to Investigate

1. **Object Definition Audit**:

   - Search for object/array definitions inside component functions
   - Identify const declarations that never change:
     - Style mappings
     - Configuration objects
     - Lookup tables

2. **Render Frequency**:

   - Add console.log with `JSON.stringify(POINTER_STYLES)` in component body
   - Navigate through trace
   - Question: Is this object recreated every render?

3. **Impact Assessment**:

   - How large are these objects?
   - How frequently does the component render?
   - Use Chrome Memory Profiler: Is there excessive allocation?

4. **Pattern Search**:
   - Are there similar patterns in other components?
   - How widespread is this issue?

### Investigation Criteria

**Red Flags**:

- Large objects defined inside component body
- High-frequency rendering components (on every step change)
- Memory profiler shows excessive allocations

**Green Flags**:

- Constants defined outside components
- Minimal object recreation
- Component renders are unavoidable

### Deliverable

- List of objects being unnecessarily recreated
- Estimated frequency (renders per minute during trace navigation)
- Performance impact: "Minor" vs "Significant"

---

## Investigation 7: Error Boundary Coverage

**Suspicion**: Some error-prone components may not be protected by error boundaries.

**File**: `src/App.jsx` (modal rendering sections)

### Questions to Investigate

1. **Coverage Audit**:

   - Identify all `ErrorBoundary` usage in App.jsx
   - List all modals and dynamic components
   - Which are wrapped? Which are not?

2. **Risk Assessment**:

   - Which components are most likely to fail?
     - Dynamic imports/registry lookups
     - Modals with complex state
     - Third-party integrations
   - What happens if `PredictionModal` throws an error?

3. **Failure Testing**:

   - Temporarily add `throw new Error("test")` to modal component
   - What happens to the app?
   - Does entire app crash or just modal?
   - Is there any user feedback?

4. **Recovery Capability**:
   - If a modal crashes, can the user recover?
   - Or do they lose all state and need to refresh?

### Investigation Criteria

**Red Flags**:

- Modal error crashes entire application
- No error boundaries around dynamic components
- User loses all state on modal error
- No graceful degradation

**Green Flags**:

- Errors contained to failing component
- User can dismiss error and continue
- State preserved on component failure

### Deliverable

- Error boundary coverage map
- Failure test results for each uncovered component
- Risk assessment: "High" vs "Low" for each uncovered component
- Recommendation: Which components need boundaries?

---

## Investigation Process & Deliverables

### Critical Requirement: Executive Summaries

Each investigation **must** produce a standardized Executive Summary document. These 7 summaries will collectively form the **Frontend Refactoring Plan**.

#### Why Executive Summaries Matter

1. **Avoid Duplicate Effort**: Understanding cross-cutting concerns before implementation
2. **Efficient Grouping**: Identify which fixes can be done together in a single refactoring session
3. **Dependency Mapping**: Some fixes may require others to be completed first
4. **Resource Planning**: Accurately estimate total effort when issues are properly grouped

---

### Executive Summary Template

Each investigator must complete this template:

```markdown
# Executive Summary: [Investigation Name]

## Investigation ID

INV-[1-7]: [Short Title]

## Status

[ ] Investigation Complete
[ ] Issue Confirmed / Not Confirmed / Partially Confirmed
Date Completed: YYYY-MM-DD

---

## Findings Summary (3-5 sentences)

[Concise description of what you found. Be specific with numbers.]

Example: "App.jsx contains 8 distinct responsibilities spanning 340 lines.
Visual layout changes require understanding business logic in 5 different
sections. Testing individual features requires mocking 12 dependencies."

---

## Evidence & Metrics

### Quantitative Data

- [Specific measurements you collected]
- [Numbers, counts, percentages]
- [Performance metrics if applicable]

### Qualitative Observations

- [Patterns you noticed]
- [Code smells identified]
- [Developer pain points]

### Test Results

- [What you tested]
- [What broke / didn't break]
- [Screenshots or recordings if relevant]

---

## Severity Assessment

**Impact**: [ ] Critical / [ ] High / [ ] Medium / [ ] Low / [ ] None
**Urgency**: [ ] Immediate / [ ] Soon / [ ] Eventually / [ ] Not Needed

**Justification**:
[Why did you assign these ratings? What's the business/technical impact?]

---

## Affected Files & Components

**Direct Impact**:

- `path/to/file.jsx` (lines X-Y)
- `path/to/another.jsx` (entire file)

**Indirect Impact** (will need changes if this is fixed):

- `path/to/dependent.jsx`
- `path/to/consumer.jsx`

**Estimated Files to Modify**: [number]

---

## Dependencies & Related Investigations

**Depends On** (must be fixed first):

- [ ] INV-X: [Investigation name]
- [ ] INV-Y: [Investigation name]

**Blocks** (other investigations waiting on this):

- [ ] INV-Z: [Investigation name]

**Related To** (could be fixed together):

- [ ] INV-W: [Investigation name]
- Reason: [Why these should be grouped]

---

## Recommended Solution Approach

**Strategy**: [High-level approach - what pattern/technique should be used?]

**Implementation Steps** (rough outline, not detailed):

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Estimated Effort**: [X hours/days]

**Risk Assessment**:

- Breaking changes: [ ] Yes / [ ] No
- Requires testing: [ ] Yes / [ ] No
- Affects user experience: [ ] Yes / [ ] No

---

## Recommendation

[ ] **Fix Now** - Critical path item, blocks other work
[ ] **Fix in Sprint 1** - High priority, clear solution
[ ] **Fix in Sprint 2** - Medium priority, plan alongside other work
[ ] **Monitor** - Not urgent, revisit in 3 months
[ ] **Not an Issue** - Suspicion not confirmed, no action needed

**Additional Notes**:
[Any context that will help during refactoring planning]

---

**Investigator**: [Name]
**Review Date**: [Date when team should review this]
```

---

### Investigation Workflow

#### Phase 1: Individual Investigation (Week 1)

Each team member takes 1-2 investigations:

1. **Day 1-2**: Conduct investigation using provided questions
2. **Day 3**: Complete Executive Summary document
3. **Day 4**: Internal review (peer check for completeness)
4. **Day 5**: Submit to lead/architect

#### Phase 2: Cross-Analysis (Week 2, Day 1)

Lead/architect reviews all 7 summaries:

1. **Identify Clusters**: Which investigations share affected files?
2. **Map Dependencies**: Create dependency graph between issues
3. **Group by Theme**: Which can be tackled in same refactoring session?

#### Phase 3: Refactoring Plan Creation (Week 2, Day 2)

Using the 7 Executive Summaries, create master plan:

```markdown
# Frontend Refactoring Plan

## Refactoring Session 1: [Theme]

**Duration**: [X hours]
**Fixes**: INV-1, INV-6, INV-7 (grouped because...)
**Files Modified**: [consolidated list]
**Dependencies**: None (can start immediately)

## Refactoring Session 2: [Theme]

**Duration**: [X hours]
**Fixes**: INV-2, INV-4 (grouped because...)
**Files Modified**: [consolidated list]
**Dependencies**: Requires Session 1 complete

## Refactoring Session 3: [Theme]

...
```

#### Phase 4: Team Review (Week 2, Day 3)

- Review consolidated refactoring plan
- Assign session owners
- Schedule implementation sprints

---

### Example Cross-Investigation Insights

After collecting all 7 Executive Summaries, you might discover:

**Efficiency Opportunity**:

> "INV-1 (App.jsx structure) and INV-4 (Props drilling) both require
> modifying the same 8 component files. By doing them together in a
> single session, we modify each file once instead of twice.
> Combined effort: 4 hours instead of 6 hours separately."

**Dependency Chain**:

> "INV-2 (Performance) requires handlers to be stable. INV-1 (App.jsx)
> will extract components that own those handlers. Therefore INV-1 must
> be completed before INV-2, or we'll need to refactor twice."

**False Positive**:

> "INV-6 (Render optimization) investigation found the object is only
> recreated 3 times per session, not per render. The performance impact
> is negligible. Marking as 'Not an Issue' and removing from plan."

**Scope Creep Prevention**:

> "INV-3 (Keyboard shortcuts) touches 4 files. INV-5 (CSS positioning)
> touches completely different files. These should NOT be grouped -
> different concerns, different risk profiles."

---

### Success Criteria

**Investigation Phase is Complete When**:

- ✅ All 7 Executive Summaries submitted
- ✅ Each summary follows the template
- ✅ All metrics/evidence collected
- ✅ Dependencies between investigations identified
- ✅ Team lead has reviewed and approved all summaries

**Ready to Refactor When**:

- ✅ Refactoring sessions are grouped efficiently
- ✅ Each session has clear scope and owner
- ✅ Dependencies are mapped (session order determined)
- ✅ Total effort estimated and approved
- ✅ Risk mitigation strategies identified

---

### Timeline

| Phase                     | Duration            | Output                              |
| ------------------------- | ------------------- | ----------------------------------- |
| Individual Investigations | Week 1 (5 days)     | 7 Executive Summaries               |
| Cross-Analysis            | Week 2 Day 1        | Dependency map, clustering analysis |
| Plan Creation             | Week 2 Day 2        | Frontend Refactoring Plan           |
| Team Review               | Week 2 Day 3        | Approved plan, assigned owners      |
| **Total**                 | **~7 working days** | **Ready to execute refactoring**    |

---

## Critical Reminders

1. **Complete the Template**: Every field must be filled. "TBD" or "Unknown" means investigation isn't complete.

2. **Be Specific with Numbers**: "App.jsx is too big" ❌ vs "App.jsx has 8 responsibilities across 340 lines" ✅

3. **Identify Overlaps**: Note when your investigation touches the same files as another investigation.

4. **Challenge Assumptions**: If investigation shows "not an issue," that's a valid finding - document why.

5. **Think Holistically**: Your investigation is one piece of a larger puzzle - help future-you during refactoring.

---

## Deliverable Structure

```
docs/frontend-investigation/
├── INV-1_app_component_responsibility.md
├── INV-2_render_performance.md
├── INV-3_keyboard_shortcuts.md
├── INV-4_props_drilling.md
├── INV-5_css_positioning.md
├── INV-6_render_optimization.md
├── INV-7_error_boundaries.md
└── REFACTORING_PLAN.md  (created after all 7 are done)
```

**Final Output**: One consolidated `REFACTORING_PLAN.md` that efficiently groups the 7 investigations into actionable refactoring sessions.
