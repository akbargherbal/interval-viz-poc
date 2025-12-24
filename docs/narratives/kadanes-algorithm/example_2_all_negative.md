# Kadane's Algorithm Execution Narrative

**Algorithm:** Kadane's Algorithm
**Input Array:** [-5, -2, -9, -1, -4]
**Array Size:** 5 elements
**Maximum Sum Found:** -1
**Maximum Subarray:** indices [3, 3] = [-1]

---

## Step 0: 🔍 Initialize with first element: -5

**Current Element:** index 0, value = **-5**

**Decision Logic:**
```
Initialize: current_sum = -5, max_sum = -5
```

**Array State:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
         ^            
```

---

## Step 1: 📊 Initial maximum: -5 at index [0, 0]

**Maximum Sum Update:**

**Comparison:** `-5 > -∞`
- Current sum: -5
- Previous max: None (first update)
- Result: -5 > -∞ ✓

**New Maximum Found:**
- Max sum: **-5**
- Subarray range: indices [0, 0]
- Subarray values: [-5]
- Verification: sum([-5]) = -5 = -5 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
        [M]            
```
*M = Maximum subarray*

---

## Step 2: 🔄 Reset: Start new subarray at index 1 (value = -2)

**Current Element:** index 1, value = **-2**

**Decision Logic:**
```
max(-2, -5 + -2) = max(-2, -7) = -2
```

**Decision:** Reset to current element (start new subarray)
- Previous current_sum: -5
- Current element: -2
- Comparison: max(-2, -5 + -2) = max(-2, -7) = -2
- Result: -2 > -7, so **start fresh** from this element

**New Subarray Started:**
- Range: index [1, 1]
- Sum: -2

**Array State:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
            ^         
```

---

## Step 3: 🎯 New maximum found: -2 at indices [1, 1]

**Maximum Sum Update:**

**Comparison:** `-2 > -5`
- Current sum: -2
- Previous max: -5
- Result: -2 > -5 ✓

**New Maximum Found:**
- Max sum: **-2**
- Subarray range: indices [1, 1]
- Subarray values: [-2]
- Verification: sum([-2]) = -2 = -2 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
           [M]         
```
*M = Maximum subarray*

---

## Step 4: 🔄 Reset: Start new subarray at index 2 (value = -9)

**Current Element:** index 2, value = **-9**

**Decision Logic:**
```
max(-9, -2 + -9) = max(-9, -11) = -9
```

**Decision:** Reset to current element (start new subarray)
- Previous current_sum: -2
- Current element: -9
- Comparison: max(-9, -2 + -9) = max(-9, -11) = -9
- Result: -9 > -11, so **start fresh** from this element

**New Subarray Started:**
- Range: index [2, 2]
- Sum: -9

**Array State:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
               ^      
```

---

## Step 5: 🔄 Reset: Start new subarray at index 3 (value = -1)

**Current Element:** index 3, value = **-1**

**Decision Logic:**
```
max(-1, -9 + -1) = max(-1, -10) = -1
```

**Decision:** Reset to current element (start new subarray)
- Previous current_sum: -9
- Current element: -1
- Comparison: max(-1, -9 + -1) = max(-1, -10) = -1
- Result: -1 > -10, so **start fresh** from this element

**New Subarray Started:**
- Range: index [3, 3]
- Sum: -1

**Array State:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
                  ^   
```

---

## Step 6: 🎯 New maximum found: -1 at indices [3, 3]

**Maximum Sum Update:**

**Comparison:** `-1 > -2`
- Current sum: -1
- Previous max: -2
- Result: -1 > -2 ✓

**New Maximum Found:**
- Max sum: **-1**
- Subarray range: indices [3, 3]
- Subarray values: [-1]
- Verification: sum([-1]) = -1 = -1 ✓

**Array with Maximum Subarray:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
                 [M]   
```
*M = Maximum subarray*

---

## Step 7: 🔄 Reset: Start new subarray at index 4 (value = -4)

**Current Element:** index 4, value = **-4**

**Decision Logic:**
```
max(-4, -1 + -4) = max(-4, -5) = -4
```

**Decision:** Reset to current element (start new subarray)
- Previous current_sum: -1
- Current element: -4
- Comparison: max(-4, -1 + -4) = max(-4, -5) = -4
- Result: -4 > -5, so **start fresh** from this element

**New Subarray Started:**
- Range: index [4, 4]
- Sum: -4

**Array State:**
```
Index:   0   1   2   3   4
Value:  -5  -2  -9  -1  -4
                     ^
```

---

## Execution Summary

**Final Result:**
- Maximum sum: **-1**
- Subarray indices: [3, 3]
- Subarray values: [-1]
- Verification: sum([-1]) = -1 = -1 ✓

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
