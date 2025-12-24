# Bubble Sort Execution Narrative

**Algorithm:** Bubble Sort
**Input Array:** [64, 34, 25, 12, 22, 11, 90]
**Array Size:** 7 elements
**Result:** Sorted array: [11, 12, 22, 25, 34, 64, 90]
**Total Comparisons:** 21
**Total Swaps:** 14

---

## Step 0: 🔢 Starting Bubble Sort on array of 7 elements

**Initial Configuration:**
- Array to sort: `[64, 34, 25, 12, 22, 11, 90]`
- Array size: 7 elements
- Strategy: Bubble largest elements to the right through adjacent comparisons

**Array Visualization:**
```
Index:   0   1   2   3   4   5   6
Value:  64  34  25  12  22  11  90
State:   U   U   U   U   U   U   U  (U = Unsorted)
```

**Algorithm Overview:**
Bubble Sort works by repeatedly comparing adjacent elements and swapping them if they're in the wrong order. Each complete pass through the array "bubbles" the largest unsorted element to its correct position at the end. The sorted region grows from right to left.

---

## Step 1: 🔍 Compare arr[0] (64) with arr[1] (34)

**Comparison:**
- Position 0: value = 64
- Position 1: value = 34
- Check: `64 > 34`

**Decision Logic:**
Compare arr[0] (64) with arr[1] (34):
- IF 64 > 34: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3
Value:  64  34  25  12
         ^  ^      
         L  R        (L = Left, R = Right in comparison)
```

---

## Step 2: 🔄 Swap arr[0] (64) ↔ arr[1] (34)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 64 ↔ 34
- Reason: 64 > 34 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 64, arr[1] = 34
- After swap: arr[0] = 34, arr[1] = 64
- Total swaps: 1

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  34  64  25  12  22  11  90
```

---

## Step 3: 🔍 Compare arr[1] (64) with arr[2] (25)

**Comparison:**
- Position 1: value = 64
- Position 2: value = 25
- Check: `64 > 25`

**Decision Logic:**
Compare arr[1] (64) with arr[2] (25):
- IF 64 > 25: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:  34  64  25  12  22
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 4: 🔄 Swap arr[1] (64) ↔ arr[2] (25)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 64 ↔ 25
- Reason: 64 > 25 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 64, arr[2] = 25
- After swap: arr[1] = 25, arr[2] = 64
- Total swaps: 2

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  34  25  64  12  22  11  90
```

---

## Step 5: 🔍 Compare arr[2] (64) with arr[3] (12)

**Comparison:**
- Position 2: value = 64
- Position 3: value = 12
- Check: `64 > 12`

**Decision Logic:**
Compare arr[2] (64) with arr[3] (12):
- IF 64 > 12: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4   5
Value:  34  25  64  12  22  11
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 6: 🔄 Swap arr[2] (64) ↔ arr[3] (12)

**Swap Performed:**
- Positions: 2 ↔ 3
- Values: 64 ↔ 12
- Reason: 64 > 12 (larger value moves right)

**Array Transformation:**
- Before swap: arr[2] = 64, arr[3] = 12
- After swap: arr[2] = 12, arr[3] = 64
- Total swaps: 3

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  34  25  12  64  22  11  90
```

---

## Step 7: 🔍 Compare arr[3] (64) with arr[4] (22)

**Comparison:**
- Position 3: value = 64
- Position 4: value = 22
- Check: `64 > 22`

**Decision Logic:**
Compare arr[3] (64) with arr[4] (22):
- IF 64 > 22: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   1   2   3   4   5   6
Value:  25  12  64  22  11  90
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 8: 🔄 Swap arr[3] (64) ↔ arr[4] (22)

**Swap Performed:**
- Positions: 3 ↔ 4
- Values: 64 ↔ 22
- Reason: 64 > 22 (larger value moves right)

**Array Transformation:**
- Before swap: arr[3] = 64, arr[4] = 22
- After swap: arr[3] = 22, arr[4] = 64
- Total swaps: 4

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  34  25  12  22  64  11  90
```

---

## Step 9: 🔍 Compare arr[4] (64) with arr[5] (11)

**Comparison:**
- Position 4: value = 64
- Position 5: value = 11
- Check: `64 > 11`

**Decision Logic:**
Compare arr[4] (64) with arr[5] (11):
- IF 64 > 11: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   2   3   4   5   6
Value:  12  22  64  11  90
               ^  ^   
               L  R     (L = Left, R = Right in comparison)
```

---

