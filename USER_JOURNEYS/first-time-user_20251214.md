# Journey: Understanding Interval Coverage Algorithm (First-Time User)

**Who**: A student or self-learner new to algorithm visualizations
**Goal**: To understand how the Interval Coverage algorithm works step-by-step.
**Starting Point**: The application's landing page, with "Interval Coverage" pre-selected and visualization at "Step 1 of 23".

---

## The Journey

### Step 1: Initial Landing and First Impressions

**What happens**: The user lands on a page displaying "Interval Coverage" as the active algorithm, with "Step 1 of 23" shown. The interface is divided into a control bar (Next/Previous, Predict, Reset), a main "Timeline Visualization" area, and a "Recursive Call Stack" for narrative explanations. The title "Interval Coverage" in the header area appears to be a label, not an interactive element.

**User's likely thought**: "Okay, I'm here. It seems to be showing something about intervals. What do I do first? 'Next Step' seems like the obvious choice to begin."

**What works well**:

- Clear "Next Step" button as a primary call to action.
- The layout is clean and divided into logical sections.

**What could be better**:

- The "Interval Coverage" text acting as a switcher isn't immediately identifiable as clickable.

### Step 2: Beginning the Visualization

**What happens**: The user clicks the "Next Step" button. The visualization advances to "Step 2 of 23." The "Previous" button becomes active. The "Recursive Call Stack" section updates to describe the initial sorting process: "Sorting intervals..." and "Sorting intervals by start time (ascending) breaks ties by preferring longer intervals."

**User's likely thought**: "Alright, it's starting to explain things. The 'Previous' button is active now, which is good if I want to go back."

**What works well**:

- Clear visual progression ("Step 2 of 23").
- Narrative in the Call Stack clearly explains the algorithm's current action.

### Step 3: Preparing for Recursion

**What happens**: The user clicks "Next Step," advancing to "Step 3 of 23." The "Recursive Call Stack" now states, "Ready to start recursion" and introduces the greedy strategy: "✓ Sorted! Now we can use a greedy strategy: process intervals left-to-right, keeping only those that extend our coverage."

**User's likely thought**: "Okay, sorting is done. Now for the main logic – a greedy approach. This explanation is helpful."

**What works well**:

- Introduces the core strategy before diving into the details.

### Step 4: First Recursive Call and Prediction

**What happens**: The user clicks "Next Step" twice, reaching "Step 5 of 23." A "TEST" section appears, asking the user to predict if interval (540, 720) will be kept or covered, with a hint to compare `interval.end` with `max_end` (which is -∞). The user clicks "Keep this interval," then "Submit."

**User's likely thought**: "Aha! An interactive part. Since `max_end` is negative infinity, this first interval must definitely be kept. This is a good way to check my understanding."

**What works well**:

- The "TEST" section immediately engages the user in active learning.
- Clear hint helps guide the user's decision.
- The options for prediction are straightforward.

**What could be better**:

- No specific "Aha!" moment on initial discovery, more of a guided interaction.

### Step 5: Correct Prediction Feedback and Coverage Update

**What happens**: Upon submitting the correct prediction, the UI confirms "Correct! Interval (540, 720) was keep." The message "Advancing to next step..." appears, and the visualization automatically progresses to "Step 7 of 23." The "Recursive Call Stack" narrative confirms "Coverage extended: max_end updated from -∞ → 720 (now we can skip intervals ending ≤ 720)." The "Timeline Visualization" updates to reflect `max_end: 720`.

**User's likely thought**: "Great, I got it right! The immediate feedback is really satisfying. Now I see how `max_end` is changing based on my decision."

**What works well**:

- Immediate, positive feedback reinforces correct learning.
- Clear explanation of the impact of the decision on `max_end`.

### Step 6: Nested Recursive Call and Second Prediction

**What happens**: The user clicks "Next Step," reaching "Step 8 of 23," where a new recursive call "CALL #1" for interval (540, 660) with `max_end_so_far: 720` is initiated. At "Step 9 of 23," another "TEST" section prompts for a prediction. The user clicks "Covered by previous," then "Submit."

