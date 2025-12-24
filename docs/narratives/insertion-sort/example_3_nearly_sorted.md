# Insertion Sort Execution Narrative

**Algorithm:** Insertion Sort
**Input Array:** [2, 1, 3, 4, 5]
**Array Size:** 5 elements
**Result:** Sorted array: [1, 2, 3, 4, 5]
**Total Comparisons:** 4
**Total Shifts:** 1

---

## Step 0: 🔢 Initial array with 5 elements (first element trivially sorted)

**Initial Configuration:**
- Array to sort: `[2, 1, 3, 4, 5]`
- Array size: 5 elements
- First element (index 0) is trivially sorted

**Array Visualization:**
```
Index:   0   1   2   3   4
Value:   2   1   3   4   5
State:   S   U   U   U   U
       (S=Sorted, U=Unsorted)
```
*Sorted region: **1 element** (index 0)*

---

## Step 1: 📌 Select key: array[1] = 1 (sorted region: 1 elements)

**Key Selection:**
- Select element at index **1** as key
- Key value: **1**
- Current sorted region: indices [0, 0] (1 elements)

**Goal:** Insert key (1) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   2   1   3   4   5
State:   S  K  U  U  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 2: 🔍 Compare: 1 < 2 → shift right

**Comparison:**
```
key (1) < array[0] (2)?
1 < 2 → 1 < 2 = True
```

**Decision:** Key is **smaller** than array[0]
- Action: Shift array[0] (2) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   2   1   3   4   5
State:   C  K  U  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 3: ➡️ Shift: array[0] (2) → array[1]

**Shift Operation:**
- Move array[0] (2) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 1

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   2   2   3   4   5
```

---

## Step 4: ✅ Insert key (1) at index 0 (1 comparisons, 1 shifts)

**Insertion:**
- Insert key (1) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 1

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **1 elements***

---

## Step 5: 📌 Select key: array[2] = 3 (sorted region: 2 elements)

**Key Selection:**
- Select element at index **2** as key
- Key value: **3**
- Current sorted region: indices [0, 1] (2 elements)

**Goal:** Insert key (3) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  K  U  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 6: 🔍 Compare: 3 ≥ 2 → found position

**Comparison:**
```
key (3) < array[1] (2)?
3 < 2 → 3 < 2 = False
```

**Decision:** Key is **not smaller** than array[1]
- Action: Found correct position for key
- Key will be inserted after array[1]

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  C  K  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 7: ✅ Insert key (3) at index 2 (1 comparisons, 0 shifts)

**Insertion:**
- Insert key (3) at index **2**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 0

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **3 elements***

---

## Step 8: 📌 Select key: array[3] = 4 (sorted region: 3 elements)

**Key Selection:**
- Select element at index **3** as key
- Key value: **4**
- Current sorted region: indices [0, 2] (3 elements)

**Goal:** Insert key (4) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  K  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 9: 🔍 Compare: 4 ≥ 3 → found position

**Comparison:**
```
key (4) < array[2] (3)?
4 < 3 → 4 < 3 = False
```

**Decision:** Key is **not smaller** than array[2]
- Action: Found correct position for key
- Key will be inserted after array[2]

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  C  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 10: ✅ Insert key (4) at index 3 (1 comparisons, 0 shifts)

**Insertion:**
- Insert key (4) at index **3**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 0

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  S  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **4 elements***

---

## Step 11: 📌 Select key: array[4] = 5 (sorted region: 4 elements)

**Key Selection:**
- Select element at index **4** as key
- Key value: **5**
- Current sorted region: indices [0, 3] (4 elements)

**Goal:** Insert key (5) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  S  K
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 12: 🔍 Compare: 5 ≥ 4 → found position

**Comparison:**
```
key (5) < array[3] (4)?
5 < 4 → 5 < 4 = False
```

**Decision:** Key is **not smaller** than array[3]
- Action: Found correct position for key
- Key will be inserted after array[3]

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  C  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 13: ✅ Insert key (5) at index 4 (1 comparisons, 0 shifts)

**Insertion:**
- Insert key (5) at index **4**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 0

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  S  S
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **5 elements***

---

## Step 14: 🎉 Sorting complete! (4 comparisons, 1 shifts)

✅ **Sorting Complete!**

**Final Statistics:**
- Total comparisons: 4
- Total shifts: 1
- All elements now in sorted order

**Final Sorted Array:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  S  S  S  S
       (All Sorted)
```

---

## Execution Summary

**Original Array:** [2, 1, 3, 4, 5]
**Sorted Array:** [1, 2, 3, 4, 5]

**Performance Metrics:**
- Total Comparisons: 4
- Total Shifts: 1
- Array Size: 5 elements

**Complexity Analysis:**
- Time Complexity: O(n²) worst case, O(n) best case (already sorted)
- Space Complexity: O(1) (in-place sorting)
- Stable: Yes (maintains relative order of equal elements)

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Sorted Boundary** (`sorted_boundary`) - Shows the growing sorted region from left to right
- **Key Value** (`key.value`) - The element currently being inserted into sorted position
- **Comparison Count** (`comparisons`) - Demonstrates how many comparisons needed for each insertion

### Visualization Priorities

1. **Highlight the sorted/unsorted boundary** - Use distinct visual separation between sorted (left) and unsorted (right) regions
2. **Emphasize the key element** - The `examining` state is the element being inserted—make it visually prominent
3. **Animate shift operations** - Show elements sliding right to make room for the key (smooth transitions)
4. **Show comparison moments** - When `comparing` state is active, highlight both key and comparison element
5. **Celebrate sorted region growth** - Each successful insertion expands the sorted region by one element

### Key JSON Paths

```
step.data.visualization.key.index
step.data.visualization.key.value
step.data.visualization.sorted_boundary
step.data.visualization.compare_index
step.data.visualization.array[*].state  // 'sorted' | 'examining' | 'comparing' | 'shifting' | 'unsorted'
step.data.visualization.array[*].value
step.data.visualization.array[*].index
step.data.key_value  // Current key being inserted
step.data.compare_value  // Value being compared with key
```

### Algorithm-Specific Guidance

Insertion sort's pedagogical power comes from its **intuitive card-sorting metaphor**: imagine sorting a hand of playing cards by picking up one card at a time and inserting it into the correct position. The most important visualization is showing the **growing sorted region** (left side) and how each new element finds its place through comparisons and shifts. Use **spatial animation** to show elements sliding right during shifts—this makes the 'making room' concept concrete. The comparison moments are critical decision points: highlight both the key and the element it's being compared with. Color-code the sorted region distinctly (e.g., green gradient) to show progress. When the key finds its position, use a satisfying 'snap into place' animation. The algorithm's efficiency varies dramatically based on input: nearly-sorted arrays require few shifts (best case O(n)), while reverse-sorted arrays require maximum shifts (worst case O(n²)). Visualize this by showing shift counts per insertion—students will see why insertion sort excels on nearly-sorted data but struggles with reverse-sorted input.
