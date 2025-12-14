# Two Pointer Pattern: Array Deduplication

**Input Array:** `[1, 1, 2, 2, 3]`
**Goal:** Remove duplicates in-place and find the count of unique elements.
**Result:** Found **3** unique elements. Final unique array: `[1, 2, 3]`

---

## Step 0: 🚀 Start: slow pointer at index 0, fast pointer at index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   2   2   3  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

---

## Step 1: ⚖️ Compare arr[fast] (1) with arr[slow] (1).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   2   2   3  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`1`) with value at slow pointer (`1`).
- **Result:** `1 == 1` → **Duplicate**

---

## Step 2: ⏭️ Duplicate found. Moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   2   2   3  
State: U   D   E   P   P  
       S       F
```
**Pointers:** slow = `0`, fast = `2`
**Unique Count so far:** `1`

**Action:**
- The values are the same, so this is a duplicate.
- We increment the `fast` pointer to look at the next element.

---

## Step 3: ⚖️ Compare arr[fast] (2) with arr[slow] (1).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   2   2   3  
State: U   D   E   P   P  
       S       F
```
**Pointers:** slow = `0`, fast = `2`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`2`) with value at slow pointer (`1`).
- **Result:** `2 != 1` → **Unique**

---

## Step 4: ✨ New unique element found. Placed 2 at index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   2   2   3  
State: U   U   D   E   P  
           S       F
```
**Pointers:** slow = `1`, fast = `3`
**Unique Count so far:** `2`

**Action:**
- The values are different, so we found a new unique element.
- The `slow` pointer is moved to index `1`.
- The unique value (`2`) is copied to `arr[1]`.
- The `fast` pointer is moved to continue scanning.

---

## Step 5: ⚖️ Compare arr[fast] (2) with arr[slow] (2).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   2   2   3  
State: U   U   D   E   P  
           S       F
```
**Pointers:** slow = `1`, fast = `3`
**Unique Count so far:** `2`

**Decision Logic:**
- Compare value at fast pointer (`2`) with value at slow pointer (`2`).
- **Result:** `2 == 2` → **Duplicate**

---

## Step 6: ⏭️ Duplicate found. Moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   2   2   3  
State: U   U   D   D   E  
           S           F
```
**Pointers:** slow = `1`, fast = `4`
**Unique Count so far:** `2`

**Action:**
- The values are the same, so this is a duplicate.
- We increment the `fast` pointer to look at the next element.

---

## Step 7: ⚖️ Compare arr[fast] (3) with arr[slow] (2).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   2   2   3  
State: U   U   D   D   E  
           S           F
```
**Pointers:** slow = `1`, fast = `4`
**Unique Count so far:** `2`

**Decision Logic:**
- Compare value at fast pointer (`3`) with value at slow pointer (`2`).
- **Result:** `3 != 2` → **Unique**

---

## Step 8: ✨ New unique element found. Placed 3 at index 2.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   2   3  
State: U   U   U   D   D  
               S
```
**Pointers:** slow = `2`, fast = `None`
**Unique Count so far:** `3`

**Action:**
- The values are different, so we found a new unique element.
- The `slow` pointer is moved to index `2`.
- The unique value (`3`) is copied to `arr[2]`.
- The `fast` pointer is moved to continue scanning.

---

## Step 9: ✅ Complete! Found 3 unique elements.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   2   3  
State: U   U   U   S   S  
               S
```
**Pointers:** slow = `2`, fast = `None`
**Unique Count so far:** `3`

The `fast` pointer has reached the end of the array. The algorithm is complete.
The unique elements are from index 0 to the final `slow` pointer position (2).

**Final Unique Array Slice:** `[1, 2, 3]`
**Total Unique Elements:** `3`

---

