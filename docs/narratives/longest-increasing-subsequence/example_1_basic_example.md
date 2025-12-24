# Longest Increasing Subsequence (Patience Sorting) Execution Narrative

**Algorithm:** Longest Increasing Subsequence (Patience Sorting)
**Input Array:** [10, 9, 2, 5, 3, 7, 101, 18]
**Array Size:** 8 elements
**Result:** LIS Length = **4**

---

## Step 0: 🎯 Initialize: Find length of longest strictly increasing subsequence

**Algorithm Overview:**
We maintain a `tails` array where `tails[i]` = smallest ending value of all increasing subsequences of length `i+1`.

**Strategy:**
- If current number > last tail: **extend** (append to tails)
- Otherwise: **replace** using binary search to find position

**Initial State:**
- Input array: `[10, 9, 2, 5, 3, 7, 101, 18]`
- Tails array: `[]` (empty)
- Array size: 8 elements

**Input Array Visualization:**
```
Index:   0   1   2   3   4   5   6   7
Value:  10   9   2   5   3   7 101  18
```

## Step 1: 📍 Examine array[0] = 10

**Current Element:** `array[0] = 10`

**Tails Array Before:** `[]`
- Empty (no subsequences yet)

**Decision Point:**
Tails array is empty → **extend** with first element

## Step 2: ➕ Extend: 10 > last tail, append to tails (new length: 1)

**Extension:**
Append `10` to tails array

**Tails Array After:**
```
[10]
```
- Length: 1 (increased by 1)
- New tail: `tails[0] = 10`

**Meaning:** We found a strictly increasing subsequence of length **1** ending with value 10

## Step 3: 📍 Examine array[1] = 9

**Current Element:** `array[1] = 9`

**Tails Array Before:** `[10]`
- Length: 1
- Last tail: `tails[0] = 10`

**Decision Point:**
Compare current number (9) with last tail (10):
- `9 ≤ 10` ✓
- Action: **Replace** using binary search

## Step 4: 🔄 Replace: tails[0] = 9 (was 10)

**Replacement Found:**
Position: `tails[0]`

**Update:**
- Old value: `tails[0] = 10`
- New value: `tails[0] = 9`

**Reason:** 9 is smaller than 10, making it a better candidate for extending subsequences of length 1

**Tails Array After:**
```
[9]
```
- Length: 1 (unchanged)
- Updated position: index 0

## Step 5: 📍 Examine array[2] = 2

**Current Element:** `array[2] = 2`

**Tails Array Before:** `[9]`
- Length: 1
- Last tail: `tails[0] = 9`

**Decision Point:**
Compare current number (2) with last tail (9):
- `2 ≤ 9` ✓
- Action: **Replace** using binary search

## Step 6: 🔄 Replace: tails[0] = 2 (was 9)

**Replacement Found:**
Position: `tails[0]`

**Update:**
- Old value: `tails[0] = 9`
- New value: `tails[0] = 2`

**Reason:** 2 is smaller than 9, making it a better candidate for extending subsequences of length 1

**Tails Array After:**
```
[2]
```
- Length: 1 (unchanged)
- Updated position: index 0

## Step 7: 📍 Examine array[3] = 5

**Current Element:** `array[3] = 5`

**Tails Array Before:** `[2]`
- Length: 1
- Last tail: `tails[0] = 2`

**Decision Point:**
Compare current number (5) with last tail (2):
- `5 > 2` ✓
- Action: **Extend** (append to tails)

## Step 8: ➕ Extend: 5 > last tail, append to tails (new length: 2)

**Extension:**
Append `5` to tails array

**Tails Array After:**
```
[2, 5]
```
- Length: 2 (increased by 1)
- New tail: `tails[1] = 5`

**Meaning:** We found a strictly increasing subsequence of length **2** ending with value 5

## Step 9: 📍 Examine array[4] = 3

**Current Element:** `array[4] = 3`

**Tails Array Before:** `[2, 5]`
- Length: 2
- Last tail: `tails[1] = 5`

**Decision Point:**
Compare current number (3) with last tail (5):
- `3 ≤ 5` ✓
- Action: **Replace** using binary search

## Step 10: 🔍 Binary search: mid=0, tails[0]=2

**Binary Search in Tails Array:**
Goal: Find leftmost position where `tails[pos] ≥ 3`

**Search Range:** indices [0, 1]
**Tails Subset:**
```
Index:   0   1
Value:   2   5
        LM  R
```

**Mid Calculation:**
```
mid = (0 + 1) // 2 = 0
```

**Comparison:** `tails[0] (2) vs 3`
- tails[0] (2) < 3

## Step 11: 🔄 Replace: tails[1] = 3 (was 5)

**Replacement Found:**
Position: `tails[1]`

**Update:**
- Old value: `tails[1] = 5`
- New value: `tails[1] = 3`

**Reason:** 3 is smaller than 5, making it a better candidate for extending subsequences of length 2

**Tails Array After:**
```
[2, 3]
```
- Length: 2 (unchanged)
- Updated position: index 1

## Step 12: 📍 Examine array[5] = 7

**Current Element:** `array[5] = 7`

**Tails Array Before:** `[2, 3]`
- Length: 2
- Last tail: `tails[1] = 3`

**Decision Point:**
Compare current number (7) with last tail (3):
- `7 > 3` ✓
- Action: **Extend** (append to tails)