## Step 10: 🔄 Swap arr[4] (64) ↔ arr[5] (11)

**Swap Performed:**
- Positions: 4 ↔ 5
- Values: 64 ↔ 11
- Reason: 64 > 11 (larger value moves right)

**Array Transformation:**
- Before swap: arr[4] = 64, arr[5] = 11
- After swap: arr[4] = 11, arr[5] = 64
- Total swaps: 5

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  34  25  12  22  11  64  90
```

---

## Step 11: 🔍 Compare arr[5] (64) with arr[6] (90)

**Comparison:**
- Position 5: value = 64
- Position 6: value = 90
- Check: `64 > 90`

**Decision Logic:**
Compare arr[5] (64) with arr[6] (90):
- IF 64 > 90: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   3   4   5   6
Value:  22  11  64  90
               ^  ^
               L  R  (L = Left, R = Right in comparison)
```

---

## Step 12: ✓ No swap needed: 64 ≤ 90

**No Swap Needed:**
- Positions: 5, 6
- Values: 64, 90
- Reason: 64 ≤ 90 (already in correct order)

**Decision:**
Since arr[5] (64) ≤ arr[6] (90), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 13: ✅ Pass 1 complete: 5 swaps, sorted boundary at index 6

**Pass 1 Summary:**
- Swaps performed: 5
- Sorted boundary: index 6 (elements from 6 to end are now sorted)
- Total comparisons so far: 6
- Total swaps so far: 5

**Current Array State:**
```
Index:   0   1   2   3   4   5   6
Value:  34  25  12  22  11  64  90
State:   U  U  U  U  U  U  S  (S = Sorted, U = Unsorted)
```

---

## Step 14: 🔍 Compare arr[0] (34) with arr[1] (25)

**Comparison:**
- Position 0: value = 34
- Position 1: value = 25
- Check: `34 > 25`

**Decision Logic:**
Compare arr[0] (34) with arr[1] (25):
- IF 34 > 25: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3
Value:  34  25  12  22
         ^  ^      
         L  R        (L = Left, R = Right in comparison)
```

---

## Step 15: 🔄 Swap arr[0] (34) ↔ arr[1] (25)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 34 ↔ 25
- Reason: 34 > 25 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 34, arr[1] = 25
- After swap: arr[0] = 25, arr[1] = 34
- Total swaps: 6

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  25  34  12  22  11  64  90
```

---

## Step 16: 🔍 Compare arr[1] (34) with arr[2] (12)

**Comparison:**
- Position 1: value = 34
- Position 2: value = 12
- Check: `34 > 12`

**Decision Logic:**
Compare arr[1] (34) with arr[2] (12):
- IF 34 > 12: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:  25  34  12  22  11
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 17: 🔄 Swap arr[1] (34) ↔ arr[2] (12)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 34 ↔ 12
- Reason: 34 > 12 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 34, arr[2] = 12
- After swap: arr[1] = 12, arr[2] = 34
- Total swaps: 7

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  25  12  34  22  11  64  90
```

---

## Step 18: 🔍 Compare arr[2] (34) with arr[3] (22)

**Comparison:**
- Position 2: value = 34
- Position 3: value = 22
- Check: `34 > 22`

**Decision Logic:**
Compare arr[2] (34) with arr[3] (22):
- IF 34 > 22: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4   5
Value:  25  12  34  22  11  64
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 19: 🔄 Swap arr[2] (34) ↔ arr[3] (22)

**Swap Performed:**
- Positions: 2 ↔ 3
- Values: 34 ↔ 22
- Reason: 34 > 22 (larger value moves right)

**Array Transformation:**
- Before swap: arr[2] = 34, arr[3] = 22
- After swap: arr[2] = 22, arr[3] = 34
- Total swaps: 8

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  25  12  22  34  11  64  90
```

---

## Step 20: 🔍 Compare arr[3] (34) with arr[4] (11)

**Comparison:**
- Position 3: value = 34
- Position 4: value = 11
- Check: `34 > 11`

**Decision Logic:**
Compare arr[3] (34) with arr[4] (11):
- IF 34 > 11: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   1   2   3   4   5   6
Value:  12  22  34  11  64  90
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 21: 🔄 Swap arr[3] (34) ↔ arr[4] (11)

**Swap Performed:**
- Positions: 3 ↔ 4
- Values: 34 ↔ 11
- Reason: 34 > 11 (larger value moves right)

