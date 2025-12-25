# Meeting Rooms II Execution Narrative

**Algorithm:** Meeting Rooms II
**Input:** 6 meetings
**Result:** Minimum **4** conference rooms required
**Total Steps:** 16

---

## Step 0: 📋 Sort 6 meetings by start time

**Initial Meetings (Unsorted):**

| Meeting ID | Start Time | End Time |
|------------|------------|----------|
| 0 | 1 | 10 |
| 1 | 2 | 7 |
| 2 | 3 | 19 |
| 3 | 8 | 12 |
| 4 | 10 | 20 |
| 5 | 11 | 30 |

**Sorting Strategy:**
- Sort meetings by **start time** (ascending order)
- Process meetings in chronological order of when they begin
- This ensures we handle earliest meetings first

**Sorted Meetings:**

| Meeting ID | Start Time | End Time |
|------------|------------|----------|
| 0 | 1 | 10 |
| 1 | 2 | 7 |
| 2 | 3 | 19 |
| 3 | 8 | 12 |
| 4 | 10 | 20 |
| 5 | 11 | 30 |

**Data Structures Initialized:**
- **Min-Heap:** Empty (will track earliest ending meetings)
- **Room Assignments:** Empty (will map meetings to rooms)
- **Rooms Used:** 0

---

## Step 1: 🆕 Allocate first room 1 for meeting 0

---

## Step 2: 📊 Initialize heap with end time 10

**Heap Operation:** Add end time 10 to min-heap

**Purpose of Heap:**
- Heap tracks end times of all currently scheduled meetings
- Top of heap = earliest ending meeting
- Heap size = number of rooms currently in use

**Updated Heap:** [10]
**Heap Size:** 1 rooms in use

---

## Step 3: 🔍 Check if meeting 1 [2, 7] can reuse a room

**Current Meeting:** ID 1 [2, 7]

**Heap State (Earliest Ending Meetings):**
- Heap: [10]
- Top of heap (earliest end time): **10**

**Decision Logic:**
Compare meeting start time (2) with earliest end time (10):

**Comparison:** 2 < 10 ✗

**Outcome:** Meeting starts **before** earliest meeting ends
- All currently scheduled meetings are still ongoing
- No rooms are free yet
- Action: Must **allocate a new room**

---

## Step 4: 🆕 Allocate new room 2 for meeting 1 (all rooms occupied)

---

## Step 5: 📊 Add end time 7 to heap (heap size: 2)

**Heap Operation:** Add end time 7 to min-heap

**Purpose of Heap:**
- Heap tracks end times of all currently scheduled meetings
- Top of heap = earliest ending meeting
- Heap size = number of rooms currently in use

**Updated Heap:** [7, 10]
**Heap Size:** 2 rooms in use

---

## Step 6: 🔍 Check if meeting 2 [3, 19] can reuse a room

**Current Meeting:** ID 2 [3, 19]

**Heap State (Earliest Ending Meetings):**
- Heap: [7, 10]
- Top of heap (earliest end time): **7**

**Decision Logic:**
Compare meeting start time (3) with earliest end time (7):

**Comparison:** 3 < 7 ✗

**Outcome:** Meeting starts **before** earliest meeting ends
- All currently scheduled meetings are still ongoing
- No rooms are free yet
- Action: Must **allocate a new room**

---

## Step 7: 🆕 Allocate new room 3 for meeting 2 (all rooms occupied)

---

## Step 8: 📊 Add end time 19 to heap (heap size: 3)

**Heap Operation:** Add end time 19 to min-heap

**Purpose of Heap:**
- Heap tracks end times of all currently scheduled meetings
- Top of heap = earliest ending meeting
- Heap size = number of rooms currently in use

**Updated Heap:** [7, 10, 19]
**Heap Size:** 3 rooms in use

---

## Step 9: 🔍 Check if meeting 3 [8, 12] can reuse a room

