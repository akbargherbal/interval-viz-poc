# Boyer-Moore Voting Execution Narrative

**Algorithm:** Boyer-Moore Voting
**Input Array:** [2, 2, 1, 1, 1, 2, 2]
**Array Size:** 7 elements
**Result:** ✅ Majority element **2** found
**Occurrences:** 4 times (> 3 required)

---

## Step 0: 🗳️ Initialize Boyer-Moore Voting for array of 7 elements

**Algorithm Overview:**
- **Phase 1 (Finding):** Identify potential majority candidate using voting
- **Phase 2 (Verification):** Confirm candidate appears > n/2 times

**Initial Configuration:**
- Array size: 7 elements
- Majority threshold: > 3 occurrences
- Starting candidate: `None`
- Starting count: `0`

**Array Visualization:**
```
Index:   0   1   2   3   4   5   6
Value:   2   2   1   1   1   2   2
```

---

## Step 1: 📍 Examine array[0] = 2 (count is 0, set as first candidate)

**Current State:**
- Examining: array[0] = **2**
- Current candidate: `2`
- Current count: `0`

**Decision Logic:**
- Count is 0 → No active candidate
- Action: Set new candidate to **2**

---

## Step 2: 🔄 Set candidate to 2, count = 1

**Candidate Change Triggered:**
- Previous candidate: `None` (count reached 0)
- New candidate: **2** (current element)
- Reset count: 0 → **1**

**Why Change?**
When count reaches 0, the current candidate has been "voted out" by opposing elements. We select the current element as the new candidate and restart counting.

---

## Step 3: 📍 Examine array[1] = 2 (candidate: 2, count: 1)

**Current State:**
- Examining: array[1] = **2**
- Current candidate: `2`
- Current count: `1`

**Comparison:**
- Compare: 2 vs candidate (2)
- Match: 2 == 2 ✓
- Action: This element **supports** the candidate

---

## Step 4: ✅ 2 matches candidate 2, increment count: 1 → 2

**Count Update:**
- Element 2 matches candidate 2
- Increment count: 1 + 1 = **2**
- Interpretation: Candidate gains support

**Updated State:**
- Candidate: `2`
- Count: `2`

**Progress:** 2/7 elements processed (5 remaining)

---

## Step 5: 📍 Examine array[2] = 1 (candidate: 2, count: 2)

**Current State:**
- Examining: array[2] = **1**
- Current candidate: `2`
- Current count: `2`

**Comparison:**
- Compare: 1 vs candidate (2)
- Mismatch: 1 ≠ 2 ✗
- Action: This element **opposes** the candidate

---

## Step 6: ❌ 1 differs from candidate 2, decrement count: 2 → 1

**Count Update:**
- Element 1 differs from candidate 2
- Decrement count: 2 - 1 = **1**
- Interpretation: Opposing vote cancels one supporting vote

**Updated State:**
- Candidate: `2`
- Count: `1`

**Progress:** 3/7 elements processed (4 remaining)

---

## Step 7: 📍 Examine array[3] = 1 (candidate: 2, count: 1)

**Current State:**
- Examining: array[3] = **1**
- Current candidate: `2`
- Current count: `1`

**Comparison:**
- Compare: 1 vs candidate (2)
- Mismatch: 1 ≠ 2 ✗
- Action: This element **opposes** the candidate

---

## Step 8: ❌ 1 differs from candidate 2, decrement count: 1 → 0

**Count Update:**
- Element 1 differs from candidate 2
- Decrement count: 1 - 1 = **0**
- Interpretation: Opposing vote cancels one supporting vote

**Updated State:**
- Candidate: `2`
- Count: `0`

**Progress:** 4/7 elements processed (3 remaining)

---

## Step 9: 📍 Examine array[4] = 1 (count reached 0, candidate change needed)

**Current State:**
- Examining: array[4] = **1**
- Current candidate: `1`
- Current count: `0`

**Decision Logic:**
- Count is 0 → No active candidate
- Action: Set new candidate to **1**

---

## Step 10: 🔄 Change candidate from 2 to 1, reset count to 1

**Candidate Change Triggered:**
- Previous candidate: `2` (count reached 0)
- New candidate: **1** (current element)
- Reset count: 0 → **1**

**Why Change?**
When count reaches 0, the current candidate has been "voted out" by opposing elements. We select the current element as the new candidate and restart counting.

---

## Step 11: 📍 Examine array[5] = 2 (candidate: 1, count: 1)

**Current State:**
- Examining: array[5] = **2**
- Current candidate: `1`
- Current count: `1`

**Comparison:**
- Compare: 2 vs candidate (1)
- Mismatch: 2 ≠ 1 ✗
- Action: This element **opposes** the candidate

---

## Step 12: ❌ 2 differs from candidate 1, decrement count: 1 → 0

**Count Update:**
- Element 2 differs from candidate 1
- Decrement count: 1 - 1 = **0**
- Interpretation: Opposing vote cancels one supporting vote

**Updated State:**
- Candidate: `1`
- Count: `0`

**Progress:** 6/7 elements processed (1 remaining)

---

## Step 13: 📍 Examine array[6] = 2 (count reached 0, candidate change needed)

**Current State:**
- Examining: array[6] = **2**
- Current candidate: `2`
- Current count: `0`

**Decision Logic:**
- Count is 0 → No active candidate
- Action: Set new candidate to **2**

---

## Step 14: 🔄 Change candidate from 1 to 2, reset count to 1

**Candidate Change Triggered:**
- Previous candidate: `1` (count reached 0)
- New candidate: **2** (current element)
- Reset count: 0 → **1**

