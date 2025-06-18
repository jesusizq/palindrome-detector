import unicodedata


def is_palindrome(text: str) -> bool:
    """
    Detects if a string is a palindrome, ignoring case, punctuation, and whitespace.

    This implementation is designed to be language-agnostic by normalizing
    Unicode characters to handle accents and diacritics from various languages.
    For example, 'é' is treated the same as 'e'.

    Args:
        text: The string to check.

    Returns:
        True if the text is a palindrome, False otherwise.
    """
    # NFD (Normalization Form D) decomposes combined characters (e.g., 'é')
    # into a base character ('e') and a combining mark (the accent).
    # We then filter out these combining marks (category 'Mn') and any character
    # that is not alphanumeric to create a sanitized string.
    normalized_chars = [
        c
        for c in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(c) != "Mn" and c.isalnum()
    ]
    sanitized_text = "".join(normalized_chars)

    # An empty or whitespace-only string is not considered a palindrome.
    if not sanitized_text:
        return False

    return sanitized_text == sanitized_text[::-1]
