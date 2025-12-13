"""
Educational Interval Coverage Removal Algorithm
================================================

Problem: Given a list of intervals (start, end), remove any interval that is
completely "covered" by another interval.

An interval A covers interval B if:
- A starts at or before B starts
- A ends at or after B ends

Example: (540, 720) covers (600, 720) because:
- 540 ≤ 600 (starts earlier or same)
- 720 ≥ 720 (ends later or same)

Strategy:
1. Sort intervals by start time (ascending), then by end time (descending)
   - This ensures longer intervals come first when starts are equal
   - Makes it easy to track the "maximum end time seen so far"

2. Use recursion to process intervals one by one:
   - If current interval ends before max_end_so_far → it's covered, skip it
   - Otherwise → keep it and update max_end_so_far

Time Complexity: O(n log n) due to sorting
"""

import argparse
from datetime import datetime
from pathlib import Path


class MarkdownLogger:
    """Captures algorithm output and writes to markdown file."""

    def __init__(self, algorithm_name, output_dir=None):
        self.algorithm_name = algorithm_name
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.buffer = []

    def write(self, text):
        """Capture output text."""
        self.buffer.append(text)

    def save_to_file(self):
        """Save captured output to markdown file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.algorithm_name}_{timestamp}.md"

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create markdown content
        md_content = self._format_as_markdown()

        # Write to file
        output_path = self.output_dir / filename
        output_path.write_text(md_content, encoding="utf-8")

        return str(output_path)

    def _format_as_markdown(self):
        """Format captured output as markdown."""
        full_text = "".join(self.buffer)

        # Build markdown document
        md = [
            f"# {self.algorithm_name}",
            "",
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
            "---",
            "",
            "```",
            full_text,
            "```",
        ]

        return "\n".join(md)


def remove_covered_intervals_educational(intervals, logger=None):
    """
    Remove intervals completely covered by other intervals.

    Args:
        intervals: List of (start, end) tuples
        logger: Optional MarkdownLogger for capturing output

    Returns:
        List of intervals with covered ones removed
    """

    def log(text):
        """Helper to print and optionally log to markdown."""
        print(text, end="")
        if logger:
            logger.write(text)

    log("\n" + "=" * 70 + "\n")
    log("ALGORITHM START: Remove Covered Intervals\n")
    log("=" * 70 + "\n")
    log(f"\n📥 Input intervals: {intervals}\n")

    # STEP 1: Sort the intervals
    log("\n" + "-" * 70 + "\n")
    log("STEP 1: SORT INTERVALS\n")
    log("-" * 70 + "\n")
    log("Sort by: (start ascending, end descending)\n")
    log("Why? Longer intervals with same start come first\n")

    sorted_intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))
    log(f"\n✓ Sorted result: {sorted_intervals}\n")

    # Visual representation
    log("\nVisual timeline:\n")
    for i, (start, end) in enumerate(sorted_intervals, 1):
        bar = " " * (start // 10) + "█" * ((end - start) // 10)
        log(f"  {i}. {start:4d}-{end:4d}: {bar}\n")

    # STEP 2: Filter covered intervals recursively
    log("\n" + "-" * 70 + "\n")
    log("STEP 2: RECURSIVE FILTERING\n")
    log("-" * 70 + "\n")
    log("Track max_end_so_far to detect covered intervals\n\n")

    def filter_covered(remaining, max_end_so_far, depth=0):
        """
        Recursively filter out covered intervals.

        Args:
            remaining: Intervals left to process
            max_end_so_far: Latest ending time we've seen
            depth: Recursion depth (for visualization)

        Returns:
            List of non-covered intervals
        """
        indent = "  " * depth

        # Show what we're processing
        intervals_preview = (
            f"[{len(remaining)} intervals]" if len(remaining) > 3 else str(remaining)
        )
        log(
            f"{indent}📞 CALL: filter_covered({intervals_preview}, "
            f"max_end={max_end_so_far if max_end_so_far != float('-inf') else 'START'})\n"
        )

        # BASE CASE: No more intervals to process
        if not remaining:
            log(f"{indent}   🛑 BASE CASE: Empty list → return []\n")
            return []

        # Process first interval
        current = remaining[0]
        rest = remaining[1:]

        log(f"{indent}   🔍 Examining: {current}\n")
        log(f"{indent}   🎯 Current max_end_so_far: {max_end_so_far}\n")

        # DECISION POINT: Is this interval covered?
        if current[1] <= max_end_so_far:
            # Covered: This interval ends before/at max_end_so_far
            log(f"{indent}   ❌ COVERED: {current[1]} ≤ {max_end_so_far}\n")
            log(f"{indent}      → Skip this interval\n")
            result = filter_covered(rest, max_end_so_far, depth + 1)
        else:
            # Not covered: Keep it and update max_end
            new_max_end = max(max_end_so_far, current[1])
            log(f"{indent}   ✅ NOT COVERED: {current[1]} > {max_end_so_far}\n")
            log(f"{indent}      → Keep this interval\n")
            log(f"{indent}      → Update max_end: {max_end_so_far} → {new_max_end}\n")
            result = [current] + filter_covered(rest, new_max_end, depth + 1)

        log(
            f"{indent}   ⬅️ RETURN: {result if len(result) <= 2 else f'[{len(result)} intervals]'}\n"
        )
        return result

    # Start recursion with -infinity as initial max_end
    final_result = filter_covered(sorted_intervals, float("-inf"))

    # SUMMARY
    log("\n" + "=" * 70 + "\n")
    log("ALGORITHM COMPLETE\n")
    log("=" * 70 + "\n")
    log(f"\n📤 Input:  {intervals}\n")
    log(f"📤 Output: {final_result}\n")
    log(f"\n📊 Removed {len(intervals) - len(final_result)} covered interval(s)\n")
    log("=" * 70 + "\n\n")

    return final_result


# ============================================================================
# TEST CASES
# ============================================================================

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Educational Interval Coverage Algorithm with Markdown Output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python overlapping_intervals.py                    # Save to current directory
  python overlapping_intervals.py ./outputs          # Save to ./outputs/
  python overlapping_intervals.py ~/Documents/logs   # Save to home directory
        """,
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=".",
        help="Directory where markdown file will be saved (default: current directory)",
    )
    args = parser.parse_args()

    # Initialize markdown logger with output directory
    logger = MarkdownLogger("interval_coverage_algorithm", args.output_dir)

    def log(text):
        """Helper to print and log."""
        print(text, end="")
        logger.write(text)

    log("\n" + "█" * 70 + "\n")
    log("EDUCATIONAL TEST: Interval Coverage Algorithm\n")
    log("█" * 70 + "\n")

    # Test Case 1: Original example
    log("\n\n🧪 TEST CASE 1: Mixed overlapping intervals\n")
    bookings = [(540, 660), (600, 720), (540, 720), (900, 960)]
    result = remove_covered_intervals_educational(bookings, logger)

    log("\n💡 KEY INSIGHTS:\n")
    log("   • (540, 720) covers both (540, 660) and (600, 720)\n")
    log("   • (900, 960) doesn't overlap with others → kept\n")
    log("   • Only 2 intervals remain in final result\n")

    # Test Case 2: No coverage
    log("\n\n" + "█" * 70 + "\n\n")
    log("🧪 TEST CASE 2: No intervals are covered\n")
    no_overlap = [(100, 200), (300, 400), (500, 600)]
    result2 = remove_covered_intervals_educational(no_overlap, logger)

    log("\n💡 KEY INSIGHTS:\n")
    log("   • No intervals overlap at all\n")
    log("   • All intervals are kept\n")

    # Test Case 3: Nested intervals
    log("\n\n" + "█" * 70 + "\n\n")
    log("🧪 TEST CASE 3: Fully nested intervals (Russian dolls)\n")
    nested = [(100, 1000), (200, 900), (300, 800), (400, 700)]
    result3 = remove_covered_intervals_educational(nested, logger)

    log("\n💡 KEY INSIGHTS:\n")
    log("   • Largest interval (100, 1000) covers all others\n")
    log("   • All inner intervals are removed\n")
    log("   • Only the outermost interval remains\n")

    # Save to markdown file
    filename = logger.save_to_file()
    print(f"\n✅ Output saved to: {filename}")
