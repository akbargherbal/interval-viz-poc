# Container With Most Water Execution Narrative

**Algorithm:** Container With Most Water
**Input Heights:** [1, 8, 6, 2, 5, 4, 8, 3, 7]
**Array Size:** 9 elements
**Maximum Area Found:** 49 square units
**Optimal Container:** indices [1, 8] with heights [8, 7]
**Total Iterations:** 8

---

## Step 0: 🔍 Initialize two pointers at array boundaries: left=0, right=8

**Algorithm Setup:**
- Heights array: [1, 8, 6, 2, 5, 4, 8, 3, 7]
- Array size: 9 elements
- Strategy: Two-pointer technique (start at both ends, move inward)

**Initial Pointers:**
- Left pointer: index 0 (height = 1)
- Right pointer: index 8 (height = 7)

**Tracking Variables:**
- `max_area`: 0 (will track maximum area found)
- `max_left`: None (will track left index of max container)
- `max_right`: None (will track right index of max container)

**Array Visualization:**
```
Index:    0   1   2   3   4   5   6   7   8
Height:   1   8   6   2   5   4   8   3   7
          ^                               ^
          L                               R
```

---

## Step 1: 📏 Calculate area: width=8 × height=1 = 8

**Current Container:**
- Left boundary: index 0 (height = 1)
- Right boundary: index 8 (height = 7)

**Area Calculation:**
```
Width = right_index - left_index
      = 8 - 0
      = 8

Height = min(left_height, right_height)
       = min(1, 7)
       = 1

Area = Width × Height
     = 8 × 1
     = 8
```

**Explanation:** Container height is limited by the shorter wall (1). Water would overflow the shorter side, so we use min(1, 7) = 1.

**Current State:**
```
Index:    0   1   2   3   4   5   6   7   8
Height:   1   8   6   2   5   4   8   3   7
          L                       R
```
*Container width: 8, height: 1, area: 8*

---

## Step 2: ⬆️ New maximum area found: 8 (previous: 0)

**New Maximum Found!**

**Comparison:** Current area (8) vs Previous max (0)
- Compare: 8 > 0 ✓
- Decision: Update maximum area

**Updates:**
- `max_area`: 0 → 8
- `max_left`: updated to 0
- `max_right`: updated to 8

**Tracking Purpose:** These variables (`max_area`, `max_left`, `max_right`) are tracked because the final result needs to return the maximum area and the indices that formed it.

---

## Step 3: ➡️ Move left pointer: 0 → 1 (left height 1 < right height 7)

**Decision: Move Left Pointer**

**Comparison:** Left height (1) vs Right height (7)
- Compare: 1 < 7 ✓
- Conclusion: Left side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by left side (1)
- Moving right pointer would only decrease width, keeping same height limit
- Moving left pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 0 → 1
- Right pointer: 8 (unchanged)

**Remaining Search Space:**
```
Index:    1   2   3   4   5   6   7   8
Height:   8   6   2   5   4   8   3   7
```

---

## Step 4: 📏 Calculate area: width=7 × height=7 = 49

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 8 (height = 7)

**Area Calculation:**
```
Width = right_index - left_index
      = 8 - 1
      = 7

Height = min(left_height, right_height)
       = min(8, 7)
       = 7

Area = Width × Height
     = 7 × 7
     = 49
```

**Explanation:** Container height is limited by the shorter wall (7). Water would overflow the shorter side, so we use min(8, 7) = 7.

**Current State:**
```
Index:    1   2   3   4   5   6   7   8
Height:   8   6   2   5   4   8   3   7
          L                    R
```
*Container width: 7, height: 7, area: 49*

---

## Step 5: ⬆️ New maximum area found: 49 (previous: 8)

**New Maximum Found!**

**Comparison:** Current area (49) vs Previous max (8)
- Compare: 49 > 8 ✓
- Decision: Update maximum area

**Updates:**
- `max_area`: 8 → 49
- `max_left`: updated to 1
- `max_right`: updated to 8

