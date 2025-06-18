import json
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, parse_qs
import pytest
from app.models import Palindrome

PALINDROMES_ENDPOINT = "/v1/palindromes"


@pytest.mark.parametrize(
    "payload, expected_status, expected_is_palindrome",
    [
        (
            {"text": "A man, a plan, a canal: Panama", "language": "en"},
            201,
            True,
        ),
        ({"text": "hello world", "language": "en"}, 201, False),
        ({"language": "en"}, 400, None),
        ({"text": "some text", "language": "e"}, 400, None),
    ],
)
def test_create_palindrome(
    test_client, db, payload, expected_status, expected_is_palindrome
):
    """
    Check that a new palindrome is created
    """
    response = test_client.post(
        PALINDROMES_ENDPOINT,
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == expected_status
    if response.status_code == 201:
        result = json.loads(response.data)
        assert result["text"] == payload["text"]
        assert result["language"] == payload["language"]
        assert result["is_palindrome"] is expected_is_palindrome
        assert "id" in result
        assert "created_at" in result


@pytest.fixture
def created_palindrome(test_client, db):
    """Fixture to create a palindrome and return its data."""
    data = {"text": "level", "language": "en"}
    response = test_client.post(
        PALINDROMES_ENDPOINT, data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    return json.loads(response.data)


def test_get_by_id(test_client, created_palindrome):
    """
    Check that a palindrome is fetched by its id
    """
    palindrome_id = created_palindrome["id"]

    # Fetch the created palindrome
    response = test_client.get(f"{PALINDROMES_ENDPOINT}/{palindrome_id}")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["id"] == palindrome_id
    assert result["text"] == created_palindrome["text"]
    assert result["is_palindrome"] is True

    # Test not found
    non_existent_id = uuid.uuid4()
    response = test_client.get(f"{PALINDROMES_ENDPOINT}/{non_existent_id}")
    assert response.status_code == 404


def test_delete_palindrome(test_client, created_palindrome):
    """
    Check that a palindrome is deleted
    """
    palindrome_id = created_palindrome["id"]

    # Delete the palindrome
    response = test_client.delete(f"{PALINDROMES_ENDPOINT}/{palindrome_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = test_client.get(f"{PALINDROMES_ENDPOINT}/{palindrome_id}")
    assert response.status_code == 404

    # Test deleting non-existent
    non_existent_id = uuid.uuid4()
    response = test_client.delete(f"{PALINDROMES_ENDPOINT}/{non_existent_id}")
    assert response.status_code == 404


@pytest.fixture
def populated_db(test_app, db):
    """Fixture to populate the database with a set of palindromes."""
    with test_app.app_context():
        p1_time = datetime.now(timezone.utc) - timedelta(days=2)
        p2_time = datetime.now(timezone.utc) - timedelta(days=1)
        p3_time = datetime.now(timezone.utc)

        p1 = Palindrome(
            text="madam",
            language="en",
            is_palindrome=True,
            created_at=p1_time,
        )
        p2 = Palindrome(
            text="test", language="en", is_palindrome=False, created_at=p2_time
        )
        p3 = Palindrome(
            text="reconocer",
            language="es",
            is_palindrome=True,
            created_at=p3_time,
        )

        db.session.add_all([p1, p2, p3])
        db.session.commit()
    return db


def test_get_all_palindromes(test_client, populated_db):
    """
    Check that the response is valid and filtered/sorted correctly
    """
    # Test 1: Get all, default order (created_at desc)
    response = test_client.get(PALINDROMES_ENDPOINT)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["total"] == 3
    assert data["palindromes"][0]["text"] == "reconocer"
    assert data["palindromes"][1]["text"] == "test"
    assert data["palindromes"][2]["text"] == "madam"

    # Test 2: Filter by language
    response = test_client.get(f"{PALINDROMES_ENDPOINT}?language=es")
    data = json.loads(response.data)
    assert data["total"] == 1
    assert data["palindromes"][0]["text"] == "reconocer"

    # Test 3: Filter by date_from
    date_from = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    response = test_client.get(f"{PALINDROMES_ENDPOINT}?date_from={date_from}")
    data = json.loads(response.data)
    assert data["total"] == 2
    assert data["palindromes"][0]["text"] == "reconocer"
    assert data["palindromes"][1]["text"] == "test"

    # Test 4: Filter by date_to
    date_to = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d")
    response = test_client.get(f"{PALINDROMES_ENDPOINT}?date_to={date_to}")
    data = json.loads(response.data)
    assert data["total"] == 1
    assert data["palindromes"][0]["text"] == "madam"

    # Test 5: Sort by text asc
    response = test_client.get(f"{PALINDROMES_ENDPOINT}?sort=text&order=asc")
    data = json.loads(response.data)
    assert data["palindromes"][0]["text"] == "madam"
    assert data["palindromes"][1]["text"] == "reconocer"
    assert data["palindromes"][2]["text"] == "test"

    # Test 6: Pagination
    response = test_client.get(f"{PALINDROMES_ENDPOINT}?per_page=1&page=2")
    data = json.loads(response.data)
    assert data["total"] == 3
    assert len(data["palindromes"]) == 1
    assert data["page"] == 2
    assert data["palindromes"][0]["text"] == "test"
    assert data["next_url"] is not None
    assert data["prev_url"] is not None

    # Check next_url params
    parsed_next = urlparse(data["next_url"])
    query_params = parse_qs(parsed_next.query)
    assert query_params["page"][0] == "3"
