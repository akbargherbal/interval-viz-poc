# Insertion Sort Execution Narrative

**Algorithm:** Insertion Sort
**Input Array:** [5, 4, 3, 2, 1]
**Array Size:** 5 elements
**Result:** Sorted array: [1, 2, 3, 4, 5]
**Total Comparisons:** 10
**Total Shifts:** 10

---

## Step 0: 🔢 Initial array with 5 elements (first element trivially sorted)

**Initial Configuration:**
- Array to sort: `[5, 4, 3, 2, 1]`
- Array size: 5 elements
- First element (index 0) is trivially sorted

**Array Visualization:**
```
Index:   0   1   2   3   4
Value:   5   4   3   2   1
State:   S   U   U   U   U
       (S=Sorted, U=Unsorted)
```
*Sorted region: **1 element** (index 0)*

---

## Step 1: 📌 Select key: array[1] = 4 (sorted region: 1 elements)

**Key Selection:**
- Select element at index **1** as key
- Key value: **4**
- Current sorted region: indices [0, 0] (1 elements)

**Goal:** Insert key (4) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   5   4   3   2   1
State:   S  K  U  U  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 2: 🔍 Compare: 4 < 5 → shift right

**Comparison:**
```
key (4) < array[0] (5)?
4 < 5 → 4 < 5 = True
```

**Decision:** Key is **smaller** than array[0]
- Action: Shift array[0] (5) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   5   4   3   2   1
State:   C  K  U  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 3: ➡️ Shift: array[0] (5) → array[1]

**Shift Operation:**
- Move array[0] (5) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 1

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   5   5   3   2   1
```

---

## Step 4: ✅ Insert key (4) at index 0 (1 comparisons, 1 shifts)

**Insertion:**
- Insert key (4) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 1
- Shifts for this key: 1

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   4   5   3   2   1
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region now contains: **2 elements** (indices [0,1])*

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
Value:   4   5   3   2   1
State:   S  S  K  U  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 6: 🔍 Compare: 3 < 5 → shift right

**Comparison:**
```
key (3) < array[1] (5)?
3 < 5 → 3 < 5 = True
```

**Decision:** Key is **smaller** than array[1]
- Action: Shift array[1] (5) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   4   5   3   2   1
State:   S  C  K  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 7: ➡️ Shift: array[1] (5) → array[2]

**Shift Operation:**
- Move array[1] (5) → array[2]
- This creates space for the key to be inserted
- Total shifts so far: 2

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   4   5   5   2   1
```

---

## Step 8: 🔍 Compare: 3 < 4 → shift right

**Comparison:**
```
key (3) < array[0] (4)?
3 < 4 → 3 < 4 = True
```

**Decision:** Key is **smaller** than array[0]
- Action: Shift array[0] (4) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   4   5   5   2   1
State:   C  S  K  U  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 9: ➡️ Shift: array[0] (4) → array[1]

**Shift Operation:**
- Move array[0] (4) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 3

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   4   4   5   2   1
```

---

## Step 10: ✅ Insert key (3) at index 0 (2 comparisons, 2 shifts)

**Insertion:**
- Insert key (3) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 2
- Shifts for this key: 2

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   3   4   5   2   1
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region now contains: **3 elements** (indices [0,2])*

---

## Step 11: 📌 Select key: array[3] = 2 (sorted region: 3 elements)

**Key Selection:**
- Select element at index **3** as key
- Key value: **2**
- Current sorted region: indices [0, 2] (3 elements)

**Goal:** Insert key (2) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   3   4   5   2   1
State:   S  S  S  K  U
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 12: 🔍 Compare: 2 < 5 → shift right

**Comparison:**
```
key (2) < array[2] (5)?
2 < 5 → 2 < 5 = True
```

**Decision:** Key is **smaller** than array[2]
- Action: Shift array[2] (5) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   3   4   5   2   1
State:   S  S  C  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 13: ➡️ Shift: array[2] (5) → array[3]

**Shift Operation:**
- Move array[2] (5) → array[3]
- This creates space for the key to be inserted
- Total shifts so far: 4

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   3   4   5   5   1
```

---

## Step 14: 🔍 Compare: 2 < 4 → shift right

**Comparison:**
```
key (2) < array[1] (4)?
2 < 4 → 2 < 4 = True
```

**Decision:** Key is **smaller** than array[1]
- Action: Shift array[1] (4) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   3   4   5   5   1
State:   S  C  S  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 15: ➡️ Shift: array[1] (4) → array[2]

