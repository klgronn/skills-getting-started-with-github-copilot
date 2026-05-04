"""
Shared pytest fixtures and configuration for backend API tests.

Provides:
- TestClient for making HTTP requests to the FastAPI app
- Reset of in-memory activity state before each test to ensure isolation
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the initial state of activities for reset before each test
INITIAL_ACTIVITIES_STATE = copy.deepcopy(activities)


@pytest.fixture
def client():
    """
    Provide a TestClient for the FastAPI application.
    
    Resets the in-memory activities state before each test to ensure
    tests are isolated and not affected by mutations from other tests.
    """
    # Arrange: Reset activities to initial state before each test
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES_STATE))
    
    # Act: Return client for test to use
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture to manually reset activities state if needed within a test.
    
    Useful for tests that need to verify behavior across multiple state transitions.
    """
    def _reset():
        activities.clear()
        activities.update(copy.deepcopy(INITIAL_ACTIVITIES_STATE))
    
    return _reset
