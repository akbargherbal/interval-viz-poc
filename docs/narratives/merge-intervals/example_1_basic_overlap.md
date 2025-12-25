# Merge Intervals Execution Narrative

**Algorithm:** Merge Intervals
**Input Intervals:** 4 intervals
**Result:** 3 merged intervals
**Merges Performed:** 1

---

## Step 0: 📊 Sort 4 intervals by start time

**Original Intervals (unsorted):**
- Interval 1: [1, 3]
- Interval 2: [2, 6]
- Interval 3: [8, 10]
- Interval 4: [15, 18]

**After Sorting by Start Time:**
- Interval 1: [1, 3]
- Interval 2: [2, 6]
- Interval 3: [8, 10]
- Interval 4: [15, 18]

**Why Sort?** Sorting by start time ensures we process intervals in chronological order, making it easy to detect overlaps by comparing each interval with the last merged interval.

**Timeline State:**
- Total intervals: 4
- Merged so far: 0
- Pending: 4

---

## Step 1: 🔍 Compare interval [2, 6] with last merged [1, 3]

**Current Interval:** [2, 6]
**Last Merged Interval:** [1, 3]

**Overlap Check:**
```
Compare current.start (2) with last_merged.end (3)
2 <= 3? → True
```

**Decision:** Intervals **overlap** because current starts (2) before or when last ends (3)
- Action: Merge by extending the last interval's end time

**Timeline State:**
- Merged so far: 1
- Pending: 2

---

## Step 2: 🔗 Merge: Extend last interval to [1, 6]

**Merging Intervals:**
- Current interval: [2, 6]
- Last merged (before): [1, 3]

**End Time Calculation:**
```
new_end = max(3, 6) = 6
```

**Result:**
- Last merged (after): [1, 6]
- The last interval now spans from 1 to 6

**Why max()?** We take the maximum of the two end times to ensure the merged interval covers both original intervals completely. If current interval is fully enclosed (ends before last ends), we keep the larger end time.

---

## Step 3: 🔍 Compare interval [8, 10] with last merged [1, 6]

**Current Interval:** [8, 10]
**Last Merged Interval:** [1, 6]

**Overlap Check:**
```
Compare current.start (8) with last_merged.end (6)
8 <= 6? → False
```

**Decision:** Intervals **do not overlap** because current starts (8) after last ends (6)
- Action: Add current interval as new separate interval

**Timeline State:**
- Merged so far: 1
- Pending: 1

---

## Step 4: ➕ Add new interval [8, 10] (no overlap)

**Adding New Interval:**
- Interval: [8, 10]
- This interval does not overlap with the last merged interval
- Added as separate interval to result

---

## Step 5: 🔍 Compare interval [15, 18] with last merged [8, 10]

**Current Interval:** [15, 18]
**Last Merged Interval:** [8, 10]

**Overlap Check:**
```
Compare current.start (15) with last_merged.end (10)
15 <= 10? → False
```

**Decision:** Intervals **do not overlap** because current starts (15) after last ends (10)
- Action: Add current interval as new separate interval

**Timeline State:**
- Merged so far: 2
- Pending: 0

---

## Step 6: ➕ Add new interval [15, 18] (no overlap)

**Adding New Interval:**
- Interval: [15, 18]
- This interval does not overlap with the last merged interval
- Added as separate interval to result

---

## Execution Summary

**Input:** 4 intervals
**Output:** 3 merged intervals
**Merges Performed:** 1

**Final Merged Intervals:**
- Interval 1: [1, 6]
- Interval 2: [8, 10]
- Interval 3: [15, 18]

**Performance:**
- Time Complexity: O(n log n) - dominated by sorting
- Space Complexity: O(n) - for storing merged result
- Merge operations: 1 (out of 3 possible)

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
