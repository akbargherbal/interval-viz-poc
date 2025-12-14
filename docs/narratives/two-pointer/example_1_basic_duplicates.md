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

## Step 2: ⏭️ Duplicate found. Skip by moving fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   2   2   3  
State: U   E   P   P   P  
       S   F
```
**Pointers:** slow = `0`, fast = `1`
**Unique Count so far:** `1`

**Action:**
- The values are the same, so this is a duplicate.
- We only increment the `fast` pointer to look at the next element.

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

## Step 4: ✨ New unique element! Move slow pointer to index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   1   2   2   3  
State: U   U   E   P   P  
           S   F
```
**Pointers:** slow = `1`, fast = `2`
**Unique Count so far:** `2`

**Action:**
- The values are different, so we found a new unique element.
- First, increment the `slow` pointer to make space for the new value.

---

## Step 5: 📝 Copy 2 to arr[1]. Move fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   2   2   3  
State: U   U   E   P   P  
           S   F
```
**Pointers:** slow = `1`, fast = `2`
**Unique Count so far:** `2`

**Action:**
- Copy the unique value (`2`) from `arr[2]` to the new slow position `arr[1]`.
- Then, increment the `fast` pointer to continue scanning.

---

## Step 6: ⚖️ Compare arr[fast] (2) with arr[slow] (2).

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

## Step 7: ⏭️ Duplicate found. Skip by moving fast pointer.

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
- The values are the same, so this is a duplicate.
- We only increment the `fast` pointer to look at the next element.

---

## Step 8: ⚖️ Compare arr[fast] (3) with arr[slow] (2).

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

## Step 9: ✨ New unique element! Move slow pointer to index 2.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   2   2   3  
State: U   U   U   D   E  
               S       F
```
**Pointers:** slow = `2`, fast = `4`
**Unique Count so far:** `3`

**Action:**
- The values are different, so we found a new unique element.
- First, increment the `slow` pointer to make space for the new value.

---

## Step 10: 📝 Copy 3 to arr[2]. Move fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   2   3  
State: U   U   U   D   E  
               S       F
```
**Pointers:** slow = `2`, fast = `4`
**Unique Count so far:** `3`

**Action:**
- Copy the unique value (`3`) from `arr[4]` to the new slow position `arr[2]`.
- Then, increment the `fast` pointer to continue scanning.

---

## Step 11: ✅ Complete! Found 3 unique elements.

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

