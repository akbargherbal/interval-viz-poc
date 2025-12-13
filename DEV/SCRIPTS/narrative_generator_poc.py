#!/usr/bin/env python3
"""
Narrative Generator - Micro-Phase 0 Proof of Concept

This minimal script generates a human-readable narrative from trace JSON.
If the narrative has gaps or unclear references, the JSON is incomplete.

Philosophy: "If you can't narrate it coherently, the frontend can't render it."

Usage:
    python narrative_generator_poc.py <trace.json>
    
    Or import and use programmatically:
    from narrative_generator_poc import generate_narrative
    narrative = generate_narrative(trace_data)
"""

import json
import sys
from pathlib import Path


class NarrativeGenerationError(Exception):
    """Raised when narrative cannot be generated due to missing data."""
    pass


def generate_narrative(trace_data: dict) -> str:
    """
    Generate human-readable narrative from trace JSON.
    
    This function intentionally fails loudly when required data is missing,
    exposing backend incompleteness before frontend integration.
    
    Args:
        trace_data: Complete trace result from backend (result + trace + metadata)
    
    Returns:
        Markdown-formatted narrative string
        
    Raises:
        NarrativeGenerationError: If required visualization state is missing
    """
    lines = []
    
    # Header
    algorithm = trace_data['metadata']['display_name']
    viz_type = trace_data['metadata'].get('visualization_type', 'unknown')
    lines.append(f"# {algorithm} - Execution Narrative\n")
    
    # Input summary (handle different algorithm types)
    input_size = trace_data['metadata']['input_size']
    output_size = trace_data['metadata'].get('output_size', '?')
    
    if viz_type == 'timeline':
        lines.append(f"**Input:** {input_size} intervals")
        lines.append(f"**Output:** {output_size} intervals kept")
    elif viz_type == 'array':
        lines.append(f"**Input:** Array of {input_size} elements")
        result = trace_data.get('result', {})
        if isinstance(result, dict) and 'found' in result:
            lines.append(f"**Result:** {'Found' if result['found'] else 'Not found'} (index: {result.get('index', 'N/A')})")
        else:
            lines.append(f"**Result:** See summary below")
    
    lines.append(f"**Total Steps:** {trace_data['trace']['total_steps']}")
    lines.append(f"**Duration:** {trace_data['trace']['duration']:.4f}s\n")
    
    lines.append("---\n")
    lines.append("## Step-by-Step Execution\n")
    
    # Process each step
    steps = trace_data['trace']['steps']
    
    for i, step in enumerate(steps):
        step_num = step['step']
        step_type = step['type']
        description = step['description']
        data = step['data']
        
        lines.append(f"### Step {step_num + 1}: {step_type}\n")
        lines.append(f"> {description}\n")
        
        # Generate step-specific narrative
        try:
            step_narrative = _generate_step_narrative(step_type, data, step_num, viz_type)
            if step_narrative:
                lines.append(step_narrative)
        except KeyError as e:
            # THIS IS THE KEY: Fail loudly when data is missing
            raise NarrativeGenerationError(
                f"❌ NARRATIVE GENERATION FAILED at step {step_num}\n"
                f"Step type: {step_type}\n"
                f"Missing required field: {e}\n"
                f"This means the backend JSON is incomplete for visualization.\n"
                f"The frontend would also fail to render this step properly."
            )
        
        lines.append("")  # Blank line between steps
    
    # Summary
    lines.append("---\n")
    lines.append("## Summary\n")
    result = trace_data['result']
    
    if viz_type == 'timeline' and isinstance(result, list):
        lines.append(f"**Final Result:** {len(result)} intervals kept\n")
        if result:
            lines.append("**Kept Intervals:**")
            for interval in result:
                lines.append(f"- Interval {interval['id']}: [{interval['start']}, {interval['end']}]")
    elif viz_type == 'array' and isinstance(result, dict):
        if result.get('found'):
            lines.append(f"**Target Found:** Yes, at index {result['index']}")
        else:
            lines.append(f"**Target Found:** No")
        lines.append(f"**Comparisons:** {result.get('comparisons', '?')}")
    
    return "\n".join(lines)


