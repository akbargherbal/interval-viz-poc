# Longest Increasing Subsequence (Patience Sorting) Execution Narrative

**Algorithm:** Longest Increasing Subsequence (Patience Sorting)
**Input Array:** [5, 4, 3, 2, 1]
**Array Size:** 5 elements
**Result:** LIS Length = **1**

---

## Step 0: 🎯 Initialize: Find length of longest strictly increasing subsequence

**Algorithm Overview:**
We maintain a `tails` array where `tails[i]` = smallest ending value of all increasing subsequences of length `i+1`.

**Strategy:**
- If current number > last tail: **extend** (append to tails)
- Otherwise: **replace** using binary search to find position

**Initial State:**
- Input array: `[5, 4, 3, 2, 1]`
- Tails array: `[]` (empty)
- Array size: 5 elements

**Input Array Visualization:**
```
Index:   0   1   2   3   4
Value:   5   4   3   2   1
```

## Step 1: 📍 Examine array[0] = 5

**Current Element:** `array[0] = 5`

**Tails Array Before:** `[]`
- Empty (no subsequences yet)

**Decision Point:**
Tails array is empty → **extend** with first element

## Step 2: ➕ Extend: 5 > last tail, append to tails (new length: 1)

**Extension:**
Append `5` to tails array

**Tails Array After:**
```
[5]
```
- Length: 1 (increased by 1)
- New tail: `tails[0] = 5`

**Meaning:** We found a strictly increasing subsequence of length **1** ending with value 5

## Step 3: 📍 Examine array[1] = 4

**Current Element:** `array[1] = 4`

**Tails Array Before:** `[5]`
- Length: 1
- Last tail: `tails[0] = 5`

**Decision Point:**
Compare current number (4) with last tail (5):
- `4 ≤ 5` ✓
- Action: **Replace** using binary search

## Step 4: 🔄 Replace: tails[0] = 4 (was 5)

**Replacement Found:**
Position: `tails[0]`

**Update:**
- Old value: `tails[0] = 5`
- New value: `tails[0] = 4`

**Reason:** 4 is smaller than 5, making it a better candidate for extending subsequences of length 1

**Tails Array After:**
```
[4]
```
- Length: 1 (unchanged)
- Updated position: index 0

## Step 5: 📍 Examine array[2] = 3

**Current Element:** `array[2] = 3`

**Tails Array Before:** `[4]`
- Length: 1
- Last tail: `tails[0] = 4`

**Decision Point:**
Compare current number (3) with last tail (4):
- `3 ≤ 4` ✓
- Action: **Replace** using binary search

## Step 6: 🔄 Replace: tails[0] = 3 (was 4)

**Replacement Found:**
Position: `tails[0]`

**Update:**
- Old value: `tails[0] = 4`
- New value: `tails[0] = 3`

**Reason:** 3 is smaller than 4, making it a better candidate for extending subsequences of length 1

**Tails Array After:**
```
[3]
```
- Length: 1 (unchanged)
- Updated position: index 0

## Step 7: 📍 Examine array[3] = 2

**Current Element:** `array[3] = 2`

**Tails Array Before:** `[3]`
- Length: 1
- Last tail: `tails[0] = 3`

**Decision Point:**
Compare current number (2) with last tail (3):
- `2 ≤ 3` ✓
- Action: **Replace** using binary search

## Step 8: 🔄 Replace: tails[0] = 2 (was 3)

**Replacement Found:**
Position: `tails[0]`

**Update:**
- Old value: `tails[0] = 3`
- New value: `tails[0] = 2`

**Reason:** 2 is smaller than 3, making it a better candidate for extending subsequences of length 1

**Tails Array After:**
```
[2]
```
- Length: 1 (unchanged)
- Updated position: index 0

## Step 9: 📍 Examine array[4] = 1

**Current Element:** `array[4] = 1`

**Tails Array Before:** `[2]`
- Length: 1
- Last tail: `tails[0] = 2`

**Decision Point:**
Compare current number (1) with last tail (2):
- `1 ≤ 2` ✓
- Action: **Replace** using binary search

## Step 10: 🔄 Replace: tails[0] = 1 (was 2)

**Replacement Found:**
Position: `tails[0]`

**Update:**
- Old value: `tails[0] = 2`
- New value: `tails[0] = 1`

**Reason:** 1 is smaller than 2, making it a better candidate for extending subsequences of length 1

**Tails Array After:**
```
[1]
```
- Length: 1 (unchanged)
- Updated position: index 0

---

## Execution Summary

**Final Result:** Longest Increasing Subsequence Length = **1**

**Final Tails Array:** `[1]`
- Length: 1
- Each position represents the smallest ending value for that subsequence length

**Performance:**
- Array size: 5
- Total operations: 10 (excluding initialization)
- Time Complexity: O(n log n) - each element processed with binary search
- Space Complexity: O(n) - tails array storage

**Algorithm Insight:**
The tails array maintains optimal candidates at each length. By keeping the smallest possible ending value for each subsequence length, we maximize opportunities for future extensions. The final length of the tails array (1) equals the LIS length.

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
