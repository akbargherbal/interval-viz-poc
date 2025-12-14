# Two Pointer Pattern: Array Deduplication

**Input Array:** `[1, 1, 1, 1, 1]`
**Goal:** Remove duplicates in-place and find the count of unique elements.
**Result:** Found **1** unique elements. Final unique array: `[1]`

---

## Step 0: 🚀 Start: slow pointer at index 0, fast pointer at index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
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
Value: 1   1   1   1   1  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`1`) with value at slow pointer (`1`).
- **Result:** `1 == 1` → **Duplicate**

---

## Step 2: ⏭️ Duplicate found. Skip by moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

**Action:**
- The values are the same, so this is a duplicate.
- We only increment the `fast` pointer to look at the next element.

---

## Step 3: ⚖️ Compare arr[fast] (1) with arr[slow] (1).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   D   E   P   P  
       S       F
```
**Pointers:** slow = `0`, fast = `2`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`1`) with value at slow pointer (`1`).
- **Result:** `1 == 1` → **Duplicate**

---

## Step 4: ⏭️ Duplicate found. Skip by moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   D   E   P   P  
       S       F
```
**Pointers:** slow = `0`, fast = `2`
**Unique Count so far:** `1`

**Action:**
- The values are the same, so this is a duplicate.
- We only increment the `fast` pointer to look at the next element.

---

## Step 5: ⚖️ Compare arr[fast] (1) with arr[slow] (1).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   D   D   E   P  
       S           F
```
**Pointers:** slow = `0`, fast = `3`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`1`) with value at slow pointer (`1`).
- **Result:** `1 == 1` → **Duplicate**

---

## Step 6: ⏭️ Duplicate found. Skip by moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   D   D   E   P  
       S           F
```
**Pointers:** slow = `0`, fast = `3`
**Unique Count so far:** `1`

**Action:**
- The values are the same, so this is a duplicate.
- We only increment the `fast` pointer to look at the next element.

---

## Step 7: ⚖️ Compare arr[fast] (1) with arr[slow] (1).

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   D   D   D   E  
       S               F
```
**Pointers:** slow = `0`, fast = `4`
**Unique Count so far:** `1`

**Decision Logic:**
- Compare value at fast pointer (`1`) with value at slow pointer (`1`).
- **Result:** `1 == 1` → **Duplicate**

---

## Step 8: ⏭️ Duplicate found. Skip by moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   D   D   D   E  
       S               F
```
**Pointers:** slow = `0`, fast = `4`
**Unique Count so far:** `1`

**Action:**
- The values are the same, so this is a duplicate.
- We only increment the `fast` pointer to look at the next element.

---

## Step 9: ✅ Complete! Found 1 unique elements.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   1   1   1  
State: U   S   S   S   S  
       S
```
**Pointers:** slow = `0`, fast = `None`
**Unique Count so far:** `1`

The `fast` pointer has reached the end of the array. The algorithm is complete.
The unique elements are from index 0 to the final `slow` pointer position (0).

**Final Unique Array Slice:** `[1]`
**Total Unique Elements:** `1`

---

