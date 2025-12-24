# Quick Sort Execution Narrative

**Algorithm:** Quick Sort
**Input Array:** [1, 2, 3, 4, 5]
**Array Size:** 5 elements
**Partition Scheme:** Lomuto (pivot = last element)

**Final Result:** [1, 2, 3, 4, 5]
**Performance Metrics:**
- Total Comparisons: 10
- Total Swaps: 0
- Partitions Created: 4
- Maximum Recursion Depth: 4

---

## Step 0: 🚀 Starting Quick Sort on array of 5 elements

**Initial Configuration:**
- Array to sort: `[1, 2, 3, 4, 5]`
- Array size: 5 elements
- Sorting range: indices [0, 4]

**Quick Sort Strategy:**
1. Choose pivot (last element in Lomuto scheme)
2. Partition: move elements < pivot to left, ≥ pivot to right
3. Recursively sort left and right partitions
4. Pivot ends up in its final sorted position after each partition

---

## Step 1: 📞 Recursive call: sort subarray[0..4] (size: 5, depth: 1)

**Recursive Call Details:**
- Subarray range: indices [0, 4]
- Subarray: `[1, 2, 3, 4, 5]`
- Size: 5 elements
- Recursion depth: 1

---

## Step 2: 🎯 Select pivot: arr[4] = 5 (partition #1)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 4 (last element of subarray)
- Pivot value: **5**
- Subarray range: [0, 4]

**Partitioning Goal:**
- Move all elements < 5 to the left
- Move all elements ≥ 5 to the right
- Place pivot in its final sorted position

---

## Step 3: 🔍 Compare arr[0] = 1 with pivot 5: 1 < 5 → True

**Comparison:**
- Current element: arr[0] = 1
- Pivot value: 5
- Comparison: `1 < 5`
- Result: **True**

**Decision:** 1 < 5 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: -1 → 0
- Prepare to swap arr[0] with arr[0]

---

## Step 4: ✓ arr[0] = 1 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[0] = 1
- Position 2: arr[0] = 1
- **Action:** No swap needed
- **Reason:** Element 1 already at partition boundary

---

## Step 5: 🔍 Compare arr[1] = 2 with pivot 5: 2 < 5 → True

**Comparison:**
- Current element: arr[1] = 2
- Pivot value: 5
- Comparison: `2 < 5`
- Result: **True**

**Decision:** 2 < 5 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: 0 → 1
- Prepare to swap arr[1] with arr[1]

---

## Step 6: ✓ arr[1] = 2 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[1] = 2
- Position 2: arr[1] = 2
- **Action:** No swap needed
- **Reason:** Element 2 already at partition boundary

---

## Step 7: 🔍 Compare arr[2] = 3 with pivot 5: 3 < 5 → True

**Comparison:**
- Current element: arr[2] = 3
- Pivot value: 5
- Comparison: `3 < 5`
- Result: **True**

**Decision:** 3 < 5 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: 1 → 2
- Prepare to swap arr[2] with arr[2]

---

## Step 8: ✓ arr[2] = 3 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[2] = 3
- Position 2: arr[2] = 3
- **Action:** No swap needed
- **Reason:** Element 3 already at partition boundary

---

## Step 9: 🔍 Compare arr[3] = 4 with pivot 5: 4 < 5 → True

**Comparison:**
- Current element: arr[3] = 4
- Pivot value: 5
- Comparison: `4 < 5`
- Result: **True**

**Decision:** 4 < 5 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: 2 → 3
- Prepare to swap arr[3] with arr[3]

---

## Step 10: ✓ arr[3] = 4 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[3] = 4
- Position 2: arr[3] = 4
- **Action:** No swap needed
- **Reason:** Element 4 already at partition boundary

---

## Step 11: ✓ Pivot arr[4] = 5 already in final position

**Swap Operation:**
- Position 1: arr[4] = 5
- Position 2: arr[4] = 5
- **Action:** No swap needed
- **Reason:** Pivot 5 already in final position

---

