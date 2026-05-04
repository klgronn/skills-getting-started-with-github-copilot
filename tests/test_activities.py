"""
Test cases for GET /activities (list all activities endpoint).

Verifies that the endpoint returns all activities with correct structure and data.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all registered activities.
    
    Arrange: Use the provided test client with fresh activity state
    Act: Make GET request to /activities endpoint
    Assert: Verify response status and that all expected activities are present
    """
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Art Studio",
        "Debate Team",
        "Science Club",
    }
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_activity_names


def test_activities_response_structure(client):
    """
    Test that each activity has the correct response structure.
    
    Arrange: Use the provided test client
    Act: Make GET request to /activities and examine one activity
    Assert: Verify each activity has required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
        assert set(activity_data.keys()) >= required_fields, f"{activity_name} missing required fields"
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activities_participant_list_contains_emails(client):
    """
    Test that participants list contains valid email strings.
    
    Arrange: Use the provided test client
    Act: Make GET request to /activities
    Assert: Verify participant entries are non-empty strings
    """
    # Arrange
    # (client fixture ready)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert isinstance(participants, list)
        for email in participants:
            assert isinstance(email, str) and len(email) > 0, f"Invalid participant in {activity_name}"


def test_activities_max_participants_is_positive(client):
    """
    Test that max_participants value is a positive integer for all activities.
    
    Arrange: Use the provided test client
    Act: Make GET request to /activities
    Assert: Verify max_participants > 0 for all activities
    """
    # Arrange
    # (client fixture ready)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert activity_data["max_participants"] > 0, f"{activity_name} has invalid capacity"
