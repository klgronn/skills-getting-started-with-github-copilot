"""
Test cases for GET / (root redirect endpoint).

Verifies that the root path redirects to the static HTML UI.
Uses AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


def test_root_redirect_returns_redirect_response(client):
    """
    Test that GET / returns a redirect response to the static UI.
    
    Arrange: Use the provided test client
    Act: Make GET request to root path
    Assert: Verify redirect status code and Location header
    """
    # Arrange
    # (client fixture sets up TestClient with fresh activity state)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert "static/index.html" in response.headers.get("location", "")


def test_root_redirect_location_is_static_index(client):
    """
    Test that redirect points specifically to the static index HTML file.
    
    Arrange: Use the provided test client
    Act: Make GET request to root path without following redirect
    Assert: Verify the exact Location header value
    """
    # Arrange
    # (client fixture ready)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
