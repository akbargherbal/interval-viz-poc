# Interval Coverage

## Overview

Interval Coverage solves the problem of finding the **minimum set of intervals** needed to cover a target range. It uses a greedy algorithm with recursive call tracking to efficiently select intervals that maximize coverage extension.

## How It Works

1. Sort intervals by start time
2. Track maximum coverage achieved so far (`max_end`)
3. For each position, find interval that extends coverage the most
4. Keep intervals that advance coverage, discard redundant ones
5. Recurse until target range is fully covered

## Time Complexity

- **Sorting:** O(n log n)
- **Greedy Selection:** O(n)
- **Overall:** O(n log n)

## Space Complexity

- **Call Stack:** O(n) worst case (deep recursion)
- **Interval Storage:** O(n)

## Real-World Applications

- **Network Coverage:** Cell tower placement optimization
- **Scheduling:** Minimizing staff shifts for continuous coverage
- **Video Streaming:** Selecting video segments for seamless playback
- **Resource Allocation:** Minimizing time slots for task coverage
- **Military Operations:** Radar/sensor coverage planning

## Key Variables

- **max_end:** Maximum coverage achieved so far
- **target_end:** Goal coverage point (e.g., 1000)
- **kept_intervals:** Intervals selected for coverage
- **examining_interval:** Current candidate being evaluated

## Algorithm Insight

The greedy strategy works because:
1. Intervals are sorted by start time
2. At each step, choosing the interval that extends coverage the most is provably optimal
3. No backtracking needed - local optimum = global optimum

## Challenge

Try to predict: Will the algorithm keep an interval or discard it as redundant? Look for intervals that don't extend `max_end` beyond what's already covered!
