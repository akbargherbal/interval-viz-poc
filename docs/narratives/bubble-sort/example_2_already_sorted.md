# Bubble Sort Execution Narrative

**Algorithm:** Bubble Sort
**Input Array:** [1, 2, 3, 4, 5]
**Array Size:** 5 elements
**Result:** Sorted array: [1, 2, 3, 4, 5]
**Total Comparisons:** 4
**Total Swaps:** 0

---

## Step 0: 🔢 Starting Bubble Sort on array of 5 elements

**Initial Configuration:**
- Array to sort: `[1, 2, 3, 4, 5]`
- Array size: 5 elements
- Strategy: Bubble largest elements to the right through adjacent comparisons

**Array Visualization:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   U   U   U   U   U  (U = Unsorted)
```

**Algorithm Overview:**
Bubble Sort works by repeatedly comparing adjacent elements and swapping them if they're in the wrong order. Each complete pass through the array "bubbles" the largest unsorted element to its correct position at the end. The sorted region grows from right to left.

---

## Step 1: 🔍 Compare arr[0] (1) with arr[1] (2)

**Comparison:**
- Position 0: value = 1
- Position 1: value = 2
- Check: `1 > 2`

**Decision Logic:**
Compare arr[0] (1) with arr[1] (2):
- IF 1 > 2: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
         ^  ^         
         L  R           (L = Left, R = Right in comparison)
```

---

## Step 2: ✓ No swap needed: 1 ≤ 2

**No Swap Needed:**
- Positions: 0, 1
- Values: 1, 2
- Reason: 1 ≤ 2 (already in correct order)

**Decision:**
Since arr[0] (1) ≤ arr[1] (2), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 3: 🔍 Compare arr[1] (2) with arr[2] (3)

**Comparison:**
- Position 1: value = 2
- Position 2: value = 3
- Check: `2 > 3`

**Decision Logic:**
Compare arr[1] (2) with arr[2] (3):
- IF 2 > 3: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 4: ✓ No swap needed: 2 ≤ 3

**No Swap Needed:**
- Positions: 1, 2
- Values: 2, 3
- Reason: 2 ≤ 3 (already in correct order)

**Decision:**
Since arr[1] (2) ≤ arr[2] (3), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 5: 🔍 Compare arr[2] (3) with arr[3] (4)

**Comparison:**
- Position 2: value = 3
- Position 3: value = 4
- Check: `3 > 4`

**Decision Logic:**
Compare arr[2] (3) with arr[3] (4):
- IF 3 > 4: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
               ^  ^   
               L  R     (L = Left, R = Right in comparison)
```

---

## Step 6: ✓ No swap needed: 3 ≤ 4

**No Swap Needed:**
- Positions: 2, 3
- Values: 3, 4
- Reason: 3 ≤ 4 (already in correct order)

**Decision:**
Since arr[2] (3) ≤ arr[3] (4), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 7: 🔍 Compare arr[3] (4) with arr[4] (5)

**Comparison:**
- Position 3: value = 4
- Position 4: value = 5
- Check: `4 > 5`

**Decision Logic:**
Compare arr[3] (4) with arr[4] (5):
- IF 4 > 5: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
                  ^  ^
                  L  R  (L = Left, R = Right in comparison)
```

---

## Step 8: ✓ No swap needed: 4 ≤ 5

**No Swap Needed:**
- Positions: 3, 4
- Values: 4, 5
- Reason: 4 ≤ 5 (already in correct order)

**Decision:**
Since arr[3] (4) ≤ arr[4] (5), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 9: ✅ Pass 1 complete: 0 swaps, sorted boundary at index 4

**Pass 1 Summary:**
- Swaps performed: 0
- Sorted boundary: index 4 (elements from 4 to end are now sorted)
- Total comparisons so far: 4
- Total swaps so far: 0

🎯 **Early Termination Triggered!**
No swaps occurred in this pass, meaning the array is already sorted. We can stop early instead of continuing unnecessary passes.

**Current Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
State:   U  U  U  U  S  (S = Sorted, U = Unsorted)
```

---

## Execution Summary

**Final Result:** [1, 2, 3, 4, 5]

**Performance Metrics:**
- Total comparisons: 4
- Total swaps: 0
- Passes completed: 1
- Array size: 5 elements

**Complexity Analysis:**
- Time Complexity: O(n²) worst/average case, O(n) best case (already sorted)
- Space Complexity: O(1) (in-place sorting)
- Stability: Stable (equal elements maintain relative order)

**Algorithm Behavior:**
The array was already sorted! Early termination saved unnecessary comparisons.

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
