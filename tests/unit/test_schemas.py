import pytest
from marshmallow import ValidationError

from app.api.schemas import PalindromeCreateSchema, PalindromeQuerySchema


def test_palindrome_create_schema_success():
    """Tests that PalindromeCreateSchema loads valid data."""
    schema = PalindromeCreateSchema()
    data = {"text": "A man a plan a canal panama", "language": "en"}
    loaded_data = schema.load(data)
    assert loaded_data == data


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"text": "test", "language": "eng"},  # language too long
        {"text": "test", "language": "e"},  # language too short
        {"text": "", "language": "en"},  # text too short
        {"language": "en"},  # missing text
        {"text": "test"},  # missing language
    ],
)
def test_palindrome_create_schema_invalid(invalid_data):
    """Tests that PalindromeCreateSchema raises validation errors for invalid data."""
    schema = PalindromeCreateSchema()
    with pytest.raises(ValidationError):
        schema.load(invalid_data)


def test_palindrome_query_schema_defaults():
    """Tests that PalindromeQuerySchema uses default values correctly."""
    schema = PalindromeQuerySchema()
    loaded_data = schema.load({})
    assert "language" not in loaded_data
    assert "date_from" not in loaded_data
    assert "date_to" not in loaded_data
    assert loaded_data["page"] == 1
    assert loaded_data["page_size"] == 50
    assert loaded_data["sort"] == "created_at"
    assert loaded_data["order"] == "desc"


def test_palindrome_query_schema_with_values():
    """Tests that PalindromeQuerySchema correctly loads provided values."""
    schema = PalindromeQuerySchema()
    data = {
        "language": "es",
        "page": 2,
        "per_page": 10,
        "sort": "text",
        "order": "asc",
    }
    loaded_data = schema.load(data)
    assert loaded_data["language"] == "es"
    assert loaded_data["page"] == 2
    assert loaded_data["page_size"] == 10
    assert loaded_data["sort"] == "text"
    assert loaded_data["order"] == "asc"


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"language": "spa"},  # language wrong length
        {"sort": "invalid_field"},  # invalid sort field
        {"order": "invalid_order"},  # invalid order value
        {"page": 0},  # page out of range
        {"per_page": 0},  # per_page out of range
    ],
)
def test_palindrome_query_schema_invalid(invalid_data):
    """Tests that PalindromeQuerySchema raises validation errors for invalid data."""
    schema = PalindromeQuerySchema()
    with pytest.raises(ValidationError):
        schema.load(invalid_data)
