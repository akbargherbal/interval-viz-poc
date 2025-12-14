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

## Step 2: ✨ New unique element! Move slow pointer to index 1.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   P   P   P  
           SF
```
**Pointers:** slow = `1`, fast = `1`
**Unique Count so far:** `2`

**Action:**
- The values are different, so we found a new unique element.
- First, increment the `slow` pointer to make space for the new value.

---

## Step 3: 📝 Copy 2 to arr[1]. Move fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   P   P   P  
           SF
```
**Pointers:** slow = `1`, fast = `1`
**Unique Count so far:** `2`

**Action:**
- Copy the unique value (`2`) from `arr[1]` to the new slow position `arr[1]`.
- Then, increment the `fast` pointer to continue scanning.

---

## Step 4: ⚖️ Compare arr[fast] (3) with arr[slow] (2).

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

## Step 5: ✨ New unique element! Move slow pointer to index 2.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   P   P  
               SF
```
**Pointers:** slow = `2`, fast = `2`
**Unique Count so far:** `3`

**Action:**
- The values are different, so we found a new unique element.
- First, increment the `slow` pointer to make space for the new value.

---

## Step 6: 📝 Copy 3 to arr[2]. Move fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   P   P  
               SF
```
**Pointers:** slow = `2`, fast = `2`
**Unique Count so far:** `3`

**Action:**
- Copy the unique value (`3`) from `arr[2]` to the new slow position `arr[2]`.
- Then, increment the `fast` pointer to continue scanning.

---

## Step 7: ⚖️ Compare arr[fast] (4) with arr[slow] (3).

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

## Step 8: ✨ New unique element! Move slow pointer to index 3.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   P  
                   SF
```
**Pointers:** slow = `3`, fast = `3`
**Unique Count so far:** `4`

**Action:**
- The values are different, so we found a new unique element.
- First, increment the `slow` pointer to make space for the new value.

---

## Step 9: 📝 Copy 4 to arr[3]. Move fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   P  
                   SF
```
**Pointers:** slow = `3`, fast = `3`
**Unique Count so far:** `4`

**Action:**
- Copy the unique value (`4`) from `arr[3]` to the new slow position `arr[3]`.
- Then, increment the `fast` pointer to continue scanning.

---

## Step 10: ⚖️ Compare arr[fast] (5) with arr[slow] (4).

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

## Step 11: ✨ New unique element! Move slow pointer to index 4.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   U  
                       SF
```
**Pointers:** slow = `4`, fast = `4`
**Unique Count so far:** `5`

**Action:**
- The values are different, so we found a new unique element.
- First, increment the `slow` pointer to make space for the new value.

---

## Step 12: 📝 Copy 5 to arr[4]. Move fast pointer.

**Array State:**
```
Index: 0   1   2   3   4  
Value: 1   2   3   4   5  
State: U   U   U   U   U  
                       SF
```
**Pointers:** slow = `4`, fast = `4`
**Unique Count so far:** `5`

**Action:**
- Copy the unique value (`5`) from `arr[4]` to the new slow position `arr[4]`.
- Then, increment the `fast` pointer to continue scanning.

---

## Step 13: ✅ Complete! Found 5 unique elements.

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

