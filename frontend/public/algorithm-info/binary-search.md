# Binary Search

## Overview

Binary Search is an efficient algorithm for finding a target value within a **sorted array**. It works by repeatedly dividing the search interval in half, eliminating half of the remaining elements in each step.

## How It Works

1. Start with the entire sorted array
2. Compare the target with the middle element
3. If target equals middle: **Found!**
4. If target < middle: Search the **left half**
5. If target > middle: Search the **right half**
6. Repeat until target is found or search space is empty

## Time Complexity

- **Best Case:** O(1) - Target is the middle element
- **Average Case:** O(log n) - Halves search space each step
- **Worst Case:** O(log n) - Target at end or not present

## Space Complexity

- **Iterative:** O(1) - Only stores pointers
- **Recursive:** O(log n) - Call stack depth

## Real-World Applications

- **Databases:** Index lookups for fast queries
- **File Systems:** Locating files in sorted directories
- **Search Engines:** Ranking and retrieval systems
- **Game Development:** Collision detection in sorted objects
- **Libraries:** Dictionary lookups, phone books

## Key Variables

- **L (Left):** Starting boundary of current search range
- **R (Right):** Ending boundary of current search range  
- **M (Mid):** Central element being compared to target
- **Target:** The specific value being searched for

## Prerequisites

⚠️ **Critical Requirement:** The input array **must be sorted** in ascending order. Binary Search does not work on unsorted data.

## Fun Fact

Binary Search is so efficient that searching a sorted array of 1 billion elements takes only ~30 comparisons! That's the power of O(log n).
