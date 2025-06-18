from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints


class PalindromeCreateDTO(BaseModel):
    text: str
    language: Annotated[str, StringConstraints(min_length=2, max_length=2)]


class PalindromeQueryDTO(BaseModel):
    language: Annotated[str, StringConstraints(min_length=2, max_length=2)] | None = (
        None
    )
    date_from: date | None = None
    date_to: date | None = None
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=50, gt=0)
    sort: Literal["text", "language", "is_palindrome", "created_at"] = "created_at"
    order: Literal["asc", "desc"] = "desc"