## Step 13: ➕ Extend: 7 > last tail, append to tails (new length: 3)

**Extension:**
Append `7` to tails array

**Tails Array After:**
```
[2, 3, 7]
```
- Length: 3 (increased by 1)
- New tail: `tails[2] = 7`

**Meaning:** We found a strictly increasing subsequence of length **3** ending with value 7

## Step 14: 📍 Examine array[6] = 101

**Current Element:** `array[6] = 101`

**Tails Array Before:** `[2, 3, 7]`
- Length: 3
- Last tail: `tails[2] = 7`

**Decision Point:**
Compare current number (101) with last tail (7):
- `101 > 7` ✓
- Action: **Extend** (append to tails)

## Step 15: ➕ Extend: 101 > last tail, append to tails (new length: 4)

**Extension:**
Append `101` to tails array

**Tails Array After:**
```
[2, 3, 7, 101]
```
- Length: 4 (increased by 1)
- New tail: `tails[3] = 101`

**Meaning:** We found a strictly increasing subsequence of length **4** ending with value 101

## Step 16: 📍 Examine array[7] = 18

**Current Element:** `array[7] = 18`

**Tails Array Before:** `[2, 3, 7, 101]`
- Length: 4
- Last tail: `tails[3] = 101`

**Decision Point:**
Compare current number (18) with last tail (101):
- `18 ≤ 101` ✓
- Action: **Replace** using binary search

## Step 17: 🔍 Binary search: mid=1, tails[1]=3

**Binary Search in Tails Array:**
Goal: Find leftmost position where `tails[pos] ≥ 18`

**Search Range:** indices [0, 3]
**Tails Subset:**
```
Index:   0   1   2   3
Value:   2   3   7 101
         L  M     R
```

**Mid Calculation:**
```
mid = (0 + 3) // 2 = 1
```

**Comparison:** `tails[1] (3) vs 18`
- tails[1] (3) < 18

## Step 18: 🔍 Binary search: mid=2, tails[2]=7

**Binary Search in Tails Array:**
Goal: Find leftmost position where `tails[pos] ≥ 18`

**Search Range:** indices [2, 3]
**Tails Subset:**
```
Index:   2   3
Value:   7 101
        LM  R
```

**Mid Calculation:**
```
mid = (2 + 3) // 2 = 2
```

**Comparison:** `tails[2] (7) vs 18`
- tails[2] (7) < 18

## Step 19: 🔄 Replace: tails[3] = 18 (was 101)

**Replacement Found:**
Position: `tails[3]`

**Update:**
- Old value: `tails[3] = 101`
- New value: `tails[3] = 18`

**Reason:** 18 is smaller than 101, making it a better candidate for extending subsequences of length 4

**Tails Array After:**
```
[2, 3, 7, 18]
```
- Length: 4 (unchanged)
- Updated position: index 3

---

## Execution Summary

**Final Result:** Longest Increasing Subsequence Length = **4**

**Final Tails Array:** `[2, 3, 7, 18]`
- Length: 4
- Each position represents the smallest ending value for that subsequence length

**Performance:**
- Array size: 8
- Total operations: 19 (excluding initialization)
- Time Complexity: O(n log n) - each element processed with binary search
- Space Complexity: O(n) - tails array storage

**Algorithm Insight:**
The tails array maintains optimal candidates at each length. By keeping the smallest possible ending value for each subsequence length, we maximize opportunities for future extensions. The final length of the tails array (4) equals the LIS length.

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Tails Array Length** (`tails_length`) - This IS the LIS length, the primary result
- **Current Element** (`current_element.value`) - Shows which number is being processed
- **Tails Array Contents** (`tails[*].value`) - Shows the optimal candidates at each length

### Visualization Priorities

1. **Highlight the tails array growth** - When length increases, this is a key moment (new LIS length found)
2. **Show extend vs replace decisions** - Use distinct visual cues (e.g., green for extend, yellow for replace)
3. **Animate binary search** - When searching for replacement position, show the narrowing search space
4. **Emphasize the current element** - Make it clear which array element is being examined
5. **Show tails overlay on input array** - Help learners see the relationship between input and tails

### Key JSON Paths

```
step.data.visualization.array[*].state  // 'pending' | 'examining' | 'processed'
step.data.visualization.array[*].value
step.data.visualization.array[*].index
step.data.visualization.tails[*].value
step.data.visualization.tails[*].index
step.data.visualization.tails[*].state  // 'active' | 'examining' | 'replacing'
step.data.visualization.tails_length
step.data.visualization.current_element.index
step.data.visualization.current_element.value
step.data.visualization.binary_search.left  // When searching
step.data.visualization.binary_search.mid
step.data.visualization.binary_search.right
```

### Algorithm-Specific Guidance

The patience sorting algorithm's power comes from maintaining **optimal candidates** at each subsequence length. The most important visualization is the **tails array** - its length IS the answer, and its contents show why. Consider using a **dual-panel view**: input array on top, tails array below with clear length indicator. The **extend vs replace decision** is the algorithm's "brain" - highlight this moment with visual emphasis. When binary searching for replacement position, show the search narrowing (similar to binary search visualization). The final state should clearly show: input array (all processed), final tails array, and the LIS length prominently displayed. Use the `show_tails_overlay` config to help learners understand which input elements correspond to tail values.