**User's likely thought**: "Okay, now we're looking at a new interval. Its end (660) is less than the current `max_end` (720), so it should be covered. This makes sense for efficiency."

**What works well**:

- Reinforces the `max_end` logic with a new scenario.

### Step 7: Second Correct Prediction and Further Progression

**What happens**: The UI confirms "Correct! Interval (540, 660) is covered by a previous interval." and shows "Advancing to next step..." The user continues clicking "Next Step," eventually leading to "Step 14 of 23," where "CALL #3" for interval (900, 960) is initiated, with `max_end_so_far: 720`. At "Step 15 of 23," a third prediction is requested. The user clicks "Keep this interval," then "Submit."

**User's likely thought**: "Another new interval. This one (960) extends beyond the current `max_end` (720), so it should be kept. I'm getting the hang of this."

**What works well**:

- Consistent interactive learning reinforces the algorithm's decision-making process.

### Step 8: Algorithm Completion and Summary

**What happens**: The algorithm continues through the remaining steps, unwinding the recursive calls ("Returning from call #3," "Returning from call #2," "Returning from call #1," "Returning from call #0"). Finally, at "Step 23 of 23," the "Next Step" button is disabled, and a "CompletionModal" appears. This modal summarizes the process: "Initial: 4," "Kept: 2," "Removed: 2," and lists the "Final Result: (540, 720), (900, 960)." Crucially, it also displays "Prediction Accuracy: Excellent work! 100% (4/4)" along with "Close" and "Start Over" buttons.

**User's likely thought**: "Wow, it's done! I got all the predictions right, that feels good. The summary is really clear, showing what was kept and why."

**What works well**:

- Clear indication of algorithm completion.
- Comprehensive summary of the results.
- The "Prediction Accuracy" feedback is a highly motivating and validating "Aha!" moment.
- "Start Over" button offers an immediate path to re-engage.

---

## Journey Summary

**Overall Experience**: The first-time user experience is very positive, combining clear step-by-step visualization with effective interactive prediction moments. The narrative explanations in the "Recursive Call Stack" are easy to follow, and the immediate feedback on predictions significantly aids learning. The final completion summary provides a satisfying conclusion and validates the user's understanding.

**Time to Complete**: Approximately 5-7 minutes (for one full algorithm run with predictions)

**Difficulty Level**: Easy to Moderate

**Key Insights**:

1.  **Interactive Learning is Highly Effective**: The prediction mode is a standout feature, transforming passive observation into active engagement. The immediate "Correct!" feedback is critical for reinforcing learning.
2.  **Clear Narrative is Essential**: The "Recursive Call Stack" provides excellent, jargon-free explanations of each step, which is vital for understanding complex algorithmic logic.
3.  **Satisfying Conclusion**: The "CompletionModal" with the summary and prediction accuracy offers a strong sense of accomplishment and validates the user's effort.
4.  **Visual Cues Aid Comprehension**: The dynamic updates to the "Timeline Visualization" (e.g., `max_end` line) help users visually track the algorithm's state.

**Recommendations**:

-   **Improve Algorithm Switcher Discoverability**: The current "Interval Coverage" text in the header, while clickable, lacks visual affordance. Adding a subtle arrow icon, a hover effect, or renaming it to something like "Change Algorithm" would make its functionality more obvious.
-   **Highlight Interactive Elements Early**: While the prediction mode appears naturally, a brief initial tooltip or a very short, optional "welcome tour" could proactively inform first-time users about the interactive features (like prediction mode and keyboard shortcuts) to maximize engagement from the outset.
-   **Provide "Incorrect" Feedback Guidance**: While not encountered in this journey, ensuring that "incorrect" predictions come with clear, concise explanations of *why* the prediction was wrong (and perhaps a suggestion to review previous steps) would further enhance the learning experience.

---

## Emotional Journey Map

😊 Confident (Initial Clarity of "Next Step") → 💡 Curious (First Prediction) → ✅ Satisfied (Correct Prediction) → 🤔 Engaged (Second Prediction) → 😄 Delighted (100% Accuracy at Completion)
↓
"Initially wondered what the clickable elements were, but quickly found the main flow."
