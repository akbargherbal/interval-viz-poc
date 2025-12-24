# Insertion Sort Execution Narrative

**Algorithm:** Insertion Sort
**Input Array:** [12, 11, 13, 5, 6]
**Array Size:** 5 elements
**Result:** Sorted array: [5, 6, 11, 12, 13]
**Total Comparisons:** 9
**Total Shifts:** 7

---

## Step 0: 🔢 Initial array with 5 elements (first element trivially sorted)

**Initial Configuration:**
- Array to sort: `[12, 11, 13, 5, 6]`
- Array size: 5 elements
- First element (index 0) is trivially sorted

**Array Visualization:**
```
Index:   0   1   2   3   4
Value:  12  11  13   5   6
State:   S   U   U   U   U
       (S=Sorted, U=Unsorted)
```
*Sorted region: **1 element** (index 0)*

---

## Step 1: 📌 Select key: array[1] = 11 (sorted region: 1 elements)

**Key Selection:**
- Select element at index **1** as key
- Key value: **11**
- Current sorted region: indices [0, 0] (1 elements)

**Goal:** Insert key (11) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:  12  11  13   5   6
State:   S  K  U  U  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 2: 🔍 Compare: 11 < 12 → shift right

**Comparison:**
```
key (11) < array[0] (12)?
11 < 12 → 11 < 12 = True
```

**Decision:** Key is **smaller** than array[0]
- Action: Shift array[0] (12) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:  12  11  13   5   6
State:   C  K  U  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 3: ➡️ Shift: array[0] (12) → array[1]

**Shift Operation:**
- Move array[0] (12) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 1

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:  12  12  13   5   6
```

---

## Step 4: ✅ Insert key (11) at index 0 (1 comparisons, 1 shifts)

**Insertion:**
- Insert key (11) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 1

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:  11  12  13   5   6
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **1 elements***

---

## Step 5: 📌 Select key: array[2] = 13 (sorted region: 2 elements)

**Key Selection:**
- Select element at index **2** as key
- Key value: **13**
- Current sorted region: indices [0, 1] (2 elements)

**Goal:** Insert key (13) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:  11  12  13   5   6
State:   S  S  K  U  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 6: 🔍 Compare: 13 ≥ 12 → found position

**Comparison:**
```
key (13) < array[1] (12)?
13 < 12 → 13 < 12 = False
```

**Decision:** Key is **not smaller** than array[1]
- Action: Found correct position for key
- Key will be inserted after array[1]

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:  11  12  13   5   6
State:   S  C  K  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 7: ✅ Insert key (13) at index 2 (1 comparisons, 0 shifts)

**Insertion:**
- Insert key (13) at index **2**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 0

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:  11  12  13   5   6
State:   S  S  S  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **3 elements***

---

## Step 8: 📌 Select key: array[3] = 5 (sorted region: 3 elements)

**Key Selection:**
- Select element at index **3** as key
- Key value: **5**
- Current sorted region: indices [0, 2] (3 elements)

**Goal:** Insert key (5) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:  11  12  13   5   6
State:   S  S  S  K  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 9: 🔍 Compare: 5 < 13 → shift right

**Comparison:**
```
key (5) < array[2] (13)?
5 < 13 → 5 < 13 = True
```

**Decision:** Key is **smaller** than array[2]
- Action: Shift array[2] (13) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:  11  12  13   5   6
State:   S  S  C  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 10: ➡️ Shift: array[2] (13) → array[3]

**Shift Operation:**
- Move array[2] (13) → array[3]
- This creates space for the key to be inserted
- Total shifts so far: 2

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:  11  12  13  13   6
```

---

## Step 11: 🔍 Compare: 5 < 12 → shift right

**Comparison:**
```
key (5) < array[1] (12)?
5 < 12 → 5 < 12 = True
```

**Decision:** Key is **smaller** than array[1]
- Action: Shift array[1] (12) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:  11  12  13  13   6
State:   S  C  S  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 12: ➡️ Shift: array[1] (12) → array[2]