**Shift Operation:**
- Move array[1] (4) → array[2]
- This creates space for the key to be inserted
- Total shifts so far: 5

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   3   4   4   5   1
```

---

## Step 16: 🔍 Compare: 2 < 3 → shift right

**Comparison:**
```
key (2) < array[0] (3)?
2 < 3 → 2 < 3 = True
```

**Decision:** Key is **smaller** than array[0]
- Action: Shift array[0] (3) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   3   4   4   5   1
State:   C  S  S  K  U
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 17: ➡️ Shift: array[0] (3) → array[1]

**Shift Operation:**
- Move array[0] (3) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 6

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   3   3   4   5   1
```

---

## Step 18: ✅ Insert key (2) at index 0 (3 comparisons, 3 shifts)

**Insertion:**
- Insert key (2) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 3
- Shifts for this key: 3

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   2   3   4   5   1
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region now contains: **4 elements** (indices [0,3])*

---

## Step 19: 📌 Select key: array[4] = 1 (sorted region: 4 elements)

**Key Selection:**
- Select element at index **4** as key
- Key value: **1**
- Current sorted region: indices [0, 3] (4 elements)

**Goal:** Insert key (1) into correct position within sorted region

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   2   3   4   5   1
State:   S  S  S  S  K
       (K=Key, S=Sorted, U=Unsorted)
```

---

## Step 20: 🔍 Compare: 1 < 5 → shift right

**Comparison:**
```
key (1) < array[3] (5)?
1 < 5 → 1 < 5 = True
```

**Decision:** Key is **smaller** than array[3]
- Action: Shift array[3] (5) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   2   3   4   5   1
State:   S  S  S  C  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 21: ➡️ Shift: array[3] (5) → array[4]

**Shift Operation:**
- Move array[3] (5) → array[4]
- This creates space for the key to be inserted
- Total shifts so far: 7

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   2   3   4   5   5
```

---

## Step 22: 🔍 Compare: 1 < 4 → shift right

**Comparison:**
```
key (1) < array[2] (4)?
1 < 4 → 1 < 4 = True
```

**Decision:** Key is **smaller** than array[2]
- Action: Shift array[2] (4) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   2   3   4   5   5
State:   S  S  C  S  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 23: ➡️ Shift: array[2] (4) → array[3]

**Shift Operation:**
- Move array[2] (4) → array[3]
- This creates space for the key to be inserted
- Total shifts so far: 8

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   2   3   4   4   5
```

---

## Step 24: 🔍 Compare: 1 < 3 → shift right

**Comparison:**
```
key (1) < array[1] (3)?
1 < 3 → 1 < 3 = True
```

**Decision:** Key is **smaller** than array[1]
- Action: Shift array[1] (3) one position right
- Continue comparing with previous elements

**Array State After Comparison:**
```
Index:   0   1   2   3   4
Value:   2   3   4   4   5
State:   S  C  S  S  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 25: ➡️ Shift: array[1] (3) → array[2]

**Shift Operation:**
- Move array[1] (3) → array[2]
- This creates space for the key to be inserted
- Total shifts so far: 9

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   2   3   3   4   5
```

---

## Step 26: 🔍 Compare: 1 < 2 → shift right

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
Value:   2   3   3   4   5
State:   C  S  S  S  K
       (K=Key, C=Comparing, S=Sorted, U=Unsorted)
```

---

## Step 27: ➡️ Shift: array[0] (2) → array[1]

**Shift Operation:**
- Move array[0] (2) → array[1]
- This creates space for the key to be inserted
- Total shifts so far: 10

**Array State After Shift:**
```
Index:   0   1   2   3   4
Value:   2   2   3   4   5
```

---

## Step 28: ✅ Insert key (1) at index 0 (4 comparisons, 4 shifts)

**Insertion:**
- Insert key (1) at index **0**
- Key is now in correct sorted position
- Comparisons for this key: 4
- Shifts for this key: 4

**Array State After Insertion:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   S  U  U  U  U
       (S=Sorted, U=Unsorted)
```
*Sorted region now contains: **5 elements** (indices [0,4])*

---

## Step 29: 🎉 Sorting complete! (10 comparisons, 10 shifts)

✅ **Sorting Complete!**

**Final Statistics:**
- Total comparisons: 10
- Total shifts: 10
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

**Original Array:** [5, 4, 3, 2, 1]
**Sorted Array:** [1, 2, 3, 4, 5]

**Performance Metrics:**
- Total Comparisons: 10
- Total Shifts: 10
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
