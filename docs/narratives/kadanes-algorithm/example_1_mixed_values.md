# Kadane's Algorithm Execution Narrative

**Algorithm:** Kadane's Algorithm
**Input Array:** [-2, 1, -3, 4, -1, 2, 1, -5, 4]
**Array Size:** 9 elements
**Maximum Sum Found:** 6
**Maximum Subarray:** indices [3, 6] = [4, -1, 2, 1]

---

## Step 0: 🔍 Initialize with first element: -2

**Current Element:** index 0, value = **-2**

**Decision Logic:**
```
Initialize: current_sum = -2, max_sum = -2
```

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
         ^                        
```

---

## Step 1: 📊 Initial maximum: -2 at index [0, 0]

**Maximum Sum Update:**

**Comparison:** `-2 > -∞`
- Current sum: -2
- Previous max: None (first update)
- Result: -2 > -∞ ✓

**New Maximum Found:**
- Max sum: **-2**
- Subarray range: indices [0, 0]
- Subarray values: [-2]
- Verification: sum([-2]) = -2 = -2 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
       [M]                        
```
*M = Maximum subarray*

---

## Step 2: 🔄 Reset: Start new subarray at index 1 (value = 1)

**Current Element:** index 1, value = **1**

**Decision Logic:**
```
max(1, -2 + 1) = max(1, -1) = 1
```

**Decision:** Reset to current element (start new subarray)
- Previous current_sum: -2
- Current element: 1
- Comparison: max(1, -2 + 1) = max(1, -1) = 1
- Result: 1 > -1, so **start fresh** from this element

**New Subarray Started:**
- Range: index [1, 1]
- Sum: 1

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
            ^                     
```

---

## Step 3: 🎯 New maximum found: 1 at indices [1, 1]

**Maximum Sum Update:**

**Comparison:** `1 > -2`
- Current sum: 1
- Previous max: -2
- Result: 1 > -2 ✓

**New Maximum Found:**
- Max sum: **1**
- Subarray range: indices [1, 1]
- Subarray values: [1]
- Verification: sum([1]) = 1 = 1 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
          [M]                     
```
*M = Maximum subarray*

---

## Step 4: ➕ Extend: Add -3 to current subarray (sum = -2)

**Current Element:** index 2, value = **-3**

**Decision Logic:**
```
max(-3, 1 + -3) = max(-3, -2) = -2
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 1
- Add current element: 1 + -3 = -2
- Comparison: max(-3, 1 + -3) = max(-3, -2) = -2
- Result: -2 ≥ -3, so **extend** the current subarray

**Current Subarray:**
- Range: indices [1, 2]
- Sum: -2

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
               ^                  
```

---

## Step 5: 🔄 Reset: Start new subarray at index 3 (value = 4)

**Current Element:** index 3, value = **4**

**Decision Logic:**
```
max(4, -2 + 4) = max(4, 2) = 4
```

**Decision:** Reset to current element (start new subarray)
- Previous current_sum: -2
- Current element: 4
- Comparison: max(4, -2 + 4) = max(4, 2) = 4
- Result: 4 > 2, so **start fresh** from this element

**New Subarray Started:**
- Range: index [3, 3]
- Sum: 4

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                  ^               
```

---

## Step 6: 🎯 New maximum found: 4 at indices [3, 3]

**Maximum Sum Update:**

**Comparison:** `4 > 1`
- Current sum: 4
- Previous max: 1
- Result: 4 > 1 ✓

**New Maximum Found:**
- Max sum: **4**
- Subarray range: indices [3, 3]
- Subarray values: [4]
- Verification: sum([4]) = 4 = 4 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                [M]               
```
*M = Maximum subarray*

---

## Step 7: ➕ Extend: Add -1 to current subarray (sum = 3)

**Current Element:** index 4, value = **-1**

**Decision Logic:**
```
max(-1, 4 + -1) = max(-1, 3) = 3
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 4
- Add current element: 4 + -1 = 3
- Comparison: max(-1, 4 + -1) = max(-1, 3) = 3
- Result: 3 ≥ -1, so **extend** the current subarray

**Current Subarray:**
- Range: indices [3, 4]
- Sum: 3

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                     ^            
```

---

## Step 8: ➕ Extend: Add 2 to current subarray (sum = 5)

**Current Element:** index 5, value = **2**

**Decision Logic:**
```
max(2, 3 + 2) = max(2, 5) = 5
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 3
- Add current element: 3 + 2 = 5
- Comparison: max(2, 3 + 2) = max(2, 5) = 5
- Result: 5 ≥ 2, so **extend** the current subarray

**Current Subarray:**
- Range: indices [3, 5]
- Sum: 5

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                        ^         
```

---

## Step 9: 🎯 New maximum found: 5 at indices [3, 5]

**Maximum Sum Update:**

**Comparison:** `5 > 4`
- Current sum: 5
- Previous max: 4
- Result: 5 > 4 ✓