## Step 12: ✅ Partition complete: pivot 5 at index 4 | Left: [1, 2, 3, 4] (4 elements) | Right: [] (0 elements)

**Partition Summary:**
- Pivot value: **5** now at index **4** (final sorted position)
- Left partition: `[1, 2, 3, 4]` (4 elements)
  - All elements < 5
- Right partition: `[]` (0 elements)
  - All elements ≥ 5

**Partition Invariant Satisfied:**
- Every element in left partition < 5
- Pivot 5 is in its final sorted position
- Every element in right partition ≥ 5

*Next: Recursively sort left partition (4 elements)*
*Right partition is empty*

---

## Step 13: 📞 Recursive call: sort subarray[0..3] (size: 4, depth: 2)

**Recursive Call Details:**
- Subarray range: indices [0, 3]
- Subarray: `[1, 2, 3, 4]`
- Size: 4 elements
- Recursion depth: 2

---

## Step 14: 🎯 Select pivot: arr[3] = 4 (partition #2)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 3 (last element of subarray)
- Pivot value: **4**
- Subarray range: [0, 3]

**Partitioning Goal:**
- Move all elements < 4 to the left
- Move all elements ≥ 4 to the right
- Place pivot in its final sorted position

---

## Step 15: 🔍 Compare arr[0] = 1 with pivot 4: 1 < 4 → True

**Comparison:**
- Current element: arr[0] = 1
- Pivot value: 4
- Comparison: `1 < 4`
- Result: **True**

**Decision:** 1 < 4 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: -1 → 0
- Prepare to swap arr[0] with arr[0]

---

## Step 16: ✓ arr[0] = 1 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[0] = 1
- Position 2: arr[0] = 1
- **Action:** No swap needed
- **Reason:** Element 1 already at partition boundary

---

## Step 17: 🔍 Compare arr[1] = 2 with pivot 4: 2 < 4 → True

**Comparison:**
- Current element: arr[1] = 2
- Pivot value: 4
- Comparison: `2 < 4`
- Result: **True**

**Decision:** 2 < 4 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: 0 → 1
- Prepare to swap arr[1] with arr[1]

---

## Step 18: ✓ arr[1] = 2 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[1] = 2
- Position 2: arr[1] = 2
- **Action:** No swap needed
- **Reason:** Element 2 already at partition boundary

---

## Step 19: 🔍 Compare arr[2] = 3 with pivot 4: 3 < 4 → True

**Comparison:**
- Current element: arr[2] = 3
- Pivot value: 4
- Comparison: `3 < 4`
- Result: **True**

**Decision:** 3 < 4 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: 1 → 2
- Prepare to swap arr[2] with arr[2]

---

## Step 20: ✓ arr[2] = 3 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[2] = 3
- Position 2: arr[2] = 3
- **Action:** No swap needed
- **Reason:** Element 3 already at partition boundary

---

## Step 21: ✓ Pivot arr[3] = 4 already in final position

**Swap Operation:**
- Position 1: arr[3] = 4
- Position 2: arr[3] = 4
- **Action:** No swap needed
- **Reason:** Pivot 4 already in final position

---

## Step 22: ✅ Partition complete: pivot 4 at index 3 | Left: [1, 2, 3] (3 elements) | Right: [] (0 elements)

**Partition Summary:**
- Pivot value: **4** now at index **3** (final sorted position)
- Left partition: `[1, 2, 3]` (3 elements)
  - All elements < 4
- Right partition: `[]` (0 elements)
  - All elements ≥ 4

**Partition Invariant Satisfied:**
- Every element in left partition < 4
- Pivot 4 is in its final sorted position
- Every element in right partition ≥ 4

*Next: Recursively sort left partition (3 elements)*
*Right partition is empty*

---

## Step 23: 📞 Recursive call: sort subarray[0..2] (size: 3, depth: 3)

**Recursive Call Details:**
- Subarray range: indices [0, 2]
- Subarray: `[1, 2, 3]`
- Size: 3 elements
- Recursion depth: 3

---

