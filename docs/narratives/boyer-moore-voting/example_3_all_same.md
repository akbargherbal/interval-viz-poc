# Boyer-Moore Voting Execution Narrative

**Algorithm:** Boyer-Moore Voting
**Input Array:** [5, 5, 5, 5, 5]
**Array Size:** 5 elements
**Result:** ✅ Majority element **5** found
**Occurrences:** 5 times (> 2 required)

---

## Step 0: 🗳️ Initialize Boyer-Moore Voting for array of 5 elements

**Algorithm Overview:**
- **Phase 1 (Finding):** Identify potential majority candidate using voting
- **Phase 2 (Verification):** Confirm candidate appears > n/2 times

**Initial Configuration:**
- Array size: 5 elements
- Majority threshold: > 2 occurrences
- Starting candidate: `None`
- Starting count: `0`

**Array Visualization:**
```
Index:   0   1   2   3   4
Value:   5   5   5   5   5
```

---

## Step 1: 📍 Examine array[0] = 5 (count is 0, set as first candidate)

**Current State:**
- Examining: array[0] = **5**
- Current candidate: `5`
- Current count: `0`

**Decision Logic:**
- Count is 0 → No active candidate
- Action: Set new candidate to **5**

---

## Step 2: 🔄 Set candidate to 5, count = 1

**Candidate Change Triggered:**
- Previous candidate: `None` (count reached 0)
- New candidate: **5** (current element)
- Reset count: 0 → **1**

**Why Change?**
When count reaches 0, the current candidate has been "voted out" by opposing elements. We select the current element as the new candidate and restart counting.

---

## Step 3: 📍 Examine array[1] = 5 (candidate: 5, count: 1)

**Current State:**
- Examining: array[1] = **5**
- Current candidate: `5`
- Current count: `1`

**Comparison:**
- Compare: 5 vs candidate (5)
- Match: 5 == 5 ✓
- Action: This element **supports** the candidate

---

## Step 4: ✅ 5 matches candidate 5, increment count: 1 → 2

**Count Update:**
- Element 5 matches candidate 5
- Increment count: 1 + 1 = **2**
- Interpretation: Candidate gains support

**Updated State:**
- Candidate: `5`
- Count: `2`

**Progress:** 2/5 elements processed (3 remaining)

---

## Step 5: 📍 Examine array[2] = 5 (candidate: 5, count: 2)

**Current State:**
- Examining: array[2] = **5**
- Current candidate: `5`
- Current count: `2`

**Comparison:**
- Compare: 5 vs candidate (5)
- Match: 5 == 5 ✓
- Action: This element **supports** the candidate

---

## Step 6: ✅ 5 matches candidate 5, increment count: 2 → 3

**Count Update:**
- Element 5 matches candidate 5
- Increment count: 2 + 1 = **3**
- Interpretation: Candidate gains support

**Updated State:**
- Candidate: `5`
- Count: `3`

**Progress:** 3/5 elements processed (2 remaining)

---

## Step 7: 📍 Examine array[3] = 5 (candidate: 5, count: 3)

**Current State:**
- Examining: array[3] = **5**
- Current candidate: `5`
- Current count: `3`

**Comparison:**
- Compare: 5 vs candidate (5)
- Match: 5 == 5 ✓
- Action: This element **supports** the candidate

---

## Step 8: ✅ 5 matches candidate 5, increment count: 3 → 4

**Count Update:**
- Element 5 matches candidate 5
- Increment count: 3 + 1 = **4**
- Interpretation: Candidate gains support

**Updated State:**
- Candidate: `5`
- Count: `4`

**Progress:** 4/5 elements processed (1 remaining)

---

## Step 9: 📍 Examine array[4] = 5 (candidate: 5, count: 4)

**Current State:**
- Examining: array[4] = **5**
- Current candidate: `5`
- Current count: `4`

**Comparison:**
- Compare: 5 vs candidate (5)
- Match: 5 == 5 ✓
- Action: This element **supports** the candidate

---

## Step 10: ✅ 5 matches candidate 5, increment count: 4 → 5

**Count Update:**
- Element 5 matches candidate 5
- Increment count: 4 + 1 = **5**
- Interpretation: Candidate gains support

**Updated State:**
- Candidate: `5`
- Count: `5`

**Progress:** 5/5 elements processed (0 remaining)

---

## Step 11: 🔍 Phase 1 complete. Candidate: 5. Begin verification phase.

**Phase 1 Complete: Candidate Found**

**Candidate Phase Results:**
- Potential majority element: **5**
- Final count: 5

**Why Verification Needed?**
The voting mechanism guarantees: *if* a majority element exists, it will be the candidate. However, the candidate might NOT be a majority element (e.g., no element appears > n/2 times). We must verify by counting actual occurrences.

**Phase 2: Verification**
- Count occurrences of candidate 5
- Required threshold: > 2 occurrences

---

## Step 12: 🔎 Verify array[0] = 5 == 5 (count: 1)

**Verification Check:**
- Examining: array[0] = 5
- Candidate: 5
- Comparison: 5 == 5

**Match Found:**
- Increment verification count: 0 + 1 = **1**

**Progress:** 1/5 elements verified (4 remaining)

---

## Step 13: 🔎 Verify array[1] = 5 == 5 (count: 2)

**Verification Check:**
- Examining: array[1] = 5
- Candidate: 5
- Comparison: 5 == 5

**Match Found:**
- Increment verification count: 1 + 1 = **2**

**Progress:** 2/5 elements verified (3 remaining)

---

## Step 14: 🔎 Verify array[2] = 5 == 5 (count: 3)

**Verification Check:**
- Examining: array[2] = 5
- Candidate: 5
- Comparison: 5 == 5

**Match Found:**
- Increment verification count: 2 + 1 = **3**

**Progress:** 3/5 elements verified (2 remaining)

---

## Step 15: 🔎 Verify array[3] = 5 == 5 (count: 4)

**Verification Check:**
- Examining: array[3] = 5
- Candidate: 5
- Comparison: 5 == 5

**Match Found:**
- Increment verification count: 3 + 1 = **4**

**Progress:** 4/5 elements verified (1 remaining)

---

## Step 16: 🔎 Verify array[4] = 5 == 5 (count: 5)

**Verification Check:**
- Examining: array[4] = 5
- Candidate: 5
- Comparison: 5 == 5

**Match Found:**
- Increment verification count: 4 + 1 = **5**

**Progress:** 5/5 elements verified (0 remaining)

---

## Step 17: ✅ Majority found: 5 appears 5 times (> 2)

✅ **Majority Element Confirmed!**

**Verification Results:**
- Candidate: **5**
- Actual occurrences: **5**
- Required threshold: > 2
- Comparison: 5 > 2 ✓

**Conclusion:**
Element **5** appears in more than half the array positions, making it the majority element.

---

## Execution Summary

**Final Result:** Majority element **5** found

**Statistics:**
- Array size: 5
- Majority threshold: > 2
- Occurrences: 5
- Percentage: 100.0%

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