**Tracking Purpose:** These variables (`max_area`, `max_left`, `max_right`) are tracked because the final result needs to return the maximum area and the indices that formed it.

---

## Step 6: ⬅️ Move right pointer: 8 → 7 (right height 7 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (7)
- Compare: 7 < 8 ✓
- Conclusion: Right side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by right side (7)
- Moving left pointer would only decrease width, keeping same height limit
- Moving right pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 8 → 7

**Remaining Search Space:**
```
Index:    1   2   3   4   5   6   7
Height:   8   6   2   5   4   8   3
```

---

## Step 7: 📏 Calculate area: width=6 × height=3 = 18

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 7 (height = 3)

**Area Calculation:**
```
Width = right_index - left_index
      = 7 - 1
      = 6

Height = min(left_height, right_height)
       = min(8, 3)
       = 3

Area = Width × Height
     = 6 × 3
     = 18
```

**Explanation:** Container height is limited by the shorter wall (3). Water would overflow the shorter side, so we use min(8, 3) = 3.

**Current State:**
```
Index:    1   2   3   4   5   6   7
Height:   8   6   2   5   4   8   3
          L                 R
```
*Container width: 6, height: 3, area: 18*

---

## Step 8: ⬅️ Move right pointer: 7 → 6 (right height 3 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (3)
- Compare: 3 < 8 ✓
- Conclusion: Right side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by right side (3)
- Moving left pointer would only decrease width, keeping same height limit
- Moving right pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 7 → 6

**Remaining Search Space:**
```
Index:    1   2   3   4   5   6
Height:   8   6   2   5   4   8
```

---

## Step 9: 📏 Calculate area: width=5 × height=8 = 40

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 6 (height = 8)

**Area Calculation:**
```
Width = right_index - left_index
      = 6 - 1
      = 5

Height = min(left_height, right_height)
       = min(8, 8)
       = 8

Area = Width × Height
     = 5 × 8
     = 40
```

**Explanation:** Container height is limited by the shorter wall (8). Water would overflow the shorter side, so we use min(8, 8) = 8.

**Current State:**
```
Index:    1   2   3   4   5   6
Height:   8   6   2   5   4   8
          L              R
```
*Container width: 5, height: 8, area: 40*

---

## Step 10: ⬅️ Move right pointer: 6 → 5 (right height 8 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (8)
- Compare: 8 = 8
- Conclusion: Heights are equal - either pointer can be moved

**Reasoning:**
- Current container height is 8 (both walls are same height)
- Moving either pointer would only decrease width, keeping same height limit
- We choose to move right pointer (arbitrary choice when heights are equal)

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 6 → 5

**Remaining Search Space:**
```
Index:    1   2   3   4   5
Height:   8   6   2   5   4
```

---

## Step 11: 📏 Calculate area: width=4 × height=4 = 16

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 5 (height = 4)

**Area Calculation:**
```
Width = right_index - left_index
      = 5 - 1
      = 4

Height = min(left_height, right_height)
       = min(8, 4)
       = 4

Area = Width × Height
     = 4 × 4
     = 16
```

**Explanation:** Container height is limited by the shorter wall (4). Water would overflow the shorter side, so we use min(8, 4) = 4.

**Current State:**
```
Index:    1   2   3   4   5
Height:   8   6   2   5   4
          L           R
```
*Container width: 4, height: 4, area: 16*

---

## Step 12: ⬅️ Move right pointer: 5 → 4 (right height 4 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (4)
- Compare: 4 < 8 ✓
- Conclusion: Right side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by right side (4)
- Moving left pointer would only decrease width, keeping same height limit
- Moving right pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 5 → 4

**Remaining Search Space:**
```
Index:    1   2   3   4
Height:   8   6   2   5
```

---

## Step 13: 📏 Calculate area: width=3 × height=5 = 15

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 4 (height = 5)

**Area Calculation:**
```
Width = right_index - left_index
      = 4 - 1
      = 3

Height = min(left_height, right_height)
       = min(8, 5)
       = 5

Area = Width × Height
     = 3 × 5
     = 15
```

