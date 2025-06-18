import uuid
from unittest.mock import MagicMock, patch

import pytest
from app.services.palindrome.palindrome_dtos import (
    PalindromeCreateDTO,
    PalindromeQueryDTO,
)
from app.services.palindrome.palindrome_service import PalindromeService


@pytest.fixture
def palindrome_service():
    """Fixture to create a PalindromeService instance for testing."""
    return PalindromeService()


def test_create_palindrome(palindrome_service: PalindromeService, db):
    """Test creating a palindrome."""
    create_dto = PalindromeCreateDTO(text="racecar", language="en")
    result = palindrome_service.create(create_dto)
    assert result.id is not None
    assert result.text == "racecar"
    assert result.is_palindrome is True

    # Test a non-palindrome
    create_dto_non = PalindromeCreateDTO(text="hello", language="en")
    result_non = palindrome_service.create(create_dto_non)
    assert result_non.id is not None
    assert result_non.text == "hello"
    assert result_non.is_palindrome is False


def test_get_by_id(palindrome_service: PalindromeService, db):
    """Test retrieving a palindrome by its ID."""
    create_dto = PalindromeCreateDTO(text="level", language="en")
    created = palindrome_service.create(create_dto)

    retrieved = palindrome_service.get_by_id(created.id)
    assert retrieved.id == created.id
    assert retrieved.text == "level"


def test_delete_by_id(palindrome_service: PalindromeService, db):
    """Test deleting a palindrome by its ID."""
    create_dto = PalindromeCreateDTO(text="deified", language="en")
    created = palindrome_service.create(create_dto)
    palindrome_id = created.id

    palindrome_service.delete_by_id(palindrome_id)

    with pytest.raises(Exception):
        palindrome_service.get_by_id(palindrome_id)


def test_get_all(palindrome_service: PalindromeService, db):
    """Test retrieving all palindromes with various filters."""
    # Create some test data
    palindrome_service.create(PalindromeCreateDTO(text="madam", language="en"))
    palindrome_service.create(PalindromeCreateDTO(text="test", language="en"))
    palindrome_service.create(PalindromeCreateDTO(text="ressasser", language="fr"))

    # Test without filters
    query_dto_all = PalindromeQueryDTO(page_size=10)
    pagination_all = palindrome_service.get_all(query_dto_all)
    assert pagination_all.total == 3
    assert len(pagination_all.items) == 3

    # Test language filter
    query_dto_fr = PalindromeQueryDTO(language="fr")
    pagination_fr = palindrome_service.get_all(query_dto_fr)
    assert pagination_fr.total == 1
    assert pagination_fr.items[0].language == "fr"