**Current Meeting:** ID 3 [8, 12]

**Heap State (Earliest Ending Meetings):**
- Heap: [7, 10, 19]
- Top of heap (earliest end time): **7**

**Decision Logic:**
Compare meeting start time (8) with earliest end time (7):

**Comparison:** 8 ≥ 7 ✓

**Outcome:** Meeting starts **after or when** earliest meeting ends
- The room from the earliest ending meeting is now **free**
- We can **reuse** that room (no new room needed)
- Action: Remove 7 from heap, reuse its room

---

## Step 10: ♻️ Reuse room 2 for meeting 3 (previous meeting ended at 7)

**Meeting:** ID 3 [8, 12]
**Assigned to:** Room 2

**Room Reuse:**
- Heap popped: end time 7 (Room 2)
- Previous meeting in Room 2 ended at 7
- Current meeting starts at 8
- Gap: 1 time units
- **Room 2** is now free and reused

---

## Step 11: 🔍 Check if meeting 4 [10, 20] can reuse a room

**Current Meeting:** ID 4 [10, 20]

**Heap State (Earliest Ending Meetings):**
- Heap: [10, 12, 19]
- Top of heap (earliest end time): **10**

**Decision Logic:**
Compare meeting start time (10) with earliest end time (10):

**Comparison:** 10 ≥ 10 ✓

**Outcome:** Meeting starts **after or when** earliest meeting ends
- The room from the earliest ending meeting is now **free**
- We can **reuse** that room (no new room needed)
- Action: Remove 10 from heap, reuse its room

---

## Step 12: ♻️ Reuse room 1 for meeting 4 (previous meeting ended at 10)

**Meeting:** ID 4 [10, 20]
**Assigned to:** Room 1

**Room Reuse:**
- Heap popped: end time 10 (Room 1)
- Previous meeting in Room 1 ended at 10
- Current meeting starts at 10
- Gap: 0 time units
- **Room 1** is now free and reused

---

## Step 13: 🔍 Check if meeting 5 [11, 30] can reuse a room

**Current Meeting:** ID 5 [11, 30]

**Heap State (Earliest Ending Meetings):**
- Heap: [12, 19, 20]
- Top of heap (earliest end time): **12**

**Decision Logic:**
Compare meeting start time (11) with earliest end time (12):

**Comparison:** 11 < 12 ✗

**Outcome:** Meeting starts **before** earliest meeting ends
- All currently scheduled meetings are still ongoing
- No rooms are free yet
- Action: Must **allocate a new room**

---

## Step 14: 🆕 Allocate new room 4 for meeting 5 (all rooms occupied)

---

## Step 15: 📊 Add end time 30 to heap (heap size: 4)

**Heap Operation:** Add end time 30 to min-heap

**Purpose of Heap:**
- Heap tracks end times of all currently scheduled meetings
- Top of heap = earliest ending meeting
- Heap size = number of rooms currently in use

**Updated Heap:** [12, 19, 20, 30]
**Heap Size:** 4 rooms in use

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
step.data.freed_room                            // room that was just freed (reuse steps)
```

### Algorithm-Specific Guidance

Meeting Rooms II is fundamentally about **resource allocation over time**. The most pedagogically powerful visualization is a **Gantt chart / timeline** showing meetings grouped by room. Students should see:

1. **Why overlaps force new rooms** - When meeting A hasn't ended but meeting B starts
2. **How the heap enables reuse** - The earliest-ending meeting's room becomes available first
3. **The greedy optimality** - Always reusing the earliest-free room minimizes total rooms

Consider using **color coding**: pending meetings (gray), examining (yellow), scheduled (green/blue). Animate the **heap pop operation** when reusing a room - show the end time being removed and the room becoming available. The heap visualization should be **synchronized with the timeline** - when heap size grows, show new room allocation; when heap size shrinks, show room reuse. This dual visualization (timeline + heap) makes the algorithm's logic transparent.

