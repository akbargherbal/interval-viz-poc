# Interval Coverage - Execution Narrative

**Input:** 4 intervals
**Output:** 2 intervals kept
**Total Steps:** 23
**Duration:** 0.0028s

---

## Step-by-Step Execution

### Step 1: INITIAL_STATE

> Original unsorted intervals

Starting with **4 intervals** (unsorted).

### Step 2: SORT_BEGIN

> Sorting intervals by start time (ascending) breaks ties by preferring longer intervals

Sorting intervals by start time (ascending), with ties broken by preferring longer intervals.

### Step 3: SORT_COMPLETE

> ✓ Sorted! Now we can use a greedy strategy: process intervals left-to-right, keeping only those that extend our coverage.

Sorted order: [540-720], [540-660], [600-720], [900-960]

### Step 4: CALL_START

> New recursive call (depth 0): examining interval (540, 720) with 3 remaining

📞 Recursive call at depth **0**
- Processing: interval (540, 720)
- Remaining: 3 intervals

### Step 5: EXAMINING_INTERVAL

> Does interval (540, 720) extend beyond max_end=-∞ (no coverage yet)? If yes, we KEEP it; if no, it's COVERED.

**Examining interval (540, 720)**
- Current coverage extends to: **-∞ (no coverage yet)**
- Interval ends at: **720**
- Decision logic: If 720 > -∞ (no coverage yet), KEEP it (extends coverage)

### Step 6: DECISION_MADE

> ✅ KEEP: end=720 > max_end=-∞ — this interval extends our coverage, so we must keep it.

✅ **KEEP** interval (540, 720) — end=720 > max_end=None

### Step 7: MAX_END_UPDATE

> Coverage extended: max_end updated from -∞ → 720 (now we can skip intervals ending ≤ 720)

Coverage extended: **-∞** → **720**

### Step 8: CALL_START

> New recursive call (depth 1): examining interval (540, 660) with 2 remaining

📞 Recursive call at depth **1**
- Processing: interval (540, 660)
- Remaining: 2 intervals

### Step 9: EXAMINING_INTERVAL

> Does interval (540, 660) extend beyond max_end=720? If yes, we KEEP it; if no, it's COVERED.

**Examining interval (540, 660)**
- Current coverage extends to: **720**
- Interval ends at: **660**
- Decision logic: If 660 > 720, KEEP it (extends coverage)

### Step 10: DECISION_MADE

> ❌ COVERED: end=660 ≤ max_end=720 — an earlier interval already covers this range, so we can skip it safely.

❌ **COVERED** interval (540, 660) — end=660 <= max_end=720

### Step 11: CALL_START

> New recursive call (depth 2): examining interval (600, 720) with 1 remaining

📞 Recursive call at depth **2**
- Processing: interval (600, 720)
- Remaining: 1 intervals

### Step 12: EXAMINING_INTERVAL

> Does interval (600, 720) extend beyond max_end=720? If yes, we KEEP it; if no, it's COVERED.

**Examining interval (600, 720)**
- Current coverage extends to: **720**
- Interval ends at: **720**
- Decision logic: If 720 > 720, KEEP it (extends coverage)

### Step 13: DECISION_MADE

> ❌ COVERED: end=720 ≤ max_end=720 — an earlier interval already covers this range, so we can skip it safely.

❌ **COVERED** interval (600, 720) — end=720 <= max_end=720

### Step 14: CALL_START

> New recursive call (depth 3): examining interval (900, 960) with 0 remaining

📞 Recursive call at depth **3**
- Processing: interval (900, 960)
- Remaining: 0 intervals

### Step 15: EXAMINING_INTERVAL

> Does interval (900, 960) extend beyond max_end=720? If yes, we KEEP it; if no, it's COVERED.

**Examining interval (900, 960)**
- Current coverage extends to: **720**
- Interval ends at: **960**
- Decision logic: If 960 > 720, KEEP it (extends coverage)

### Step 16: DECISION_MADE

> ✅ KEEP: end=960 > max_end=720 — this interval extends our coverage, so we must keep it.

✅ **KEEP** interval (900, 960) — end=960 > max_end=720

### Step 17: MAX_END_UPDATE

> Coverage extended: max_end updated from 720 → 960 (now we can skip intervals ending ≤ 960)

Coverage extended: **720** → **960**

### Step 18: BASE_CASE

> Base case: no more intervals to process, return empty result

Base case: No more intervals to process, returning empty list

### Step 19: CALL_RETURN

> ↩️ Returning from call #3: kept 1 interval(s) from this branch

↩️ Returning from depth **3** with **1** intervals kept

### Step 20: CALL_RETURN

> ↩️ Returning from call #2: kept 1 interval(s) from this branch

↩️ Returning from depth **2** with **1** intervals kept

### Step 21: CALL_RETURN

> ↩️ Returning from call #1: kept 1 interval(s) from this branch

↩️ Returning from depth **1** with **1** intervals kept

### Step 22: CALL_RETURN

> ↩️ Returning from call #0: kept 2 interval(s) from this branch

↩️ Returning from depth **0** with **2** intervals kept

### Step 23: ALGORITHM_COMPLETE

> 🎉 Algorithm complete! Kept 2 essential intervals, removed 2 covered intervals.

🎉 Algorithm complete! Kept **2** intervals, removed **2** covered intervals

---

## Summary

**Final Result:** 2 intervals kept

**Kept Intervals:**
- Interval 3: [540, 720]
- Interval 4: [900, 960]
