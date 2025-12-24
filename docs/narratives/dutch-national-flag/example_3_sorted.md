# Dutch National Flag (Sort Colors) Execution Narrative

**Algorithm:** Sort Colors (Dutch National Flag)
**Input Array:** [0, 0, 1, 1, 2, 2]
**Array Size:** 6 elements
**Goal:** Sort array of 0s (red), 1s (white), and 2s (blue) in one pass
**Result:** [0, 0, 1, 1, 2, 2]
**Total Swaps:** 4

---

## Step 0: 🎨 Initialize three pointers for sorting 6 elements (0s, 1s, 2s)

**Initial Configuration:**
- Array to sort: `[0, 0, 1, 1, 2, 2]`
- Array size: 6 elements
- Three pointers initialized:
  - `low = 0` (boundary for 0s region)
  - `mid = 0` (current element to examine)
  - `high = 5` (boundary for 2s region)

**Strategy:**
- Maintain three regions: [0s | 1s | unsorted | 2s]
- Process elements at `mid` pointer:
  - If 0 (red): swap with `low`, advance both `low` and `mid`
  - If 1 (white): already in correct region, advance `mid`
  - If 2 (blue): swap with `high`, decrement `high` (don't advance `mid`)

**Array Visualization:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
       LMH                    
```
*All pointers start at position 0 (low=mid) and 5 (high)*

---

## Step 1: 🔍 Examine array[0] = 0 (color: red)

**Current State:**
- Examining element at index `mid = 0`
- Value at mid: `0` (color: red)
- Pointer positions: `low = 0`, `mid = 0`, `high = 5`

**Current Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
       LM             H  
```

**Regions:**
- 0s (red): indices [0, 0) - **0 elements**
- 1s (white): indices [0, 0) - **0 elements**
- Unsorted: indices [0, 6) - **6 elements**
- 2s (blue): indices (5, 6) - **0 elements**

**Decision Point:** What to do with value `0`?

---

## Step 2: 🔴 Value is 0 (red): swap array[0] ↔ array[0], advance low and mid

**Value is 0 (red) - Move to 0s region:**

**Comparison:** `array[mid] = 0` → This is a 0 (red)

**Action:** Swap with `low` boundary and advance both pointers
- Swap `array[0]` (value: 0) with `array[0]` (value: 0)
- Calculation: `low = 0 + 1 = 1`
- Calculation: `mid = 0 + 1 = 1`

**Swap Details:**
```
Before: array[0] = 0, array[0] = 0
After:  array[0] = 0, array[0] = 0
```

**Reasoning:**
- The 0 at position 0 belongs in the 0s region
- Swap it with the element at `low` boundary (position 0)
- Advance `low` to expand the 0s region: 0 → 1
- Advance `mid` because swapped element from `low` is already processed (it's either 0 or 1): 0 → 1

**Updated Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
          LM          H  
```

---

## Step 3: 🔍 Examine array[1] = 0 (color: red)

**Current State:**
- Examining element at index `mid = 1`
- Value at mid: `0` (color: red)
- Pointer positions: `low = 1`, `mid = 1`, `high = 5`

**Current Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
          LM          H  
```

**Regions:**
- 0s (red): indices [0, 1) - **1 elements**
- 1s (white): indices [1, 1) - **0 elements**
- Unsorted: indices [1, 6) - **5 elements**
- 2s (blue): indices (5, 6) - **0 elements**

**Decision Point:** What to do with value `0`?

---

## Step 4: 🔴 Value is 0 (red): swap array[1] ↔ array[1], advance low and mid

**Value is 0 (red) - Move to 0s region:**

**Comparison:** `array[mid] = 0` → This is a 0 (red)

**Action:** Swap with `low` boundary and advance both pointers
- Swap `array[1]` (value: 0) with `array[1]` (value: 0)
- Calculation: `low = 1 + 1 = 2`
- Calculation: `mid = 1 + 1 = 2`

**Swap Details:**
```
Before: array[1] = 0, array[1] = 0
After:  array[1] = 0, array[1] = 0
```

**Reasoning:**
- The 0 at position 1 belongs in the 0s region
- Swap it with the element at `low` boundary (position 1)
- Advance `low` to expand the 0s region: 1 → 2
- Advance `mid` because swapped element from `low` is already processed (it's either 0 or 1): 1 → 2

**Updated Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             LM       H  
```

---

## Step 5: 🔍 Examine array[2] = 1 (color: white)

**Current State:**
- Examining element at index `mid = 2`
- Value at mid: `1` (color: white)
- Pointer positions: `low = 2`, `mid = 2`, `high = 5`

**Current Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             LM       H  
```

**Regions:**
- 0s (red): indices [0, 2) - **2 elements**
- 1s (white): indices [2, 2) - **0 elements**
- Unsorted: indices [2, 6) - **4 elements**
- 2s (blue): indices (5, 6) - **0 elements**

**Decision Point:** What to do with value `1`?

---

## Step 6: ⚪ Value is 1 (white): already in correct region, advance mid

**Value is 1 (white) - Already in correct region:**

**Comparison:** `array[mid] = 1` → This is a 1 (white)

**Action:** Simply advance `mid` pointer
- Calculation: `mid = 2 + 1 = 3`
- No swap needed (1s belong between `low` and `mid`)

**Reasoning:**
- The 1 at position 2 is already in the correct region (1s region)
- The 1s region is defined as indices [2, 2)
- By advancing `mid`, we expand the 1s region to include this element
- New 1s region: [2, 3)

**Updated Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L  M     H  
```

---

## Step 7: 🔍 Examine array[3] = 1 (color: white)

**Current State:**
- Examining element at index `mid = 3`
- Value at mid: `1` (color: white)
- Pointer positions: `low = 2`, `mid = 3`, `high = 5`

**Current Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L  M     H  
```

**Regions:**
- 0s (red): indices [0, 2) - **2 elements**
- 1s (white): indices [2, 3) - **1 elements**
- Unsorted: indices [3, 6) - **3 elements**
- 2s (blue): indices (5, 6) - **0 elements**

**Decision Point:** What to do with value `1`?

---

## Step 8: ⚪ Value is 1 (white): already in correct region, advance mid

**Value is 1 (white) - Already in correct region:**

**Comparison:** `array[mid] = 1` → This is a 1 (white)

**Action:** Simply advance `mid` pointer
- Calculation: `mid = 3 + 1 = 4`
- No swap needed (1s belong between `low` and `mid`)

**Reasoning:**
- The 1 at position 3 is already in the correct region (1s region)
- The 1s region is defined as indices [2, 3)
- By advancing `mid`, we expand the 1s region to include this element
- New 1s region: [2, 4)

**Updated Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L     M  H  
```

---

## Step 9: 🔍 Examine array[4] = 2 (color: blue)

**Current State:**
- Examining element at index `mid = 4`
- Value at mid: `2` (color: blue)
- Pointer positions: `low = 2`, `mid = 4`, `high = 5`

**Current Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L     M  H  
```

**Regions:**
- 0s (red): indices [0, 2) - **2 elements**
- 1s (white): indices [2, 4) - **2 elements**
- Unsorted: indices [4, 6) - **2 elements**
- 2s (blue): indices (5, 6) - **0 elements**

**Decision Point:** What to do with value `2`?

---

## Step 10: 🔵 Value is 2 (blue): swap array[4] ↔ array[5], decrement high (mid stays)

**Value is 2 (blue) - Move to 2s region:**

**Comparison:** `array[mid] = 2` → This is a 2 (blue)

**Action:** Swap with `high` boundary and decrement `high`
- Swap `array[4]` (value: 2) with `array[5]` (value: 2)
- Calculation: `high = 5 - 1 = 4`
- Note: `mid` stays at 4 (need to examine swapped element)

**Swap Details:**
```
Before: array[4] = 2, array[5] = 2
After:  array[4] = 2, array[5] = 2
```

**Reasoning:**
- The 2 at position 4 belongs in the 2s region
- Swap it with the element at `high` boundary (position 5)
- Decrement `high` to expand the 2s region: 5 → 4
- **Don't advance `mid`** because the element swapped from `high` (value: 2) hasn't been examined yet
- Next iteration will examine this newly swapped element at position 4

**Updated Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L     MH    
```

---

## Step 11: 🔍 Examine array[4] = 2 (color: blue)

**Current State:**
- Examining element at index `mid = 4`
- Value at mid: `2` (color: blue)
- Pointer positions: `low = 2`, `mid = 4`, `high = 4`

**Current Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L     MH    
```

**Regions:**
- 0s (red): indices [0, 2) - **2 elements**
- 1s (white): indices [2, 4) - **2 elements**
- Unsorted: indices [4, 5) - **1 elements**
- 2s (blue): indices (4, 6) - **1 elements**

**Decision Point:** What to do with value `2`?

---

## Step 12: 🔵 Value is 2 (blue): swap array[4] ↔ array[4], decrement high (mid stays)

**Value is 2 (blue) - Move to 2s region:**

**Comparison:** `array[mid] = 2` → This is a 2 (blue)

**Action:** Swap with `high` boundary and decrement `high`
- Swap `array[4]` (value: 2) with `array[4]` (value: 2)
- Calculation: `high = 4 - 1 = 3`
- Note: `mid` stays at 4 (need to examine swapped element)

**Swap Details:**
```
Before: array[4] = 2, array[4] = 2
After:  array[4] = 2, array[4] = 2
```

**Reasoning:**
- The 2 at position 4 belongs in the 2s region
- Swap it with the element at `high` boundary (position 4)
- Decrement `high` to expand the 2s region: 4 → 3
- **Don't advance `mid`** because the element swapped from `high` (value: 2) hasn't been examined yet
- Next iteration will examine this newly swapped element at position 4

**Updated Array:**
```
Index:   0   1   2   3   4   5
Value:   0   0   1   1   2   2
Color: red red whi whi blu blu
             L  H  M     
```

---

## Execution Summary

**Original Array:** [0, 0, 1, 1, 2, 2]
**Sorted Array:** [0, 0, 1, 1, 2, 2]

**Final Regions:**
- 0s (red): indices [0, 2) → [0, 0]
- 1s (white): indices [2, 4) → [1, 1]
- 2s (blue): indices [4, 6) → [2, 2]

**Performance:**
- Total swaps: 4
- Single pass through array: O(n) time complexity
- In-place sorting: O(1) space complexity
- Optimal for three-value sorting problems

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Three Pointer Positions** (`pointers.low`, `pointers.mid`, `pointers.high`) - Core of the algorithm's partitioning strategy
- **Region Boundaries** (`regions.zeros`, `regions.ones`, `regions.twos`) - Visual representation of the three-way partition
- **Swap Count** (`swaps`) - Demonstrates in-place efficiency

### Visualization Priorities

1. **Color-code elements by value** - Use red (0), white (1), blue (2) to match Dutch flag theme
2. **Highlight the three regions** - Use background shading or borders to show [0s | 1s | unsorted | 2s]
3. **Emphasize pointer movements** - Show when `low` and `mid` advance together vs. when only one moves
4. **Animate swaps clearly** - When swapping with `low` or `high`, show the element movement
5. **Show the examining state** - The element at `mid` is the decision point—highlight it distinctly

### Key JSON Paths

```
step.data.visualization.pointers.low
step.data.visualization.pointers.mid
step.data.visualization.pointers.high
step.data.visualization.regions.zeros
step.data.visualization.regions.ones
step.data.visualization.regions.twos
step.data.visualization.array[*].state  // 'examining' | 'sorted_low' | 'sorted_mid' | 'sorted_high' | 'unsorted'
step.data.visualization.array[*].value  // 0, 1, or 2
step.data.visualization.array[*].color  // 'red', 'white', 'blue'
step.data.visualization.array[*].index
```

### Algorithm-Specific Guidance

The Dutch National Flag algorithm's elegance comes from **maintaining invariants with three pointers**. The most pedagogically important visualization is showing how the three regions grow and shrink: the 0s region expands from the left, the 2s region expands from the right, and the 1s region grows in the middle. The **unsorted region shrinks** as `mid` approaches `high`. Consider using **distinct background colors** for each region to make the partitioning crystal clear. The key insight to emphasize: when we swap with `low`, we advance `mid` (because we know what came from `low`), but when we swap with `high`, we **don't advance `mid`** (because we need to examine what came from `high`). This asymmetry is the algorithm's clever trick. Use the color theme (red/white/blue) not just for aesthetics but to reinforce the three-way partition concept. When the algorithm completes (`mid > high`), show the final sorted array with clear region boundaries to celebrate the one-pass achievement.
