# backend/tests/test_api_health.py
"""
API Health and Algorithm Listing Tests.

Tests the health check and algorithm listing endpoints.
"""

import pytest


@pytest.mark.integration
class TestHealthEndpoint:
    """Test /api/health endpoint."""

    def test_health_check_returns_200(self, client):
        """Health endpoint should return 200 OK."""
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_check_json_response(self, client):
        """Health endpoint should return JSON."""
        response = client.get('/api/health')
        assert response.content_type == 'application/json'

    def test_health_check_status_healthy(self, client):
        """Health check should report healthy status."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert data['status'] == 'healthy'

    def test_health_check_service_name(self, client):
        """Health check should include service name."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'service' in data
        assert data['service'] == 'algorithm-trace-backend'

    def test_health_check_includes_algorithm_count(self, client):
        """Health check should report number of registered algorithms."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'algorithms_registered' in data
        assert isinstance(data['algorithms_registered'], int)
        assert data['algorithms_registered'] >= 2  # At least binary-search and interval-coverage

    def test_health_check_lists_available_algorithms(self, client):
        """Health check should list algorithm names."""
        response = client.get('/api/health')
        data = response.get_json()
        
        assert 'available_algorithms' in data
        assert isinstance(data['available_algorithms'], list)
        assert 'binary-search' in data['available_algorithms']
        assert 'interval-coverage' in data['available_algorithms']


@pytest.mark.integration
class TestAlgorithmsListEndpoint:
    """Test /api/algorithms endpoint."""

    def test_algorithms_list_returns_200(self, client):
        """Algorithms list endpoint should return 200 OK."""
        response = client.get('/api/algorithms')
        assert response.status_code == 200

    def test_algorithms_list_json_response(self, client):
        """Algorithms list should return JSON."""
        response = client.get('/api/algorithms')
        assert response.content_type == 'application/json'

    def test_algorithms_list_is_array(self, client):
        """Algorithms list should return an array."""
        response = client.get('/api/algorithms')
        data = response.get_json()
        
        assert isinstance(data, list)
        assert len(data) >= 2  # At least 2 algorithms

    def test_algorithm_metadata_structure(self, client):
        """Each algorithm should have complete metadata."""
        response = client.get('/api/algorithms')
        algorithms = response.get_json()
        
        for alg in algorithms:
            assert 'name' in alg
            assert 'display_name' in alg
            assert 'description' in alg
            assert 'example_inputs' in alg

    def test_binary_search_in_list(self, client):
        """Binary search algorithm should be in the list."""
        response = client.get('/api/algorithms')
        algorithms = response.get_json()
        
        names = [alg['name'] for alg in algorithms]
        assert 'binary-search' in names
        
        binary_search = next(alg for alg in algorithms if alg['name'] == 'binary-search')
        assert binary_search['display_name'] == 'Binary Search'

    def test_interval_coverage_in_list(self, client):
        """Interval coverage algorithm should be in the list."""
        response = client.get('/api/algorithms')
        algorithms = response.get_json()
        
        names = [alg['name'] for alg in algorithms]
        assert 'interval-coverage' in names
        
        interval_cov = next(alg for alg in algorithms if alg['name'] == 'interval-coverage')
        assert interval_cov['display_name'] == 'Interval Coverage'

    def test_algorithm_has_example_inputs(self, client):
        """Each algorithm should have example inputs."""
        response = client.get('/api/algorithms')
        algorithms = response.get_json()
        
        for alg in algorithms:
            assert isinstance(alg['example_inputs'], list)
            assert len(alg['example_inputs']) > 0
            
            # Each example should have name and input
            for example in alg['example_inputs']:
                assert 'name' in example
                assert 'input' in example

    def test_server_error_handling(self, client, monkeypatch):
        """Should handle server errors gracefully."""
        # Simulate an error by making registry.list_algorithms() raise
        from algorithms.registry import registry
        
        def mock_list_error():
            raise RuntimeError("Simulated error")
        
        # Patch the instance method
        monkeypatch.setattr(registry, 'list_algorithms', mock_list_error)
        
        response = client.get('/api/algorithms')
        assert response.status_code == 500
        
        data = response.get_json()
        assert 'error' in data
