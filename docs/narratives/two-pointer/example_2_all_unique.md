# Two Pointer Pattern: Array Deduplication

**Input Array:** `[1, 2, 3, 4, 5]`
**Goal:** Remove duplicates in-place and find the count of unique elements.
**Result:** Found **5** unique elements. Final unique array: `[1, 2, 3, 4, 5]`

---

## Step 0: 🚀 Start: slow pointer at index 0, fast pointer at index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

---

## Step 1: ⚖️ Compare arr[fast] (2) with arr[slow] (1).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`2`) with value at slow pointer (`1`).
- **Result:** `2 != 1` → **Unique**

---

## Step 2: ✨ New unique element found. Placed 2 at index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   E   P   P  
           S   F
```
**Pointers:** slow = `1`, fast = `2`
**Unique Count so far:** `2`

**Action:**
- The values are different, so we found a new unique element.
- The `slow` pointer is moved to index `1`.
- The unique value (`2`) is copied to `arr[1]`.
- The `fast` pointer is moved to continue scanning.

---

## Step 3: ⚖️ Compare arr[fast] (3) with arr[slow] (2).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   E   P   P  
           S   F
```
**Pointers:** slow = `1`, fast = `2`
**Unique Count so far:** `2`

**Decision Logic:**
- Compare value at fast pointer (`3`) with value at slow pointer (`2`).
- **Result:** `3 != 2` → **Unique**

---

## Step 4: ✨ New unique element found. Placed 3 at index 2.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   E   P  
               S   F
```
**Pointers:** slow = `2`, fast = `3`
**Unique Count so far:** `3`

**Action:**
- The values are different, so we found a new unique element.
- The `slow` pointer is moved to index `2`.
- The unique value (`3`) is copied to `arr[2]`.
- The `fast` pointer is moved to continue scanning.

---

## Step 5: ⚖️ Compare arr[fast] (4) with arr[slow] (3).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   E   P  
               S   F
```
**Pointers:** slow = `2`, fast = `3`
**Unique Count so far:** `3`

**Decision Logic:**
- Compare value at fast pointer (`4`) with value at slow pointer (`3`).
- **Result:** `4 != 3` → **Unique**

---

## Step 6: ✨ New unique element found. Placed 4 at index 3.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   E  
                   S   F
```
**Pointers:** slow = `3`, fast = `4`
**Unique Count so far:** `4`

**Action:**
- The values are different, so we found a new unique element.
- The `slow` pointer is moved to index `3`.
- The unique value (`4`) is copied to `arr[3]`.
- The `fast` pointer is moved to continue scanning.

---

## Step 7: ⚖️ Compare arr[fast] (5) with arr[slow] (4).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   E  
                   S   F
```
**Pointers:** slow = `3`, fast = `4`
**Unique Count so far:** `4`

**Decision Logic:**
- Compare value at fast pointer (`5`) with value at slow pointer (`4`).
- **Result:** `5 != 4` → **Unique**

---

## Step 8: ✨ New unique element found. Placed 5 at index 4.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   U  
                       S
```
**Pointers:** slow = `4`, fast = `None`
**Unique Count so far:** `5`

**Action:**
- The values are different, so we found a new unique element.
- The `slow` pointer is moved to index `4`.
- The unique value (`5`) is copied to `arr[4]`.
- The `fast` pointer is moved to continue scanning.

---

## Step 9: ✅ Complete! Found 5 unique elements.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   U  
                       S
```
**Pointers:** slow = `4`, fast = `None`
**Unique Count so far:** `5`

The `fast` pointer has reached the end of the array. The algorithm is complete.
The unique elements are from index 0 to the final `slow` pointer position (4).

**Final Unique Array Slice:** `[1, 2, 3, 4, 5]`
**Total Unique Elements:** `5`

---

