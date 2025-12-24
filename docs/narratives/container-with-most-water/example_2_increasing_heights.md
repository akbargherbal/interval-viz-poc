# Container With Most Water Execution Narrative

**Algorithm:** Container With Most Water
**Input Heights:** [1, 2, 3, 4, 5]
**Array Size:** 5 elements
**Maximum Area Found:** 6 square units
**Optimal Container:** indices [1, 4] with heights [2, 5]
**Total Iterations:** 4

---

## Step 0: 🔍 Initialize two pointers at array boundaries: left=0, right=4

**Algorithm Setup:**
- Heights array: [1, 2, 3, 4, 5]
- Array size: 5 elements
- Strategy: Two-pointer technique (start at both ends, move inward)

**Initial Pointers:**
- Left pointer: index 0 (height = 1)
- Right pointer: index 4 (height = 5)

**Tracking Variables:**
- `max_area`: 0 (will track maximum area found)
- `max_left`: None (will track left index of max container)
- `max_right`: None (will track right index of max container)

**Array Visualization:**
```
Index:    0   1   2   3   4
Height:   1   2   3   4   5
          ^               ^
          L               R
```

---

## Step 1: 📏 Calculate area: width=4 × height=1 = 4

**Current Container:**
- Left boundary: index 0 (height = 1)
- Right boundary: index 4 (height = 5)

**Area Calculation:**
```
Width = right_index - left_index
      = 4 - 0
      = 4

Height = min(left_height, right_height)
       = min(1, 5)
       = 1

Area = Width × Height
     = 4 × 1
     = 4
```

**Explanation:** Container height is limited by the shorter wall (1). Water would overflow the shorter side, so we use min(1, 5) = 1.

**Current State:**
```
Index:    0   1   2   3   4
Height:   1   2   3   4   5
          L           R
```
*Container width: 4, height: 1, area: 4*

---

## Step 2: ⬆️ New maximum area found: 4 (previous: 0)

**New Maximum Found!**

**Comparison:** Current area (4) vs Previous max (0)
- Compare: 4 > 0 ✓
- Decision: Update maximum area

**Updates:**
- `max_area`: 0 → 4
- `max_left`: updated to 0
- `max_right`: updated to 4

**Tracking Purpose:** These variables (`max_area`, `max_left`, `max_right`) are tracked because the final result needs to return the maximum area and the indices that formed it.

---

## Step 3: ➡️ Move left pointer: 0 → 1 (left height 1 < right height 5)

**Decision: Move Left Pointer**

**Comparison:** Left height (1) vs Right height (5)
- Compare: 1 < 5 ✓
- Conclusion: Left side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by left side (1)
- Moving right pointer would only decrease width, keeping same height limit
- Moving left pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 0 → 1
- Right pointer: 4 (unchanged)

**Remaining Search Space:**
```
Index:    1   2   3   4
Height:   2   3   4   5
```

---

## Step 4: 📏 Calculate area: width=3 × height=2 = 6

**Current Container:**
- Left boundary: index 1 (height = 2)
- Right boundary: index 4 (height = 5)

**Area Calculation:**
```
Width = right_index - left_index
      = 4 - 1
      = 3

Height = min(left_height, right_height)
       = min(2, 5)
       = 2

Area = Width × Height
     = 3 × 2
     = 6
```

**Explanation:** Container height is limited by the shorter wall (2). Water would overflow the shorter side, so we use min(2, 5) = 2.

**Current State:**
```
Index:    1   2   3   4
Height:   2   3   4   5
          L        R
```
*Container width: 3, height: 2, area: 6*

---

## Step 5: ⬆️ New maximum area found: 6 (previous: 4)

**New Maximum Found!**

**Comparison:** Current area (6) vs Previous max (4)
- Compare: 6 > 4 ✓
- Decision: Update maximum area

**Updates:**
- `max_area`: 4 → 6
- `max_left`: updated to 1
- `max_right`: updated to 4

**Tracking Purpose:** These variables (`max_area`, `max_left`, `max_right`) are tracked because the final result needs to return the maximum area and the indices that formed it.

---

## Step 6: ➡️ Move left pointer: 1 → 2 (left height 2 < right height 5)

**Decision: Move Left Pointer**

**Comparison:** Left height (2) vs Right height (5)
- Compare: 2 < 5 ✓
- Conclusion: Left side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by left side (2)
- Moving right pointer would only decrease width, keeping same height limit
- Moving left pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 → 2
- Right pointer: 4 (unchanged)

**Remaining Search Space:**
```
Index:    2   3   4
Height:   3   4   5
```

---

## Step 7: 📏 Calculate area: width=2 × height=3 = 6

**Current Container:**
- Left boundary: index 2 (height = 3)
- Right boundary: index 4 (height = 5)

**Area Calculation:**
```
Width = right_index - left_index
      = 4 - 2
      = 2

Height = min(left_height, right_height)
       = min(3, 5)
       = 3

Area = Width × Height
     = 2 × 3
     = 6
```

