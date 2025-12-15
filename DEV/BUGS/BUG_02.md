---

**Sliding Window Algorithm**

**ISSUE 1:**
[Panel Steps] should auto-scroll on each step, similar to the interval coverage algorithm. See the static mockup for details.

**ISSUE 2:**
Prediction Modal: button colors should vary. Currently, all buttons are blue. See the static mockup.

---

**Two Pointer Algorithm**

**ISSUE 3:**
Prediction Modal: button colors should vary. Currently, all buttons are green. See the static mockup.

**ISSUE 4:**
Prediction Modal: there is a conflict with the keyboard shortcut **[S]**, which is used both for skipping and as part of the algorithm operations. This should be reconsidered and replaced with a shortcut that is clear and sensible.

---

**Algorithm Details Modal**

**ISSUE 5: Redundant closing methods**

I) **X** in the top-right corner (should remain)
II) Close button (remove)
III) Text saying “Press [Esc] to close” (remove the text)

The **Esc** key should still close the modal; only the explanatory text should be removed.

**ISSUE 6:**
Inline code in the Algorithm Details Modal breaks onto separate lines instead of remaining inline with surrounding text.

For example, the following should appear on a single line:
One pointer starts at the beginning (`left`), the other at the end (`right`).

Currently, it is rendered incorrectly as:

```
One pointer starts at the beginning (
left
), the other at the end (
```
