import json
import uuid
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
import pytest
from app.models import Palindrome


@pytest.fixture
def mock_palindrome():
    """Fixture for a mock Palindrome object."""
    p_id = uuid.uuid4()
    p_time = datetime.now(timezone.utc)
    return Palindrome(
        id=p_id,
        text="racecar",
        language="en",
        is_palindrome=True,
        created_at=p_time,
    )


@patch("app.api.palindromes.palindrome_service")
def test_create_palindrome(mock_service, test_client, mock_palindrome):
    """Test creating a palindrome."""
    mock_service.create.return_value = mock_palindrome

    response = test_client.post(
        "/v1/palindromes",
        data=json.dumps({"text": "racecar", "language": "en"}),
        content_type="application/json",
    )

    assert response.status_code == 201
    mock_service.create.assert_called_once()
    response_data = response.get_json()
    assert response_data["id"] == str(mock_palindrome.id)
    assert response_data["text"] == "racecar"


@patch("app.api.palindromes.palindrome_service")
def test_get_palindrome_by_id(mock_service, test_client, mock_palindrome):
    """Test retrieving a palindrome by its ID."""
    mock_service.get_by_id.return_value = mock_palindrome

    response = test_client.get(f"/v1/palindromes/{mock_palindrome.id}")

    assert response.status_code == 200
    mock_service.get_by_id.assert_called_once_with(mock_palindrome.id)
    response_data = response.get_json()
    assert response_data["id"] == str(mock_palindrome.id)


@patch("app.api.palindromes.palindrome_service")
def test_get_palindromes(mock_service, test_client):
    """Test retrieving a list of palindromes."""
    mock_pagination = MagicMock()
    mock_pagination.items = []
    mock_pagination.has_prev = False
    mock_pagination.has_next = False
    mock_pagination.total = 0
    mock_pagination.pages = 1
    mock_pagination.page = 1
    mock_pagination.per_page = 50
    mock_service.get_all.return_value = mock_pagination

    response = test_client.get("/v1/palindromes")
    assert response.status_code == 200
    mock_service.get_all.assert_called_once()


@patch("app.api.palindromes.palindrome_service")
def test_delete_palindrome(mock_service, test_client):
    """Test deleting a palindrome."""
    palindrome_id = uuid.uuid4()
    mock_service.delete_by_id.return_value = None

    response = test_client.delete(f"/v1/palindromes/{palindrome_id}")

    assert response.status_code == 204
    mock_service.delete_by_id.assert_called_once_with(palindrome_id)