**Array Transformation:**
- Before swap: arr[3] = 34, arr[4] = 11
- After swap: arr[3] = 11, arr[4] = 34
- Total swaps: 9

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  25  12  22  11  34  64  90
```

---

## Step 22: 🔍 Compare arr[4] (34) with arr[5] (64)

**Comparison:**
- Position 4: value = 34
- Position 5: value = 64
- Check: `34 > 64`

**Decision Logic:**
Compare arr[4] (34) with arr[5] (64):
- IF 34 > 64: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   2   3   4   5   6
Value:  22  11  34  64  90
               ^  ^   
               L  R     (L = Left, R = Right in comparison)
```

---

## Step 23: ✓ No swap needed: 34 ≤ 64

**No Swap Needed:**
- Positions: 4, 5
- Values: 34, 64
- Reason: 34 ≤ 64 (already in correct order)

**Decision:**
Since arr[4] (34) ≤ arr[5] (64), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 24: ✅ Pass 2 complete: 4 swaps, sorted boundary at index 5

**Pass 2 Summary:**
- Swaps performed: 4
- Sorted boundary: index 5 (elements from 5 to end are now sorted)
- Total comparisons so far: 11
- Total swaps so far: 9

**Current Array State:**
```
Index:   0   1   2   3   4   5   6
Value:  25  12  22  11  34  64  90
State:   U  U  U  U  U  S  S  (S = Sorted, U = Unsorted)
```

---

## Step 25: 🔍 Compare arr[0] (25) with arr[1] (12)

**Comparison:**
- Position 0: value = 25
- Position 1: value = 12
- Check: `25 > 12`

**Decision Logic:**
Compare arr[0] (25) with arr[1] (12):
- IF 25 > 12: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3
Value:  25  12  22  11
         ^  ^      
         L  R        (L = Left, R = Right in comparison)
```

---

## Step 26: 🔄 Swap arr[0] (25) ↔ arr[1] (12)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 25 ↔ 12
- Reason: 25 > 12 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 25, arr[1] = 12
- After swap: arr[0] = 12, arr[1] = 25
- Total swaps: 10

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  12  25  22  11  34  64  90
```

---

## Step 27: 🔍 Compare arr[1] (25) with arr[2] (22)

**Comparison:**
- Position 1: value = 25
- Position 2: value = 22
- Check: `25 > 22`

**Decision Logic:**
Compare arr[1] (25) with arr[2] (22):
- IF 25 > 22: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:  12  25  22  11  34
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 28: 🔄 Swap arr[1] (25) ↔ arr[2] (22)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 25 ↔ 22
- Reason: 25 > 22 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 25, arr[2] = 22
- After swap: arr[1] = 22, arr[2] = 25
- Total swaps: 11

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  12  22  25  11  34  64  90
```

---

## Step 29: 🔍 Compare arr[2] (25) with arr[3] (11)

**Comparison:**
- Position 2: value = 25
- Position 3: value = 11
- Check: `25 > 11`

**Decision Logic:**
Compare arr[2] (25) with arr[3] (11):
- IF 25 > 11: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4   5
Value:  12  22  25  11  34  64
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 30: 🔄 Swap arr[2] (25) ↔ arr[3] (11)

**Swap Performed:**
- Positions: 2 ↔ 3
- Values: 25 ↔ 11
- Reason: 25 > 11 (larger value moves right)

**Array Transformation:**
- Before swap: arr[2] = 25, arr[3] = 11
- After swap: arr[2] = 11, arr[3] = 25
- Total swaps: 12

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  12  22  11  25  34  64  90
```

---

## Step 31: 🔍 Compare arr[3] (25) with arr[4] (34)

**Comparison:**
- Position 3: value = 25
- Position 4: value = 34
- Check: `25 > 34`

**Decision Logic:**
Compare arr[3] (25) with arr[4] (34):
- IF 25 > 34: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   1   2   3   4   5   6
Value:  22  11  25  34  64  90
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 32: ✓ No swap needed: 25 ≤ 34

**No Swap Needed:**
- Positions: 3, 4
- Values: 25, 34
- Reason: 25 ≤ 34 (already in correct order)

**Decision:**
Since arr[3] (25) ≤ arr[4] (34), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 33: ✅ Pass 3 complete: 3 swaps, sorted boundary at index 4

**Pass 3 Summary:**
- Swaps performed: 3
- Sorted boundary: index 4 (elements from 4 to end are now sorted)
- Total comparisons so far: 15
- Total swaps so far: 12

**Current Array State:**
```
Index:   0   1   2   3   4   5   6
Value:  12  22  11  25  34  64  90
State:   U  U  U  U  S  S  S  (S = Sorted, U = Unsorted)
```