**Shift Operation:**
- Move array[1] (12) → array[2]
- This creates space for the key to be inserted
- Total shifts so far: 3

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:  11  12  12  13   6
```

---

## Step 13: 🔍 Compare: 5 < 11 → shift right

**Comparison:**
```
key (5) < array[0] (11)?
5 < 11 → 5 < 11 = True
```

**Decision:** Key is **smaller** than array[0]
- Action: Shift array[0] (11) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:  11  12  12  13   6
State:   C  S  S  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 14: ➡️ Shift: array[0] (11) → array[1]

**Shift Operation:**
- Move array[0] (11) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 4

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:  11  11  12  13   6
```

---

## Step 15: ✅ Insert key (5) at index 0 (3 comparisons, 3 shifts)

**Insertion:**
- Insert key (5) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 3
- Shifts for this key: 3

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   5  11  12  13   6
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **1 elements***

---

## Step 16: 📌 Select key: array[4] = 6 (sorted region: 4 elements)

**Key Selection:**
- Select element at index **4** as key
- Key value: **6**
- Current sorted region: indices [0, 3] (4 elements)

**Goal:** Insert key (6) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   5  11  12  13   6
State:   S  S  S  S  K
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 17: 🔍 Compare: 6 < 13 → shift right

**Comparison:**
```
key (6) < array[3] (13)?
6 < 13 → 6 < 13 = True
```

**Decision:** Key is **smaller** than array[3]
- Action: Shift array[3] (13) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   5  11  12  13   6
State:   S  S  S  C  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 18: ➡️ Shift: array[3] (13) → array[4]

**Shift Operation:**
- Move array[3] (13) → array[4]
- This creates space for the key to be inserted
- Total shifts so far: 5

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   5  11  12  13  13
```

---

## Step 19: 🔍 Compare: 6 < 12 → shift right

**Comparison:**
```
key (6) < array[2] (12)?
6 < 12 → 6 < 12 = True
```

**Decision:** Key is **smaller** than array[2]
- Action: Shift array[2] (12) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   5  11  12  13  13
State:   S  S  C  S  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 20: ➡️ Shift: array[2] (12) → array[3]

**Shift Operation:**
- Move array[2] (12) → array[3]
- This creates space for the key to be inserted
- Total shifts so far: 6

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   5  11  12  12  13
```

---

## Step 21: 🔍 Compare: 6 < 11 → shift right

**Comparison:**
```
key (6) < array[1] (11)?
6 < 11 → 6 < 11 = True
```

**Decision:** Key is **smaller** than array[1]
- Action: Shift array[1] (11) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   5  11  12  12  13
State:   S  C  S  S  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 22: ➡️ Shift: array[1] (11) → array[2]

**Shift Operation:**
- Move array[1] (11) → array[2]
- This creates space for the key to be inserted
- Total shifts so far: 7

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   5  11  11  12  13
```

---

## Step 23: 🔍 Compare: 6 ≥ 5 → found position

**Comparison:**
```
key (6) < array[0] (5)?
6 < 5 → 6 < 5 = False
```

**Decision:** Key is **not smaller** than array[0]
- Action: Found correct position for key
- Key will be inserted after array[0]

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   5  11  11  12  13
State:   C  S  S  S  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 24: ✅ Insert key (6) at index 1 (4 comparisons, 3 shifts)

**Insertion:**
- Insert key (6) at index **1**
- Key is now in correct sorted position
- Comparisons for this key: 4
- Shifts for this key: 3

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   5   6  11  12  13
State:   S  S  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region expanded: **2 elements***

---

## Step 25: 🎉 Sorting complete! (9 comparisons, 7 shifts)

✅ **Sorting Complete!**

**Final Statistics:**
- Total comparisons: 9
- Total shifts: 7
- All elements now in sorted order

**Final Sorted Array:**
```
Index:   0   1   2   3   4
Value:   5   6  11  12  13
State:   S  S  S  S  S
       (All Sorted)
```

---

## Execution Summary

**Original Array:** [12, 11, 13, 5, 6]
**Sorted Array:** [5, 6, 11, 12, 13]

**Performance Metrics:**
- Total Comparisons: 9
- Total Shifts: 7
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
