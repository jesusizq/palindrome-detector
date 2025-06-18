import pytest
from app.core.parser import is_palindrome

# Test cases for palindromes
# Each tuple contains: (input_string, expected_result, description)
palindrome_test_cases = [
    (
        "A man, a plan, a canal: Panama",
        True,
        "Complex palindrome with punctuation and casing",
    ),
    ("racecar", True, "Simple lowercase palindrome"),
    ("RaceCar", True, "Mixed case palindrome"),
    ("Was it a car or a cat I saw?", True, "Palindrome with spaces and question mark"),
    ("No 'x' in Nixon", True, "Palindrome with quotes and casing"),
    ("Able was I ere I saw Elba", True, "Classic palindrome"),
    # Palindromes with diacritics
    ("Sátorótas", True, "Hungarian palindrome with diacritics"),
    (
        "A mamá, Roma le aviva el amor a papá y a papá, Roma le aviva el amor a mamá",
        True,
        "Spanish palindrome with diacritics",
    ),
    ("été", True, "Unicode with diacritic, palindrome"),
]

# Test cases for non-palindromes
non_palindrome_test_cases = [
    ("hello", False, "Simple non-palindrome"),
    ("not a palindrome", False, "Multi-word non-palindrome"),
    ("réservé", False, "Unicode with diacritic, not a palindrome"),
]

# Edge cases
edge_test_cases = [
    ("", False, "Empty string"),
    (" ", False, "String with only whitespace"),
    ("a", True, "Single character string"),
    ("aa", True, "Two identical characters"),
    (".,", False, "String with only punctuation"),
    ("12321", True, "Numeric palindrome"),
    ("12345", False, "Numeric non-palindrome"),
]


@pytest.mark.parametrize("text, expected, description", palindrome_test_cases)
def test_is_palindrome_with_palindromes(text, expected, description):
    """Test that is_palindrome correctly identifies palindromes."""
    assert is_palindrome(text) is expected, f"Failed on: {description}"


@pytest.mark.parametrize("text, expected, description", non_palindrome_test_cases)
def test_is_palindrome_with_non_palindromes(text, expected, description):
    """Test that is_palindrome correctly identifies non-palindromes."""
    assert is_palindrome(text) is expected, f"Failed on: {description}"


@pytest.mark.parametrize("text, expected, description", edge_test_cases)
def test_is_palindrome_with_edge_cases(text, expected, description):
    """Test that is_palindrome handles edge cases correctly."""
    assert is_palindrome(text) is expected, f"Failed on: {description}"