## Step 24: 🎯 Select pivot: arr[2] = 3 (partition #3)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 2 (last element of subarray)
- Pivot value: **3**
- Subarray range: [0, 2]

**Partitioning Goal:**
- Move all elements < 3 to the left
- Move all elements ≥ 3 to the right
- Place pivot in its final sorted position

---

## Step 25: 🔍 Compare arr[0] = 1 with pivot 3: 1 < 3 → True

**Comparison:**
- Current element: arr[0] = 1
- Pivot value: 3
- Comparison: `1 < 3`
- Result: **True**

**Decision:** 1 < 3 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: -1 → 0
- Prepare to swap arr[0] with arr[0]

---

## Step 26: ✓ arr[0] = 1 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[0] = 1
- Position 2: arr[0] = 1
- **Action:** No swap needed
- **Reason:** Element 1 already at partition boundary

---

## Step 27: 🔍 Compare arr[1] = 2 with pivot 3: 2 < 3 → True

**Comparison:**
- Current element: arr[1] = 2
- Pivot value: 3
- Comparison: `2 < 3`
- Result: **True**

**Decision:** 2 < 3 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: 0 → 1
- Prepare to swap arr[1] with arr[1]

---

## Step 28: ✓ arr[1] = 2 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[1] = 2
- Position 2: arr[1] = 2
- **Action:** No swap needed
- **Reason:** Element 2 already at partition boundary

---

## Step 29: ✓ Pivot arr[2] = 3 already in final position

**Swap Operation:**
- Position 1: arr[2] = 3
- Position 2: arr[2] = 3
- **Action:** No swap needed
- **Reason:** Pivot 3 already in final position

---

## Step 30: ✅ Partition complete: pivot 3 at index 2 | Left: [1, 2] (2 elements) | Right: [] (0 elements)

**Partition Summary:**
- Pivot value: **3** now at index **2** (final sorted position)
- Left partition: `[1, 2]` (2 elements)
  - All elements < 3
- Right partition: `[]` (0 elements)
  - All elements ≥ 3

**Partition Invariant Satisfied:**
- Every element in left partition < 3
- Pivot 3 is in its final sorted position
- Every element in right partition ≥ 3

*Next: Recursively sort left partition (2 elements)*
*Right partition is empty*

---

## Step 31: 📞 Recursive call: sort subarray[0..1] (size: 2, depth: 4)

**Recursive Call Details:**
- Subarray range: indices [0, 1]
- Subarray: `[1, 2]`
- Size: 2 elements
- Recursion depth: 4

*Two-element subarray will be sorted in one partition.*

---

## Step 32: 🎯 Select pivot: arr[1] = 2 (partition #4)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 1 (last element of subarray)
- Pivot value: **2**
- Subarray range: [0, 1]

**Partitioning Goal:**
- Move all elements < 2 to the left
- Move all elements ≥ 2 to the right
- Place pivot in its final sorted position

---

## Step 33: 🔍 Compare arr[0] = 1 with pivot 2: 1 < 2 → True

**Comparison:**
- Current element: arr[0] = 1
- Pivot value: 2
- Comparison: `1 < 2`
- Result: **True**

**Decision:** 1 < 2 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: -1 → 0
- Prepare to swap arr[0] with arr[0]

---

## Step 34: ✓ arr[0] = 1 already in correct position (no swap needed)

**Swap Operation:**
- Position 1: arr[0] = 1
- Position 2: arr[0] = 1
- **Action:** No swap needed
- **Reason:** Element 1 already at partition boundary

---

## Step 35: ✓ Pivot arr[1] = 2 already in final position

**Swap Operation:**
- Position 1: arr[1] = 2
- Position 2: arr[1] = 2
- **Action:** No swap needed
- **Reason:** Pivot 2 already in final position

---

## Step 36: ✅ Partition complete: pivot 2 at index 1 | Left: [1] (1 elements) | Right: [] (0 elements)

**Partition Summary:**
- Pivot value: **2** now at index **1** (final sorted position)
- Left partition: `[1]` (1 element)
  - All elements < 2
