# backend/tests/conftest.py
"""
Pytest configuration and fixtures for API tests.

Provides Flask test client and other shared fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture
def app():
    """
    Create Flask app for testing.
    
    Returns Flask app instance with testing configuration.
    """
    from app import app as flask_app
    
    # Set testing configuration
    flask_app.config['TESTING'] = True
    flask_app.config['DEBUG'] = False
    
    return flask_app


@pytest.fixture
def client(app):
    """
    Create Flask test client.
    
    This fixture provides a test client that can make requests
    to the Flask app without running a server.
    
    Usage:
        def test_endpoint(client):
            response = client.get('/api/health')
            assert response.status_code == 200
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create Flask CLI test runner.
    
    Useful for testing CLI commands if added in the future.
    """
    return app.test_cli_runner()
