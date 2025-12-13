# backend/tests/test_api_legacy.py
"""
Legacy API Endpoint Tests.

Tests backward compatibility endpoints:
- /api/trace (interval coverage)
- /api/trace/binary-search
- /api/examples
- /api/examples/binary-search
"""

import pytest


@pytest.mark.integration
class TestLegacyIntervalCoverageEndpoint:
    """Test legacy /api/trace endpoint for interval coverage."""

    def test_legacy_interval_trace_success(self, client):
        """Legacy interval coverage endpoint should work."""
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': 1, 'start': 10, 'end': 50, 'color': 'blue'},
                {'id': 2, 'start': 20, 'end': 60, 'color': 'green'}
            ]
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'trace' in data
        assert 'result' in data
        assert 'metadata' in data

    def test_legacy_interval_validation_error(self, client):
        """Invalid interval data should return 400 with validation details."""
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': -1, 'start': 10, 'end': 50, 'color': 'blue'}  # Negative ID
            ]
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'details' in data

    def test_legacy_interval_end_before_start(self, client):
        """Interval with end <= start should return 400."""
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': 1, 'start': 50, 'end': 10, 'color': 'blue'}
            ]
        })
        assert response.status_code == 400

    def test_legacy_interval_missing_fields(self, client):
        """Missing required fields should return 400."""
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': 1, 'start': 10}  # Missing 'end'
            ]
        })
        assert response.status_code == 400

    def test_legacy_interval_default_color(self, client):
        """Color should default to 'blue' if not provided."""
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': 1, 'start': 10, 'end': 50}  # No color
            ]
        })
        assert response.status_code == 200


@pytest.mark.integration
class TestLegacyBinarySearchEndpoint:
    """Test legacy /api/trace/binary-search endpoint."""

    def test_legacy_binary_search_success(self, client):
        """Legacy binary search endpoint should work."""
        response = client.post('/api/trace/binary-search', json={
            'array': [1, 3, 5, 7, 9],
            'target': 5
        })
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'trace' in data
        assert 'result' in data
        assert 'metadata' in data

    def test_legacy_binary_search_empty_array(self, client):
        """Empty array should return 400."""
        response = client.post('/api/trace/binary-search', json={
            'array': [],
            'target': 5
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data
        assert 'details' in data

    def test_legacy_binary_search_unsorted_array(self, client):
        """Unsorted array should return 400 with validation error."""
        response = client.post('/api/trace/binary-search', json={
            'array': [5, 3, 1],
            'target': 3
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'error' in data

    def test_legacy_binary_search_missing_array(self, client):
        """Missing array field should return 400."""
        response = client.post('/api/trace/binary-search', json={
            'target': 5
        })
        assert response.status_code == 400

    def test_legacy_binary_search_missing_target(self, client):
        """Missing target field should return 400."""
        response = client.post('/api/trace/binary-search', json={
            'array': [1, 3, 5]
        })
        assert response.status_code == 400


@pytest.mark.integration
class TestExamplesEndpoints:
    """Test example retrieval endpoints."""

    def test_interval_examples_returns_200(self, client):
        """Interval examples endpoint should return 200."""
        response = client.get('/api/examples')
        assert response.status_code == 200

    def test_interval_examples_is_array(self, client):
        """Interval examples should return array."""
        response = client.get('/api/examples')
        data = response.get_json()
        
        assert isinstance(data, list)
        assert len(data) > 0

    def test_interval_examples_structure(self, client):
        """Each interval example should have name and intervals."""
        response = client.get('/api/examples')
        examples = response.get_json()
        
        for example in examples:
            assert 'name' in example
            assert 'intervals' in example
            assert isinstance(example['intervals'], list)

    def test_binary_search_examples_returns_200(self, client):
        """Binary search examples endpoint should return 200."""
        response = client.get('/api/examples/binary-search')
        assert response.status_code == 200

    def test_binary_search_examples_is_array(self, client):
        """Binary search examples should return array."""
        response = client.get('/api/examples/binary-search')
        data = response.get_json()
        
        assert isinstance(data, list)
        assert len(data) > 0

    def test_binary_search_examples_structure(self, client):
        """Each binary search example should have name, array, and target."""
        response = client.get('/api/examples/binary-search')
        examples = response.get_json()
        
        for example in examples:
            assert 'name' in example
            assert 'array' in example
            assert 'target' in example
            assert isinstance(example['array'], list)
            assert isinstance(example['target'], int)

    def test_binary_search_examples_include_edge_cases(self, client):
        """Binary search examples should include various scenarios."""
        response = client.get('/api/examples/binary-search')
        examples = response.get_json()
        
        names = [ex['name'] for ex in examples]
        
        # Should have found and not found cases
        assert any('Found' in name for name in names)
        assert any('Not Found' in name for name in names)


@pytest.mark.integration
class TestLegacyEndpointCompatibility:
    """Test that legacy endpoints produce same results as unified endpoint."""

    def test_binary_search_legacy_matches_unified(self, client):
        """Legacy and unified endpoints should produce identical results."""
        test_input = {
            'array': [1, 3, 5, 7, 9],
            'target': 5
        }
        
        # Call legacy endpoint
        legacy_response = client.post('/api/trace/binary-search', json=test_input)
        legacy_data = legacy_response.get_json()
        
        # Call unified endpoint
        unified_response = client.post('/api/trace/unified', json={
            'algorithm': 'binary-search',
            'input': test_input
        })
        unified_data = unified_response.get_json()
        
        # Results should match
        assert legacy_data['result'] == unified_data['result']
        assert legacy_data['metadata']['algorithm'] == unified_data['metadata']['algorithm']
        assert len(legacy_data['trace']['steps']) == len(unified_data['trace']['steps'])

    def test_interval_coverage_legacy_matches_unified(self, client):
        """Legacy and unified interval coverage endpoints should match."""
        test_input = {
            'intervals': [
                {'id': 1, 'start': 10, 'end': 50, 'color': 'blue'},
                {'id': 2, 'start': 20, 'end': 60, 'color': 'green'}
            ]
        }
        
        # Call legacy endpoint
        legacy_response = client.post('/api/trace', json=test_input)
        legacy_data = legacy_response.get_json()
        
        # Call unified endpoint
        unified_response = client.post('/api/trace/unified', json={
            'algorithm': 'interval-coverage',
            'input': test_input
        })
        unified_data = unified_response.get_json()
        
        # Results should match
        assert len(legacy_data['result']) == len(unified_data['result'])
        assert legacy_data['metadata']['algorithm'] == unified_data['metadata']['algorithm']