---

## Step 34: 🔍 Compare arr[0] (12) with arr[1] (22)

**Comparison:**
- Position 0: value = 12
- Position 1: value = 22
- Check: `12 > 22`

**Decision Logic:**
Compare arr[0] (12) with arr[1] (22):
- IF 12 > 22: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3
Value:  12  22  11  25
         ^  ^      
         L  R        (L = Left, R = Right in comparison)
```

---

## Step 35: ✓ No swap needed: 12 ≤ 22

**No Swap Needed:**
- Positions: 0, 1
- Values: 12, 22
- Reason: 12 ≤ 22 (already in correct order)

**Decision:**
Since arr[0] (12) ≤ arr[1] (22), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 36: 🔍 Compare arr[1] (22) with arr[2] (11)

**Comparison:**
- Position 1: value = 22
- Position 2: value = 11
- Check: `22 > 11`

**Decision Logic:**
Compare arr[1] (22) with arr[2] (11):
- IF 22 > 11: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:  12  22  11  25  34
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 37: 🔄 Swap arr[1] (22) ↔ arr[2] (11)

**Swap Performed:**
- Positions: 1 ↔ 2
- Values: 22 ↔ 11
- Reason: 22 > 11 (larger value moves right)

**Array Transformation:**
- Before swap: arr[1] = 22, arr[2] = 11
- After swap: arr[1] = 11, arr[2] = 22
- Total swaps: 13

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  12  11  22  25  34  64  90
```

---

## Step 38: 🔍 Compare arr[2] (22) with arr[3] (25)

**Comparison:**
- Position 2: value = 22
- Position 3: value = 25
- Check: `22 > 25`

**Decision Logic:**
Compare arr[2] (22) with arr[3] (25):
- IF 22 > 25: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4   5
Value:  12  11  22  25  34  64
               ^  ^      
               L  R        (L = Left, R = Right in comparison)
```

---

## Step 39: ✓ No swap needed: 22 ≤ 25

**No Swap Needed:**
- Positions: 2, 3
- Values: 22, 25
- Reason: 22 ≤ 25 (already in correct order)

**Decision:**
Since arr[2] (22) ≤ arr[3] (25), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 40: ✅ Pass 4 complete: 1 swaps, sorted boundary at index 3

**Pass 4 Summary:**
- Swaps performed: 1
- Sorted boundary: index 3 (elements from 3 to end are now sorted)
- Total comparisons so far: 18
- Total swaps so far: 13

**Current Array State:**
```
Index:   0   1   2   3   4   5   6
Value:  12  11  22  25  34  64  90
State:   U  U  U  S  S  S  S  (S = Sorted, U = Unsorted)
```

---

## Step 41: 🔍 Compare arr[0] (12) with arr[1] (11)

**Comparison:**
- Position 0: value = 12
- Position 1: value = 11
- Check: `12 > 11`

**Decision Logic:**
Compare arr[0] (12) with arr[1] (11):
- IF 12 > 11: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3
Value:  12  11  22  25
         ^  ^      
         L  R        (L = Left, R = Right in comparison)
```

---

## Step 42: 🔄 Swap arr[0] (12) ↔ arr[1] (11)

**Swap Performed:**
- Positions: 0 ↔ 1
- Values: 12 ↔ 11
- Reason: 12 > 11 (larger value moves right)

**Array Transformation:**
- Before swap: arr[0] = 12, arr[1] = 11
- After swap: arr[0] = 11, arr[1] = 12
- Total swaps: 14

**Updated Array:**
```
Index:   0   1   2   3   4   5   6
Value:  11  12  22  25  34  64  90
```

---

## Step 43: 🔍 Compare arr[1] (12) with arr[2] (22)

**Comparison:**
- Position 1: value = 12
- Position 2: value = 22
- Check: `12 > 22`

**Decision Logic:**
Compare arr[1] (12) with arr[2] (22):
- IF 12 > 22: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3   4
Value:  11  12  22  25  34
            ^  ^      
            L  R        (L = Left, R = Right in comparison)
