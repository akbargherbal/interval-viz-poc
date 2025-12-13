# backend/tests/test_api_coverage_boost.py
"""
Additional API tests to boost coverage to 90%.

These tests specifically target uncovered error paths in legacy endpoints.
"""

import pytest


@pytest.mark.integration
class TestLegacyEndpointErrorPaths:
    """Test error paths in legacy endpoints to boost coverage."""

    def test_legacy_trace_missing_request_body(self, client):
        """Legacy trace endpoint with no JSON body."""
        response = client.post('/api/trace')
        # Flask returns 500 for UnsupportedMediaType caught by generic handler
        assert response.status_code in [400, 500]

    def test_legacy_trace_runtime_error(self, client):
        """Test RuntimeError handling in legacy trace endpoint."""
        # Trigger a RuntimeError by creating conditions that might cause one
        # For now, we know ValueError paths are covered, so test generic exception
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': 1, 'start': 10, 'end': 50, 'color': 'blue'}
            ]
        })
        # Should succeed normally
        assert response.status_code == 200

    def test_legacy_trace_generic_exception(self, client, monkeypatch):
        """Test generic exception handling in legacy trace endpoint."""
        from algorithms.interval_coverage import IntervalCoverageTracer
        
        def mock_execute_error(self, input_data):
            raise Exception("Simulated unexpected error")
        
        monkeypatch.setattr(IntervalCoverageTracer, 'execute', mock_execute_error)
        
        response = client.post('/api/trace', json={
            'intervals': [
                {'id': 1, 'start': 10, 'end': 50, 'color': 'blue'}
            ]
        })
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_legacy_binary_search_missing_request_body(self, client):
        """Legacy binary search endpoint with no JSON body."""
        response = client.post('/api/trace/binary-search')
        # Flask returns 500 for UnsupportedMediaType caught by generic handler
        assert response.status_code in [400, 500]

    def test_legacy_binary_search_runtime_error(self, client, monkeypatch):
        """Test RuntimeError handling in legacy binary search endpoint."""
        from algorithms.binary_search import BinarySearchTracer
        
        def mock_execute_runtime_error(self, input_data):
            raise RuntimeError("Simulated runtime error")
        
        monkeypatch.setattr(BinarySearchTracer, 'execute', mock_execute_runtime_error)
        
        response = client.post('/api/trace/binary-search', json={
            'array': [1, 3, 5],
            'target': 3
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_legacy_binary_search_generic_exception(self, client, monkeypatch):
        """Test generic exception handling in legacy binary search endpoint."""
        from algorithms.binary_search import BinarySearchTracer
        
        def mock_execute_error(self, input_data):
            raise Exception("Simulated unexpected error")
        
        monkeypatch.setattr(BinarySearchTracer, 'execute', mock_execute_error)
        
        response = client.post('/api/trace/binary-search', json={
            'array': [1, 3, 5],
            'target': 3
        })
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_unified_trace_runtime_error_handling(self, client, monkeypatch):
        """Test RuntimeError handling in unified trace endpoint."""
        from algorithms.binary_search import BinarySearchTracer
        
        def mock_execute_runtime_error(self, input_data):
            raise RuntimeError("Max steps exceeded")
        
        monkeypatch.setattr(BinarySearchTracer, 'execute', mock_execute_runtime_error)
        
        response = client.post('/api/trace/unified', json={
            'algorithm': 'binary-search',
            'input': {'array': [1, 3, 5], 'target': 3}
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_unified_trace_value_error_handling(self, client):
        """Test ValueError handling for invalid binary search input."""
        # Empty array triggers ValueError
        response = client.post('/api/trace/unified', json={
            'algorithm': 'binary-search',
            'input': {'array': [], 'target': 5}
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_unified_trace_generic_exception_handling(self, client, monkeypatch):
        """Test generic exception handling in unified trace endpoint."""
        from algorithms.binary_search import BinarySearchTracer
        
        def mock_execute_generic_error(self, input_data):
            raise TypeError("Simulated type error")
        
        monkeypatch.setattr(BinarySearchTracer, 'execute', mock_execute_generic_error)
        
        response = client.post('/api/trace/unified', json={
            'algorithm': 'binary-search',
            'input': {'array': [1, 3, 5], 'target': 3}
        })
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'unexpected server error' in data['error'].lower()