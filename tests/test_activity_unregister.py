"""
Test cases for DELETE /activities/{activity_name}/participants (unregister endpoint).

Verifies unregister logic: successful removal, validation, error handling.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_unregister_success_removes_participant(client):
    """
    Test that an enrolled student can be successfully removed from an activity.
    
    Arrange: Identify an activity and existing participant
    Act: DELETE request to remove the participant
    Assert: Verify 200 response and participant removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"  # Pre-enrolled in fixtures
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert participant_email in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    assert participant_email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_404(client):
    """
    Test that attempting to remove a non-participant returns 404.
    
    Arrange: Use an activity and an email not enrolled in that activity
    Act: DELETE request with non-participant email
    Assert: Verify 404 error response
    """
    # Arrange
    activity_name = "Drama Club"
    nonparticipant_email = "notinclub@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": nonparticipant_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data.get("detail", "").lower()


def test_unregister_nonexistent_activity_returns_404(client):
    """
    Test that attempting to unregister from a non-existent activity returns 404.
    
    Arrange: Use a non-existent activity name
    Act: DELETE request for unknown activity
    Assert: Verify 404 error response
    """
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    student_email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/participants",
        params={"email": student_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data.get("detail", "").lower()


def test_unregister_then_signup_again_succeeds(client):
    """
    Test that a student can unregister and then re-enroll in the same activity.
    
    Arrange: Prepare an enrolled student
    Act: Delete participant, then sign up again
    Assert: Verify both operations succeed and participant is re-enrolled
    """
    # Arrange
    activity_name = "Art Studio"
    student_email = "mia@mergington.edu"  # Pre-enrolled
    
    # Act - Remove
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": student_email}
    )
    
    # Assert - Remove succeeded
    assert delete_response.status_code == 200
    
    # Act - Re-signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student_email}
    )
    
    # Assert - Re-signup succeeded
    assert signup_response.status_code == 200
    
    # Verify participant is re-enrolled
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    assert student_email in activities[activity_name]["participants"]


def test_unregister_multiple_participants_from_same_activity(client):
    """
    Test removing multiple participants from one activity in sequence.
    
    Arrange: Identify activity with multiple participants
    Act: Remove two participants sequentially
    Assert: Verify both are removed
    """
    # Arrange
    activity_name = "Debate Team"
    participant1 = "lucas@mergington.edu"
    participant2 = "ava@mergington.edu"
    
    # Act - Remove first
    response1 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant1}
    )
    
    # Assert - First removal succeeded
    assert response1.status_code == 200
    
    # Act - Remove second
    response2 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": participant2}
    )
    
    # Assert - Second removal succeeded
    assert response2.status_code == 200
    
    # Verify both are removed
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    participants = activities[activity_name]["participants"]
    
    assert participant1 not in participants
    assert participant2 not in participants


def test_unregister_then_attempt_again_fails(client):
    """
    Test that attempting to unregister the same participant twice fails on second attempt.
    
    Arrange: Prepare an enrolled student
    Act: Delete same participant twice
    Assert: First deletion succeeds, second returns 404
    """
    # Arrange
    activity_name = "Science Club"
    student_email = "ethan@mergington.edu"
    
    # Act & Assert - First deletion
    response1 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": student_email}
    )
    assert response1.status_code == 200
    
    # Act & Assert - Second deletion (should fail)
    response2 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": student_email}
    )
    assert response2.status_code == 404
    data = response2.json()
    assert "not found" in data.get("detail", "").lower()