**Why Change?**
When count reaches 0, the current candidate has been "voted out" by opposing elements. We select the current element as the new candidate and restart counting.

---

## Step 15: 🔍 Phase 1 complete. Candidate: 2. Begin verification phase.

**Phase 1 Complete: Candidate Found**

**Candidate Phase Results:**
- Potential majority element: **2**
- Final count: 1

**Why Verification Needed?**
The voting mechanism guarantees: *if* a majority element exists, it will be the candidate. However, the candidate might NOT be a majority element (e.g., no element appears > n/2 times). We must verify by counting actual occurrences.

**Phase 2: Verification**
- Count occurrences of candidate 2
- Required threshold: > 3 occurrences

---

## Step 16: 🔎 Verify array[0] = 2 == 2 (count: 1)

**Verification Check:**
- Examining: array[0] = 2
- Candidate: 2
- Comparison: 2 == 2

**Match Found:**
- Increment verification count: 0 + 1 = **1**

**Progress:** 1/7 elements verified (6 remaining)

---

## Step 17: 🔎 Verify array[1] = 2 == 2 (count: 2)

**Verification Check:**
- Examining: array[1] = 2
- Candidate: 2
- Comparison: 2 == 2

**Match Found:**
- Increment verification count: 1 + 1 = **2**

**Progress:** 2/7 elements verified (5 remaining)

---

## Step 18: 🔎 Verify array[2] = 1 ≠ 2 (count: 2)

**Verification Check:**
- Examining: array[2] = 1
- Candidate: 2
- Comparison: 1 ≠ 2

**No Match:**
- Verification count unchanged: **2**

**Progress:** 3/7 elements verified (4 remaining)

---

## Step 19: 🔎 Verify array[3] = 1 ≠ 2 (count: 2)

**Verification Check:**
- Examining: array[3] = 1
- Candidate: 2
- Comparison: 1 ≠ 2

**No Match:**
- Verification count unchanged: **2**

**Progress:** 4/7 elements verified (3 remaining)

---

## Step 20: 🔎 Verify array[4] = 1 ≠ 2 (count: 2)

**Verification Check:**
- Examining: array[4] = 1
- Candidate: 2
- Comparison: 1 ≠ 2

**No Match:**
- Verification count unchanged: **2**

**Progress:** 5/7 elements verified (2 remaining)

---

## Step 21: 🔎 Verify array[5] = 2 == 2 (count: 3)

**Verification Check:**
- Examining: array[5] = 2
- Candidate: 2
- Comparison: 2 == 2

**Match Found:**
- Increment verification count: 2 + 1 = **3**

**Progress:** 6/7 elements verified (1 remaining)

---

## Step 22: 🔎 Verify array[6] = 2 == 2 (count: 4)

**Verification Check:**
- Examining: array[6] = 2
- Candidate: 2
- Comparison: 2 == 2

**Match Found:**
- Increment verification count: 3 + 1 = **4**

**Progress:** 7/7 elements verified (0 remaining)

---

## Step 23: ✅ Majority found: 2 appears 4 times (> 3)

✅ **Majority Element Confirmed!**

**Verification Results:**
- Candidate: **2**
- Actual occurrences: **4**
- Required threshold: > 3
- Comparison: 4 > 3 ✓

**Conclusion:**
Element **2** appears in more than half the array positions, making it the majority element.

---

## Execution Summary

**Final Result:** Majority element **2** found

**Statistics:**
- Array size: 7
- Majority threshold: > 3
- Occurrences: 4
- Percentage: 57.1%

**Algorithm Complexity:**
- Time: O(n) - Two passes through array (finding + verification)
- Space: O(1) - Only stores candidate and count

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Candidate** (`candidate`) - The current potential majority element
- **Count** (`count`) - Voting balance (support vs opposition)
- **Phase** (`phase`) - 'FINDING' vs 'VERIFYING' to show algorithm structure
- **Verification Count** (`verification_count`) - Actual occurrences during Phase 2

### Visualization Priorities

1. **Highlight the voting mechanism** - Use distinct colors for `supporting` (green) vs `opposing` (red) states
2. **Emphasize count reaching 0** - This is the critical moment when candidate changes
3. **Show phase transition clearly** - Visual break between finding and verification phases
4. **Animate verification progress** - Show accumulating `verified` elements vs `rejected` elements
5. **Celebrate/reject final result** - Clear visual feedback when majority confirmed or denied

### Key JSON Paths

```
step.data.visualization.candidate
step.data.visualization.count
step.data.visualization.phase  // 'FINDING' | 'VERIFYING'
step.data.visualization.current_index
step.data.visualization.verification_count
step.data.visualization.array[*].state  // 'examining' | 'supporting' | 'opposing' | 'verified' | 'rejected' | 'neutral'
step.data.visualization.array[*].value
step.data.visualization.array[*].index
```

### Algorithm-Specific Guidance

Boyer-Moore Voting's elegance comes from its **voting metaphor**: each element either supports or opposes the current candidate. The most pedagogically important visualization is showing this **balance of power** through the count variable. When count reaches 0, it's like a political upset—the candidate is "voted out" and replaced. Consider using a **balance scale visual** or **tug-of-war metaphor** where supporting elements pull one way and opposing elements pull the other. The phase transition is crucial: Phase 1 finds a *candidate* (not guaranteed majority), Phase 2 *verifies* it. Show this distinction clearly—perhaps with different background colors or a visual separator. During verification, the accumulating count should feel different from the voting count—it's a simple tally, not a balance. The final moment (majority confirmed or denied) should be dramatic, as it reveals whether the clever voting mechanism found a true majority or just a strong candidate.