def _generate_step_narrative(step_type: str, data: dict, step_num: int, viz_type: str) -> str:
    """
    Generate narrative for a specific step type.
    
    This function is intentionally strict: it accesses fields that SHOULD
    be present according to the platform's "complete state" philosophy.
    If a field is missing, it raises KeyError, which bubbles up as
    NarrativeGenerationError.
    """
    
    # === INTERVAL COVERAGE (TIMELINE) STEPS ===
    
    if step_type == "INITIAL_STATE" and viz_type == 'timeline':
        count = data['count']
        return f"Starting with **{count} intervals** (unsorted)."
    
    elif step_type == "INITIAL_STATE" and viz_type == 'array':
        array_size = data.get('array_size', data.get('count', '?'))
        target = data.get('target', '?')
        return f"Starting binary search for target **{target}** in array of **{array_size}** elements."
    
    elif step_type == "SORT_BEGIN":
        return "Sorting intervals by start time (ascending), with ties broken by preferring longer intervals."
    
    elif step_type == "SORT_COMPLETE":
        intervals = data['intervals']
        sorted_display = ", ".join(
            f"[{i['start']}-{i['end']}]" for i in intervals[:5]
        )
        more = f" and {len(intervals) - 5} more" if len(intervals) > 5 else ""
        return f"Sorted order: {sorted_display}{more}"
    
    elif step_type == "EXAMINING_INTERVAL":
        interval = data['interval']
        
        # 🔥 CRITICAL CHECK: This is where the bug will surface
        # We need max_end from visualization to explain the decision context
        viz = data['visualization']
        
        # Try to access max_end - THIS WILL FAIL if it's missing
        max_end = viz['max_end']  # KeyError if missing!
        
        max_end_display = f"{max_end}" if max_end is not None else "-∞ (no coverage yet)"
        
        return (
            f"**Examining interval ({interval['start']}, {interval['end']})**\n"
            f"- Current coverage extends to: **{max_end_display}**\n"
            f"- Interval ends at: **{interval['end']}**\n"
            f"- Decision logic: If {interval['end']} > {max_end_display}, KEEP it (extends coverage)"
        )
    
    elif step_type == "DECISION_MADE":
        interval = data['interval']
        decision = data['decision']
        reason = data.get('reason', 'N/A')
        
        if decision == 'keep':
            return f"✅ **KEEP** interval ({interval['start']}, {interval['end']}) — {reason}"
        else:
            return f"❌ **COVERED** interval ({interval['start']}, {interval['end']}) — {reason}"
    
    elif step_type == "MAX_END_UPDATE":
        old_max = data['old_max_end']
        new_max = data['new_max_end']
        old_display = f"{old_max}" if old_max is not None else "-∞"
        
        return f"Coverage extended: **{old_display}** → **{new_max}**"
    
    elif step_type == "CALL_START":
        depth = data['depth']
        examining = data['examining']
        remaining = data['remaining_count']
        
        return (
            f"📞 Recursive call at depth **{depth}**\n"
            f"- Processing: interval ({examining['start']}, {examining['end']})\n"
            f"- Remaining: {remaining} intervals"
        )
    
    elif step_type == "CALL_RETURN":
        depth = data['depth']
        kept_count = data['kept_count']
        
        return f"↩️ Returning from depth **{depth}** with **{kept_count}** intervals kept"
    
    elif step_type == "BASE_CASE":
        return "Base case: No more intervals to process, returning empty list"
    
    elif step_type == "ALGORITHM_COMPLETE":
        kept = data.get('kept_count', '?')
        removed = data.get('removed_count', '?')
        return f"🎉 Algorithm complete! Kept **{kept}** intervals, removed **{removed}** covered intervals"
    
    # === BINARY SEARCH (ARRAY) STEPS ===
    
    elif step_type == "CALCULATE_MID":
        mid_index = data['mid_index']
        mid_value = data['mid_value']
        calculation = data.get('calculation', f"mid = {mid_index}")
        
        return f"📍 Calculated middle index: **{mid_index}** (value: **{mid_value}**)\n- Calculation: `{calculation}`"
    
    elif step_type == "TARGET_FOUND":
        index = data['index']
        value = data['value']
        comparisons = data.get('comparisons', '?')
        
        return f"✅ **Target found!** At index **{index}** (value: **{value}**) after **{comparisons}** comparisons"
    
    elif step_type == "SEARCH_LEFT":
        comparison = data.get('comparison', '?')
        eliminated = data.get('eliminated_elements', '?')
        
        return f"⬅️ Search left half\n- Comparison: {comparison}\n- Eliminated: **{eliminated}** elements"
    
    elif step_type == "SEARCH_RIGHT":
        comparison = data.get('comparison', '?')
        eliminated = data.get('eliminated_elements', '?')
        
        return f"➡️ Search right half\n- Comparison: {comparison}\n- Eliminated: **{eliminated}** elements"
    
    elif step_type == "TARGET_NOT_FOUND":
        comparisons = data.get('comparisons', '?')
        
        return f"❌ Target not found after **{comparisons}** comparisons (search space exhausted)"
    
    # For unknown step types, return minimal narrative
    return f"_(Step type: {step_type})_"


def main():
    """CLI entry point for testing."""
    if len(sys.argv) < 2:
        print("Usage: python narrative_generator_poc.py <trace.json>")
        print("\nGenerates a human-readable narrative from trace JSON.")
        print("Fails loudly if required visualization state is missing.")
        sys.exit(1)
    
    trace_file = Path(sys.argv[1])
    
    if not trace_file.exists():
        print(f"Error: File not found: {trace_file}")
        sys.exit(1)
    
    # Load trace JSON
    with open(trace_file) as f:
        trace_data = json.load(f)
    
    # Generate narrative
    try:
        narrative = generate_narrative(trace_data)
        print(narrative)
    except NarrativeGenerationError as e:
        print("\n" + "=" * 70)
        print("NARRATIVE GENERATION FAILED")
        print("=" * 70)
        print(str(e))
        print("\n💡 FIX: Add missing field to backend's _get_visualization_state()")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
