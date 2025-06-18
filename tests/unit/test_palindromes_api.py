import json
import uuid
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from app.models import Palindrome


@patch("app.api.palindromes.palindrome_service")
def test_create_palindrome(mock_service, test_client):
    """Test creating a palindrome."""
    p_id = uuid.uuid4()
    p_time = datetime.now(timezone.utc)
    mock_palindrome = Palindrome(
        id=p_id,
        text="racecar",
        language="en",
        is_palindrome=True,
        created_at=p_time,
    )
    mock_service.create.return_value = mock_palindrome

    response = test_client.post(
        "/v1/palindromes",
        data=json.dumps({"text": "racecar", "language": "en"}),
        content_type="application/json",
    )

    assert response.status_code == 201
    mock_service.create.assert_called_once()
    response_data = response.get_json()
    assert response_data["id"] == str(p_id)
    assert response_data["text"] == "racecar"


@patch("app.api.palindromes.palindrome_service")
def test_get_palindrome_by_id(mock_service, test_client):
    """Test retrieving a palindrome by its ID."""
    p_id = uuid.uuid4()
    p_time = datetime.now(timezone.utc)
    mock_palindrome = Palindrome(
        id=p_id,
        text="racecar",
        language="en",
        is_palindrome=True,
        created_at=p_time,
    )
    mock_service.get_by_id.return_value = mock_palindrome

    response = test_client.get(f"/v1/palindromes/{p_id}")

    assert response.status_code == 200
    mock_service.get_by_id.assert_called_once_with(p_id)
    response_data = response.get_json()
    assert response_data["id"] == str(p_id)


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
