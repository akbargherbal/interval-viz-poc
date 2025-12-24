# Kadane's Algorithm Execution Narrative

**Algorithm:** Kadane's Algorithm
**Input Array:** [1, 2, 3, 4, 5]
**Array Size:** 5 elements
**Maximum Sum Found:** 15
**Maximum Subarray:** indices [0, 4] = [1, 2, 3, 4, 5]

---

## Step 0: 🔍 Initialize with first element: 1

**Current Element:** index 0, value = **1**

**Decision Logic:**
```
Initialize: current_sum = 1, max_sum = 1
```

**Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
         ^            
```

---

## Step 1: 📊 Initial maximum: 1 at index [0, 0]

**Maximum Sum Update:**

**Comparison:** `1 > -∞`
- Current sum: 1
- Previous max: None (first update)
- Result: 1 > -∞ ✓

**New Maximum Found:**
- Max sum: **1**
- Subarray range: indices [0, 0]
- Subarray values: [1]
- Verification: sum([1]) = 1 = 1 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
        [M]            
```
*M = Maximum subarray*

---

## Step 2: ➕ Extend: Add 2 to current subarray (sum = 3)

**Current Element:** index 1, value = **2**

**Decision Logic:**
```
max(2, 1 + 2) = max(2, 3) = 3
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 1
- Add current element: 1 + 2 = 3
- Comparison: max(2, 1 + 2) = max(2, 3) = 3
- Result: 3 ≥ 2, so **extend** the current subarray

**Current Subarray:**
- Range: indices [0, 1]
- Sum: 3

**Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
            ^         
```

---

## Step 3: 🎯 New maximum found: 3 at indices [0, 1]

**Maximum Sum Update:**

**Comparison:** `3 > 1`
- Current sum: 3
- Previous max: 1
- Result: 3 > 1 ✓

**New Maximum Found:**
- Max sum: **3**
- Subarray range: indices [0, 1]
- Subarray values: [1, 2]
- Verification: sum([1, 2]) = 3 = 3 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
        [M] M]         
```
*M = Maximum subarray*

---

## Step 4: ➕ Extend: Add 3 to current subarray (sum = 6)

**Current Element:** index 2, value = **3**

**Decision Logic:**
```
max(3, 3 + 3) = max(3, 6) = 6
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 3
- Add current element: 3 + 3 = 6
- Comparison: max(3, 3 + 3) = max(3, 6) = 6
- Result: 6 ≥ 3, so **extend** the current subarray

**Current Subarray:**
- Range: indices [0, 2]
- Sum: 6

**Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
               ^      
```

---

## Step 5: 🎯 New maximum found: 6 at indices [0, 2]

**Maximum Sum Update:**

**Comparison:** `6 > 3`
- Current sum: 6
- Previous max: 3
- Result: 6 > 3 ✓

**New Maximum Found:**
- Max sum: **6**
- Subarray range: indices [0, 2]
- Subarray values: [1, 2, 3]
- Verification: sum([1, 2, 3]) = 6 = 6 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
        [M]  M M]      
```
*M = Maximum subarray*

---

## Step 6: ➕ Extend: Add 4 to current subarray (sum = 10)

**Current Element:** index 3, value = **4**

**Decision Logic:**
```
max(4, 6 + 4) = max(4, 10) = 10
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 6
- Add current element: 6 + 4 = 10
- Comparison: max(4, 6 + 4) = max(4, 10) = 10
- Result: 10 ≥ 4, so **extend** the current subarray

**Current Subarray:**
- Range: indices [0, 3]
- Sum: 10

**Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
                  ^   
```

---

## Step 7: 🎯 New maximum found: 10 at indices [0, 3]

**Maximum Sum Update:**

**Comparison:** `10 > 6`
- Current sum: 10
- Previous max: 6
- Result: 10 > 6 ✓

**New Maximum Found:**
- Max sum: **10**
- Subarray range: indices [0, 3]
- Subarray values: [1, 2, 3, 4]
- Verification: sum([1, 2, 3, 4]) = 10 = 10 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
        [M]  M  M M]   
```
*M = Maximum subarray*

---

## Step 8: ➕ Extend: Add 5 to current subarray (sum = 15)

**Current Element:** index 4, value = **5**

**Decision Logic:**
```
max(5, 10 + 5) = max(5, 15) = 15
```

**Decision:** Add to current sum (extending subarray)
- Previous current_sum: 10
- Add current element: 10 + 5 = 15
- Comparison: max(5, 10 + 5) = max(5, 15) = 15
- Result: 15 ≥ 5, so **extend** the current subarray

**Current Subarray:**
- Range: indices [0, 4]
- Sum: 15

**Array State:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
                     ^
```

---

## Step 9: 🎯 New maximum found: 15 at indices [0, 4]

**Maximum Sum Update:**

**Comparison:** `15 > 10`
- Current sum: 15
- Previous max: 10
- Result: 15 > 10 ✓

**New Maximum Found:**
- Max sum: **15**
- Subarray range: indices [0, 4]
- Subarray values: [1, 2, 3, 4, 5]
- Verification: sum([1, 2, 3, 4, 5]) = 15 = 15 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
        [M]  M  M  M M]
```
*M = Maximum subarray*

---

## Execution Summary

**Final Result:**
- Maximum sum: **15**
- Subarray indices: [0, 4]
- Subarray values: [1, 2, 3, 4, 5]
- Verification: sum([1, 2, 3, 4, 5]) = 15 = 15 ✓

**Algorithm Efficiency:**
- Elements processed: 5
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
