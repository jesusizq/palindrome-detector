import uuid
from datetime import datetime, time
from sqlalchemy import select
from app.core.parser import is_palindrome
from app.extensions import db
from app.models import Palindrome
from .palindrome_dtos import PalindromeCreateDTO, PalindromeQueryDTO


class PalindromeService:
    def create(self, payload: PalindromeCreateDTO) -> Palindrome:
        """Create a new palindrome entry."""
        is_pal = is_palindrome(payload.text)

        palindrome = Palindrome(
            text=payload.text, language=payload.language, is_palindrome=is_pal
        )
        db.session.add(palindrome)
        db.session.commit()
        return palindrome

    def get_by_id(self, palindrome_id: uuid.UUID) -> Palindrome:
        """Retrieve a palindrome by its ID."""
        return db.get_or_404(Palindrome, palindrome_id)

    def get_all(self, query_params: PalindromeQueryDTO):
        """Retrieve a query for all palindrome entries, with optional filters."""
        stmt = select(Palindrome)

        if query_params.language:
            stmt = stmt.where(Palindrome.language == query_params.language)

        if query_params.date_from:
            stmt = stmt.where(
                Palindrome.created_at
                >= datetime.combine(query_params.date_from, time.min)
            )

        if query_params.date_to:
            stmt = stmt.where(
                Palindrome.created_at
                <= datetime.combine(query_params.date_to, time.max)
            )

        if query_params.sort:
            sort_column = getattr(Palindrome, query_params.sort, None)
            if sort_column:
                if query_params.order == "asc":
                    stmt = stmt.order_by(sort_column.asc())
                else:
                    stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(Palindrome.created_at.desc())

        return db.paginate(
            stmt,
            page=query_params.page,
            per_page=query_params.page_size,
            error_out=False,
        )

    def delete_by_id(self, palindrome_id: uuid.UUID):
        """Delete a palindrome entry by its ID."""
        palindrome = db.get_or_404(Palindrome, palindrome_id)
        db.session.delete(palindrome)
        db.session.commit()


palindrome_service = PalindromeService()