- Right partition: `[]` (0 elements)
  - All elements ≥ 2

**Partition Invariant Satisfied:**
- Every element in left partition < 2
- Pivot 2 is in its final sorted position
- Every element in right partition ≥ 2

*Left partition has 1 element (already sorted)*
*Right partition is empty*

---

## Execution Summary

**Original Array:** [1, 2, 3, 4, 5]
**Sorted Array:** [1, 2, 3, 4, 5]

**Algorithm Performance:**
- **Comparisons:** 10
  - Each element compared with pivot during partitioning
- **Swaps:** 0
  - Elements moved to correct partitions
- **Partitions:** 4
  - Number of times array was divided
- **Max Recursion Depth:** 4
  - Deepest level of recursive calls

**Complexity Analysis:**
- **Time Complexity:**
  - Average case: O(n log n) - balanced partitions
  - Worst case: O(n²) - unbalanced partitions (already sorted)
  - Best case: O(n log n) - perfectly balanced partitions
- **Space Complexity:** O(log n) - recursion stack depth

**Quick Sort Characteristics:**
- **In-place:** Sorts array without extra space (except recursion stack)
- **Unstable:** Equal elements may change relative order
- **Divide-and-conquer:** Recursively partition and sort
- **Pivot choice matters:** Last element (Lomuto) vs. random/median (better average case)

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Partition Progress** - Show how array is divided into left (< pivot) and right (≥ pivot) regions
- **Pivot Position** - Highlight pivot element and its movement to final sorted position
- **Recursion Depth** (`recursion_depth`) - Visualize call stack to show divide-and-conquer strategy
- **Comparison Count** (`comparison_count`) - Track efficiency of partitioning

### Visualization Priorities

1. **Highlight pivot selection** - Use distinct color for pivot element (last element in subarray)
2. **Show partition boundaries** - Visual separator between left partition (< pivot) and right partition (≥ pivot)
3. **Animate swaps** - Show element movements when swapping to left partition or placing pivot
4. **Emphasize sorted positions** - When pivot reaches final position, mark as 'sorted' (won't move again)
5. **Visualize recursion** - Use indentation or tree structure to show recursive calls on subarray ranges

### Key JSON Paths

```
step.data.pivot_index
step.data.pivot_value
step.data.low                    // Start of current subarray
step.data.high                   // End of current subarray
step.data.partition_index        // Boundary between left/right partitions
step.data.comparing_index        // Element being compared with pivot
step.data.comparing_value
step.data.comparison             // String: 'X < pivot'
step.data.result                 // Boolean: comparison result
step.data.index1, index2         // Swap positions
step.data.value1, value2         // Swap values
step.data.reason                 // Swap reason: 'move_to_left_partition', 'place_pivot_final_position'
step.data.left_partition         // Elements < pivot after partition
step.data.right_partition        // Elements ≥ pivot after partition
step.data.visualization.array[*].state  // 'unsorted', 'pivot', 'comparing', 'partitioned', 'sorted'
step.data.visualization.recursion_depth
step.data.visualization.swap_count
step.data.visualization.comparison_count
```

### Algorithm-Specific Guidance

Quick Sort's power comes from **in-place partitioning** - rearranging elements without extra space. The most pedagogically important visualization is showing the **partition process**: how elements are compared with the pivot and swapped to the correct side. Use **color coding** to distinguish:
- **Pivot** (yellow/gold) - The element being used to partition
- **Comparing** (blue) - Element currently being compared with pivot
- **Left partition** (green) - Elements < pivot
- **Right partition** (red) - Elements ≥ pivot
- **Sorted** (gray) - Elements in final position (pivots after partitioning)

The **recursion visualization** is critical for understanding divide-and-conquer. Show the call stack or use a tree structure where each node represents a subarray being sorted. Animate the **recursive descent** (dividing) and **ascent** (combining sorted partitions). When a pivot reaches its final position, emphasize that it **never moves again** - this is the key insight that makes Quick Sort work. The algorithm's efficiency depends on **balanced partitions** - visualize how pivot choice affects partition sizes.
