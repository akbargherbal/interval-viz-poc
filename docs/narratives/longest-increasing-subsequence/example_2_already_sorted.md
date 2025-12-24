# Longest Increasing Subsequence (Patience Sorting) Execution Narrative

**Algorithm:** Longest Increasing Subsequence (Patience Sorting)
**Input Array:** [1, 2, 3, 4, 5]
**Array Size:** 5 elements
**Result:** LIS Length = **5**

---

## Step 0: 🎯 Initialize: Find length of longest strictly increasing subsequence

**Algorithm Overview:**
We maintain a `tails` array where `tails[i]` = smallest ending value of all increasing subsequences of length `i+1`.

**Strategy:**
- If current number > last tail: **extend** (append to tails)
- Otherwise: **replace** using binary search to find position

**Initial State:**
- Input array: `[1, 2, 3, 4, 5]`
- Tails array: `[]` (empty)
- Array size: 5 elements

**Input Array Visualization:**
```
Index:   0   1   2   3   4
Value:   1   2   3   4   5
```

## Step 1: 📍 Examine array[0] = 1

**Current Element:** `array[0] = 1`

**Tails Array Before:** `[]`
- Empty (no subsequences yet)

**Decision Point:**
Tails array is empty → **extend** with first element

## Step 2: ➕ Extend: 1 > last tail, append to tails (new length: 1)

**Extension:**
Append `1` to tails array

**Tails Array After:**
```
[1]
```
- Length: 1 (increased by 1)
- New tail: `tails[0] = 1`

**Meaning:** We found a strictly increasing subsequence of length **1** ending with value 1

## Step 3: 📍 Examine array[1] = 2

**Current Element:** `array[1] = 2`

**Tails Array Before:** `[1]`
- Length: 1
- Last tail: `tails[0] = 1`

**Decision Point:**
Compare current number (2) with last tail (1):
- `2 > 1` ✓
- Action: **Extend** (append to tails)

## Step 4: ➕ Extend: 2 > last tail, append to tails (new length: 2)

**Extension:**
Append `2` to tails array

**Tails Array After:**
```
[1, 2]
```
- Length: 2 (increased by 1)
- New tail: `tails[1] = 2`

**Meaning:** We found a strictly increasing subsequence of length **2** ending with value 2

## Step 5: 📍 Examine array[2] = 3

**Current Element:** `array[2] = 3`

**Tails Array Before:** `[1, 2]`
- Length: 2
- Last tail: `tails[1] = 2`

**Decision Point:**
Compare current number (3) with last tail (2):
- `3 > 2` ✓
- Action: **Extend** (append to tails)

## Step 6: ➕ Extend: 3 > last tail, append to tails (new length: 3)

**Extension:**
Append `3` to tails array

**Tails Array After:**
```
[1, 2, 3]
```
- Length: 3 (increased by 1)
- New tail: `tails[2] = 3`

**Meaning:** We found a strictly increasing subsequence of length **3** ending with value 3

## Step 7: 📍 Examine array[3] = 4

**Current Element:** `array[3] = 4`

**Tails Array Before:** `[1, 2, 3]`
- Length: 3
- Last tail: `tails[2] = 3`

**Decision Point:**
Compare current number (4) with last tail (3):
- `4 > 3` ✓
- Action: **Extend** (append to tails)

## Step 8: ➕ Extend: 4 > last tail, append to tails (new length: 4)

**Extension:**
Append `4` to tails array

**Tails Array After:**
```
[1, 2, 3, 4]
```
- Length: 4 (increased by 1)
- New tail: `tails[3] = 4`

**Meaning:** We found a strictly increasing subsequence of length **4** ending with value 4

## Step 9: 📍 Examine array[4] = 5

**Current Element:** `array[4] = 5`

**Tails Array Before:** `[1, 2, 3, 4]`
- Length: 4
- Last tail: `tails[3] = 4`

**Decision Point:**
Compare current number (5) with last tail (4):
- `5 > 4` ✓
- Action: **Extend** (append to tails)

## Step 10: ➕ Extend: 5 > last tail, append to tails (new length: 5)

**Extension:**
Append `5` to tails array

**Tails Array After:**
```
[1, 2, 3, 4, 5]
```
- Length: 5 (increased by 1)
- New tail: `tails[4] = 5`

**Meaning:** We found a strictly increasing subsequence of length **5** ending with value 5

---

## Execution Summary

**Final Result:** Longest Increasing Subsequence Length = **5**

**Final Tails Array:** `[1, 2, 3, 4, 5]`
- Length: 5
- Each position represents the smallest ending value for that subsequence length

**Performance:**
- Array size: 5
- Total operations: 10 (excluding initialization)
- Time Complexity: O(n log n) - each element processed with binary search
- Space Complexity: O(n) - tails array storage

**Algorithm Insight:**
The tails array maintains optimal candidates at each length. By keeping the smallest possible ending value for each subsequence length, we maximize opportunities for future extensions. The final length of the tails array (5) equals the LIS length.

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