**Explanation:** Container height is limited by the shorter wall (5). Water would overflow the shorter side, so we use min(8, 5) = 5.

**Current State:**
```
Index:    1   2   3   4
Height:   8   6   2   5
          L        R
```
*Container width: 3, height: 5, area: 15*

---

## Step 14: ⬅️ Move right pointer: 4 → 3 (right height 5 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (5)
- Compare: 5 < 8 ✓
- Conclusion: Right side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by right side (5)
- Moving left pointer would only decrease width, keeping same height limit
- Moving right pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 4 → 3

**Remaining Search Space:**
```
Index:    1   2   3
Height:   8   6   2
```

---

## Step 15: 📏 Calculate area: width=2 × height=2 = 4

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 3 (height = 2)

**Area Calculation:**
```
Width = right_index - left_index
      = 3 - 1
      = 2

Height = min(left_height, right_height)
       = min(8, 2)
       = 2

Area = Width × Height
     = 2 × 2
     = 4
```

**Explanation:** Container height is limited by the shorter wall (2). Water would overflow the shorter side, so we use min(8, 2) = 2.

**Current State:**
```
Index:    1   2   3
Height:   8   6   2
          L     R
```
*Container width: 2, height: 2, area: 4*

---

## Step 16: ⬅️ Move right pointer: 3 → 2 (right height 2 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (2)
- Compare: 2 < 8 ✓
- Conclusion: Right side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by right side (2)
- Moving left pointer would only decrease width, keeping same height limit
- Moving right pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 3 → 2

**Remaining Search Space:**
```
Index:    1   2
Height:   8   6
```

---

## Step 17: 📏 Calculate area: width=1 × height=6 = 6

**Current Container:**
- Left boundary: index 1 (height = 8)
- Right boundary: index 2 (height = 6)

**Area Calculation:**
```
Width = right_index - left_index
      = 2 - 1
      = 1

Height = min(left_height, right_height)
       = min(8, 6)
       = 6

Area = Width × Height
     = 1 × 6
     = 6
```

**Explanation:** Container height is limited by the shorter wall (6). Water would overflow the shorter side, so we use min(8, 6) = 6.

**Current State:**
```
Index:    1   2
Height:   8   6
          L  R
```
*Container width: 1, height: 6, area: 6*

---

## Step 18: ⬅️ Move right pointer: 2 → 1 (right height 6 ≤ left height 8)

**Decision: Move Right Pointer**

**Comparison:** Left height (8) vs Right height (6)
- Compare: 6 < 8 ✓
- Conclusion: Right side is the limiting factor (shorter wall)

**Reasoning:**
- Current container height is limited by right side (6)
- Moving left pointer would only decrease width, keeping same height limit
- Moving right pointer might find a taller wall, potentially increasing area

**Pointer Update:**
- Left pointer: 1 (unchanged)
- Right pointer: 2 → 1

**Remaining Search Space:**
```
Index:    1
Height:   8
```

---

## Step 19: ✅ Search complete: Maximum area = 49 at indices [1, 8]

**Search Complete**

**Final State:**
- Pointers have met (left ≥ right)
- All possible containers have been evaluated
- Total iterations: 8

**Maximum Container Found:**
- Indices: [1, 8]
- Heights: [8, 7]
- Maximum area: **49** square units

**Final Visualization:**
```
Index:    0   1   2   3   4   5   6   7   8
Height:   1   8   6   2   5   4   8   3   7
             *                    *
```
*Elements marked with * form the maximum area container*

---

## Execution Summary

**Final Result:**
- Maximum area: **49** square units
- Optimal container: indices [1, 8]
- Container dimensions:
  - Width: 7
  - Height: 7
  - Left wall height: 8
  - Right wall height: 7

**Performance:**
- Iterations: 8
- Time Complexity: O(n) - single pass through array
- Space Complexity: O(1) - only constant extra space

**Algorithm Efficiency:**
The two-pointer technique evaluates 8 containers out of 36 possible pairs, achieving optimal solution in linear time by always moving the pointer at the shorter height.

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
