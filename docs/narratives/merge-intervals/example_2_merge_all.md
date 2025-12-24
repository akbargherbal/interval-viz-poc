# Merge Intervals Execution Narrative

**Algorithm:** Merge Intervals
**Input Intervals:** 2 intervals
**Result:** 1 merged intervals
**Merges Performed:** 1

---

## Step 0: 📊 Sort 2 intervals by start time

**Original Intervals (unsorted):**
- Interval 1: [1, 4]
- Interval 2: [4, 5]

**After Sorting by Start Time:**
- Interval 1: [1, 4]
- Interval 2: [4, 5]

**Why Sort?** Sorting by start time ensures we process intervals in chronological order, making it easy to detect overlaps by comparing each interval with the last merged interval.

**Timeline State:**
- Total intervals: 2
- Merged so far: 0
- Pending: 2

---

## Step 1: 🔍 Compare interval [4, 5] with last merged [1, 4]

**Current Interval:** [4, 5]
**Last Merged Interval:** [1, 5]

**Overlap Check:**
```
Compare current.start (4) with last_merged.end (5)
4 <= 5? → True
```

**Decision:** Intervals **overlap** because current starts (4) before or when last ends (5)
- Action: Merge by extending the last interval's end time

**Timeline State:**
- Merged so far: 1
- Pending: 0

---

## Step 2: 🔗 Merge: Extend last interval to [1, 5]

**Merging Intervals:**
- Current interval: [4, 5]
- Last merged (before): [1, 4]

**End Time Calculation:**
```
new_end = max(4, 5) = 5
```

**Result:**
- Last merged (after): [1, 5]
- The last interval now spans from 1 to 5

**Why max()?** We take the maximum of the two end times to ensure the merged interval covers both original intervals completely. If current interval is fully enclosed (ends before last ends), we keep the larger end time.

---

## Execution Summary

**Input:** 2 intervals
**Output:** 1 merged intervals
**Merges Performed:** 1

**Final Merged Intervals:**
- Interval 1: [1, 5]

**Performance:**
- Time Complexity: O(n log n) - dominated by sorting
- Space Complexity: O(n) - for storing merged result
- Merge operations: 1 (out of 1 possible)

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
