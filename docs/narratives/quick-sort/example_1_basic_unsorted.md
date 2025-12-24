# Quick Sort Execution Narrative

**Algorithm:** Quick Sort
**Input Array:** [10, 7, 8, 9, 1, 5]
**Array Size:** 6 elements
**Partition Scheme:** Lomuto (pivot = last element)

**Final Result:** [1, 5, 7, 8, 9, 10]
**Performance Metrics:**
- Total Comparisons: 11
- Total Swaps: 5
- Partitions Created: 4
- Maximum Recursion Depth: 4

---

## Step 0: 🚀 Starting Quick Sort on array of 6 elements

**Initial Configuration:**
- Array to sort: `[10, 7, 8, 9, 1, 5]`
- Array size: 6 elements
- Sorting range: indices [0, 5]

**Quick Sort Strategy:**
1. Choose pivot (last element in Lomuto scheme)
2. Partition: move elements < pivot to left, ≥ pivot to right
3. Recursively sort left and right partitions
4. Pivot ends up in its final sorted position after each partition

---

## Step 1: 📞 Recursive call: sort subarray[0..5] (size: 6, depth: 1)

**Recursive Call Details:**
- Subarray range: indices [0, 5]
- Subarray: `[10, 7, 8, 9, 1, 5]`
- Size: 6 elements
- Recursion depth: 1

---

## Step 2: 🎯 Select pivot: arr[5] = 5 (partition #1)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 5 (last element of subarray)
- Pivot value: **5**
- Subarray range: [0, 5]

**Partitioning Goal:**
- Move all elements < 5 to the left
- Move all elements ≥ 5 to the right
- Place pivot in its final sorted position

---

## Step 3: 🔍 Compare arr[0] = 10 with pivot 5: 10 < 5 → False

**Comparison:**
- Current element: arr[0] = 10
- Pivot value: 5
- Comparison: `10 < 5`
- Result: **False**

**Decision:** 10 ≥ 5
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: -1

---

## Step 4: 🔍 Compare arr[1] = 7 with pivot 5: 7 < 5 → False

**Comparison:**
- Current element: arr[1] = 7
- Pivot value: 5
- Comparison: `7 < 5`
- Result: **False**

**Decision:** 7 ≥ 5
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: -1

---

## Step 5: 🔍 Compare arr[2] = 8 with pivot 5: 8 < 5 → False

**Comparison:**
- Current element: arr[2] = 8
- Pivot value: 5
- Comparison: `8 < 5`
- Result: **False**

**Decision:** 8 ≥ 5
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: -1

---

## Step 6: 🔍 Compare arr[3] = 9 with pivot 5: 9 < 5 → False

**Comparison:**
- Current element: arr[3] = 9
- Pivot value: 5
- Comparison: `9 < 5`
- Result: **False**

**Decision:** 9 ≥ 5
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: -1

---

## Step 7: 🔍 Compare arr[4] = 1 with pivot 5: 1 < 5 → True

**Comparison:**
- Current element: arr[4] = 1
- Pivot value: 5
- Comparison: `1 < 5`
- Result: **True**

**Decision:** 1 < 5 ✓
- Element belongs in **left partition** (values < pivot)
- Increment partition index: -1 → 0
- Prepare to swap arr[0] with arr[4]

---

## Step 8: 🔄 Swap arr[0] ↔ arr[4]: 10 ↔ 1 (move 1 to left partition)

**Swap Operation:**
- Position 1: arr[0] = 1
- Position 2: arr[4] = 10
- **Action:** Swap arr[0] ↔ arr[4]
- **Reason:** Move 1 to left partition (< pivot)
- **Result:** arr[0] = 1, arr[4] = 10

---

## Step 9: 🔄 Place pivot in final position: swap arr[1] ↔ arr[5]: 7 ↔ 5

**Swap Operation:**
- Position 1: arr[1] = 5
- Position 2: arr[5] = 7
- **Action:** Swap arr[1] ↔ arr[5]
- **Reason:** Place pivot 5 in its final sorted position
- **Result:** Pivot now at index 1 (all left < pivot, all right ≥ pivot)

