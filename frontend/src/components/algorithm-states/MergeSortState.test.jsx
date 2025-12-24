import React from "react";
import { render, screen } from "@testing-library/react";
import MergeSortState from "./MergeSortState";

// Mock data based on actual trace payload
const mockStepData = {
  data: {
    visualization: {
      call_stack_state: [
        {
          id: "call_0",
          depth: 0,
          array: [6, 5, 3, 1],
          operation: "split",
          is_active: false,
        },
        {
          id: "call_1",
          depth: 1,
          array: [6, 5],
          operation: "merge",
          is_active: true,
        },
      ],
      comparison_count: 5,
      merge_count: 2,
    },
    // Comparison data at root level
    left_value: 6,
    right_value: 5,
    chose: "right",
  },
};

describe("MergeSortState Component", () => {
  test("renders without crashing", () => {
    render(<MergeSortState step={mockStepData} />);
    expect(screen.getByText("Comparisons")).toBeInTheDocument();
    expect(screen.getByText("Merges")).toBeInTheDocument();
  });

  test("displays metrics correctly", () => {
    render(<MergeSortState step={mockStepData} />);
    // Use getAllByText because '5' appears in metrics and comparison box
    const fives = screen.getAllByText("5");
    expect(fives.length).toBeGreaterThan(0);

    // Verify one of them is in the metrics section (checking parent class or context)
    const metricsFive = fives.find((el) => el.className.includes("text-2xl"));
    expect(metricsFive).toBeInTheDocument();

    expect(screen.getByText("2")).toBeInTheDocument(); // merge_count
  });

  test("renders call stack frames", () => {
    render(<MergeSortState step={mockStepData} />);
    expect(screen.getByText("Size: 4")).toBeInTheDocument();
    expect(screen.getByText("Size: 2")).toBeInTheDocument();
    expect(screen.getByText("[6, 5, 3, 1]")).toBeInTheDocument();
  });

  test("highlights active frame", () => {
    render(<MergeSortState step={mockStepData} />);
    // Find all elements with "merge" (case insensitive)
    const mergeElements = screen.getAllByText(/merge/i);

    // Filter for the one that is likely the badge (has border class or is inside relative container)
    const activeBadge = mergeElements.find(
      (el) => el.tagName === "SPAN" && el.className.includes("rounded"),
    );

    expect(activeBadge).toBeInTheDocument();
    const activeFrame = activeBadge.closest(".relative");
    expect(activeFrame).toHaveClass("border-amber-500/50");
  });

  test("shows comparison box when active and data exists", () => {
    render(<MergeSortState step={mockStepData} />);
    expect(screen.getByText("Comparing")).toBeInTheDocument();
    expect(screen.getByText("Left")).toBeInTheDocument();
    expect(screen.getByText("Right")).toBeInTheDocument();

    // Check values in comparison box specifically
    const comparisonValues = screen.getAllByText("5");
    const comparisonFive = comparisonValues.find((el) =>
      el.className.includes("w-8 h-8"),
    );
    expect(comparisonFive).toBeInTheDocument();

    expect(screen.getByText("6")).toBeInTheDocument();
  });

  test("handles missing visualization data gracefully", () => {
    const emptyStep = { data: {} };
    render(<MergeSortState step={emptyStep} />);
    expect(screen.getByText("No state data available")).toBeInTheDocument();
  });

  test("does not show comparison box if data is missing", () => {
    const noComparisonStep = {
      data: {
        visualization: {
          call_stack_state: [
            {
              id: "1",
              depth: 0,
              array: [],
              operation: "split",
              is_active: true,
            },
          ],
        },
        // Missing left_value/right_value
      },
    };
    render(<MergeSortState step={noComparisonStep} />);
    expect(screen.queryByText("Comparing")).not.toBeInTheDocument();
  });
});