**Explanation:** Container height is limited by the shorter wall (3). Water would overflow the shorter side, so we use min(3, 5) = 3.

**Current State:**
```
Index:    2   3   4
Height:   3   4   5
          L     R
```
*Container width: 2, height: 3, area: 6*

---

## Step 8: ➡️ Move left pointer: 2 → 3 (left height 3 < right height 5)

**Decision: Move Left Pointer**

**Comparison:** Left height (3) vs Right height (5)
- Compare: 3 < 5 ✓
- Conclusion: Left side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by left side (3)
- Moving right pointer would only decrease width, keeping same height limit
- Moving left pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 2 → 3
- Right pointer: 4 (unchanged)

**Remaining Search Space:**
```
Index:    3   4
Height:   4   5
```

---

## Step 9: 📏 Calculate area: width=1 × height=4 = 4

**Current Container:**
- Left boundary: index 3 (height = 4)
- Right boundary: index 4 (height = 5)

**Area Calculation:**
```
Width = right_index - left_index
      = 4 - 3
      = 1

Height = min(left_height, right_height)
       = min(4, 5)
       = 4

Area = Width × Height
     = 1 × 4
     = 4
```

**Explanation:** Container height is limited by the shorter wall (4). Water would overflow the shorter side, so we use min(4, 5) = 4.

**Current State:**
```
Index:    3   4
Height:   4   5
          L  R
```
*Container width: 1, height: 4, area: 4*

---

## Step 10: ➡️ Move left pointer: 3 → 4 (left height 4 < right height 5)

**Decision: Move Left Pointer**

**Comparison:** Left height (4) vs Right height (5)
- Compare: 4 < 5 ✓
- Conclusion: Left side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by left side (4)
- Moving right pointer would only decrease width, keeping same height limit
- Moving left pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 3 → 4
- Right pointer: 4 (unchanged)

**Remaining Search Space:**
```
Index:    4
Height:   5
```

---

## Step 11: ✅ Search complete: Maximum area = 6 at indices [1, 4]

**Search Complete**

**Final State:**
- Pointers have met (left ≥ right)
- All possible containers have been evaluated
- Total iterations: 4

**Maximum Container Found:**
- Indices: [1, 4]
- Heights: [2, 5]
- Maximum area: **6** square units

**Final Visualization:**
```
Index:    0   1   2   3   4
Height:   1   2   3   4   5
             *        *
```
*Elements marked with * form the maximum area container*

---

## Execution Summary

**Final Result:**
- Maximum area: **6** square units
- Optimal container: indices [1, 4]
- Container dimensions:
  - Width: 3
  - Height: 2
  - Left wall height: 2
  - Right wall height: 5

**Performance:**
- Iterations: 4
- Time Complexity: O(n) - single pass through array
- Space Complexity: O(1) - only constant extra space

**Algorithm Efficiency:**
The two-pointer technique evaluates 4 containers out of 10 possible pairs, achieving optimal solution in linear time by always moving the pointer at the shorter height.

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Current Area** (`current_area`) - Shows area of container being evaluated at each step
- **Max Area** (`max_area`) - Tracks the best solution found so far
- **Container Dimensions** (`container_width`, `container_height`) - Visual representation of current container

### Visualization Priorities

1. **Highlight the active container** - Use distinct visual for the two `examining` elements forming current container
2. **Show area calculation visually** - Consider shading/filling the rectangular area between pointers
3. **Emphasize the limiting height** - The shorter of the two walls determines container height
4. **Animate pointer movements** - Show left/right pointer moving inward based on which wall is shorter
5. **Celebrate max updates** - When `max_area` increases, use visual feedback (pulse, color change)
6. **Final state highlight** - Mark the `max_container` elements distinctly in final visualization

### Key JSON Paths

```
step.data.visualization.pointers.left
step.data.visualization.pointers.right
step.data.visualization.current_area
step.data.visualization.max_area
step.data.visualization.container_width
step.data.visualization.container_height
step.data.visualization.array[*].state  // 'examining' | 'active' | 'excluded' | 'max_container'
step.data.visualization.array[*].value  // height at each index
step.data.visualization.array[*].index
step.data.left_height  // height at left pointer
step.data.right_height  // height at right pointer
step.data.area  // calculated area for current container
```

### Algorithm-Specific Guidance

The Container With Most Water problem is fundamentally about **visualizing area maximization**. The most pedagogically important aspect is showing WHY we move the pointer at the shorter height: moving the taller side can only decrease area (width decreases, height stays limited by shorter side), but moving the shorter side might find a taller wall and increase area despite width decrease. Consider using a **filled rectangle** or **shaded area** between the two pointers to make the container concept concrete. The height should be visually limited by the shorter wall (perhaps with a horizontal line at min height). When max_area updates, emphasize this moment - it's a key learning point that the greedy choice (move shorter pointer) leads to optimal solution. The final state should clearly show the winning container with both its dimensions and why this particular pair of heights produces maximum area.