---

## Step 10: ✅ Partition complete: pivot 5 at index 1 | Left: [1] (1 elements) | Right: [8, 9, 10, 7] (4 elements)

**Partition Summary:**
- Pivot value: **5** now at index **1** (final sorted position)
- Left partition: `[1]` (1 element)
  - All elements < 5
- Right partition: `[8, 9, 10, 7]` (4 elements)
  - All elements ≥ 5

**Partition Invariant Satisfied:**
- Every element in left partition < 5
- Pivot 5 is in its final sorted position
- Every element in right partition ≥ 5

*Left partition has 1 element (already sorted)*
*Then: Recursively sort right partition (4 elements)*

---

## Step 11: 📞 Recursive call: sort subarray[2..5] (size: 4, depth: 2)

**Recursive Call Details:**
- Subarray range: indices [2, 5]
- Subarray: `[8, 9, 10, 7]`
- Size: 4 elements
- Recursion depth: 2

---

## Step 12: 🎯 Select pivot: arr[5] = 7 (partition #2)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 5 (last element of subarray)
- Pivot value: **7**
- Subarray range: [2, 5]

**Partitioning Goal:**
- Move all elements < 7 to the left
- Move all elements ≥ 7 to the right
- Place pivot in its final sorted position

---

## Step 13: 🔍 Compare arr[2] = 8 with pivot 7: 8 < 7 → False

**Comparison:**
- Current element: arr[2] = 8
- Pivot value: 7
- Comparison: `8 < 7`
- Result: **False**

**Decision:** 8 ≥ 7
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: 1

---

## Step 14: 🔍 Compare arr[3] = 9 with pivot 7: 9 < 7 → False

**Comparison:**
- Current element: arr[3] = 9
- Pivot value: 7
- Comparison: `9 < 7`
- Result: **False**

**Decision:** 9 ≥ 7
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: 1

---

## Step 15: 🔍 Compare arr[4] = 10 with pivot 7: 10 < 7 → False

**Comparison:**
- Current element: arr[4] = 10
- Pivot value: 7
- Comparison: `10 < 7`
- Result: **False**

**Decision:** 10 ≥ 7
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: 1

---

## Step 16: 🔄 Place pivot in final position: swap arr[2] ↔ arr[5]: 8 ↔ 7

**Swap Operation:**
- Position 1: arr[2] = 7
- Position 2: arr[5] = 8
- **Action:** Swap arr[2] ↔ arr[5]
- **Reason:** Place pivot 7 in its final sorted position
- **Result:** Pivot now at index 2 (all left < pivot, all right ≥ pivot)

---

## Step 17: ✅ Partition complete: pivot 7 at index 2 | Left: [] (0 elements) | Right: [9, 10, 8] (3 elements)

**Partition Summary:**
- Pivot value: **7** now at index **2** (final sorted position)
- Left partition: `[]` (0 elements)
  - All elements < 7
- Right partition: `[9, 10, 8]` (3 elements)
  - All elements ≥ 7

**Partition Invariant Satisfied:**
- Every element in left partition < 7
- Pivot 7 is in its final sorted position
- Every element in right partition ≥ 7

*Left partition is empty*
*Then: Recursively sort right partition (3 elements)*

---

## Step 18: 📞 Recursive call: sort subarray[3..5] (size: 3, depth: 3)

**Recursive Call Details:**
- Subarray range: indices [3, 5]
- Subarray: `[9, 10, 8]`
- Size: 3 elements
- Recursion depth: 3

---

## Step 19: 🎯 Select pivot: arr[5] = 8 (partition #3)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 5 (last element of subarray)
- Pivot value: **8**
- Subarray range: [3, 5]

**Partitioning Goal:**
- Move all elements < 8 to the left
- Move all elements ≥ 8 to the right
- Place pivot in its final sorted position

---

## Step 20: 🔍 Compare arr[3] = 9 with pivot 8: 9 < 8 → False

