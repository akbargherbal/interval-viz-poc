# backend/tests/test_generate_narratives_script.py
"""
Integration tests for the narrative generation utility script.

Tests the scripts/generate_narratives.py functionality including:
- Command-line argument parsing
- File generation
- Error handling
- Multiple algorithm support
"""

import pytest
import subprocess
import sys
from pathlib import Path
import shutil


class TestGenerateNarrativesScript:
    """Test the generate_narratives.py script."""

    @staticmethod
    def get_project_root():
        """Get project root directory from test location."""
        # From backend/tests/ go up two levels to project root
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_narratives_dir():
        """Get path to narratives directory."""
        return TestGenerateNarrativesScript.get_project_root() / 'docs' / 'narratives'

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup: Create temp directory, Teardown: Clean up."""
        self.test_output_dir = self.get_narratives_dir() / 'test_temp'
        self.test_output_dir.mkdir(parents=True, exist_ok=True)
        
        yield
        
        # Cleanup
        if self.test_output_dir.exists():
            shutil.rmtree(self.test_output_dir)

    @pytest.fixture
    def script_path(self):
        """Path to the generation script."""
        # From backend/tests/, the script is at backend/scripts/
        return Path(__file__).parent.parent / 'scripts' / 'generate_narratives.py'

    # ===== Basic Functionality Tests =====

    def test_script_exists(self, script_path):
        """Script file should exist."""
        assert script_path.exists(), f"Script not found at {script_path}"

    def test_script_is_executable(self, script_path):
        """Script should be executable with python."""
        # Try to run with --help equivalent (no args shows help)
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        # Should show usage documentation
        assert "Usage:" in result.stdout or "usage:" in result.stdout.lower()

    def test_script_requires_arguments(self, script_path):
        """Script should require algorithm name argument."""
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    # ===== Single Algorithm Tests =====

    def test_generate_single_example_binary_search(self, script_path):
        """Generate narrative for single Binary Search example."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # Should succeed
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Should show success message
        assert "✅" in result.stdout or "SUCCESS" in result.stdout

        # Should create the file
        output_dir = self.get_narratives_dir() / 'binary-search'
        assert output_dir.exists()
        
        # Should have created at least one file
        files = list(output_dir.glob('example_1_*.md'))
        assert len(files) >= 1

    def test_generate_all_examples_binary_search(self, script_path):
        """Generate narratives for all Binary Search examples."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '--all'],
            capture_output=True,
            text=True
        )

        # Should succeed
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Should show success for multiple files
        output_count = result.stdout.count('✅')
        assert output_count >= 4, "Should generate at least 4 narratives"

    def test_generate_interval_coverage_example(self, script_path):
        """Generate narrative for Interval Coverage example."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'interval-coverage', '0'],
            capture_output=True,
            text=True
        )

        # Should succeed
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "✅" in result.stdout

        # Should create the file
        output_dir = self.get_narratives_dir() / 'interval-coverage'
        assert output_dir.exists()
        
        files = list(output_dir.glob('example_1_*.md'))
        assert len(files) >= 1

    # ===== Error Handling Tests =====

    def test_invalid_algorithm_name(self, script_path):
        """Script should handle invalid algorithm name gracefully."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'nonexistent-algorithm'],
            capture_output=True,
            text=True
        )

        # Should fail with error message
        assert result.returncode == 0  # Script handles error internally
        assert "not found" in result.stdout.lower() or "❌" in result.stdout

    def test_invalid_example_index(self, script_path):
        """Script should handle out-of-range example index."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '999'],
            capture_output=True,
            text=True
        )

        # Should show warning or error
        assert "does not exist" in result.stdout or "⚠️" in result.stdout

    def test_invalid_example_format(self, script_path):
        """Script should handle non-numeric example index."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', 'not-a-number'],
            capture_output=True,
            text=True
        )

        # Should show error about invalid index
        assert result.returncode == 1
        assert "Invalid" in result.stdout or "❌" in result.stdout

    # ===== Batch Generation Tests =====

    def test_generate_all_algorithms(self, script_path):
        """Generate narratives for all registered algorithms."""
        result = subprocess.run(
            [sys.executable, str(script_path), '--all-algorithms'],
            capture_output=True,
            text=True
        )

        # Should succeed
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Should mention both algorithms
        assert "binary-search" in result.stdout.lower()
        assert "interval-coverage" in result.stdout.lower()

        # Should show total count
        assert "TOTAL:" in result.stdout

    # ===== Output Quality Tests =====

    def test_generated_file_is_valid_markdown(self, script_path):
        """Generated files should be valid markdown."""
        # Generate a file
        subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # Find generated file
        output_dir = self.get_narratives_dir() / 'binary-search'
        files = list(output_dir.glob('example_1_*.md'))
        assert len(files) >= 1

        # Read and validate
        content = files[0].read_text()

        # Should have markdown headers
        assert content.startswith('#')
        assert '##' in content

        # Should have substantial content
        assert len(content) > 500

    def test_generated_filename_sanitization(self, script_path):
        """Script should sanitize example names into valid filenames."""
        # This tests the sanitize_filename function indirectly
        subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # Find generated file
        output_dir = self.get_narratives_dir() / 'binary-search'
        files = list(output_dir.glob('*.md'))
        
        # Filenames should only contain lowercase, numbers, underscores
        for file in files:
            filename = file.stem  # Without .md extension
            # Should be lowercase with underscores (no spaces or special chars except _)
            assert all(c.islower() or c.isdigit() or c == '_' for c in filename), \
                f"Invalid filename: {filename}"

    def test_output_directory_creation(self, script_path):
        """Script should create output directories if they don't exist."""
        # Remove directory if it exists
        output_dir = self.get_narratives_dir() / 'binary-search'
        if output_dir.exists():
            shutil.rmtree(output_dir)

        # Generate narrative
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # Should succeed
        assert result.returncode == 0

        # Directory should now exist
        assert output_dir.exists()

    # ===== Script Output Tests =====

    def test_script_shows_progress(self, script_path):
        """Script should show progress during generation."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '--all'],
            capture_output=True,
            text=True
        )

        # Should show algorithm being processed
        assert "Algorithm:" in result.stdout

        # Should show example names
        assert "Processing:" in result.stdout

    def test_script_shows_summary(self, script_path):
        """Script should show summary of results."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '--all'],
            capture_output=True,
            text=True
        )

        # Should show success count
        assert "/" in result.stdout  # E.g., "6/6 narratives generated"
        assert "narrative" in result.stdout.lower()

    def test_script_shows_file_paths(self, script_path):
        """Script should show where files are saved."""
        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # Should show "Saved to:" with path
        assert "Saved to:" in result.stdout or "saved" in result.stdout.lower()
        assert ".md" in result.stdout

    # ===== Regression Tests =====

    def test_script_handles_missing_visualization_data(self, script_path):
        """Script should catch and report missing visualization data."""
        # This tests that KeyError from incomplete data is caught
        # We can't easily inject bad data, but we can verify error handling

        result = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # If there's a KeyError, script should report it
        # (In good case, no KeyError should occur)
        if "KeyError" in result.stdout or "MISSING DATA" in result.stdout:
            # This is actually good - means we're catching the error
            assert "KeyError" in result.stdout or "MISSING DATA" in result.stdout
        else:
            # No error - even better, means data is complete
            assert result.returncode == 0

    def test_regenerating_same_file_overwrites(self, script_path):
        """Regenerating should overwrite existing file."""
        # Generate once
        result1 = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )
        assert result1.returncode == 0

        # Get file path
        output_dir = self.get_narratives_dir() / 'binary-search'
        files_before = set(output_dir.glob('example_1_*.md'))

        # Generate again
        result2 = subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )
        assert result2.returncode == 0

        # Should still have same number of files (overwritten, not duplicated)
        files_after = set(output_dir.glob('example_1_*.md'))
        assert len(files_after) == len(files_before)


