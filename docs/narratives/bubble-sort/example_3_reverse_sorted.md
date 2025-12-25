# Bubble Sort Execution Narrative

**Algorithm:** Bubble Sort
**Input Array:** [5, 4, 3, 2, 1]
**Array Size:** 5 elements
**Result:** Sorted array: [1, 2, 3, 4, 5]
**Total Comparisons:** 10
**Total Swaps:** 10

---

## Step 0: 🔢 Starting Bubble Sort on array of 5 elements

**Initial Configuration:**
- Array to sort: `[5, 4, 3, 2, 1]`
- Array size: 5 elements
- Strategy: Bubble largest elements to the right through adjacent comparisons

**Array Visualization:**
```
Index:   0   1   2   3   4
Value:   5   4   3   2   1
State:   U   U   U   U   U  (U = Unsorted)
```

**Algorithm Overview:**
Bubble Sort works by repeatedly comparing adjacent elements and swapping them if they're in the wrong order. Each complete pass through the array "bubbles" the largest unsorted element to its correct position at the end. The sorted region grows from right to left.

---

## Step 1: 🔍 Compare arr[0] (5) with arr[1] (4)

**Comparison:**
- Position 0: value = 5
- Position 1: value = 4
- Check: `5 > 4`

**Decision Logic:**
Compare arr[0] (5) with arr[1] (4):
- IF 5 > 4: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   5   4   3   2   1
         ^  ^         
         L  R           (L = Left, R = Right in comparison)
```

---

## Step 2: 🔄 Swap arr[0] (5) ↔ arr[1] (4)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 5 ↔ 4
- Reason: 5 > 4 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 5, arr[1] = 4
- After swap: arr[0] = 4, arr[1] = 5
- Total swaps: 1

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   4   5   3   2   1
```

---

## Step 3: 🔍 Compare arr[1] (5) with arr[2] (3)

**Comparison:**
- Position 1: value = 5
- Position 2: value = 3
- Check: `5 > 3`

**Decision Logic:**
Compare arr[1] (5) with arr[2] (3):
- IF 5 > 3: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   4   5   3   2   1
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 4: 🔄 Swap arr[1] (5) ↔ arr[2] (3)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 5 ↔ 3
- Reason: 5 > 3 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 5, arr[2] = 3
- After swap: arr[1] = 3, arr[2] = 5
- Total swaps: 2

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   4   3   5   2   1
```

---

## Step 5: 🔍 Compare arr[2] (5) with arr[3] (2)

**Comparison:**
- Position 2: value = 5
- Position 3: value = 2
- Check: `5 > 2`

**Decision Logic:**
Compare arr[2] (5) with arr[3] (2):
- IF 5 > 2: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   4   3   5   2   1
               ^  ^   
               L  R     (L = Left, R = Right in comparison)
```

---

## Step 6: 🔄 Swap arr[2] (5) ↔ arr[3] (2)

**Swap Performed:**
- Positions: 2 ↔ 3
- Values: 5 ↔ 2
- Reason: 5 > 2 (larger value moves right)

**Array Transformation:**
- Before swap: arr[2] = 5, arr[3] = 2
- After swap: arr[2] = 2, arr[3] = 5
- Total swaps: 3

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   4   3   2   5   1
```

---

## Step 7: 🔍 Compare arr[3] (5) with arr[4] (1)

**Comparison:**
- Position 3: value = 5
- Position 4: value = 1
- Check: `5 > 1`

**Decision Logic:**
Compare arr[3] (5) with arr[4] (1):
- IF 5 > 1: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   4   3   2   5   1
                  ^  ^
                  L  R  (L = Left, R = Right in comparison)
```

---

## Step 8: 🔄 Swap arr[3] (5) ↔ arr[4] (1)

**Swap Performed:**
- Positions: 3 ↔ 4
- Values: 5 ↔ 1
- Reason: 5 > 1 (larger value moves right)