**New Maximum Found:**
- Max sum: **5**
- Subarray range: indices [3, 5]
- Subarray values: [4, -1, 2]
- Verification: sum([4, -1, 2]) = 5 = 5 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                [M   M M]         
```
*M = Maximum subarray*

---

## Step 10: ➕ Extend: Add 1 to current subarray (sum = 6)

**Current Element:** index 6, value = **1**

**Decision Logic:**
```
max(1, 5 + 1) = max(1, 6) = 6
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 5
- Add current element: 5 + 1 = 6
- Comparison: max(1, 5 + 1) = max(1, 6) = 6
- Result: 6 ≥ 1, so **extend** the current subarray

**Current Subarray:**
- Range: indices [3, 6]
- Sum: 6

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                           ^      
```

---

## Step 11: 🎯 New maximum found: 6 at indices [3, 6]

**Maximum Sum Update:**

**Comparison:** `6 > 5`
- Current sum: 6
- Previous max: 5
- Result: 6 > 5 ✓

**New Maximum Found:**
- Max sum: **6**
- Subarray range: indices [3, 6]
- Subarray values: [4, -1, 2, 1]
- Verification: sum([4, -1, 2, 1]) = 6 = 6 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                [M   M  M M]      
```
*M = Maximum subarray*

---

## Step 12: ➕ Extend: Add -5 to current subarray (sum = 1)

**Current Element:** index 7, value = **-5**

**Decision Logic:**
```
max(-5, 6 + -5) = max(-5, 1) = 1
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 6
- Add current element: 6 + -5 = 1
- Comparison: max(-5, 6 + -5) = max(-5, 1) = 1
- Result: 1 ≥ -5, so **extend** the current subarray

**Current Subarray:**
- Range: indices [3, 7]
- Sum: 1

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                              ^   
```

---

## Step 13: ➕ Extend: Add 4 to current subarray (sum = 5)

**Current Element:** index 8, value = **4**

**Decision Logic:**
```
max(4, 1 + 4) = max(4, 5) = 5
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 1
- Add current element: 1 + 4 = 5
- Comparison: max(4, 1 + 4) = max(4, 5) = 5
- Result: 5 ≥ 4, so **extend** the current subarray

**Current Subarray:**
- Range: indices [3, 8]
- Sum: 5

**Array State:**
```
Index:   0   1   2   3   4   5   6   7   8
Value:  -2   1  -3   4  -1   2   1  -5   4
                                 ^
```

---

## Execution Summary

**Final Result:**
- Maximum sum: **6**
- Subarray indices: [3, 6]
- Subarray values: [4, -1, 2, 1]
- Verification: sum([4, -1, 2, 1]) = 6 = 6 ✓

**Algorithm Efficiency:**
- Elements processed: 9
- Time Complexity: O(n) - single pass through array
- Space Complexity: O(1) - constant extra space

**Key Insight:**
At each position, we decide: extend the current subarray (if it helps) or start fresh (if previous sum is negative). This greedy choice at each step guarantees finding the global maximum.

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Current Sum** (`current_sum`) - Shows the running sum of the current subarray being considered
- **Max Sum** (`max_sum`) - The best sum found so far (goal metric)
- **Decision Logic** - The comparison `max(num, current + num)` is the heart of the algorithm

### Visualization Priorities

1. **Highlight the decision moment** - When processing each element, emphasize the choice: extend vs. reset
2. **Show subarray evolution** - Use distinct colors for `in_current_subarray` (candidate) vs `in_max_subarray` (best so far)
3. **Animate sum updates** - When current_sum changes, show the arithmetic visually (old + new = result)
4. **Celebrate max updates** - When max_sum improves, use visual feedback (pulse, color change, trophy icon)
5. **Show the examining element** - The current element being processed should stand out clearly

### Key JSON Paths

```
step.data.visualization.current_sum
step.data.visualization.max_sum
step.data.visualization.current_subarray.start
step.data.visualization.current_subarray.end
step.data.visualization.max_subarray.start
step.data.visualization.max_subarray.end
step.data.visualization.array[*].state  // 'examining' | 'in_current_subarray' | 'in_max_subarray' | 'excluded'
step.data.visualization.array[*].value
step.data.visualization.array[*].index
step.data.decision  // 'add_to_current' | 'reset_to_current' (for ITERATE steps)
```

### Algorithm-Specific Guidance

Kadane's Algorithm is elegant because it makes a **local greedy decision** at each element that leads to the **global optimal solution**. The most pedagogically important moment is the decision: "Should I extend my current subarray or start fresh?" Visualize this as a **fork in the road** at each element. When the algorithm resets (starts a new subarray), show the old subarray fading away and a new one beginning. When max_sum updates, emphasize that we've found a **new champion** - this is a milestone moment. Consider using a **dual-track visualization**: one track showing the current candidate subarray (dynamic, changes frequently) and another showing the best subarray found so far (stable, only updates when beaten). The contrast between these two tracks helps students understand the algorithm's strategy: constantly exploring new possibilities while remembering the best one encountered.
