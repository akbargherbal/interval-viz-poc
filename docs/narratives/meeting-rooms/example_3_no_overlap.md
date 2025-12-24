# Meeting Rooms II Execution Narrative

**Algorithm:** Meeting Rooms II
**Input:** 2 meetings
**Result:** Minimum **1** conference rooms required
**Total Steps:** 5

---

## Step 0: 📋 Sort 2 meetings by start time

**Initial Meetings (Unsorted):**

| Meeting ID | Start Time | End Time |
|------------|------------|----------|
| 0 | 7 | 10 |
| 1 | 2 | 4 |

**Sorting Strategy:**
- Sort meetings by **start time** (ascending order)
- Process meetings in chronological order of when they begin
- This ensures we handle earliest meetings first

**Sorted Meetings:**

| Meeting ID | Start Time | End Time |
|------------|------------|----------|
| 1 | 2 | 4 |
| 0 | 7 | 10 |

**Data Structures Initialized:**
- **Min-Heap:** Empty (will track earliest ending meetings)
- **Room Assignments:** Empty (will map meetings to rooms)
- **Rooms Used:** 0

---

## Step 1: 🆕 Allocate first room 1 for meeting 1

**Meeting:** ID 1 [2, 4]
**Decision:** Allocate **new Room 1**

**Reason:**
- Heap is empty (first meeting being scheduled)
- Must allocate first room

**Rooms Used:** 1

---

## Step 2: 📊 Initialize heap with end time 4

**Heap Operation:** Add end time 4 to min-heap

**Purpose of Heap:**
- Heap tracks end times of all currently scheduled meetings
- Top of heap = earliest ending meeting
- Heap size = number of rooms currently in use

**Updated Heap:** [4]
**Heap Size:** 1 rooms in use

---

## Step 3: 🔍 Check if meeting 0 [7, 10] can reuse a room

**Current Meeting:** ID 0 [7, 10]

**Heap State (Earliest Ending Meetings):**
- Heap: [4]
- Top of heap (earliest end time): **4**

**Decision Logic:**
Compare meeting start time (7) with earliest end time (4):

**Comparison:** 7 ≥ 4 ✓

**Outcome:** Meeting starts **after or when** earliest meeting ends
- The room from the earliest ending meeting is now **free**
- We can **reuse** that room (no new room needed)
- Action: Remove 4 from heap, reuse its room

---

## Step 4: ♻️ Reuse room 1 for meeting 0 (previous meeting ended at 4)

**Meeting:** ID 0 [7, 10]
**Assigned to:** Room 1

**Room Reuse:**
- Previous meeting in this room ended at 4
- Current meeting starts at 7
- Gap: 3 time units
- Room was freed and is now reused

**Heap Update:**
- Add meeting end time (10) to heap
- Updated heap: [10]
- Heap size: 1 (= rooms currently in use)

**Room Assignments So Far:**

| Meeting ID | Start | End | Room |
|------------|-------|-----|------|
| 1 | 2 | 4 | 1 |
| 0 | 7 | 10 | 1 |

---

## Execution Summary

**Minimum Rooms Required:** 1

**Final Room Assignments:**

**Room 1:**
- Meeting 1: [2, 4]
- Meeting 0: [7, 10]

**Algorithm Efficiency:**
- Time Complexity: O(n log n) where n = 2
  - Sorting: O(n log n)
  - Heap operations: O(n log n) for n insertions/deletions
- Space Complexity: O(n) for heap storage
- Optimal Solution: Uses minimum possible rooms (greedy algorithm)

**Key Insight:**
The heap size at any point represents the number of rooms in use. The maximum heap size throughout execution equals the minimum rooms needed. By always reusing the earliest-ending room when possible, we ensure optimal room utilization.

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Rooms Used** (`rooms_used`) - The core result metric, shows minimum rooms needed
- **Heap Size** (`heap_state.length`) - Real-time indicator of concurrent meetings
- **Current Meeting** (`current_interval_id`) - Which meeting is being scheduled

### Visualization Priorities

1. **Timeline grouping by room** - Show meetings stacked vertically by room assignment
2. **Heap visualization** - Display min-heap as a priority queue showing earliest end times
3. **Reuse vs. new room decisions** - Highlight when a room is reused (green) vs. new allocation (blue)
4. **Temporal overlap** - Emphasize when meetings overlap (why new rooms are needed)
5. **Animate heap operations** - Show pop (reuse) and push (schedule) operations clearly

### Key JSON Paths

```
step.data.visualization.all_intervals[*].id
step.data.visualization.all_intervals[*].start
step.data.visualization.all_intervals[*].end
step.data.visualization.all_intervals[*].state  // 'pending' | 'examining' | 'scheduled'
step.data.visualization.all_intervals[*].room   // null or room number
step.data.visualization.heap_state              // array of end times (sorted)
step.data.visualization.room_assignments        // map of interval_id -> room_number
step.data.visualization.rooms_used              // total rooms allocated
step.data.interval_id                           // current meeting being processed
step.data.heap_top                              // earliest end time (for comparisons)
```

### Algorithm-Specific Guidance

Meeting Rooms II is fundamentally about **resource allocation over time**. The most pedagogically powerful visualization is a **Gantt chart / timeline** showing meetings grouped by room. Students should see:
1. **Why overlaps force new rooms** - When meeting A hasn't ended but meeting B starts
2. **How the heap enables reuse** - The earliest-ending meeting's room becomes available first
3. **The greedy optimality** - Always reusing the earliest-free room minimizes total rooms

Consider using **color coding**: pending meetings (gray), examining (yellow), scheduled (green/blue). Animate the **heap pop operation** when reusing a room - show the end time being removed and the room becoming available. The heap visualization should be **synchronized with the timeline** - when heap size grows, show new room allocation; when heap size shrinks, show room reuse. This dual visualization (timeline + heap) makes the algorithm's logic transparent.
