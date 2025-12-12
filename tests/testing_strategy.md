# Testing Strategy - Core Features

This document outlines the priority tests for critical functionalities of the Algorithm Visualization Platform.

## 1. End-to-End Prediction Mode Validation

### Objective
Ensure the interactive prediction mode functions flawlessly across all algorithms, delivering a consistent and accurate active learning experience.

### Why this is critical
The prediction mode is a core active learning feature and crucial for the platform's pedagogical impact. It needs to work seamlessly for both existing algorithms to ensure users can effectively engage.

### How to Test
1.  **Select Algorithm:** Choose an algorithm (e.g., Binary Search or Interval Coverage) from the dropdown.
2.  **Enable Prediction Mode:** Click the "⏳ Predict" button to activate prediction mode.
3.  **Navigate to Prediction Point:** Step through the algorithm execution until a prediction modal appears.
4.  **Verify Modal Content:**
    *   Confirm the modal has the exact ID `#prediction-modal`.
    *   Verify a clear question about the next decision is presented.
    *   Ensure 2-3 choice buttons are visible.
    *   Check for a "Skip" button.
5.  **Test Predictions:**
    *   Make a correct prediction (click the correct choice or press 'K'/'C'). Verify immediate positive feedback and explanation.
    *   Make an incorrect prediction (click an incorrect choice). Verify immediate negative feedback and explanation.
    *   Use the 'S' key to skip a prediction.
6.  **Check Accuracy Tracking:**
    *   Observe the accuracy percentage update in the header after each prediction.
7.  **Complete Trace:** Finish the algorithm execution.
8.  **Verify Completion Modal:**
    *   Confirm the modal has the exact ID `#completion-modal`.
    *   Verify the final accuracy statistics match expectations.
    *   Press 'Esc' to close the modal.
9.  **Repeat:** Perform these steps for both Binary Search and Interval Coverage.

## 2. Cross-Algorithm Compatibility & Regression

### Objective
Validate that the registry-based architecture correctly handles algorithm switching, ensuring that selecting one algorithm does not negatively impact the functionality or display of others.

### Why this is critical
The "registry-based architecture" is designed for extensibility. This test verifies that adding new algorithms doesn't break existing ones and that the switching mechanism works as intended. This is a critical regression prevention check.

### How to Test
1.  **Initial Load:** Load the frontend (`http://localhost:3000`) and ensure it loads without errors.
2.  **Algorithm Discovery:** Verify that the algorithm selector dropdown (top-left) correctly lists "Binary Search" and "Interval Coverage".
3.  **Select Binary Search:**
    *   Choose "Binary Search" from the dropdown.
    *   Select an example input.
    *   Verify `ArrayView` renders correctly, showing array elements, pointers, and the target.
    *   Navigate a few steps using `→` or `Space` and observe the visualization updates.
4.  **Switch to Interval Coverage:**
    *   Choose "Interval Coverage" from the dropdown.
    *   Verify `TimelineView` renders correctly with intervals and the call stack.
    *   Select an example input.
    *   Navigate a few steps and observe the visualization updates and highlight effects.
5.  **Switch back to Binary Search:**
    *   Choose "Binary Search" again.
    *   Select a different example input.
    *   Verify `ArrayView` re-renders correctly for the new input.
    *   Navigate steps.
6.  **Repeated Switching:** Perform multiple switches between the algorithms, ensuring consistent behavior and correct rendering each time.
7.  **API Verification:** Optionally, use `curl http://localhost:5000/api/algorithms | jq` to confirm both algorithms are correctly registered and discoverable by the backend.

## 3. Backend API Contract Validation (Unified Trace Endpoint & Metadata)

### Objective
Ensure the `/api/trace/unified` endpoint consistently returns trace data and metadata that adheres strictly to the defined API contract for all registered algorithms.

### Why this is critical
The backend is designed to do "ALL the thinking," and the trace structure is a LOCKED requirement for frontend functionality. Ensuring the `/api/trace/unified` endpoint returns correctly structured data, especially the metadata (algorithm, display_name, visualization_type), is vital.

### How to Test
1.  **Start Backend:** Ensure the backend is running on `http://localhost:5000`.
2.  **Test Binary Search Trace:**
    *   Execute the following `curl` command:
        ```bash
        curl -X POST http://localhost:5000/api/trace/unified \
          -H "Content-Type: application/json" \
          -d 
            "{
              "algorithm": "binary-search",
              "input": {
                "array": [1, 3, 5, 7, 9],
                "target": 5
              }
            }" | jq
        ```
    *   **Validate Response:**
        *   Confirm HTTP status code is 200.
        *   Verify the top-level keys: `result`, `trace`, `metadata` exist.
        *   **`metadata` validation:**
            *   `algorithm`: Must be `"binary-search"`.
            *   `display_name`: Must be `"Binary Search"`.
            *   `visualization_type`: Must be `"array"`.
            *   Ensure other expected metadata fields (`input_size`, `target_value`, `prediction_points` if applicable) are present and correctly formatted.
        *   **`trace` validation:**
            *   `steps`: Must be a non-empty array of objects.
            *   Each step object contains: `step`, `type`, `timestamp`, `data`, `description`.
            *   `data.visualization`: Should contain `array` and `pointers` specific to array visualization.
        *   **`result` validation:** Contains `found`, `index`, `comparisons` for Binary Search.
3.  **Test Interval Coverage Trace:**
    *   Execute the following `curl` command:
        ```bash
        curl -X POST http://localhost:5000/api/trace/unified \
          -H "Content-Type: application/json" \
          -d 
            "{
              "algorithm": "interval-coverage",
              "input": {
                "intervals": [
                  {"id": 1, "start": 540, "end": 660, "color": "blue"},
                  {"id": 2, "start": 600, "end": 720, "color": "green"}
                ]
              }
            }" | jq
        ```
    *   **Validate Response:**
        *   Confirm HTTP status code is 200.
        *   Verify the top-level keys: `result`, `trace`, `metadata` exist.
        *   **`metadata` validation:**
            *   `algorithm`: Must be `"interval-coverage"`.
            *   `display_name`: Must be `"Interval Coverage"`.
            *   `visualization_type`: Must be `"timeline"`.
        *   **`trace` validation:**
            *   `steps`: Must be a non-empty array of objects.
            *   `data.visualization`: Should contain `intervals` and `max_end` specific to timeline visualization.
4.  **Test Error Handling for Unknown Algorithm:**
    *   Execute the following `curl` command:
        ```bash
        curl -X POST http://localhost:5000/api/trace/unified \
          -H "Content-Type: application/json" \
          -d 
            "{
              "algorithm": "unknown-algorithm",
              "input": {}
            }" | jq
        ```
    *   **Validate Error Response:**
        *   Confirm HTTP status code is 400.
        *   Verify an `error` message indicating an unknown algorithm.
        *   Verify `available_algorithms` lists the currently registered algorithms (`binary-search`, `interval-coverage`).
