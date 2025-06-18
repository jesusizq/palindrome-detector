import uuid
from datetime import datetime, time
from app.core.parser import is_palindrome
from app.extensions import db
from app.models import Palindrome
from .palindrome_dtos import PalindromeCreateDTO, PalindromeQueryDTO


class PalindromeService:
    def create(self, payload: PalindromeCreateDTO) -> Palindrome:
        """Create a new palindrome."""
        is_pal = is_palindrome(payload.text, payload.language)

        palindrome = Palindrome(
            text=payload.text, language=payload.language, is_palindrome=is_pal
        )
        db.session.add(palindrome)
        db.session.commit()
        return palindrome

    def get_by_id(self, palindrome_id: uuid.UUID) -> Palindrome:
        """Retrieve a palindrome by its ID."""
        return Palindrome.query.get_or_404(palindrome_id)

    def get_all(self, query_params: PalindromeQueryDTO):
        """Retrieve a query for all palindrome entries, with optional filters."""
        query = Palindrome.query

        if query_params.language:
            query = query.filter(Palindrome.language == query_params.language)

        if query_params.date_from:
            query = query.filter(
                Palindrome.created_at
                >= datetime.combine(query_params.date_from, time.min)
            )

        if query_params.date_to:
            query = query.filter(
                Palindrome.created_at
                <= datetime.combine(query_params.date_to, time.max)
            )

        if query_params.sort:
            sort_column = getattr(Palindrome, query_params.sort, None)
            if sort_column:
                if query_params.order == "asc":
                    query = query.order_by(sort_column.asc())
                else:
                    query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(Palindrome.created_at.desc())

        return query.paginate(
            page=query_params.page,
            per_page=query_params.page_size,
            error_out=False,
        )

    def delete_by_id(self, palindrome_id: uuid.UUID):
        """Delete a palindrome entry by its ID."""
        palindrome = Palindrome.query.get_or_404(palindrome_id)
        db.session.delete(palindrome)
        db.session.commit()


palindrome_service = PalindromeService()
