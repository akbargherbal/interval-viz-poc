# Frontend Developer Checklist: Algorithm Integration Compliance

**Version:** 2.1.0  
**Authority:** Derived from project workflow documentation  
**Purpose:** Verify new algorithm frontend components comply with platform architecture and design standards  
**Scope:** Frontend-specific requirements only - focus on this checklist and Frontend ADRs

---

## LOCKED REQUIREMENTS (Mandatory - Cannot Be Modified)

### Registry Registration

- [ ] **State component registered in `stateRegistry.js`**

  - Import statement added at top of file
  - Entry added to `STATE_REGISTRY` object
  - Key matches backend algorithm name exactly (e.g., "binary-search")
  - Verify registration with: `isStateComponentRegistered('algorithm-name')`

- [ ] **Visualization component registered in `visualizationRegistry.js`** (if new type needed)
  - Import statement added at top of file
  - Entry added to `VISUALIZATION_REGISTRY` object
  - Key matches backend `visualization_type` metadata
  - Most algorithms reuse existing: "array" → `ArrayView`, "timeline" → `TimelineView`

### Component Organization (ADR-002)

- [ ] **State component in correct directory**

  - File location: `frontend/src/components/algorithm-states/`
  - Naming convention: `{AlgorithmName}State.jsx` (PascalCase + "State" suffix)
  - Examples: `BinarySearchState.jsx`, `MergeSortState.jsx`, `DijkstraState.jsx`
  - NOT in `visualizations/` directory (that's for reusable components)

- [ ] **Visualization component in correct directory** (if creating new reusable component)
  - File location: `frontend/src/components/visualizations/`
  - Naming convention: `{ConceptName}View.jsx` (PascalCase + "View" suffix)
  - Examples: `ArrayView.jsx`, `TimelineView.jsx`, `GraphView.jsx`
  - Only create if no existing visualization fits your needs

### Unified Dashboard Architecture

#### Dashboard Structure Compliance

- [ ] **Unified dashboard structure applied**

  - All algorithms use the same 5-zone grid layout (RSP)
  - Zone 1 (Primary): Main focus value, spans rows 1-2
  - Zone 2 (Goal): Target/objective value, top-right
  - Zone 3 (Logic): Comparison expression, middle-right
  - Zone 4 (Action): Next operation, bottom-right
  - Zone 5 (Overlay): Metadata strip (2-3 cells) at bottom of Zone 1

- [ ] **Dashboard CSS classes used correctly**

  - `.dashboard` wrapper with `h-full`
  - `.zone` for all zone containers
  - `.zone-primary`, `.zone-goal`, `.zone-logic`, `.zone-action` for specific zones
  - `.zone-boundaries` for Zone 5 overlay
  - `.boundary-cell` for individual metadata cells

- [ ] **Container query sizing applied**

  - Dashboard uses `container-type: size`
  - All sizing uses container query units (`cqh`)
  - Primary value: `clamp(40px, 26cqh, 60px)` or similar
  - Zone labels: `clamp(10px, 3.5cqh, 14px)` or similar
  - Boundary values: `clamp(12px, 7.5cqh, 16px)` or similar

- [ ] **Visual compliance verified**

  - Dashboard fills 100% of `#panel-steps` height
  - Edge-to-edge filling (no padding on `.dashboard` wrapper)
  - No borders or box-shadows on dashboard container
  - Zone labels positioned consistently (top-left, 6px inset)
  - Metadata labels positioned consistently (top-right, 6px inset)

#### Dashboard Content Mapping

- [ ] **Zone content mapped appropriately**

  - Zone 1: Main algorithm value with label and metadata
  - Zone 2: Goal/target value with label
  - Zone 3: Logic expression (two-line format: expression + result)
  - Zone 4: Action description (verb phrase)
  - Zone 5: 2-3 metadata cells (no more, no less)

- [ ] **Content mapping documented**
  - Zone assignments justified in implementation notes
  - Alternative approaches considered and rejected (if applicable)
  - Content fits within spatial constraints

#### Visualization Pattern Selection

- [ ] **LSP visualization pattern identified**

  - Iterative algorithm → Array/pointer or sliding window visualization
  - Recursive algorithm → Timeline/call stack visualization
  - Pattern documented in implementation notes

- [ ] **Visualization component chosen**
  - Existing component reused (ArrayView, TimelineView) if possible
  - New component created only if existing patterns don't fit
  - Component registered in `visualizationRegistry.js` if new

#### Reference Mockup Compliance

- [ ] **Dashboard structure matches reference**

  - Reference: `docs/static_mockup/unified_dashboard_reference.html`
  - Grid layout identical (only content differs)
  - Container query behavior matches
  - Zone positioning and sizing matches

- [ ] **Color palette aligned**
  - Primary value color matches algorithm theme
  - Goal zone uses emerald-400 (`#34d399`)
  - Logic zone uses white/blue tones
  - Action zone uses slate tones

### Static Mockup Compliance

- [ ] **Algorithm-specific mockup created and approved**

  - File location: `docs/static_mockup/{algorithm-name}-mockup.html`
  - Mockup uses unified dashboard as base
  - Mockup populated with real data from JSON payload
  - Mockup demonstrates representative algorithm state
  - Approval obtained before implementation

- [ ] **Prediction modal matches mockup**

  - Reference: `docs/static_mockup/prediction_modal_mockup.html`
  - Choice styling consistent (hover states, selection)
  - Button placement and sizing correct
  - Modal dimensions and positioning match

- [ ] **Completion modal matches mockup**
  - Reference: `docs/static_mockup/completion_modal_mockup.html`
  - Score display formatting matches
  - Button styling consistent
  - Success/partial success states match design

### Modal Keyboard Shortcuts (LOCKED Elements - INV-3)

- [ ] **Prediction modal shortcuts verified**

  - `1`, `2`, `3` keys select choices (hardcoded in PredictionModal.jsx)
  - `s` key skips current prediction (RESERVED - critical for learning flow)
  - `Enter` submits selected answer
  - `Escape` closes modal
  - NO modifications to these shortcuts without full team approval

- [ ] **Completion modal shortcuts verified**

  - `r` key restarts algorithm
  - `Enter` restarts algorithm
  - `Escape` closes modal
  - NO modifications to these shortcuts without full team approval

- [ ] **Keyboard shortcut conflicts checked**
  - Verify no component uses `s` key for other purposes (reserved for Skip in Prediction Modal)
  - Verify no component uses `1`, `2`, `3` keys for other purposes (reserved for Prediction choices)
  - Verify no component uses `r` key for other purposes (reserved for Restart in Completion Modal)
  - Check KeyboardContext priority levels if implementing new shortcuts
  - Document any new shortcuts to avoid future conflicts

### Panel Dimensions and Overflow Pattern (LOCKED Elements - INV-4)

- [ ] **Panel dimensions preserved**

  - Left panel (visualization): `flex-[3]` (responsive - fills remaining space)
  - Right panel (state): `w-96` (384px fixed width)
  - Verify responsive behavior at different screen sizes
  - NO modifications to dimensions without full team approval

- [ ] **Overflow pattern implemented correctly**
  - Panel content uses `overflow-y-auto` for vertical scrolling
  - Horizontal overflow hidden (`overflow-x-hidden`)
  - Content never forces horizontal scroll
  - Scrollbars appear only when content exceeds panel height

### Algorithm Info Markdown

- [ ] **Algorithm info file exists**

  - File location: `public/algorithm-info/{algorithm-name}.md`
  - Naming convention: Match algorithm name exactly (e.g., `binary-search.md`)
  - Accessible via: `GET /algorithm-info/{algorithm-name}.md`

- [ ] **Info content follows standard structure**
  - Educational overview (what, why, where used)
  - Complexity analysis (time/space)
  - Real-world applications
  - No code-heavy content (conceptual focus)
  - 150-250 words recommended length

---

## CONSTRAINED REQUIREMENTS (Follow Architecture Patterns)

### Architecture Documentation Review

- [ ] **Frontend ADRs reviewed before implementation**

  - Read `docs/ADR/FRONTEND/ADR-001-registry-based-architecture.md`
  - Read `docs/ADR/FRONTEND/ADR-002-component-organization-principles.md`
  - Read `docs/ADR/FRONTEND/ADR-003-context-state-management.md`
  - Understand registry pattern, component organization, context usage

- [ ] **Project README reviewed for context**

  - Read `README.md` for architecture overview
  - Understand backend/frontend contract (trace structure)
  - Review data flow: API → TraceContext → NavigationContext → Components

- [ ] **Document contradictions flagged**
  - If ADR conflicts with this checklist → Flag to PM
  - If ADR conflicts with README → Flag to PM
  - If README appears outdated or incorrect → Flag to PM
  - Escalate architectural conflicts before implementation

### Narrative-Driven Visualization Design

#### Backend Narrative Review (Foundation)

- [ ] **Backend narrative reviewed thoroughly**
  - File location: `docs/narratives/{algorithm-name}/`
  - All example scenarios reviewed
  - ⚠️ **IMPORTANT:** Take narrative seriously—backend engineer invested significant effort
  - Narrative contains: self-checks, mathematical accuracy, pedagogical explanations
  - Identify key data points mentioned in narrative
  - Identify state transitions described in narrative
  - Identify decision points requiring visual emphasis
  - Note: Narrative provides helpful context—JSON is definitive source of truth

#### JSON Payload Deep Analysis (CRITICAL)

- [ ] **JSON payload analyzed as primary source**

  - ⚠️ **WARNING:** JSON is the driving engine and source of truth
  - ⚠️ **BALANCE:** Don't ignore narrative—use it to understand pedagogical intent
  - Pull complete trace data for analysis
  - Inspect trace structure, steps array, metadata
  - Document all fields in `data.visualization`
  - Identify state transitions across steps
  - Map how narrative concepts appear in JSON
  - List all unique `step.type` values
  - Note any optional vs. required fields

- [ ] **Visualization outline created**

  - Document what to show (which JSON fields)
  - Document how to map (dashboard zones, LSP visualization)
  - Document what to omit (unnecessary details)
  - Justify each decision with narrative + JSON evidence
  - Get outline approved before mockup creation

#### Data Contract Understanding

- [ ] **Trace structure documented**

  - Understand `trace.metadata` structure
  - Understand `trace.steps` array structure
  - Understand `step.data.visualization` contract
  - Identify algorithm-specific fields
  - Document edge cases (missing data, first/last steps)

- [ ] **Backend contract verified**
  - Confirm `metadata.algorithm` matches registry key
  - Confirm `metadata.visualization_type` is correct
  - Verify prediction points structure (if applicable)
  - Check example traces for consistency

### Dashboard Implementation Pattern

- [ ] **Unified dashboard structure implemented**

```jsx
export const {Algorithm}State = ({ step, trace }) => {
  // Extract visualization data
  const visualizationData = step.data.visualization;
  
  // Map to dashboard zones
  const zone1 = {
    label: "...",
    meta: "...",
    value: "..."
  };
  
  const zone2 = { label: "...", value: "..." };
  const zone3 = { label: "...", content: "..." };
  const zone4 = { text: "..." };
  const zone5 = [
    { label: "...", value: "..." },
    { label: "...", value: "..." }
  ];
  
  return (
    <div className="dashboard h-full">
      {/* Zone 1: Primary Focus */}
      <div className="zone zone-primary">
        <div className="zone-label">{zone1.label}</div>
        <div className="zone-meta">{zone1.meta}</div>
        <div className="primary-value">{zone1.value}</div>
        
        {/* Zone 5: Overlay */}
        <div className="zone-boundaries">
          {zone5.map((cell, i) => (
            <div key={i} className="boundary-cell">
              <div className="boundary-label">{cell.label}</div>
              <div className="boundary-value">{cell.value}</div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Zone 2: Goal */}
      <div className="zone zone-goal">
        <div className="zone-label">{zone2.label}</div>
        <div className="goal-value">{zone2.value}</div>
      </div>
      
      {/* Zone 3: Logic */}
      <div className="zone zone-logic">
        <div className="zone-label">LOGIC</div>
        <div className="logic-content">{zone3.content}</div>
      </div>
      
      {/* Zone 4: Action */}
      <div className="zone zone-action">
        <div className="action-text">{zone4.text}</div>
      </div>
    </div>
  );
};
```

- [ ] **Reference implementations reviewed**
  - Studied `BinarySearchState.jsx` (iterative example)
  - Studied `IntervalCoverageState.jsx` (recursive example)
  - Pattern adapted to algorithm-specific needs

### Component Structure Best Practices

- [ ] **Safe data access implemented**

  - Optional chaining used (`step?.data?.visualization`)
  - Null checks before rendering
  - Graceful degradation for missing data
  - Early returns for error states

- [ ] **PropTypes defined**

  - All component props typed
  - Nested object shapes documented
  - Required vs. optional props marked

- [ ] **Error boundaries considered**
  - Component wrapped in ErrorBoundary if needed
  - Error states handled gracefully
  - User-friendly error messages displayed

### Context Usage (ADR-003)

- [ ] **Context hooks used correctly**

  - `useTrace()` for trace data access
  - `useNavigation()` for step control
  - `usePrediction()` for prediction state
  - `useKeyboard()` for keyboard shortcuts
  - NO direct context consumption in state components

- [ ] **Props pattern followed**
  - State components receive `step` and `trace` as props
  - No direct context access in algorithm-specific components
  - Context usage limited to top-level components

### Testing Requirements

- [ ] **Testing plan created**

  - Unit tests for component rendering
  - Tests for data transformations
  - Tests for edge cases (missing data, first/last steps)
  - Integration tests for full flow

- [ ] **Tests implemented**
  - Component renders without errors
  - Dashboard zones populated correctly
  - Graceful handling of missing data
  - PropTypes validation working

---

## FREE CHOICES (Developer Discretion)

### Visual Styling (Within Dashboard Constraints)

- ✅ Algorithm-specific color palette (primary value color)
- ✅ Typography choices (within font families)
- ✅ Animation timing and easing
- ✅ Hover states and transitions
- ✅ Icon choices (if applicable)

### Component Implementation Details

- ✅ Helper function organization
- ✅ Data transformation approach
- ✅ Conditional rendering logic
- ✅ Component composition
- ✅ Custom hooks for logic reuse

### LSP Visualization Customization

- ✅ Layout within LSP panel
- ✅ Spacing and padding
- ✅ Animation choreography
- ✅ Visual metaphors (within algorithm theme)
- ✅ Interactive elements (if appropriate)

---

## Mockup-First Workflow

### Mockup Creation (BEFORE Coding)

- [ ] **Static mockup created in HTML**

  - File location: `docs/static_mockup/{algorithm-name}-mockup.html`
  - Uses unified dashboard base structure
  - Populated with real JSON data
  - Shows representative algorithm state (mid-execution preferred)

- [ ] **Mockup demonstrates key features**

  - Dashboard zones populated with actual values
  - LSP visualization shows algorithm state
  - Color palette and typography applied
  - Responsive behavior considered

- [ ] **Mockup approved before implementation**
  - Team/PM review completed
  - Feedback incorporated
  - Final approval documented
  - Mockup serves as implementation spec

### Mockup Comparison Verification

- [ ] **Side-by-side comparison performed**

  - Implemented component vs. approved mockup
  - Dashboard structure matches
  - Colors and typography match
  - Spacing and sizing match
  - Visual polish consistent

- [ ] **Deviations documented and approved**
  - Any runtime-necessitated changes explained
  - Technical constraints documented
  - Approval obtained for deviations

---

## Quality Gates

### Pre-Implementation

- 🚨 DO NOT CODE without JSON payload analysis
- 🚨 DO NOT CODE without visualization outline
- 🚨 DO NOT CODE without static mockup approval
- 🚨 DO NOT CODE without reviewing unified dashboard reference

### Pre-Submission

- 🚨 DO NOT SUBMIT without completing this checklist
- 🚨 DO NOT SUBMIT without testing plan + implementation
- 🚨 DO NOT SUBMIT without mockup compliance verification
- 🚨 DO NOT SUBMIT without registry registration

### Escalation Triggers

- 🚨 If ADR conflicts with this checklist → Flag to PM
- 🚨 If ADR conflicts with README → Flag to PM
- 🚨 If README appears outdated → Flag to PM
- 🚨 If unified dashboard doesn't fit algorithm → Flag to PM
- 🚨 Escalate before implementing conflicting requirements

---

## Workflow Integration

**Stage 3: Frontend Integration**

1. ✅ Review this compliance checklist completely
2. ✅ Review Frontend ADRs (ADR-001, ADR-002, ADR-003)
3. ✅ Review project README.md for architecture
4. ✅ Review unified dashboard reference mockup
5. ✅ Review backend narratives for visualization insights
6. ✅ Analyze JSON payload deeply (pull trace data, document structure)
7. ✅ Identify visualization pattern (iterative/recursive)
8. ✅ Map dashboard content to 5 zones
9. ✅ Create visualization outline (what to show, how to map, what to omit)
10. ✅ Create static mockup with real data
11. ✅ Get mockup approval before coding
12. ✅ Create state component in `algorithm-states/` directory
13. ✅ Register component in `stateRegistry.js`
14. ✅ Create/verify LSP visualization component (reuse if possible)
15. ✅ Register visualization in `visualizationRegistry.js` (if new)
16. ✅ Create algorithm info markdown in `public/algorithm-info/`
17. ✅ Verify unified dashboard compliance
18. ✅ Create testing plan
19. ✅ Implement tests
20. ✅ Run all tests (unit + integration)
21. ✅ Complete this checklist
22. ✅ Submit PR with code + tests + checklist

**Next Stage:** Integration Testing (Stage 4)

---

## Time Estimates

- **ADR and Architecture Review:** 15 minutes
- **Unified Dashboard Reference Review:** 10 minutes
- **Narrative Review:** 10 minutes
- **JSON Payload Deep Analysis:** 20-30 minutes
- **Visualization Pattern Selection:** 5 minutes
- **Dashboard Content Mapping:** 5 minutes
- **Visualization Outline Creation:** 10 minutes
- **Static Mockup Creation:** 30-45 minutes
- **Mockup Approval Meeting:** 15-30 minutes
- **Component Implementation:** 20-30 minutes
- **Registry Registration:** 5 minutes
- **Algorithm Info Markdown:** 10 minutes
- **Testing Plan Creation:** 10 minutes
- **Test Implementation:** 15-20 minutes
- **Dashboard Compliance Verification:** 10 minutes

**Total:** ~2.5-3.5 hours for complete algorithm integration

---

## Key Reminders

**Your Focus:**

- ✅ Registry registration (state + visualization)
- ✅ Component organization (correct directories, naming)
- ✅ Unified dashboard compliance (5-zone structure, container queries)
- ✅ Visualization pattern selection (iterative vs. recursive)
- ✅ Dashboard content mapping (zone assignments)
- ✅ Respect narrative quality (backend engineer's pedagogical work)
- ✅ JSON-driven design (analyze payload deeply, don't reimplement logic)
- ✅ Mockup-first workflow (create and get approval before coding)
- ✅ Narrative-driven design (read narratives first!)
- ✅ Testing (plan + implementation)

**Architecture Compliance:**

- ✅ Review ADRs before implementation
- ✅ Use context hooks (avoid prop drilling)
- ✅ Follow unified dashboard structure
- ✅ Respect LOCKED elements (shortcuts, panel ratio, overflow)
- ✅ Check keyboard shortcut conflicts (`s`, `1`, `2`, `3`, `r` reserved)

**Quality Standards:**

- ✅ Safe data access (optional chaining, null checks)
- ✅ PropTypes for all components
- ✅ Graceful degradation (handle missing data)
- ✅ Visual-narrative alignment
- ✅ Balance information density (not too little, not too much)
- ✅ Respect spatial constraints (dashboard ~384px width)

**Critical Workflow Gates:**

- 🚨 DO NOT CODE without JSON analysis
- 🚨 DO NOT CODE without dashboard content mapping
- 🚨 DO NOT CODE without visualization outline
- 🚨 DO NOT CODE without static mockup approval
- 🚨 If ADR conflicts with this checklist → Flag to PM
- 🚨 If unified dashboard doesn't fit → Flag to PM before deviating
- 🚨 Escalate before implementing conflicting requirements

---

**Remember:**

- JSON payload is the driving engine - narrative is helpful but JSON is definitive
- Narrative contains valuable work - respect backend engineer's effort (self-checks, pedagogy, accuracy)
- Use narrative for "why" (pedagogical intent) and JSON for "what" (actual data)
- All algorithms use unified dashboard - only visualization pattern changes
- Dashboard zones are consistent - only content differs between algorithms
- Create mockup before code - get approval on design before implementation
- Balance is key - not too little (underwhelming), not too much (overwhelming)
- Read narratives BEFORE designing components (narrative-driven approach)
- Register EVERY component you create (both registries)
- Verify dashboard compliance BEFORE submitting (reference mockup comparison)
- Create tests BEFORE considering done (testing plan + implementation)
- Flag architectural conflicts IMMEDIATELY (don't implement contradictions)

---