**Array Transformation:**
- Before swap: arr[3] = 5, arr[4] = 1
- After swap: arr[3] = 1, arr[4] = 5
- Total swaps: 4

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   4   3   2   1   5
```

---

## Step 9: ✅ Pass 1 complete: 4 swaps, sorted boundary at index 4

**Pass 1 Summary:**
- Swaps performed: 4
- Sorted boundary: index 4 (elements from 4 to end are now sorted)
- Total comparisons so far: 4
- Total swaps so far: 4

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   4   3   2   1   5
State:   U  U  U  U  S  (S = Sorted, U = Unsorted)
```

---

## Step 10: 🔍 Compare arr[0] (4) with arr[1] (3)

**Comparison:**
- Position 0: value = 4
- Position 1: value = 3
- Check: `4 > 3`

**Decision Logic:**
Compare arr[0] (4) with arr[1] (3):
- IF 4 > 3: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   4   3   2   1   5
         ^  ^         
         L  R           (L = Left, R = Right in comparison)
```

---

## Step 11: 🔄 Swap arr[0] (4) ↔ arr[1] (3)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 4 ↔ 3
- Reason: 4 > 3 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 4, arr[1] = 3
- After swap: arr[0] = 3, arr[1] = 4
- Total swaps: 5

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   3   4   2   1   5
```

---

## Step 12: 🔍 Compare arr[1] (4) with arr[2] (2)

**Comparison:**
- Position 1: value = 4
- Position 2: value = 2
- Check: `4 > 2`

**Decision Logic:**
Compare arr[1] (4) with arr[2] (2):
- IF 4 > 2: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   3   4   2   1   5
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 13: 🔄 Swap arr[1] (4) ↔ arr[2] (2)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 4 ↔ 2
- Reason: 4 > 2 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 4, arr[2] = 2
- After swap: arr[1] = 2, arr[2] = 4
- Total swaps: 6

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   3   2   4   1   5
```

---

## Step 14: 🔍 Compare arr[2] (4) with arr[3] (1)

**Comparison:**
- Position 2: value = 4
- Position 3: value = 1
- Check: `4 > 1`

**Decision Logic:**
Compare arr[2] (4) with arr[3] (1):
- IF 4 > 1: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   3   2   4   1   5
               ^  ^   
               L  R     (L = Left, R = Right in comparison)
```

---

## Step 15: 🔄 Swap arr[2] (4) ↔ arr[3] (1)

**Swap Performed:**
- Positions: 2 ↔ 3
- Values: 4 ↔ 1
- Reason: 4 > 1 (larger value moves right)

**Array Transformation:**
- Before swap: arr[2] = 4, arr[3] = 1
- After swap: arr[2] = 1, arr[3] = 4
- Total swaps: 7

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   3   2   1   4   5
```

---

## Step 16: ✅ Pass 2 complete: 3 swaps, sorted boundary at index 3

**Pass 2 Summary:**
- Swaps performed: 3
- Sorted boundary: index 3 (elements from 3 to end are now sorted)
- Total comparisons so far: 7
- Total swaps so far: 7

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   3   2   1   4   5
State:   U  U  U  S  S  (S = Sorted, U = Unsorted)
```

---

## Step 17: 🔍 Compare arr[0] (3) with arr[1] (2)

**Comparison:**
- Position 0: value = 3
- Position 1: value = 2
- Check: `3 > 2`

**Decision Logic:**
Compare arr[0] (3) with arr[1] (2):
- IF 3 > 2: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   3   2   1   4   5
         ^  ^         
         L  R           (L = Left, R = Right in comparison)
```

---

## Step 18: 🔄 Swap arr[0] (3) ↔ arr[1] (2)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 3 ↔ 2
- Reason: 3 > 2 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 3, arr[1] = 2
- After swap: arr[0] = 2, arr[1] = 3
- Total swaps: 8

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   2   3   1   4   5
```

---

## Step 19: 🔍 Compare arr[1] (3) with arr[2] (1)

**Comparison:**
- Position 1: value = 3
- Position 2: value = 1
- Check: `3 > 1`

