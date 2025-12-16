# ADR-003: Context-Based State Management Architecture

## Status

✅ Accepted (2025-01-16)
Supersedes: Hook-based prop passing pattern
Resolves: INV-1, INV-2, INV-4, INV-3

## Context

The frontend application suffered from a "God Object" anti-pattern in `App.jsx`, which had grown to ~340 lines of code. This component was responsible for:

1. Fetching trace data
2. Managing navigation state (current step)
3. Handling prediction mode logic
4. Managing visual highlighting
5. Coordinating keyboard shortcuts
6. Rendering the UI layout

This centralization caused several issues:

- **Prop Drilling**: Data had to be passed through multiple layers of components (e.g., `App` -> `MainVisualization` -> `TimelineView`).
- **Performance**: Any state change in `App.jsx` (like a step increment) caused the entire application tree to re-render.
- **Fragility**: Modifying one concern (e.g., prediction logic) risked breaking unrelated features (e.g., navigation).
- **Maintenance**: The file was difficult to read and reason about.

## Decision

We decided to refactor the state management architecture to use the **React Context API**, splitting the monolithic state into four domain-specific contexts:

1. **TraceContext**: Manages raw trace data loading and metadata.
2. **NavigationContext**: Manages current step index and derived step data.
3. **PredictionContext**: Manages active learning mode, questions, and scoring.
4. **KeyboardContext**: Centralizes keyboard event handling with a priority system.

We also introduced a **Container/Presentational** pattern for the main panels (`VisualizationPanel`, `StatePanel`) to further decouple layout from logic.

## Consequences

### Positive

- **Decoupling**: `App.jsx` reduced from ~340 lines to <100 lines. It now acts solely as a layout coordinator and provider root.
- **Performance**: Re-renders are scoped to the specific context consumers. Changing the step doesn't re-render the header or unrelated controls.
- **Maintainability**: Logic is encapsulated in dedicated providers (`src/contexts/`).
- **Scalability**: New features (e.g., a new "Tutorial Mode") can be added as new Contexts without bloating existing files.
- **Event Management**: The `KeyboardContext` solves the "fighting listeners" problem (INV-3) by enforcing a priority system for global shortcuts vs. modal interactions.

### Negative

- **Complexity**: New contributors must understand the Context API and the provider hierarchy.
- **Boilerplate**: Creating a new piece of global state requires setting up a Context and Provider, rather than just a `useState` hook.
- **Nesting**: The component tree in React DevTools is deeper due to the stack of Providers.

## Alternatives Considered

### 1. Redux / Redux Toolkit

- **Pros**: Robust debugging tools, standardized patterns, middleware support.
- **Cons**: Significant boilerplate, steep learning curve, overkill for the current scale of state (mostly read-only trace data + simple counters).
- **Decision**: Rejected. The app's state is not complex enough to warrant Redux.

### 2. Zustand

- **Pros**: Minimal boilerplate, no provider wrapping, high performance.
- **Cons**: Adds an external dependency.
- **Decision**: Rejected. React Context is built-in and sufficient for our needs. If performance becomes a bottleneck in the future, migration to Zustand is straightforward.

### 3. Keep Hooks (Status Quo)

- **Pros**: Simple, explicit data flow.
- **Cons**: Did not solve the prop drilling or `App.jsx` bloat issues.
- **Decision**: Rejected.

## Implementation Details

### Provider Hierarchy

```jsx
<TraceProvider>
  {" "}
  {/* Loads data */}
  <NavigationProvider>
    {" "}
    {/* Depends on Trace */}
    <PredictionProvider>
      {" "}
      {/* Depends on Nav & Trace */}
      <HighlightProvider>
        <KeyboardProvider>
          <App />
        </KeyboardProvider>
      </HighlightProvider>
    </PredictionProvider>
  </NavigationProvider>
</TraceProvider>
```

### Keyboard Event Management

We implemented a centralized `KeyboardContext` that replaces scattered `window.addEventListener` calls. Components register handlers with a priority level:

- **Priority 10 (Critical)**: Modals (Prediction, Completion) - blocks lower priorities.
- **Priority 5 (High)**: Dropdowns, temporary UI.
- **Priority 1 (Global)**: General navigation (Arrow keys).

This ensures that pressing `Esc` closes the top-most modal without triggering other listeners.
EOF

````

### 2. Create `docs/MIGRATION_GUIDE.md`

```bash
cat > docs/MIGRATION_GUIDE.md << 'EOF'
# Frontend Migration Guide

## Overview

The frontend architecture has moved from a monolithic `App.jsx` using custom hooks to a **Context-based architecture**. This guide explains how to migrate existing components or create new ones using the new patterns.

## Architecture Changes

| Old Pattern | New Pattern |
|-------------|-------------|
| State in `App.jsx` | State in `src/contexts/*.jsx` |
| Props passed down 3+ levels | `useContext` (via custom hooks) |
| `useTraceLoader` returns state | `useTraceLoader` wraps `TraceContext` |
| `window.addEventListener` | `useKeyboardShortcuts` (via `KeyboardContext`) |

## Migrating a Component

### 1. Accessing Data

**Before:**
```jsx
// Component received props from App.jsx
const MyComponent = ({ currentStep, trace }) => {
  // ...
};
````

**After:**

```jsx
// Component consumes context hooks
import { useTraceNavigation } from "../hooks/useTraceNavigation";
import { useTraceLoader } from "../hooks/useTraceLoader";

const MyComponent = () => {
  const { currentStep } = useTraceNavigation();
  const { trace } = useTraceLoader();
  // ...
};
```

### 2. Handling Keyboard Shortcuts

**Before:**

```jsx
useEffect(() => {
  const handler = (e) => {
    if (e.key === "ArrowRight") nextStep();
  };
  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, []);
```

**After:**

```jsx
import { useKeyboardShortcuts } from "../hooks/useKeyboardShortcuts";

// Inside component
useKeyboardShortcuts({
  ArrowRight: nextStep,
  // Priority is handled automatically (default: 1)
});
```

### 3. Adding a New Algorithm State Component

1. Create the component in `src/components/algorithm-states/{AlgorithmName}State.jsx`.
2. Use the `step` prop (passed by `StatePanel`) or context if global data is needed.
3. Register it in `src/utils/stateRegistry.js`.

```jsx
// src/components/algorithm-states/MyAlgoState.jsx
import React from "react";

const MyAlgoState = ({ step }) => {
  // Local state logic
  return <div>...</div>;
};

export default MyAlgoState;
```

## Best Practices

1. **Memoization**: Use `useCallback` for event handlers passed to Context or children to prevent re-renders.
2. **Selectors**: If you only need one piece of data from a context, destructure it: `const { currentStep } = useTraceNavigation();`.
3. **Strict Mode**: The app runs in Strict Mode; ensure effects have proper cleanup.
