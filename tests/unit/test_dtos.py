import pytest
from pydantic import ValidationError

from app.services.palindrome.palindrome_dtos import (
    PalindromeCreateDTO,
    PalindromeQueryDTO,
)


def test_palindrome_create_dto_success():
    """Tests successful creation of PalindromeCreateDTO."""
    data = {"text": "A man a plan a canal panama", "language": "en"}
    dto = PalindromeCreateDTO(**data)
    assert dto.text == data["text"]
    assert dto.language == data["language"]


@pytest.mark.parametrize(
    "language",
    [
        "eng",  # Too long
        "e",  # Too short
    ],
)
def test_palindrome_create_dto_invalid_language(language):
    """Tests that PalindromeCreateDTO raises validation error for invalid language."""
    with pytest.raises(ValidationError):
        PalindromeCreateDTO(text="some text", language=language)


def test_palindrome_query_dto_defaults():
    """Tests that PalindromeQueryDTO uses default values correctly."""
    dto = PalindromeQueryDTO()
    assert dto.language is None
    assert dto.date_from is None
    assert dto.date_to is None
    assert dto.page == 1
    assert dto.page_size == 50
    assert dto.sort == "created_at"
    assert dto.order == "desc"


def test_palindrome_query_dto_with_values():
    """Tests that PalindromeQueryDTO correctly assigns provided values."""
    data = {
        "language": "es",
        "page": 2,
        "page_size": 10,
        "sort": "text",
        "order": "asc",
    }
    dto = PalindromeQueryDTO(**data)
    assert dto.language == "es"
    assert dto.page == 2
    assert dto.page_size == 10
    assert dto.sort == "text"
    assert dto.order == "asc"


def test_palindrome_query_dto_invalid_language():
    """Tests that PalindromeQueryDTO raises validation error for invalid language."""
    with pytest.raises(ValidationError):
        PalindromeQueryDTO(language="spa")