**Decision Logic:**
Compare arr[1] (3) with arr[2] (1):
- IF 3 > 1: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   2   3   1   4   5
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 20: 🔄 Swap arr[1] (3) ↔ arr[2] (1)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 3 ↔ 1
- Reason: 3 > 1 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 3, arr[2] = 1
- After swap: arr[1] = 1, arr[2] = 3
- Total swaps: 9

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   2   1   3   4   5
```

---

## Step 21: ✅ Pass 3 complete: 2 swaps, sorted boundary at index 2

**Pass 3 Summary:**
- Swaps performed: 2
- Sorted boundary: index 2 (elements from 2 to end are now sorted)
- Total comparisons so far: 9
- Total swaps so far: 9

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   2   1   3   4   5
State:   U  U  S  S  S  (S = Sorted, U = Unsorted)
```

---

## Step 22: 🔍 Compare arr[0] (2) with arr[1] (1)

**Comparison:**
- Position 0: value = 2
- Position 1: value = 1
- Check: `2 > 1`

**Decision Logic:**
Compare arr[0] (2) with arr[1] (1):
- IF 2 > 1: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   2   1   3   4   5
         ^  ^         
         L  R           (L = Left, R = Right in comparison)
```

---

## Step 23: 🔄 Swap arr[0] (2) ↔ arr[1] (1)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 2 ↔ 1
- Reason: 2 > 1 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 2, arr[1] = 1
- After swap: arr[0] = 1, arr[1] = 2
- Total swaps: 10

**Updated Array:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
```

---

## Step 24: ✅ Pass 4 complete: 1 swaps, sorted boundary at index 1

**Pass 4 Summary:**
- Swaps performed: 1
- Sorted boundary: index 1 (elements from 1 to end are now sorted)
- Total comparisons so far: 10
- Total swaps so far: 10

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   U  S  S  S  S  (S = Sorted, U = Unsorted)
```

---

## Execution Summary

**Final Result:** [1, 2, 3, 4, 5]

**Performance Metrics:**
- Total comparisons: 10
- Total swaps: 10
- Passes completed: 4
- Array size: 5 elements

**Complexity Analysis:**
- Time Complexity: O(n²) worst/average case, O(n) best case (already sorted)
- Space Complexity: O(1) (in-place sorting)
- Stability: Stable (equal elements maintain relative order)

**Algorithm Behavior:**
The algorithm performed 10 swaps across 4 passes to sort the array. Each pass bubbled the largest unsorted element to its correct position at the end.

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Sorted Boundary** (`sorted_boundary`) - Shows the growing sorted region from right to left
- **Comparison Count** (`comparisons`) - Demonstrates O(n²) behavior in real-time
- **Swap Count** (`swaps`) - Shows actual work being done (0 swaps = already sorted)

### Visualization Priorities

1. **Highlight the sorted tail** - Use distinct color for `sorted` state elements (right side of array)
2. **Animate comparisons** - The `comparing` state shows the active pair being evaluated
3. **Emphasize swaps** - When elements swap, use smooth animation to show the exchange
4. **Show pass completion** - Visual indicator when sorted_boundary moves left (one more element sorted)
5. **Celebrate early termination** - If a pass has 0 swaps, highlight that optimization kicked in

### Key JSON Paths

```
step.data.visualization.comparing_indices  // [i, i+1] tuple or null
step.data.visualization.sorted_boundary    // Index where sorted region begins
step.data.visualization.current_pass       // Which pass through array (1-indexed)
step.data.visualization.comparisons        // Running total of comparisons
step.data.visualization.swaps              // Running total of swaps
step.data.visualization.array[*].state     // 'unsorted' | 'comparing' | 'sorted'
step.data.visualization.array[*].value
step.data.visualization.array[*].index
```

### Algorithm-Specific Guidance

Bubble Sort's defining characteristic is the **growing sorted region from right to left**. This is pedagogically crucial - students should see that each pass guarantees one more element is in its final sorted position. The `sorted_boundary` moving leftward is the visual proof of progress. The comparison pairs (`comparing_indices`) should be highlighted as they march left-to-right through the unsorted region. When a swap occurs, animate it clearly - this is the "bubble" action that gives the algorithm its name. The early termination optimization (when `swaps_in_pass = 0`) is a key teaching moment - show that the algorithm is smart enough to detect when work is done. Consider using a **color gradient** for the sorted tail to emphasize the progressive nature of the sort.