**Comparison:**
- Current element: arr[3] = 9
- Pivot value: 8
- Comparison: `9 < 8`
- Result: **False**

**Decision:** 9 ≥ 8
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: 2

---

## Step 21: 🔍 Compare arr[4] = 10 with pivot 8: 10 < 8 → False

**Comparison:**
- Current element: arr[4] = 10
- Pivot value: 8
- Comparison: `10 < 8`
- Result: **False**

**Decision:** 10 ≥ 8
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: 2

---

## Step 22: 🔄 Place pivot in final position: swap arr[3] ↔ arr[5]: 9 ↔ 8

**Swap Operation:**
- Position 1: arr[3] = 8
- Position 2: arr[5] = 9
- **Action:** Swap arr[3] ↔ arr[5]
- **Reason:** Place pivot 8 in its final sorted position
- **Result:** Pivot now at index 3 (all left < pivot, all right ≥ pivot)

---

## Step 23: ✅ Partition complete: pivot 8 at index 3 | Left: [] (0 elements) | Right: [10, 9] (2 elements)

**Partition Summary:**
- Pivot value: **8** now at index **3** (final sorted position)
- Left partition: `[]` (0 elements)
  - All elements < 8
- Right partition: `[10, 9]` (2 elements)
  - All elements ≥ 8

**Partition Invariant Satisfied:**
- Every element in left partition < 8
- Pivot 8 is in its final sorted position
- Every element in right partition ≥ 8

*Left partition is empty*
*Then: Recursively sort right partition (2 elements)*

---

## Step 24: 📞 Recursive call: sort subarray[4..5] (size: 2, depth: 4)

**Recursive Call Details:**
- Subarray range: indices [4, 5]
- Subarray: `[10, 9]`
- Size: 2 elements
- Recursion depth: 4

*Two-element subarray will be sorted in one partition.*

---

## Step 25: 🎯 Select pivot: arr[5] = 9 (partition #4)

**Pivot Selection (Lomuto Scheme):**
- Pivot index: 5 (last element of subarray)
- Pivot value: **9**
- Subarray range: [4, 5]

**Partitioning Goal:**
- Move all elements < 9 to the left
- Move all elements ≥ 9 to the right
- Place pivot in its final sorted position

---

## Step 26: 🔍 Compare arr[4] = 10 with pivot 9: 10 < 9 → False

**Comparison:**
- Current element: arr[4] = 10
- Pivot value: 9
- Comparison: `10 < 9`
- Result: **False**

**Decision:** 10 ≥ 9
- Element belongs in **right partition** (values ≥ pivot)
- Leave in current position (no swap needed)
- Partition index remains: 3

---

## Step 27: 🔄 Place pivot in final position: swap arr[4] ↔ arr[5]: 10 ↔ 9

**Swap Operation:**
- Position 1: arr[4] = 9
- Position 2: arr[5] = 10
- **Action:** Swap arr[4] ↔ arr[5]
- **Reason:** Place pivot 9 in its final sorted position
- **Result:** Pivot now at index 4 (all left < pivot, all right ≥ pivot)

---

## Step 28: ✅ Partition complete: pivot 9 at index 4 | Left: [] (0 elements) | Right: [10] (1 elements)

**Partition Summary:**
- Pivot value: **9** now at index **4** (final sorted position)
- Left partition: `[]` (0 elements)
  - All elements < 9
- Right partition: `[10]` (1 element)
  - All elements ≥ 9

**Partition Invariant Satisfied:**
- Every element in left partition < 9
- Pivot 9 is in its final sorted position
- Every element in right partition ≥ 9

*Left partition is empty*
*Right partition has 1 element (already sorted)*

---

## Execution Summary

**Original Array:** [10, 7, 8, 9, 1, 5]
**Sorted Array:** [1, 5, 7, 8, 9, 10]

**Algorithm Performance:**
- **Comparisons:** 11
  - Each element compared with pivot during partitioning
- **Swaps:** 5
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
