# Merge Intervals Execution Narrative

**Algorithm:** Merge Intervals
**Input Intervals:** 3 intervals
**Result:** 3 merged intervals
**Merges Performed:** 0

---

## Step 0: 📊 Sort 3 intervals by start time

**Original Intervals (unsorted):**
- Interval 1: [1, 2]
- Interval 2: [3, 4]
- Interval 3: [5, 6]

**After Sorting by Start Time:**
- Interval 1: [1, 2]
- Interval 2: [3, 4]
- Interval 3: [5, 6]

**Why Sort?** Sorting by start time ensures we process intervals in chronological order, making it easy to detect overlaps by comparing each interval with the last merged interval.

**Timeline State:**
- Total intervals: 3
- Merged so far: 0
- Pending: 3

---

## Step 1: 🔍 Compare interval [3, 4] with last merged [1, 2]

**Current Interval:** [3, 4]
**Last Merged Interval:** [1, 2]

**Overlap Check:**
```
Compare current.start (3) with last_merged.end (2)
3 <= 2? → False
```

**Decision:** Intervals **do not overlap** because current starts (3) after last ends (2)
- Action: Add current interval as new separate interval

**Timeline State:**
- Merged so far: 1
- Pending: 1

---

## Step 2: ➕ Add new interval [3, 4] (no overlap)

**Adding New Interval:**
- Interval: [3, 4]
- This interval does not overlap with the last merged interval
- Added as separate interval to result

---

## Step 3: 🔍 Compare interval [5, 6] with last merged [3, 4]

**Current Interval:** [5, 6]
**Last Merged Interval:** [3, 4]

**Overlap Check:**
```
Compare current.start (5) with last_merged.end (4)
5 <= 4? → False
```

**Decision:** Intervals **do not overlap** because current starts (5) after last ends (4)
- Action: Add current interval as new separate interval

**Timeline State:**
- Merged so far: 2
- Pending: 0

---

## Step 4: ➕ Add new interval [5, 6] (no overlap)

**Adding New Interval:**
- Interval: [5, 6]
- This interval does not overlap with the last merged interval
- Added as separate interval to result

---

## Execution Summary

**Input:** 3 intervals
**Output:** 3 merged intervals
**Merges Performed:** 0

**Final Merged Intervals:**
- Interval 1: [1, 2]
- Interval 2: [3, 4]
- Interval 3: [5, 6]

**Performance:**
- Time Complexity: O(n log n) - dominated by sorting
- Space Complexity: O(n) - for storing merged result
- Merge operations: 0 (out of 2 possible)

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Merged Count** (`merged_count`) - Shows progressive building of result
- **Pending Count** (`pending_count`) - Shows remaining work
- **Overlap Comparisons** - The critical decision point (current.start vs last.end)

### Visualization Priorities

1. **Timeline axis** - Show intervals as horizontal bars on a time axis (0-24 hours)
2. **Highlight examining interval** - Use distinct color for `examining` state
3. **Show merge animation** - When intervals merge, animate the extension of last interval's end
4. **Distinguish merged vs new** - Use different colors for `merged` vs `new_interval` states
5. **Call stack visualization** - Show which interval is currently being examined

### Key JSON Paths

```
step.data.visualization.all_intervals[*].id
step.data.visualization.all_intervals[*].start
step.data.visualization.all_intervals[*].end
step.data.visualization.all_intervals[*].state  // 'pending' | 'examining' | 'merged' | 'new_interval'
step.data.visualization.call_stack_state[*].interval_id
step.data.visualization.call_stack_state[*].type
step.data.visualization.merged_count
step.data.visualization.pending_count
step.data.current_interval  // [start, end] being examined
step.data.last_merged  // [start, end] of last merged interval
step.data.overlaps  // boolean - critical decision
```

### Algorithm-Specific Guidance

Merge Intervals is fundamentally about **temporal overlap detection**. The most important visualization is the **timeline itself** - showing intervals as horizontal bars makes overlaps visually obvious. The key pedagogical moment is the **comparison step** (current.start <= last.end) - this should be highlighted with visual indicators showing the two values being compared. When a merge happens, animate the **extension** of the last interval's end time to show how the intervals combine. Use color coding to show the **state progression**: pending (gray) → examining (yellow) → merged (green) or new_interval (blue). The call stack visualization helps students track which interval is currently being processed. Consider showing a **before/after comparison** for merge operations to emphasize the transformation.