```

---

## Step 44: ✓ No swap needed: 12 ≤ 22

**No Swap Needed:**
- Positions: 1, 2
- Values: 12, 22
- Reason: 12 ≤ 22 (already in correct order)

**Decision:**
Since arr[1] (12) ≤ arr[2] (22), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 45: ✅ Pass 5 complete: 1 swaps, sorted boundary at index 2

**Pass 5 Summary:**
- Swaps performed: 1
- Sorted boundary: index 2 (elements from 2 to end are now sorted)
- Total comparisons so far: 20
- Total swaps so far: 14

**Current Array State:**
```
Index:   0   1   2   3   4   5   6
Value:  11  12  22  25  34  64  90
State:   U  U  S  S  S  S  S  (S = Sorted, U = Unsorted)
```

---

## Step 46: 🔍 Compare arr[0] (11) with arr[1] (12)

**Comparison:**
- Position 0: value = 11
- Position 1: value = 12
- Check: `11 > 12`

**Decision Logic:**
Compare arr[0] (11) with arr[1] (12):
- IF 11 > 12: Swap (wrong order, larger value should be on right)
- ELSE: No swap (correct order, continue)

**Current Comparison Visualization:**
```
Index:   0   1   2   3
Value:  11  12  22  25
         ^  ^      
         L  R        (L = Left, R = Right in comparison)
```

---

## Step 47: ✓ No swap needed: 11 ≤ 12

**No Swap Needed:**
- Positions: 0, 1
- Values: 11, 12
- Reason: 11 ≤ 12 (already in correct order)

**Decision:**
Since arr[0] (11) ≤ arr[1] (12), these elements are already in the correct relative order. No swap is needed. Continue to next pair.

---

## Step 48: ✅ Pass 6 complete: 0 swaps, sorted boundary at index 1

**Pass 6 Summary:**
- Swaps performed: 0
- Sorted boundary: index 1 (elements from 1 to end are now sorted)
- Total comparisons so far: 21
- Total swaps so far: 14

🎯 **Early Termination Triggered!**
No swaps occurred in this pass, meaning the array is already sorted. We can stop early instead of continuing unnecessary passes.

**Current Array State:**
```
Index:   0   1   2   3   4   5   6
Value:  11  12  22  25  34  64  90
State:   U  S  S  S  S  S  S  (S = Sorted, U = Unsorted)
```

---

## Execution Summary

**Final Result:** [11, 12, 22, 25, 34, 64, 90]

**Performance Metrics:**
- Total comparisons: 21
- Total swaps: 14
- Passes completed: 6
- Array size: 7 elements

**Complexity Analysis:**
- Time Complexity: O(n²) worst/average case, O(n) best case (already sorted)
- Space Complexity: O(1) (in-place sorting)
- Stability: Stable (equal elements maintain relative order)

**Algorithm Behavior:**
The algorithm performed 14 swaps across 6 passes to sort the array. Each pass bubbled the largest unsorted element to its correct position at the end.

---

## 🎨 Frontend Visualization Hints

### Primary Metrics to Emphasize

- **Sorted Boundary** (`sorted_boundary`) - Shows the growing sorted region from right to left
- **Comparison Count** (`comparisons`) - Demonstrates O(n²) behavior in real-time
- **Swap Count** (`swaps`) - Shows actual work being done (0 swaps = already sorted)

### Visualization Priorities

1. **Highlight the sorted tail** - Use distinct color for `sorted` state elements (right side of array)
2. **Animate comparisons** - The `comparing` state shows the active pair being evaluated
3. **Emphasize swaps** - When elements swap, use smooth animation to show the exchange
4. **Show pass completion** - Visual indicator when sorted_boundary moves left (one more element sorted)
5. **Celebrate early termination** - If a pass has 0 swaps, highlight that optimization kicked in

### Key JSON Paths

```
step.data.visualization.comparing_indices  // [i, i+1] tuple or null
step.data.visualization.sorted_boundary    // Index where sorted region begins
step.data.visualization.current_pass       // Which pass through array (1-indexed)
step.data.visualization.comparisons        // Running total of comparisons
step.data.visualization.swaps              // Running total of swaps
step.data.visualization.array[*].state     // 'unsorted' | 'comparing' | 'sorted'
step.data.visualization.array[*].value
step.data.visualization.array[*].index
```

### Algorithm-Specific Guidance

Bubble Sort's defining characteristic is the **growing sorted region from right to left**. This is pedagogically crucial - students should see that each pass guarantees one more element is in its final sorted position. The `sorted_boundary` moving leftward is the visual proof of progress. The comparison pairs (`comparing_indices`) should be highlighted as they march left-to-right through the unsorted region. When a swap occurs, animate it clearly - this is the "bubble" action that gives the algorithm its name. The early termination optimization (when `swaps_in_pass = 0`) is a key teaching moment - show that the algorithm is smart enough to detect when work is done. Consider using a **color gradient** for the sorted tail to emphasize the progressive nature of the sort.