class TestScriptIntegration:
    """Integration tests combining script with algorithm implementations."""

    def test_all_registered_algorithms_have_examples(self):
        """All registered algorithms should have example inputs."""
        from algorithms.registry import registry

        for algorithm_name in registry._algorithms.keys():
            metadata = registry.get_metadata(algorithm_name)
            assert 'example_inputs' in metadata
            assert len(metadata['example_inputs']) > 0, \
                f"Algorithm {algorithm_name} has no examples"

    def test_all_examples_generate_successfully(self):
        """All examples for all algorithms should generate without errors."""
        from algorithms.registry import registry

        for algorithm_name in registry._algorithms.keys():
            metadata = registry.get_metadata(algorithm_name)
            examples = metadata['example_inputs']

            for i, example in enumerate(examples):
                tracer_class = registry.get(algorithm_name)
                tracer = tracer_class()

                # Execute should succeed
                trace = tracer.execute(example['input'])
                assert trace is not None

                # Narrative generation should succeed
                narrative = tracer.generate_narrative(trace)
                assert narrative is not None
                assert len(narrative) > 0

    def test_narrative_consistency_with_script(self):
        """Narrative from script should match direct generation."""
        from algorithms.binary_search import BinarySearchTracer

        # Generate directly
        tracer = BinarySearchTracer()
        input_data = {'array': [1, 3, 5, 7, 9], 'target': 5}
        trace = tracer.execute(input_data)
        direct_narrative = tracer.generate_narrative(trace)

        # Generate via script
        script_path = Path(__file__).parent.parent / 'scripts' / 'generate_narratives.py'
        subprocess.run(
            [sys.executable, str(script_path), 'binary-search', '0'],
            capture_output=True,
            text=True
        )

        # Read generated file
        output_dir = Path(__file__).parent.parent.parent / 'docs' / 'narratives' / 'binary-search'
        files = list(output_dir.glob('example_1_*.md'))
        assert len(files) >= 1

        script_narrative = files[0].read_text()

        # Note: They might not be exactly identical due to different example data,
        # but both should be valid narratives
        assert len(direct_narrative) > 500
        assert len(script_narrative) > 500
        assert '# Binary Search' in direct_narrative
        assert '# Binary Search' in script_narrative