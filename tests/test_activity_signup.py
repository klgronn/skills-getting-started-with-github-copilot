"""
Test cases for POST /activities/{activity_name}/signup (student registration endpoint).

Verifies signup logic: success path, duplicate prevention, capacity limits, validation.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_signup_success_adds_participant(client):
    """
    Test that a new student can successfully sign up for an activity.
    
    Arrange: Prepare test data with activity name and new student email
    Act: POST signup request
    Assert: Verify response status, message, and participant list updated
    """
    # Arrange
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert student_email in data["message"]
    
    # Verify participant was added by checking activities endpoint
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    assert student_email in activities[activity_name]["participants"]


def test_signup_duplicate_prevents_double_registration(client):
    """
    Test that a student cannot sign up for the same activity twice.
    
    Arrange: Sign up a student once, then attempt signup again
    Act: POST signup with same email and activity
    Assert: Verify 400 error and appropriate error message
    """
    # Arrange
    activity_name = "Programming Class"
    student_email = "emma@mergington.edu"  # Already signed up in fixtures
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data.get("detail", "").lower()


def test_signup_full_activity_rejects_new_signup(client, reset_activities):
    """
    Test that signup fails when an activity is at maximum capacity.
    
    Arrange: Fill an activity to capacity, then attempt to add another student
    Act: POST signup for the full activity
    Assert: Verify 400 error and capacity-related error message
    """
    # Arrange
    activity_name = "Tennis Club"  # max_participants = 10
    
    # Fill the activity by adding students up to max capacity
    # Tennis Club currently has 2 participants, max is 10
    # We'll add 8 new students to reach capacity
    for i in range(8):
        email = f"student{i}@mergington.edu"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Attempt to sign up one more (should exceed capacity)
    over_capacity_email = "overcapacity@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": over_capacity_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "full" in data.get("detail", "").lower()


def test_signup_nonexistent_activity_returns_404(client):
    """
    Test that signup fails with 404 when activity does not exist.
    
    Arrange: Use a non-existent activity name
    Act: POST signup request for unknown activity
    Assert: Verify 404 error response
    """
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    student_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data.get("detail", "").lower()


def test_signup_multiple_students_same_activity(client):
    """
    Test that multiple different students can sign up for the same activity.
    
    Arrange: Prepare multiple new email addresses
    Act: Sign up three different students sequentially
    Assert: Verify all three are added to the activity
    """
    # Arrange
    activity_name = "Gym Class"
    new_students = [
        "newgym1@mergington.edu",
        "newgym2@mergington.edu",
        "newgym3@mergington.edu"
    ]
    
    # Act & Assert (for each signup)
    for email in new_students:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all were added
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activity_participants = activities_response.json()[activity_name]["participants"]
    
    for email in new_students:
        assert email in activity_participants
